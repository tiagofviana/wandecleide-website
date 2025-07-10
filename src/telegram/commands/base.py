import traceback
from abc import abstractmethod, ABC

from django.conf import settings
from django.core.mail import mail_admins

from telegram.models import TelegramChatMessage, TelegramAccount



class BaseCommand(ABC):
    def __init__(self, telegram_chat_message: TelegramChatMessage):
        self._telegram_chat_message = telegram_chat_message
        self._telegram_account = telegram_chat_message.TelegramAccount_telegram_id
        self._arguments = telegram_chat_message.message.split(' ')[1:]
    

    @property
    def telegram_chat_message(self) -> TelegramChatMessage:
        return self._telegram_chat_message
    

    @property
    def telegram_account(self) -> TelegramAccount:
        return self._telegram_account


    @property
    def arguments(self):
        return self._arguments


    @abstractmethod
    def process(self) -> None:
        pass


    @staticmethod
    def log_exception(exception: Exception):
        if not settings.DEBUG:
            message = traceback.format_exc()
            mail_admins(
                subject='Command error', message=message
            )