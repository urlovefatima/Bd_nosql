from django.urls import path
from .views import get_events

urlpatterns = [
    path('events/', get_events, name='events'),
    # path('categories/', get_events_categories, name='categories'),
#     path('delete_event/', delete_event, name='delete_event'),
#     path('create_event/', create_event, name='create_event'),
# 
]
