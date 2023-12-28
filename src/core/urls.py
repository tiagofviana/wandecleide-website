from django.conf import settings
from django.urls import path
from django.shortcuts import redirect
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from .sitemaps import SITEMAPS


from . import views

app_name = 'core'

urlpatterns = [
    path('messages/', views.MessagesTemplateView.as_view(), name='messages'),
    # FAVICONS
    path('favicon.ico', lambda request: redirect('/static/core/favicons/favicon.ico')),
    path('android-chrome-512x512.png', lambda request: redirect('/static/core/favicons/android-chrome-512x512.png')),
    path('android-chrome-192x192.png', lambda request: redirect('/static/core/favicons/android-chrome-192x192.png')),
    path('favicon-32x32.png', lambda request: redirect('/static/core/favicons/favicon-32x32.png')),
    path('favicon-16x16.png', lambda request: redirect('/static/core/favicons/favicon-16x16.png')),
    path('site.webmanifest', lambda request: redirect('/static/core/favicons/site.webmanifest')),
    # SEO
    path('sitemap.xml', sitemap,{'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views.sitemap'),
]

handler404 = TemplateView.as_view(template_name='core/errors/404.html')
handler500 = TemplateView.as_view(template_name='core/errors/500.html')

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path('404', handler404),
        path('500', handler500),
    ]
