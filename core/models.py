import uuid

from django.db import models
from django.conf import settings

from pckgs.crpt.sync_encryptor import SyncEncryptor


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Command(models.Model):
    code = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title if self.title else 'Untitled'


class Note(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=2000, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        if self.description:
            encryptor = SyncEncryptor()
            encrypted_description, _ = encryptor.encrypt(
                data=self.description,
                passphrase=settings.SECRET_KEY
            )
            self.description = encrypted_description

        super().save(*args, **kwargs)

    def get_decrypted_description(self):
        if not self.description:
            return None

        encryptor = SyncEncryptor()
        decrypted_description = encryptor.decrypt(
            encrypted_data=self.description,
            passphrase=settings.SECRET_KEY
        )
        return decrypted_description


    def __str__(self):
        return self.title if self.title else 'Untitled'


class File(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
