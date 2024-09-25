from django.db import models


class Link(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField()
    image = models.ImageField()
    link_type = models.TextField(default='website')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
