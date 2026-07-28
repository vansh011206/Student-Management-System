from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.class_list_create, name='class_list'),
    path('classes/<int:class_id>/delete/', views.delete_class, name='delete_class'),
    path('subjects/', views.subject_list_create, name='subject_list'),
    path('subjects/<int:subject_id>/delete/', views.delete_subject, name='delete_subject'),
]
