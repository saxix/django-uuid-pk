import uuid
from django.db import models
from django_uuid_pk.fields import UUIDField


class ModelUUIDField(models.Model):
    uuid1 = UUIDField(version=1, auto=True)
    uuid3 = UUIDField(namespace=uuid.NAMESPACE_URL, version=3, auto=True)
    uuid4 = UUIDField(version=4, auto=True)
    uuid5 = UUIDField(namespace=uuid.NAMESPACE_URL, version=5, auto=True)

class AutoUUIDField(models.Model):
    uuid = UUIDField(auto=True)


class ManualUUIDField(models.Model):
    uuid = UUIDField(auto=False)


class NamespaceUUIDField(models.Model):
    uuid = UUIDField(auto=True, namespace=uuid.NAMESPACE_URL, version=5)


class BrokenNamespaceUUIDField(models.Model):
    uuid = UUIDField(auto=True, namespace='lala', version=5)


class PrimaryKeyUUIDField(models.Model):
    uuid = UUIDField(primary_key=True)


class BrokenPrimaryKeyUUIDField(models.Model):
    uuid = UUIDField(primary_key=True)
    unique = models.IntegerField(unique=True)
