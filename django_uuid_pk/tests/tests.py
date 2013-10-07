import json
import uuid
from django.core.serializers import serialize

from django.db import IntegrityError
from django.test import TestCase
import pytest
from django_uuid_pk.fields import StringUUID

from django_uuid_pk.tests.models import (AutoUUIDFieldModel, ManualUUIDFieldModel, NamespaceUUIDFieldModel,
                                         BrokenNamespaceUUIDFieldModel, PrimaryKeyUUIDFieldModel,
                                         BrokenPrimaryKeyUUIDFieldModel, ModelUUIDField)



def assertJSON(data):
    try:
        json.loads(data)
    except ValueError:
        raise



@pytest.mark.django_db
class UUIDFieldTestCase(TestCase):
    def test_protocols(self):
        obj = ModelUUIDField.objects.create()
        self.assertTrue(isinstance(obj.uuid1, uuid.UUID))
        self.assertTrue(isinstance(obj.uuid3, uuid.UUID))
        self.assertTrue(isinstance(obj.uuid4, uuid.UUID))
        self.assertTrue(isinstance(obj.uuid5, uuid.UUID))

    def test_auto_uuid4(self):
        obj = AutoUUIDFieldModel.objects.create()
        self.assertTrue(obj.uuid)
        self.assertEquals(len(obj.uuid), 32)
        #self.assertTrue(isinstance(obj.uuid, uuid.UUID))
        self.assertEquals(obj.uuid.version, 4)

    def test_raises_exception(self):
        self.assertRaises(IntegrityError, ManualUUIDFieldModel.objects.create)

    def test_manual(self):
        obj = ManualUUIDFieldModel.objects.create(uuid=uuid.uuid4())
        self.assertTrue(obj)
        self.assertEquals(len(obj.uuid), 32)
        #self.assertTrue(isinstance(obj.uuid, uuid.UUID))
        self.assertEquals(obj.uuid.version, 4)

    def test_namespace(self):
        obj = NamespaceUUIDFieldModel.objects.create()
        self.assertTrue(obj)
        self.assertEquals(len(obj.uuid), 32)
        #self.assertTrue(isinstance(obj.uuid, uuid.UUID))
        self.assertEquals(obj.uuid.version, 5)

    def test_broken_namespace(self):
        self.assertRaises(ValueError, BrokenNamespaceUUIDFieldModel.objects.create)

    def test_wrongvalue(self):
        obj = PrimaryKeyUUIDFieldModel.objects.create()
        with pytest.raises(ValueError):
            obj.uuid = 1

    def test_assign1(self):
        obj = PrimaryKeyUUIDFieldModel.objects.create()
        obj.uuid = uuid.UUID('5b27d1bd-e7c3-46f3-aaf2-11e4d32f60d4')
        obj.save()
        assert str(obj.uuid) == '5b27d1bde7c346f3aaf211e4d32f60d4'
        #assert obj.uuid == '5b27d1bd-e7c3-46f3-aaf2-11e4d32f60d4'
        assert obj.uuid == uuid.UUID('5b27d1bd-e7c3-46f3-aaf2-11e4d32f60d4')

    def test_assign2(self):
        obj = PrimaryKeyUUIDFieldModel.objects.create()
        obj.uuid = '5b27d1bd-e7c3-46f3-aaf2-11e4d32f60d4'
        obj.save()
        assert str(obj.uuid) == '5b27d1bde7c346f3aaf211e4d32f60d4'


    def test_primary_key(self):
        obj = PrimaryKeyUUIDFieldModel.objects.create()
        assert obj.pk

        obj = PrimaryKeyUUIDFieldModel()
        assert not obj.pk

        # reset primary key if save() fails
        BrokenPrimaryKeyUUIDFieldModel.objects.create(unique=1)
        obj = BrokenPrimaryKeyUUIDFieldModel(unique=1)
        with pytest.raises(IntegrityError):
            obj.save()
        assert not obj.pk

    def test_serialize(self):
        obj = PrimaryKeyUUIDFieldModel.objects.create()
        obj.uuid = uuid.UUID("2e9280cfdc8e42bdbf0afa3043acaa7e")
        obj.save()
        serialized = serialize('json', PrimaryKeyUUIDFieldModel.objects.all())
        assertJSON(serialized)

    #def test_json(self):
    #    obj = PrimaryKeyUUIDFieldModel.objects.create()
    #    obj.save()
    #    serialized = json.dumps(obj)
    #    assertJSON(serialized)

        #deserialized = json.loads(serialized, object_hook=registry.object_hook)
        #
        #print 111, deserialized
        #
        #assert PrimaryKeyUUIDField(**deserialized).uuid == obj.uuid
