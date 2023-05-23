from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasklist, name='tasks'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]