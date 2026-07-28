from django.urls import path
from . import views
from apps.attendance.views import my_attendance
from apps.exams.views import my_results

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('attendance/', my_attendance, name='my_attendance'),
    path('results/', my_results, name='my_results'),
]
