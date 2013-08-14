import uuid

from django.db import IntegrityError
from django.test import TestCase
import pytest

from django_uuid_pk.tests.models import (AutoUUIDField, ManualUUIDField, NamespaceUUIDField,
                                         BrokenNamespaceUUIDField, PrimaryKeyUUIDField,
                                         BrokenPrimaryKeyUUIDField, ModelUUIDField)


class UUIDFieldTestCase(TestCase):
    def test_protocols(self):
        obj = ModelUUIDField.objects.create()
        self.assertTrue(isinstance(obj.uuid1, uuid.UUID))
        self.assertTrue(isinstance(obj.uuid3, uuid.UUID))
        self.assertTrue(isinstance(obj.uuid4, uuid.UUID))
        self.assertTrue(isinstance(obj.uuid5, uuid.UUID))

    def test_auto_uuid4(self):
        obj = AutoUUIDField.objects.create()
        self.assertTrue(obj.uuid)
        self.assertEquals(len(obj.uuid), 32)
        self.assertTrue(isinstance(obj.uuid, uuid.UUID))
        self.assertEquals(obj.uuid.version, 4)

    def test_raises_exception(self):
        self.assertRaises(IntegrityError, ManualUUIDField.objects.create)

    def test_manual(self):
        obj = ManualUUIDField.objects.create(uuid=uuid.uuid4())
        self.assertTrue(obj)
        self.assertEquals(len(obj.uuid), 32)
        self.assertTrue(isinstance(obj.uuid, uuid.UUID))
        self.assertEquals(obj.uuid.version, 4)

    def test_namespace(self):
        obj = NamespaceUUIDField.objects.create()
        self.assertTrue(obj)
        self.assertEquals(len(obj.uuid), 32)
        self.assertTrue(isinstance(obj.uuid, uuid.UUID))
        self.assertEquals(obj.uuid.version, 5)

    def test_broken_namespace(self):
        self.assertRaises(ValueError, BrokenNamespaceUUIDField.objects.create)

    def test_primary_key(self):
        obj = PrimaryKeyUUIDField.objects.create()
        assert obj.pk

        obj = PrimaryKeyUUIDField()
        assert not obj.pk

        # reset primary key if save() fails
        BrokenPrimaryKeyUUIDField.objects.create(unique=1)
        obj = BrokenPrimaryKeyUUIDField(unique=1)
        with pytest.raises(IntegrityError):
            obj.save()
        assert not obj.pk
