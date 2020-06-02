from django.db import models
from django.db.models import Avg
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from course.fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify

import numpy as np

class Classe(models.Model):
    classe_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('classe_name',)

    def __str__(self):
        return self.classe_name


class Course(models.Model):
    prof = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='courses_created', on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, related_name='courses', on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses_joined', blank=False)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.titre

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.titre)


class ItemBase(models.Model):
    prof = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_related', on_delete=models.CASCADE)
    titre = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self})

    def __str__(self):
        return self.titre

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    fichier = models.FileField(upload_to='course/fichier/')

class Image(ItemBase):
    image = models.FileField(upload_to='course/fichier/')

class Video(ItemBase):
    video = models.FileField(upload_to='course/fichier/')


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, limit_choices_to={'model__in':('text', 'video', 'image', 'file')}, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.module.titre
    