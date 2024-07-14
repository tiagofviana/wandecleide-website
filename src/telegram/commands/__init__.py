import os, importlib, logging
from django.utils.translation import gettext as _

from telegram.retrived_data import RetrivedData
from .base import BaseCommand


__all__ = ["command_manager"]


logger = logging.getLogger(__name__)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class CommandManager:
    @property
    def commands(self) -> dict:
        if hasattr(self, '_commands'):
            return self._commands
        
        self._commands = dict()
        for filename in self._get_command_filenames():
            keyword = f'/{filename[:-3]}'
            self._commands[keyword] = self._load_command_class(filename)

        return self._commands


    def execute(self, retrived_data: RetrivedData) -> dict:
        logger.debug(f'Starting process message: {retrived_data.message}')
        command = retrived_data.message.split(' ')[0]

        if not self.is_command_valid(command):
            return {
                'method': 'sendMessage',
                'text':  _("This command is not valid"),
                'chat_id': retrived_data.telegram_id,
                'reply_to_message_id': retrived_data.message_id,
            }
        try:
            command_obj: BaseCommand = self.commands[command]()
            return command_obj.process(retrived_data)
        except Exception as exception:
            retrived_data.telegram_account.send_message(
                _("An error occurred while we were processing your request"),
            )

            retrived_data.telegram_account.send_message(
                _("A report has been sent to our team, we will fix it as soon as possible"),
            )

            raise exception
    

    def is_command_valid(self, command: str) -> bool:
        if command not in self.commands:
            return False
        
        return True
    

    def _get_command_filenames(self) -> list:
        return [
            filename for filename in os.listdir(CURRENT_DIR)
                if os.path.isfile(f'{CURRENT_DIR}/{filename}')
                if filename.endswith('.py')
                if not filename.startswith('__init__.py')
                if not filename.startswith('base.py')
        ]


    def _load_command_class(self, filename: str) -> BaseCommand:
        module_name = f'telegram.commands.{filename[:-3]}'
        module = importlib.import_module(module_name)
        command_class = module.Command
        if not issubclass(command_class, BaseCommand):
            raise NotImplementedError(f"Module: {module} is not a subclass of {BaseCommand}")
        
        return command_class



command_manager = CommandManager()