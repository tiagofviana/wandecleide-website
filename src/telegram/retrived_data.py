from enum import Enum
from django.utils import timezone
from .models import TelegramAccount, TelegramChatMessage


class ChatType(Enum):
    PRIVATE = 1
    GROUP = 2


class RetrivedData:
    def __init__(self, telegram_id: int, update_id: int, username: str, first_name: str, last_name: str, is_bot: bool, message_id: int, message: str,  chat_type: ChatType):
        self._telegram_id =  telegram_id
        self._update_id = update_id
        self._username = username
        self._first_name = first_name
        self._last_name = last_name
        self._is_bot = is_bot
        self._message = message
        self._message_id = message_id
        self._chat_type = chat_type


    @property
    def telegram_id(self) -> int:
        return self._telegram_id


    @property
    def chat_type(self) -> ChatType:
        return self._chat_type
    
    
    @property
    def message_id(self) -> int:
        return self._message_id
    

    @property
    def message(self) -> str:
        return self._message
    
    
    @property
    def update_id(self) -> int:
        return self._update_id
    

    @property
    def telegram_account(self) -> TelegramAccount:
        if hasattr(self, '_telegram_account'):
            return self._telegram_account

        telegram_account, was_created = TelegramAccount.objects.get_or_create(
            telegram_id=self._telegram_id,
            defaults={
                'first_name': self._first_name,
                'last_name': self._last_name,
                'username': self._username,
                'is_bot': self._is_bot,
            }
        )

        if not was_created:
            telegram_account = self.update_account(telegram_account)

        self._telegram_account = telegram_account
        return self._telegram_account
    

    def update_account(self, telegram_account: TelegramAccount) -> TelegramAccount:
        account_data = {
            'first_name': self._first_name,
            'last_name': self._last_name,
            'username':self._username,
            'is_bot': self._is_bot,
        }
        update_fields = []

        # Look for updates
        for key in account_data.keys():
            new_value = account_data[key]
            old_value = getattr(telegram_account, key)

            if new_value != old_value:
                setattr(telegram_account, key, new_value)
                update_fields.append(key)
        
        if not update_fields:
            # Update database
            telegram_account.save(update_fields=update_fields)

        return telegram_account
    

    def is_already_responded(self) -> bool:
        if hasattr(self, '_is_already_responded'):
            return self._is_already_responded

        TelegramChatMessage.remove_old_chat_messages()
        self._is_already_responded = TelegramChatMessage.objects.filter(update_id=self._update_id).exists()
        return self._is_already_responded
    
    
    def is_allowed_chat_type(self) -> bool:
        if self.chat_type == ChatType.GROUP:
            return False
        
        return True
