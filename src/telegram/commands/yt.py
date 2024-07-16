import re
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from youtube import AudioDownloader
from youtube.exceptions import AudioStreamNotFoundError, InvalidUrlError, VideoAgeRestrictedError
from telegram.models import TelegramYoutubeDownload, TelegramChatMessage
from .base import BaseCommand

class Command(BaseCommand):
    def process(self, telegram_chat_message: TelegramChatMessage) -> None:
        telegram_account = telegram_chat_message.TelegramAccount_telegram_id
        arguments = telegram_chat_message.message.split(' ')[1:]
        youtube_url = self._get_youtube_url(*arguments)

        telegram_account.send_message(
            _('We have received your request and started processing it. Remember that the larger the video size, the longer the processing time')
        )
        
        try:
            audio_downlaoder = AudioDownloader(youtube_url)
            result = audio_downlaoder.download()

            telegram_youtube_download = TelegramYoutubeDownload.objects.create(
                TelegramChatMessage_update_id = telegram_chat_message,
                url = youtube_url,
                file_path = result['file_path'],
                title = result['title'],
                content_type = 0
            )

            text = render_to_string(
                template_name = 'telegram/commands/yt/response.html',
                context = {
                    'player_url' : telegram_youtube_download.generate_player_full_url()
                }
            )

            telegram_account.send_message(text)
        

        except InvalidUrlError:
            telegram_account.send_message(
                _('This command doesn\'t have a supported youtube url')
            )
        except AudioStreamNotFoundError:
            telegram_account.send_message(
                _('This url is doesn\'t have a supported audio stream')
            )
        
        except VideoAgeRestrictedError:
            telegram_account.send_message(
                _('The video has an age restriction and can\'t be accessed')
            )


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