from django.urls import path
from .views import inscription, connexion, accueil, deconnexion, upload_photo
urlpatterns = [
    path("inscription/", inscription, name = 'inscription'),
    path('upload-photo/', upload_photo, name='upload_photo'),
    path("connexion/", connexion, name = 'connexion'),
    path("deconnexion/", deconnexion, name = 'deconnexion'),
    path("", accueil, name = 'accueil')
]