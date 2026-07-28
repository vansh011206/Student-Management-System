from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role        = models.CharField(max_length=20, choices=ROLES, default='student')
    phone       = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default_avatar.png', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username
