from django.urls import path
from .views import inscription, connexion, accueil, deconnexion
urlpatterns = [
    path("inscription/", inscription, name = 'inscription'),
    path("connexion/", connexion, name = 'connexion'),
    path("deconnexion/", deconnexion, name = 'deconnexion'),
    path("", accueil, name = 'accueil')
]