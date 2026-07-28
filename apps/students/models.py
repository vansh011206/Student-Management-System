from django.db import models
from apps.accounts.models import CustomUser
from apps.academics.models import Class, Subject

class Teacher(models.Model):
    user           = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id    = models.CharField(max_length=20, unique=True)
    subject        = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    joining_date   = models.DateField()
    qualification  = models.CharField(max_length=200)

    class Meta:
        ordering = ['user__first_name']

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"

class Student(models.Model):
    BLOOD_GROUPS = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    )
    user             = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=20, unique=True)
    student_class    = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    roll_number      = models.IntegerField()
    date_of_birth    = models.DateField()
    blood_group      = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    parent_name      = models.CharField(max_length=100)
    parent_phone     = models.CharField(max_length=15)
    address          = models.TextField()
    admission_date   = models.DateField(auto_now_add=True)
    is_active        = models.BooleanField(default=True)

    class Meta:
        ordering = ['student_class', 'roll_number']

    def __str__(self):
        return f"{self.admission_number} - {self.user.get_full_name() or self.user.username}"
