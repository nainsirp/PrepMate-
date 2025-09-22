from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('student/', views.student_dashboard, name='student'),
    path('assessor/', views.assessor_dashboard, name='assessor'),
    path('health/', views.health_check, name='health_check'),
]
