import uuid
from django.db import models
from django_uuid_pk.fields import UUIDField


class ModelUUIDField(models.Model):
    uuid1 = UUIDField(version=1, auto=True)
    uuid3 = UUIDField(namespace=uuid.NAMESPACE_URL, version=3, auto=True)
    uuid4 = UUIDField(version=4, auto=True)
    uuid5 = UUIDField(namespace=uuid.NAMESPACE_URL, version=5, auto=True)

class AutoUUIDFieldModel(models.Model):
    uuid = UUIDField(auto=True)


class ManualUUIDFieldModel(models.Model):
    uuid = UUIDField(auto=False)


class NamespaceUUIDFieldModel(models.Model):
    uuid = UUIDField(auto=True, namespace=uuid.NAMESPACE_URL, version=5)


class BrokenNamespaceUUIDFieldModel(models.Model):
    uuid = UUIDField(auto=True, namespace='lala', version=5)


class PrimaryKeyUUIDFieldModel(models.Model):
    uuid = UUIDField(primary_key=True)
    #char = models.CharField(max_length=10, null=True)

class BrokenPrimaryKeyUUIDFieldModel(models.Model):
    uuid = UUIDField(primary_key=True)
    unique = models.IntegerField(unique=True)

    def __repr__(self):
        return {}
