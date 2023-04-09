"""
A way to convert callable python commands with arbitrary arguments
into universal commands for telegram bot

CommandParser should accept string and return *args, **kwargs sets.

Later on, the CommandParser object / class would be used to handle commands

I have three clear options in mind right away:
1) trivial parser str -> (), {}
2) singular parser str -> (arg) where it returns all
3) Single-line parser
"/cmd arg1 arg2 kwarg1=1 kwarg2=2" -> (arg1, arg2), {"kwarg1": 1, "kwarg2": 2}
4) Multi-line parser
5) Body parser
first line - command and kwargs
rest of the lines - body (main arg, text)
"""

from abc import ABC, abstractmethod
from typing import Tuple


class CommandParser(ABC):
    @abstractmethod
    def parse(self, message: str) -> Tuple[tuple, dict]:  # args, kwargs
        pass


# option 1 - implement multiple different parsers and chose among them
class NoArgsParser(CommandParser):
    def parse(self, message: str) -> Tuple[tuple, dict]:
        return (), {}


class SingleArgParser(CommandParser):
    def parse(self, message: str) -> Tuple[tuple, dict]:
        if message.startswith('/'):
            message = message[1:]
        return (message,), {}


class MultiLineParser(CommandParser):
    def parse(self, message: str) -> Tuple[tuple, dict]:
        pass


def select_arg_parser(func):
    """Select which arg parser is optimal for """
    pass


# option 2 - implement one parser and use it for all commands
MISSING = object()


class ArgDescription:
    def __init__(self, name, type=None, default=MISSING, doc=None):
        self.name = name
        self.type = type
        self.default = default
        self.doc = doc


def get_expected_args(func) -> list[ArgDescription]:
    """Get expected args for the function"""
    pass


def parse_args(message, expected_args):
    """Parse args from the message
    Logic:
    - all text is treated as single arg
    - kwargs start with --: --kwarg1 1 --kwarg2 2
    - if type is str: all text until the end of the line or the next arg is treated as a single arg.
    Special case: "". Then
    - if not str: just until space"""
    pass
