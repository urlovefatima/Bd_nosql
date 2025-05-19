from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .views import get_events, get_events_categories, delete_event, create_event, get_events_gratuits, get_events_payants, get_events_aujourdhui, get_events_semaine, get_events_mois, get_historique

urlpatterns = [
    # path('events/', get_events, name='events'),
    path('test/', get_events, name='events'),
    path('categories/', get_events_categories, name='categories'),
    path('gratuits/', get_events_gratuits, name='gratuits'),
    path('payants/', get_events_payants, name='payants'),
    path('aujourdhui/', get_events_aujourdhui, name='aujourdhui'),
    path('semaine/', get_events_semaine, name='semaine'),
    path('mois/', get_events_mois, name='mois'),
    path('delete_event/', delete_event, name='delete_event'),
    path('create_event/', create_event, name='create_event'),
    path('historique/', get_historique, name='historique'),
    # path('test/', TemplateView.as_view(template_name='test.html'), name='test',
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
