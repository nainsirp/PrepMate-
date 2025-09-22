from django.urls import path
from . import views

app_name = 'groupdiscussion'

urlpatterns = [
    path('list/', views.gd_list, name='list'),
    path('manage/', views.manage_gd, name='manage'),
    path('join/<int:session_id>/', views.join_gd, name='join'),
    path('session/<int:session_id>/', views.gd_session, name='session'),
    path('end/<int:session_id>/', views.end_gd, name='end'),
    path('leave/<int:session_id>/', views.leave_gd, name='leave'),
    path('remove-participant/<int:session_id>/<int:participant_id>/', views.remove_participant, name='remove_participant'),
    path('block-participant/<int:session_id>/<int:participant_id>/', views.block_participant, name='block_participant'),
    path('unblock-participant/<int:session_id>/<int:participant_id>/', views.unblock_participant, name='unblock_participant'),
]
