from django.urls import path
from . import views

app_name = 'EventDetail'
urlpatterns = [
    path('<str:id>/', views.post_event, name='event_detail'),
    # path('event/create/', views.create_event, name='create_event'),
    # path('event/update/<str:id>/', views.update_event, name='update_event'),
    # path('event/delete/<str:id>/', views.delete_event, name='delete_event'),
]