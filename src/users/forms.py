import threading
import logging
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django import forms

from .models import CustomGroup

class CustomGroupAdminForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        fields = '__all__'
        widgets = {
            'permissions': FilteredSelectMultiple(_('Permissions'), is_stacked=False)
        }


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _('Email and password incorrect, try again'),
        'invalid_permission': _('This user does not have access permission'),
        'inactive': _('This account has been deactivated'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)     
        self.fields['username'].widget.attrs.pop('autofocus', None)
        
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = ' form-input'

            if self.has_error(field_name):
                self.fields[field_name].widget.attrs['class'] += ' invalid-field'
    

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            
            if self.user_cache.is_staff is False:
                raise forms.ValidationError(self.error_messages['invalid_permission'])
            
            self.confirm_login_allowed(self.user_cache)
    

class ContactForm(forms.Form):
    fullname = forms.CharField(
        required=True,
        label=_('Fullname'),
        max_length=50,
    )

    email = forms.EmailField(
        required=True,
        max_length=100,
        label='Email',
    )

    telephone = forms.CharField(
        required=False,
        label=_('Telephone (optional)'),
        max_length=20,
    )

    message = forms.CharField(
        required=True,
        label=_('Message'),
        max_length=800,
        widget=forms.Textarea()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            if field_name in ('fullname', 'email', 'telephone'):
                self.fields[field_name].widget.attrs['class'] = 'form-input'

            if field_name in ('message',):
                self.fields[field_name].widget.attrs['class'] = 'form-textarea'

            if self.has_error(field_name):
                self.fields[field_name].widget.attrs['class'] += ' invalid-field'


    class EmailThread(threading.Thread):
        def __init__(self, subject, html_message, recipient_list, fail_silently=False):
            self.subject = subject
            self.recipient_list = recipient_list
            self.html_message = html_message
            self.fail_silently = fail_silently
            threading.Thread.__init__(self)

        def run(self):
            send_mail(
                subject=self.subject,
                html_message=self.html_message,
                recipient_list=self.recipient_list,
                message=None,
                from_email=None,
                fail_silently=self.fail_silently,
            )


    def sendEmail(self):
        html_message = f'''
            <div>
                <p style='display:block'>Name: {self.cleaned_data['fullname']}</p>
                <p style='display:block'>Email: {self.cleaned_data['email']}</p>
                <p style='display:block'>Telefone: {self.cleaned_data['telephone']}</p>
                <p style='display:block'>Mensagem: {self.cleaned_data['message']}</p>
            </div>
        '''
        logging.info(f'Website Contact: {html_message}')
        self.EmailThread(
            subject='Contact',
            html_message=html_message,
            recipient_list=[settings.EMAIL_SUPPORT],
        ).start()