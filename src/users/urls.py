from django.conf import settings
from django.urls import include, path
from django.contrib.auth.views import LogoutView 
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from . import views

app_name = 'users'

urlpatterns = [
    path('', TemplateView.as_view(template_name='users/index.html'), name='index'),
    path(_('contact/'), views.ContactFormView.as_view(), name='contact'),
    path(_('about/'), TemplateView.as_view(template_name='users/about.html'), name='about'),
    path(_('my-work/'), TemplateView.as_view(template_name='users/my-work.html'), name='my-work'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGIN_URL), name='logout'),
]
