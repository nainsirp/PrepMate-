from django.urls import path
from . import views

app_name = 'aptitude'

urlpatterns = [
    path('tests/', views.test_list, name='tests'),
    path('take/<str:category>/', views.take_test, name='take_test'),
    path('results/', views.test_results, name='results'),
    path('manage/', views.manage_tests, name='manage'),
    path('result/<int:result_id>/', views.test_detail, name='test_detail'),
]
