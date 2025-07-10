import re, logging

from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from youtube import AudioDownloader, PlaylistDownloader
from youtube import exceptions as youtube_exceptions

from telegram.models import TelegramYoutubeDownload
from .base import BaseCommand


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    _PLAYLIST_ARGUMENT_PATTERN = r'^pl$'
    '''
        Valid youtube url:
        //www.youtube.com/
        https://www.youtube.com/
        www.youtube.com/
        https://youtu.be/
        //youtu.be/
        youtu.be/
    '''
    _YOUTUBE_LINK_PATTERN = r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu\.be))/'


    @property
    def url_argument(self) -> str | None:
        if hasattr(self, '_url_argument'):
            return self._url_argument

        self._url_argument = None
        for item in self.arguments:
            result = re.search(pattern=self._YOUTUBE_LINK_PATTERN, string=item)
            if result is not None:
                self._url_argument = item

        return self._url_argument
    

    def process(self) -> None:
        self.telegram_account.send_message(
            _('Remember that the larger the video size, the longer the processing time')
        )

        if self.url_argument is None:
            self.telegram_account.send_message(_('Youtube link could not be identified'))
            return

        if self.has_playlist_argument():
            self._download_playlist()
            return

        
        self._download_audio()
    
    
    def has_playlist_argument(self) -> bool:
        for item in self.arguments:
            result = re.search(pattern=self._PLAYLIST_ARGUMENT_PATTERN, string=item)
            if result is not None:
                return True
        return False

     
    def _download_playlist(self):
        playlist_downloader = PlaylistDownloader(self.url_argument)
        download_ids_str = ""
        total_downloads = 0

        if not playlist_downloader.is_url_valid():
            self.telegram_account.send_message(
                _('The url doesn\'t have a valid playlist identifier')
            )
            return
    
        while (True):
            try:
                result = playlist_downloader.download_next()

            except StopIteration:
                break

            except youtube_exceptions.ConnectionNotResponded:
                video_link = playlist_downloader.get_current_video_link()
                if video_link is not None:
                    self.telegram_account.send_message(
                        _(f'We could not connect to this <a href="{ video_link }">video</a>')
                    )

            except youtube_exceptions.VideoAgeRestrictedError:
                video_link = playlist_downloader.get_current_video_link()
                if video_link is not None:
                    self.telegram_account.send_message(
                        _(f'Ths <a href="{ video_link }">video</a> has an age restriction and can\'t be accessed')
                    )

            except youtube_exceptions.AudioStreamNotFoundError:
                video_link = playlist_downloader.get_current_video_link()
                if video_link is not None:
                    self.telegram_account.send_message(
                        _(f'This <a href="{ video_link }">video</a> doesn\'t have a supported audio stream')
                    )
            except Exception as exception:
                video_link = playlist_downloader.get_current_video_link()
                if video_link is not None:
                    self.telegram_account.send_message(
                        _(f'An unexpected error occurred while downloading the <a href="{ video_link }">video</a>. A report has been made to our team. This will not interfere with the download')
                    )
                logger.error(f'Playlist download error: {exception}')
                BaseCommand.send_manually_exception_email(exception)

            else:
                telegram_youtube_download = TelegramYoutubeDownload.objects.create(
                    TelegramChatMessage_update_id = self.telegram_chat_message,
                    url = playlist_downloader.get_current_video_link(),
                    file_path = result['file_path'],
                    title = result['title'],
                    content_type = 0
                )
                download_ids_str += f'{telegram_youtube_download.id}-'
                total_downloads += 1


        self.telegram_account.send_message(_(f'A total of {total_downloads} songs were downloaded'))

        if total_downloads > 0:
            audio_player_url = "https://{current_site}{path}".format(
                current_site = Site.objects.get_current(),
                path = reverse_lazy('telegram:audio-player', kwargs={'ids_str': download_ids_str[:-1]}
                )
            )

            self.telegram_account.send_message(
                _(f'You can access them on this this<a href="{ audio_player_url }">link</a>')
            )
        
        


    def _download_audio(self):
        audio_downloader = AudioDownloader(self.url_argument)
        if not audio_downloader.is_url_valid():
            self.telegram_account.send_message(
                _('The url doesn\'t have a valid video identifier')
            )
            return

        try:
            result = audio_downloader.download()
        
        except youtube_exceptions.InvalidUrlError:
            self.telegram_account.send_message(
                _('This command doesn\'t have a supported youtube url')
            )
        
        except youtube_exceptions.ConnectionNotResponded:
            self.telegram_account.send_message(
                _('Couldn\'t connect to youtube, try again later')
            )
        
        except youtube_exceptions.AudioStreamNotFoundError:
            self.telegram_account.send_message(
                _('This url is doesn\'t have a supported audio stream')
            )
        
        except youtube_exceptions.VideoAgeRestrictedError:
            self.telegram_account.send_message(
                _('The video has an age restriction and can\'t be accessed')
            )

        except Exception as exception:
            self.telegram_account.send_message(
                _(f'An unexpected error occurred while downloading the video. A report has been made to our team.')
            )
            logger.error(f'Audio download error: {exception}')
            BaseCommand.send_manually_exception_email(exception)
        
        else:
            telegram_youtube_download = TelegramYoutubeDownload.objects.create(
                TelegramChatMessage_update_id = self.telegram_chat_message,
                url = self.url_argument,
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

            self.telegram_account.send_message(text)