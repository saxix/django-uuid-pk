from functools import update_wrapper
import uuid

from django import forms
from django.db.models import Field, SubfieldBase
from django.utils.encoding import smart_unicode

try:
    #psycopg2 needs us to register the uuid type
    import psycopg2

    psycopg2.extras.register_uuid()
except (ImportError, AttributeError):
    pass


class StringUUID(uuid.UUID):
    def __init__(self, *args, **kwargs):
        # get around UUID's immutable setter
        object.__setattr__(self, 'hyphenate', kwargs.pop('hyphenate', False))

        super(StringUUID, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return unicode(str(self))

    def __str__(self):
        if self.hyphenate:
            return super(StringUUID, self).__str__()

        return self.hex

    def __len__(self):
        return len(self.__unicode__())


class UUIDField(Field):
    """
    A field which stores a UUID value in hex format. This may also have
    the Boolean attribute 'auto' which will set the value on initial save to a
    new UUID value (calculated using the UUID1 method). Note that while all
    UUIDs are expected to be unique we enforce this with a DB constraint.
    """
    __metaclass__ = SubfieldBase

    def __init__(self, version=4, node=None, clock_seq=None,
                 namespace=None, name=None, auto=False, *args, **kwargs):
        assert version in (1, 3, 4, 5), "UUID version %s is not supported." % version

        self.version = version
        # We store UUIDs in hex format, which is fixed at 32 characters.
        kwargs['max_length'] = 36

        if kwargs.get('primary_key', False):
            auto = True
        self.auto = auto
        if auto:
            # Do not let the user edit UUIDs if they are auto-assigned.
            kwargs['editable'] = False
            kwargs['blank'] = True
            kwargs['unique'] = True
        if version == 1:
            self.node, self.clock_seq = node, clock_seq
        elif version in (3, 5):
            self.namespace, self.name = namespace, name
        super(UUIDField, self).__init__(*args, **kwargs)

    #def get_internal_type(self):
    #    return "CharField"

    def _create_uuid(self):
        if self.version == 1:
            args = (self.node, self.clock_seq)
        elif self.version in (3, 5):
            error_attr = None
            if self.name is None:
                error_attr = 'name'
            elif self.namespace is None:
                error_attr = 'namespace'
            if error_attr is not None:
                raise ValueError("The %s parameter of %s needs to be set." %
                                 (error_attr, self))
            if not isinstance(self.namespace, uuid.UUID):
                raise ValueError("The name parameter of %s must be an "
                                 "UUID instance." % self)
            args = (self.namespace, self.name)
        else:
            args = ()
        return getattr(uuid, 'uuid%s' % self.version)(*args)

    def db_type(self, connection=None):
        """
        Return the special uuid data type on Postgres databases.
        """
        if connection and 'postgres' in connection.vendor:
            return 'uuid'
        return 'char(%s)' % self.max_length

    def pre_save(self, model_instance, add):
        """
        This is used to ensure that we auto-set values if required.
        See CharField.pre_save
        """
        value = getattr(model_instance, self.attname, None)
        if self.auto and add and not value:
            # Assign a new value for this attribute if required.
            uuid = self._create_uuid()
            setattr(model_instance, self.attname, uuid)
            value = uuid.hex
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Casts uuid.UUID values into the format expected by the back end
        """
        if isinstance(value, uuid.UUID):
            return str(value)
            #elif isinstance(value, StringUUID):
        #    return str(value)
        return value

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        if val is None:
            data = ''
        else:
            data = unicode(val)
        return data

    def to_python(self, value):
        """
        Returns a ``StringUUID`` instance from the value returned by the
        database. This doesn't use uuid.UUID directly for backwards
        compatibility, as ``StringUUID`` implements ``__unicode__`` with
        ``uuid.UUID.hex()``.
        """
        if not value:
            return None
            # attempt to parse a UUID including cases in which value is a UUID
        # instance already to be able to get our StringUUID in.
        return StringUUID(smart_unicode(value))

    def get_prep_value(self, value):
        value = super(UUIDField, self).get_prep_value(value)
        return self.to_python(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.CharField,
            'max_length': self.max_length,
        }
        defaults.update(kwargs)
        return super(UUIDField, self).formfield(**defaults)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector

        field_class = "django_uuid_pk.fields.UUIDField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)

    def contribute_to_class(self, cls, name):
        super(UUIDField, self).contribute_to_class(cls, name)
        if self.primary_key:
            _wrap_model_save(cls)


def _wrap_model_save(model):
    if not hasattr(model, '_uuid_patched'):
        old_save = getattr(model, 'save')
        setattr(model, 'save', _wrap_save(old_save))
        model._uuid_patched = True


def _wrap_save(func):
    def inner(self, force_insert=False, force_update=False, using=None, **kwargs):
        try:
            return func(self, force_insert, force_update, using, **kwargs)
        except:
            self.pk = None
            raise

    return update_wrapper(inner, func)
