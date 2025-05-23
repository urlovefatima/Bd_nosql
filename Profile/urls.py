from django.urls import path
from .views import *
urlpatterns = [
    path('', profil_utilisateur, name='profil_utilisateur'),
    path('profile/<str:email>/', consulted_profil, name='consulted_profil'),
]
