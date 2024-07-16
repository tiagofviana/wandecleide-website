import logging
import json, os
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import SuspiciousOperation
import requests

from .models import TelegramAccount
from .retrived_data import RetrivedData
from .commands import command_manager
from . import forms
from .models import TelegramYoutubeDownload, TelegramChatMessage


class SettingsView(TemplateView):
    template_name = 'telegram/settings.html'
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            raise Http404()
        
        return super().dispatch(request, *args, **kwargs)  
    

    def has_permission(self) -> bool:
        return self.request.user.is_superuser  
    

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['telegram'] = {
            'settings': self._telagram_settings_request(),
            'delete': self._delete_url(),
            'setup': self._setup_url()
        }
        return context
    
    def _setup_url(self) -> str:
        webhook_url = "https://{current_site}{webhook}".format(
            current_site = str(get_current_site(self.request)),
            webhook = reverse('telegram:webhook')
        )

        return "{telegram}{token}/setWebhook?url={webhook_url}&secret_token={secret_token}".format(
            telegram = settings.TELEGRAM_BOT_API_URL,
            token = settings.TELEGRAM_BOT_TOKEN,
            webhook_url = webhook_url,
            secret_token = settings.TELEGRAM_BOT_SECRET
        )
    
    def _delete_url(self) -> str:
        return '{telegram}{token}/deleteWebhook'.format(
            telegram = settings.TELEGRAM_BOT_API_URL,
            token = settings.TELEGRAM_BOT_TOKEN
        )


    def  _telagram_settings_request(self) -> dict:
        url = '{telegram}{token}/getWebhookInfo'.format(
            telegram = settings.TELEGRAM_BOT_API_URL,
            token = settings.TELEGRAM_BOT_TOKEN
        )

        result = requests.get(url).json()['result']
        return json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False)

class WebhookView(View):
    http_method_names = ['post',]

    ERROR_MESSAGES = {
        'bot': _("We don't process commands from bots"),
        'blocked': _("Your account was blocked, talk to the support team to find out more"),
        'invalid_command': _("This command is not valid"),
    }

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            raise SuspiciousOperation("Invalid secret key in telegram webhook")

        return super().dispatch(request, *args, **kwargs)
    
    def has_permission(self) -> bool:
        secret_token = self.request.headers.get('X-Telegram-Bot-Api-Secret-Token', None)
        if secret_token != settings.TELEGRAM_BOT_SECRET:
            return False
        
        return True
    
    def post(self, request) -> JsonResponse:
        telegram_form = forms.TelegramForm({'telegram_data': request.body})
        
        if not telegram_form.is_valid():
            raise SuspiciousOperation(f"Invalid telegram webhook form. Errors: {telegram_form.errors}")
        
        retrived_data: RetrivedData = telegram_form.get_retrived_data()

        if retrived_data.is_already_responded():
            logging.debug('Already responded')
            return JsonResponse({})
        
        if not retrived_data.is_allowed_chat_type():
            return JsonResponse({
                'method': 'leaveChat',
                'chat_id': retrived_data.telegram_id
            })
        
        if retrived_data.telegram_account.is_bot:
            return JsonResponse({
                'method': 'sendMessage',
                'text': str(self.ERROR_MESSAGES['bot']),
                'chat_id': retrived_data.telegram_id,
                'reply_to_message_id': retrived_data.message_id,
            })
        
        if retrived_data.telegram_account.is_blocked:
            return JsonResponse({
                'method': 'sendMessage',
                'text': str(self.ERROR_MESSAGES['blocked']),
                'chat_id': retrived_data.telegram_id,
                'reply_to_message_id': retrived_data.message_id,
            })
        
        if not command_manager.is_command_valid(retrived_data):
            return {
                'method': 'sendMessage',
                'text':  self.ERROR_MESSAGES['invalid_command'],
                'chat_id': retrived_data.telegram_id,
                'reply_to_message_id': retrived_data.message_id,
            }
        
        TelegramChatMessage.objects.create(
            TelegramAccount_telegram_id = retrived_data.telegram_account,
            update_id = retrived_data.update_id,
            message_id = retrived_data.message_id,
            message = retrived_data.message,
            request_data = telegram_form.cleaned_data['telegram_data']
        )
        
        command_manager.execute(retrived_data)

        return JsonResponse({})
    

class PlayerView(TemplateView):
    template_name = 'telegram/player.html'
    http_method_names = ['get']
        
    def get(self, request, id: int, *args, **kwargs):
        TelegramYoutubeDownload.remove_old_youtube_downloads()
        youtube_download = TelegramYoutubeDownload.objects.filter(id=id).first()

        self.additional_context = {
            'youtube_download': youtube_download            
        }

        if youtube_download:
            self.additional_context.update({
                'id': id
            })

        return super().get(request, id, *args, **kwargs)
    

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update(self.additional_context)
        return context
    

class DownloadView(View):
    http_method_names = ['get']
        
    def get(self, request, id: int, *args, **kwargs):
        youtube_download = get_object_or_404(TelegramYoutubeDownload, id=id)
        content_type = youtube_download.get_content_type_display()

        with open(youtube_download.file_path, 'rb') as f:
           file_data = f.read()

        response = HttpResponse(file_data, content_type=content_type)

        if content_type == 'audio/mp3':
            response['Content-Disposition'] = f'attachment; filename="{youtube_download.title}.mp3"'
            # Support for partial requests from the client for file downloads
            response['Accept-Ranges'] = 'bytes'

        return response

    
