from abc import abstractmethod, ABC

from telegram.retrived_data import RetrivedData


class BaseCommand(ABC):
    @abstractmethod
    def process(self, retrived_data: RetrivedData) -> dict:
        pass
              