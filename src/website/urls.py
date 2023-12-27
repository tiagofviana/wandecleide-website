from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/login/', lambda request: redirect(settings.LOGIN_URL)),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

urlpatterns += i18n_patterns(
    path('', include('users.urls')),
)