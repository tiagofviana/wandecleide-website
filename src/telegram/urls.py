from django.urls import path, re_path

from . import views

app_name = 'telegram'

urlpatterns = [
    path('settings', view=views.SettingsView.as_view(), name='settings'),
    path('webhook', view=views.WebhookView.as_view(), name='webhook'),
    path('get-file/<int:id>/',view=views.GetFileView.as_view(), name='get-file'),
    re_path(r'^audio-player/(?P<ids_str>([0-9]+-)*[0-9]+)/$', view=views.AudioPlayerView.as_view(), name='audio-player'),
    re_path(
        r'^download/multiple-audio/(?P<ids_str>([0-9]+-)*[0-9]+)/$',
        view=views.MultipleAudioDonwloadView.as_view(),
        name='multiple-audio-download'
    ),
]