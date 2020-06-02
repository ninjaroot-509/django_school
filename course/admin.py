import csv
import datetime

from django.http import HttpResponse
from django.contrib import admin
from course.models import *
from django.utils.translation import gettext_lazy as _

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ['classe_name', 'slug']
    prepopulated_fields = {'slug': ('classe_name',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['titre', 'classe', 'created']
    list_filter = ['created', 'classe']
    search_fields = ['titre', 'description']
    prepopulated_fields = {'slug': ('titre',)}
    inlines = [ModuleInline]

admin.site.register(Content)
admin.site.register(Text)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(File)
