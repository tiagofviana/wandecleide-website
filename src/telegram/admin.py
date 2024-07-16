import json
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.templatetags.static import static
from django.utils.translation import gettext as _, ngettext
from django.contrib import messages
from . import models

@admin.register(models.TelegramAccount)
class TelegramAccountAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'telegram_id', 'registration_date')
    search_fields = ('telegram_id',)
    readonly_fields = (
        'telegram_id', 'first_name', 'last_name', 'username', 'is_bot', 'registration_date', 'last_message_processed_date'
    )
    fieldsets = (        
        (_('Telegram data'), {
            'fields': ('telegram_id', ('first_name', 'last_name'), 'username', 'is_bot'),
        }),

        (_('System data'), {
            'fields': ('registration_date', 'last_message_processed_date'),
        }),

        (_('Permissions'), {
            'fields': ('is_blocked',),
        }),
    )

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
    
    def has_add_permission(self, request, obj=None) -> bool:
        return False



@admin.register(models.TelegramChatMessage)
class TelegramChatMessageAdmin(admin.ModelAdmin):
    change_list_template = 'telegram/admin/chat-message-changelist.html'
    list_display = ('update_id', 'TelegramAccount_telegram_id', 'message', 'creation_date')
    ordering = ('creation_date',)
    search_fields = ('TelegramAccount_telegram_id__telegram_id', 'message')
    readonly_fields = ('TelegramAccount_telegram_id', 'update_id', 'message_id', 'creation_date', 'message', 'request_data')
    fieldsets = (        
        (_('Telegram data'), {
            'fields': ('update_id', 'TelegramAccount_telegram_id', 'message_id', 'message',),
        }),

        (_('System data'), {
            'fields': ('creation_date',),
        }),

        ('JSON', {
            'fields': ('prettified_request_data', 'prettified_response_data'),
        }),

    )

    def player_link(self, obj):
        return format_html(
            '<a target="_blank" href="{}">Player</a>',
            reverse('telegram:player', kwargs={'id': 1}),
        )  
    player_link.short_description = _("player link")


    def prettified_request_data(self, obj):
        indented_request_data = json.dumps(
            obj.request_data,
            sort_keys = True,
            indent = 4,
            ensure_ascii = False
        )

        return format_html(
            '''
                <script src="{}" defer></script>
                <pre style="overflow: auto;"><code class="hljs language-json">{}</code></pre>
                
            ''',
            static('telegram/_js/highlight/json.min.js'),
            indented_request_data
        ) 
    prettified_request_data.short_description = _("request data")


    def prettified_response_data(self, obj):
        indented_response_data = json.dumps(
            obj.response_data,
            sort_keys = True,
            indent = 4,
            ensure_ascii = False
        )

        return format_html(
            # "telegram/_js/highlight/json.min.js" already imported at prettified_request_data
            '''
                <pre><code class="hljs language-json">{}</code></pre>
            ''',
            indented_response_data
        ) 
    prettified_response_data.short_description = _("response data")

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('cm-remove-old-data', self.remove_old_data, name='cm-remove-old-data')
        ]
        return urls
    
    def remove_old_data(self, request, *args):
        amount, objs = models.TelegramChatMessage.remove_old_chat_messages()
        text = ngettext(
            '{amount} chat message was successfully removed.',
            '{amount} chat messages were successfully removed.',
            amount
        )
        messages.success(request, text.format(amount = amount))
        return redirect('admin:telegram_telegramchatmessage_changelist')


    def has_change_permission(self, request, obj=None) -> bool:
        return False
    
    def has_add_permission(self, request, obj=None) -> bool:
        return False
    


@admin.register(models.TelegramYoutubeDownload)
class TelegramYoutubeDownloadAdmin(admin.ModelAdmin):
    change_list_template = 'telegram/admin/youtube-download-changelist.html'
    list_display = ('id', 'TelegramChatMessage_update_id', 'file_path')
    fieldsets = (        
        (_('Identifier'), {
            'fields': ('id', 'TelegramChatMessage_update_id'),
        }),

        (_('Data'), {
            'fields': ('url', 'file_path', 'player_link','creation_date',),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('ytd-remove-old-data', self.remove_old_data, name='ytd-remove-old-data')
        ]
        return urls
    
    def remove_old_data(self, request, *args):
        amount, objs = models.TelegramYoutubeDownload.remove_old_youtube_downloads()
        text = ngettext(
            '{amount} download was successfully removed.',
            '{amount} downloads were successfully removed.',
            amount
        )
        messages.success(request, text.format(amount = amount))
        return redirect('admin:telegram_telegramyoutubedownload_changelist')

    def has_change_permission(self, request, obj=None) -> bool:
        return False
    
    def has_add_permission(self, request, obj=None) -> bool:
        return False


    def player_link(self, obj):
        return format_html(
            '<a target="_blank" href="{}">Player</a>',
            reverse('telegram:player', kwargs={'id': obj.id}),
        )  
    player_link.short_description = _("player link")


    