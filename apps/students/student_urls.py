from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('export/csv/', views.export_students_csv, name='export_students_csv'),
    path('<int:student_id>/', views.student_detail, name='student_detail'),
    path('<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('<int:student_id>/pdf/', views.generate_student_pdf, name='student_pdf'),
]
