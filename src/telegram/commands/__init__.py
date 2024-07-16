from threading import Thread
import os, importlib, logging
from typing import Callable
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
        logger.debug(f'Starting to process the message: {retrived_data.message}')
        command = retrived_data.message.split(' ')[0]

        if not self.is_command_valid(retrived_data):
            raise RuntimeError(f'The command "{command}" is not valid')

        command_obj: BaseCommand = self.commands[command]()

        class RunnerThread(Thread):
            def __init__(
                self, 
                fn: Callable[[RetrivedData], None],
                retrived_data: RetrivedData, 
                group = None, *args, **kwargs
            ):
                super().__init__(group, args, kwargs)
                self._fn = fn
                self._retrived_data = retrived_data



            def run(self) -> None:
                try:
                   self._fn(self._retrived_data)
                except Exception as exception:
                    text = f'Fail to run the message "{retrived_data.message}". Error: {exception}'
                    logger.error(text)
                    self._retrived_data.telegram_account.send_message(
                        _('Something went wrong in processing. A report has been sent to our team and we will fix it as soon as possible.')
                    )
                finally:
                    del self._fn, self._retrived_data

        runner_thread = RunnerThread(fn=command_obj.process, retrived_data=retrived_data)
        runner_thread.start()

    
    def is_command_valid(self, retrived_data: RetrivedData) -> bool:
        command = retrived_data.message.split(' ')[0]
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