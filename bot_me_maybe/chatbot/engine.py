from abc import ABC, abstractmethod
from typing import List

from bot_me_maybe.chatbot.command_description import CommandDescription


class Engine(ABC):
    @abstractmethod
    def chat(self, message: str) -> str:
        pass

    @abstractmethod
    def get_commands(self) -> List[CommandDescription]:
        pass

    @abstractmethod
    def run(self):
        pass