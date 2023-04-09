from abc import ABC, abstractmethod
from .command_description import CommandDescription


class UserInterface(ABC):
    @abstractmethod
    def register_message_handler(self, handler: callable):
        pass

    @abstractmethod
    def register_command_handler(self, handler: CommandDescription):
        pass

    @abstractmethod
    def run(self):
        pass


