import re
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from youtube import AudioDownloader
from youtube.exceptions import AudioStreamNotFoundError, InvalidUrlError
from telegram.retrived_data import RetrivedData
from telegram.models import TelegramYoutubeDownload
from .base import BaseCommand

class Command(BaseCommand):
    def process(self, retrived_data: RetrivedData) -> dict:
        arguments = retrived_data.message.split(' ')[1:]
        youtube_url = self._get_youtube_url(*arguments)
        retrived_data.telegram_account.send_message(
            _('We have received your request and started processing it. Remember that the larger the video size, the longer the processing time')
        )
        
        try:
            audio_downlaoder = AudioDownloader(youtube_url)
            result = audio_downlaoder.download()
        except AudioStreamNotFoundError:
            return {
                'method': 'sendMessage',
                'text':  _('This url is doesn\'t have a supported audio stream'),
                'chat_id': retrived_data.telegram_id,
                'reply_to_message_id': retrived_data.message_id,
            }
        except InvalidUrlError:
            return {
                'method': 'sendMessage',
                'text':  _('This command doesn\'t have a supported youtube url'),
                'chat_id': retrived_data.telegram_id,
                'reply_to_message_id': retrived_data.message_id,
            }
        
        telegram_youtube_download = TelegramYoutubeDownload.objects.create(
            TelegramAccount_telegram_id = retrived_data.telegram_account,
            file_path = result['file_path'],
            url = youtube_url,
            title = result['title'],
            content_type = 0
        )

        context = {
            'player_url' : telegram_youtube_download.generate_player_full_url()
        }

        return {
            'chat_id': retrived_data.telegram_id,
            'method': 'sendMessage',
            'reply_to_message_id': retrived_data.message_id,
            'parse_mode': 'HTML',
            'text': render_to_string('telegram/commands/yt/response.html', context)
        }

    def _get_youtube_url(self, *args) -> str | None:
        '''
            This function supports the following patterns:

                //www.youtube.com/v/y6120QOlsfU
                https://www.youtube.com/watch?v=y6120QOlsfU
                www.youtube.com/v/y6120QOlsfU
                https://youtu.be/y6120QOlsfU
                //youtu.be/y6120QOlsfU
                youtu.be/y6120QOlsfU
        '''
        for item in args:
            youtube_url_pattern = r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu\.be))/((?:[\w\-]+\?v=|v\/)?)'
            result = re.search(pattern=youtube_url_pattern, string=item)
            if result is not None:
                return item