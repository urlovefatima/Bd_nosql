from django.urls import path
from django.views.generic import TemplateView
from .views import *
urlpatterns = [
    path('', profil_utilisateur, name='profil_utilisateur'),
    path('profile/<str:email>/', consulted_profil, name='consulted_profil'),
    path('infos/', infos_utilisateur, name='infos-user')
]
