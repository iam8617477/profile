from django.db import models


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

    def __str__(self):
        return self.title if self.title else 'Untitled'
