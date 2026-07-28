from django.contrib import admin
from .models import Exam, Result

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'subject', 'class_name', 'exam_date', 'total_marks']
    list_filter = ['exam_type', 'class_name', 'subject']
    search_fields = ['name']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'marks_obtained', 'grade', 'percentage', 'is_pass']
    list_filter = ['exam__class_name', 'exam__subject']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'exam__name']
