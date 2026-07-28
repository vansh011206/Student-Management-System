from django.db import models
from apps.students.models import Student, Teacher

class Attendance(models.Model):
    STATUS = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    student   = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date      = models.DateField()
    status    = models.CharField(max_length=10, choices=STATUS)
    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    remark    = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date', 'student__roll_number']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.date}: {self.status}"
