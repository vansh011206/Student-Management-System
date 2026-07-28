from django.db import models
from apps.accounts.models import CustomUser
from apps.academics.models import Class, Subject
from apps.students.models import Student

class Exam(models.Model):
    TYPES = (
        ('unit_test', 'Unit Test'),
        ('midterm', 'Mid Term'),
        ('final', 'Final Exam'),
    )
    name        = models.CharField(max_length=100)
    exam_type   = models.CharField(max_length=20, choices=TYPES)
    subject     = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    class_name  = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    exam_date   = models.DateField()
    total_marks = models.IntegerField(default=100)
    created_by  = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-exam_date', 'name']

    def __str__(self):
        return f"{self.name} - {self.subject.name} ({self.class_name.name})"

class Result(models.Model):
    student        = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    exam           = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.FloatField()
    remarks        = models.CharField(max_length=200, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'exam')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.name}: {self.marks_obtained}/{self.exam.total_marks}"

    @property
    def percentage(self):
        if not self.exam.total_marks:
            return 0.0
        return round((self.marks_obtained / self.exam.total_marks) * 100, 2)

    @property
    def grade(self):
        p = self.percentage
        if p >= 90: return 'A+'
        elif p >= 80: return 'A'
        elif p >= 70: return 'B+'
        elif p >= 60: return 'B'
        elif p >= 50: return 'C'
        elif p >= 40: return 'D'
        else: return 'F'

    @property
    def is_pass(self):
        return self.marks_obtained >= (self.exam.total_marks * 0.40)
