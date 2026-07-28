from django.contrib import admin
from .models import Teacher, Student

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'subject', 'assigned_class', 'joining_date']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_number', 'user', 'student_class', 'roll_number', 'is_active']
    list_filter = ['student_class', 'is_active', 'blood_group']
    search_fields = ['admission_number', 'user__first_name', 'user__last_name', 'user__username']
