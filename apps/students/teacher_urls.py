from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('add/', views.add_teacher, name='add_teacher'),
    path('<int:teacher_id>/edit/', views.edit_teacher, name='edit_teacher'),
    path('<int:teacher_id>/delete/', views.delete_teacher, name='delete_teacher'),
]
