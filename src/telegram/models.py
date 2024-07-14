from pathlib import Path
from shutil import rmtree
import requests
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.sites.models import Site
from django.urls import reverse_lazy

class TelegramAccount(models.Model):
    telegram_id = models.PositiveBigIntegerField(
        _('telegram ID'), 
        unique=True, 
        null=False, 
        db_index=True,
        primary_key=True,
        editable=False
    )

    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=255,
        null=False,
        editable=False
    )

    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=255,
        null=True,
        editable=False,
    )

    username = models.CharField(
        verbose_name=_('username'),
        max_length=255,
        null=True
    )
    
    registration_date = models.DateTimeField(
        verbose_name=_('registration date'),
        default=timezone.now,
        editable=False
    )

    last_message_processed_date = models.DateTimeField(
        verbose_name=_('date of last message processed'),
        null=True,
        blank=True,
        editable=False
    )
    
    is_bot = models.BooleanField(
        verbose_name=_('is a bot'),
        null=False,
        blank=False,
        editable=False
    
    )
    is_blocked = models.BooleanField(
        verbose_name=_('is blocked'),
        default=True,
        null=False
    )

    class Meta:
        managed = True
        db_table = 'telegram_account'
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    
    def fullname(self):
        """ Return the 'first_name' and the 'lastName' with a space in between """
        full_name = '%s %s' % (self.first_name, self.last_name or "")
        return full_name.strip()
    fullname.short_description = _('fullname')


    def __str__(self):
        return f"{self.username} ({self.telegram_id})"
    

    def send_message(self, message: str):
        telegram_send_message_url = '{telegram}{token}/sendMessage'.format(
            telegram = settings.TELEGRAM_BOT_API_URL,
            token = settings.TELEGRAM_BOT_TOKEN
        )
        
        requests.get(
            url=telegram_send_message_url,
            data={
                'text':  f'<strong>{message}</strong>',
                'chat_id': self.telegram_id,
                'parse_mode': 'HTML',
            }
        )


class TelegramChatMessage(models.Model):
    TelegramAccount_telegram_id = models.ForeignKey(
        TelegramAccount,
        on_delete=models.RESTRICT,
        verbose_name=_('telegram account'), 
        db_column='TelegramAccount_telegram_id',
        null=False,
        db_index=True
    )

    update_id = models.PositiveBigIntegerField(
        verbose_name=_('update ID'),
        help_text=_(
            "update's unique identifier, allows you to ignore repeated updates or to restore the correct update sequence"
        ),
        primary_key=True,
        null=False,
        db_index=True,
    )

    message_id = models.PositiveIntegerField(
        verbose_name=_('message ID'),
        null=False,
        help_text=_("unique message identifier inside the chat")
    )

    message = models.CharField(
        verbose_name=_('message'),
        max_length=255,
        unique=False,
        null=False,
    )

    request_data = models.JSONField(
        verbose_name=_("request data"),
        null=False
    )

    response_data = models.JSONField(
        verbose_name=_("response data"),
        null=True,
    )
    
    creation_date = models.DateTimeField(
        verbose_name=_('creation date'),
        null=False,
        default=timezone.now,
        editable=False
    )

    class Meta:
        managed = True
        db_table = 'telegram_chat_message'
        verbose_name = _('chat message')
        verbose_name_plural = _('chat messages')


    def __str__(self):
        return f"{self.update_id}"


    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            self.TelegramAccount_telegram_id.last_message_processed_date = timezone.now()
            self.TelegramAccount_telegram_id.save(update_fields=['last_message_processed_date'])
        return super().save(*args, **kwargs)
    
    
    @staticmethod
    def remove_old_chat_messages():
        six_days_ago = timezone.now() - timezone.timedelta(days=6)
        return TelegramChatMessage.objects.filter(creation_date__lte=six_days_ago).delete()



class TelegramYoutubeDownload(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name='ID',
        editable=False
    )

    url = models.URLField(
        null=False,
        blank=False,
        help_text=_('Youtube url where file was downloaded from')
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        unique=False,
        null=False,
    )

    CONTENT_TYPE =  [
        (0, 'audio/mp3'),
    ]

    content_type = models.PositiveSmallIntegerField(
        verbose_name=_('content type'),
        choices=CONTENT_TYPE
    )

    TelegramAccount_telegram_id = models.ForeignKey(
        TelegramAccount,
        on_delete=models.RESTRICT,
        verbose_name=_('telegram account'), 
        db_column='TelegramAccount_telegram_id',
        null=False,
        blank=False,
        db_index=True,
    )

    file_path = models.FilePathField(
        verbose_name=_('file path'),
        path=(settings.BASE_DIR / 'temp' / 'youtube').resolve(),
        allow_folders=False,
        allow_files=True,
        recursive=True,
        max_length=200,
        null=False,
        blank=False,
    )

    creation_date = models.DateTimeField(
        verbose_name=_('creation date'),
        null=False,
        default=timezone.now,
        editable=False
    )

    class Meta:
        managed = True
        db_table = 'telegram_youtube_download'
        verbose_name = _('Youtube download')
        verbose_name_plural = _('Youtube downloads')


    def __str__(self):
        return f"{self.file_path}"
    

    def generate_player_full_url(self):
        return "https://{current_site}{path}".format(
            current_site = Site.objects.get_current(),
            path = reverse_lazy(
                viewname='telegram:player',
                kwargs={
                    'id': self.id,
                }
            )
        )

    @staticmethod
    def remove_old_youtube_downloads():
        three_days_ago = timezone.now() - timezone.timedelta(days=3)
        return TelegramYoutubeDownload.objects.filter(creation_date__lte=three_days_ago).delete()


@receiver(models.signals.post_delete, sender=TelegramYoutubeDownload)
def auto_delete_file_on_delete_telegram_youtube_download(sender, instance, **kwargs):
    """
        Deletes file from filesystem when corresponding `TelegramYoutubeDownload` object is deleted.
    """
    if instance.file_path:
        dir_path = Path(instance.file_path).parent
        if dir_path.exists():
            rmtree(dir_path.resolve())