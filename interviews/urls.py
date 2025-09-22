from django.urls import path
from . import views

app_name = 'interviews'

urlpatterns = [
    path('list/', views.interview_list, name='list'),
    path('manage/', views.manage_interviews, name='manage'),
]
