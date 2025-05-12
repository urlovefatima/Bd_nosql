from django.urls import path
from .views import app_info

urlpatterns = [
    path('PageAdmin/<str:id>/', app_info, name='admin_page'),
]
