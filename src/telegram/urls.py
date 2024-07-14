from django.urls import path

from . import views

app_name = 'telegram'

urlpatterns = [
    path('settings', view=views.SettingsView.as_view(), name='settings'),
    path('webhook', view=views.WebhookView.as_view(), name='webhook'),
    path('player/<int:id>/', view=views.PlayerView.as_view(), name='player'),
    path('download/<int:id>/',view=views.DownloadView.as_view(), name='download'),
]
