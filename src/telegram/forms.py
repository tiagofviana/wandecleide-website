from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import SuspiciousOperation
from .retrived_data import RetrivedData, ChatType

class TelegramForm(forms.Form):
    telegram_data = forms.JSONField()


    def clean_telegram_data(self):
        return self.cleaned_data['telegram_data']

    def get_retrived_data(self) -> RetrivedData:
        telegram_data = self.cleaned_data['telegram_data']
        if 'message' in telegram_data:
            return self._retrive_message_data()
        
        if 'edited_message' in telegram_data:
            return self._retrive_edited_message_data()
        
        if 'my_chat_member' in telegram_data:
            return self._retrive_my_chat_member_data()

        raise SuspiciousOperation(f"Telegram data can not be processed: {telegram_data}")

    def _retrive_message_data(self):
        telegram_data = self.cleaned_data['telegram_data']
        from_data = telegram_data['message']['from']

        return RetrivedData(
            telegram_id=from_data['id'],
            update_id=telegram_data['update_id'],
            username=from_data['username'],
            first_name=from_data['first_name'],
            last_name=from_data['last_name'],
            is_bot=from_data['is_bot'],
            chat_type=ChatType.PRIVATE,
            message_id=telegram_data['message']['message_id'],
            message=telegram_data['message']['text']
        )
    

    def _retrive_edited_message_data(self) -> dict:
        telegram_data = self.cleaned_data['telegram_data']
        from_data = telegram_data['edited_message']['from']

        return RetrivedData(
            telegram_id=from_data['id'],
            update_id=telegram_data['update_id'],
            username=from_data['username'],
            first_name=from_data['first_name'],
            last_name=from_data['last_name'],
            is_bot=from_data['is_bot'],
            chat_type=ChatType.PRIVATE,
            message_id=telegram_data['edited_message']['message_id'],
            message=telegram_data['edited_message']['text']
        )
    