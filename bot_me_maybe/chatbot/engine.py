from abc import ABC, abstractmethod
from typing import Dict

from bot_me_maybe.chatbot.command_description import CommandDescription


class Engine(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def chat(self, message: str) -> str:
        pass

    @abstractmethod
    def get_commands(self) -> Dict[str, CommandDescription]:
        pass

    @abstractmethod
    def run(self):
        pass