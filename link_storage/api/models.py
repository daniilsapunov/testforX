from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    TYPES = [
        ('website', 'Website'),
        ('book', 'Book'),
        ('article', 'Article'),
        ('music', 'Music'),
        ('video', 'Video'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(unique=True)
    image = models.URLField(blank=True)
    link_type = models.CharField(max_length=20, choices=TYPES, default='website')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    collections = models.ManyToManyField('Collection', related_name='links', blank=True)

    def __str__(self):
        return self.collections


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
