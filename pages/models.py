from django.db import models
from django.utils.text import slugify


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class TextBlock(models.Model):
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Block {self.id}"


class Footer(models.Model):
    text = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "Site Footer"