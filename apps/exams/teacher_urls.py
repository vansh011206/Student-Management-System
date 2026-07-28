from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('add/', views.create_exam, name='create_exam'),
    path('results/enter/<int:exam_id>/', views.enter_results, name='enter_results'),
]
