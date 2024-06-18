from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/login/', lambda request: redirect(settings.LOGIN_URL)),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('error/test', lambda x:None),
]

urlpatterns += i18n_patterns(
    path('', include('users.urls')),
)

if settings.DEBUG:
    from django.views.generic import TemplateView
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path('404', TemplateView.as_view(template_name='404.html')),
        path('500', TemplateView.as_view(template_name='500.html')),
    ]
