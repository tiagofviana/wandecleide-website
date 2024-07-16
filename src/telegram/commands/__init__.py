from threading import Thread
import os, importlib, logging
from typing import Callable
from django.utils.translation import gettext as _
from telegram.models import TelegramChatMessage
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


    def execute(self, telegram_chat_message: TelegramChatMessage) -> dict:
        logger.debug(f'Starting to process the message: {telegram_chat_message.message}')
        command = telegram_chat_message.message.split(' ')[0]
        
        if not self.is_command_valid(command):
            raise RuntimeError(f'The command "{command}" is not valid')

        command_obj: BaseCommand = self.commands[command]()

        class RunnerThread(Thread):
            def __init__(
                self, 
                fn: Callable[[TelegramChatMessage], None],
                telegram_chat_message: TelegramChatMessage, 
                group = None, *args, **kwargs
            ):
                super().__init__(group, args, kwargs)
                self._fn = fn
                self._telegram_chat_message = telegram_chat_message



            def run(self) -> None:
                try:
                   self._fn(self._telegram_chat_message)
                except Exception as exception:
                    logger.error(f'Fail to run the chat message "{telegram_chat_message.update_id}". Error: {exception}')
                    self._telegram_chat_message.TelegramAccount_telegram_id.send_message(
                        _('Something went wrong in processing. A report has been sent to our team and we will fix it as soon as possible.')
                    )
                finally:
                    del self._fn, self._telegram_chat_message

        runner_thread = RunnerThread(fn=command_obj.process, telegram_chat_message=telegram_chat_message)
        runner_thread.start()

    
    def is_command_valid(self, command: str) -> bool:
        ''' command example: `/example` '''
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