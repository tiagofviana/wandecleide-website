from abc import abstractmethod, ABC

from telegram.models import TelegramChatMessage


class BaseCommand(ABC):
    @abstractmethod
    def process(self, telegram_chat_message: TelegramChatMessage) -> None:
        pass
              