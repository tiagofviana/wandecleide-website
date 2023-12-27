import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import reverse, redirect
from django.utils.translation import gettext_lazy as _

from .forms import *


class Login(LoginView):
    form_class=CustomAuthenticationForm
    template_name='users/login.html'
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('admin:index')
    

class ContactFormView(FormView):
    template_name = 'users/contact.html'
    form_class = ContactForm
    
    def form_valid(self, form) -> HttpResponse:
        form.sendEmail()
        self.request.session[settings.SESSION_REDIRECT_URL] = reverse('users:index')
        messages.success(
            request=self.request, 
            message=_('Message received, I will contact you as soon as possible.')
        )
        return redirect('core:messages')
