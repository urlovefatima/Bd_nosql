from django.urls import path
from .views import app_info, stats_view, user_section, delete_user, event_section,delete_event,search_events,search_users

urlpatterns = [
    path('stats/', stats_view, name='stats'),
    path('admin-acceuil', app_info, name='admin_acceuil'), 
    path('users/', user_section, name='user_section'),
    path('events/', event_section, name='event_section'),
    path('delete_user/<str:email>/', delete_user, name='delete_user'),
    path('delete_event/<str:id>/', delete_event, name='delete_event'),
    path('search/events/', search_events, name='search_events'),
    path('search/users/', search_users, name='search_users'),
]
