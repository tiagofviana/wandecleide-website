from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from . import forms, models


class Login(LoginView):
    form_class = forms.CustomAuthenticationForm
    template_name = 'users/login.html'
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('admin:index')
    

class ContactFormView(FormView):
    template_name = 'users/contact.html'
    form_class = forms.ContactForm
    
    def form_valid(self, form) -> HttpResponse:
        form.sendEmail()
        self.request.session[settings.SESSION_REDIRECT_URL] = reverse('users:index')
        messages.success(
            request=self.request, 
            message=_('Message received, I will contact you as soon as possible.')
        )
        return redirect('core:messages')

class MyWorkTemplateView(TemplateView):
    template_name='users/my-work.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['like_dislike_1'] = models.LikeDislikeCounter.objects.get(id=1)
        context['like_dislike_2'] = models.LikeDislikeCounter.objects.get(id=2)
        return context
    
class LikeDislikeView(View):
    http_method_names = ['post', 'get']
    
    def get(self, request, id, reply, is_update, *args, **kwargs):
        counter = get_object_or_404(models.LikeDislikeCounter, id=id)
        is_update = True if is_update == 1 else False
        
        if reply == 'like':
            counter.qt_likes += 1
            if is_update:
                counter.qt_dislikes -=1

        if reply == 'dislike':
            counter.qt_dislikes +=1
            if is_update:
                counter.qt_likes -=1

        if reply == 'remove-like':
            counter.qt_likes -=1

        if reply == 'remove-dislike':
            counter.qt_dislikes -=1

        counter.save(update_fields=['qt_likes', 'qt_dislikes']) 
        return HttpResponse('ok')