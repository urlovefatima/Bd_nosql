from django.urls import path
from . import views

app_name = 'EventDetail'
urlpatterns = [
    path('<str:id>/', views.post_event, name='event_detail'),
    path('<str:id>/reserver/', views.reserve_evenement, name='reserve_evenement'),
    path('<str:id>/annuler/', views.annuler_reserve_evenement, name='annuler_reserve_evenement'),
]
