from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Classes"
        ordering = ['name']

    def __str__(self):
        return self.name

class Subject(models.Model):
    name       = models.CharField(max_length=100)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    code       = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"
