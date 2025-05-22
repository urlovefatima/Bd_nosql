from django.urls import path
from .views import inscription, connexion, accueil

urlpatterns = [
    path("inscription/", inscription, name = 'inscription'),
    path("connexion/", connexion, name = 'connexion'),
    path("accueil/", accueil, name = 'accueil')
]