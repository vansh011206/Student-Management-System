from django.contrib import admin
from .models import Class, Subject

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'class_name']
    list_filter = ['class_name']
