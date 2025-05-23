from django.urls import path
from .views import *
urlpatterns = [
    path('evenement/<str:email>/', get_historique_event, name='get_historique_event'),
    path('reservation/<str:email>/', get_historique_event_reserved, name='get_historique_event_reserved'),
]
