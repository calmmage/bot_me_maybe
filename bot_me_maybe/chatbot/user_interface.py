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


class CLIUserInterface(UserInterface):
    def __init__(self):
        self.message_handler = None
        self.command_handlers = {}

    def register_message_handler(self, handler: callable):
        self.message_handler = handler

    def register_command_handler(self, command_description: CommandDescription):
        self.command_handlers[command_description.name] = command_description.func
        for shortcut in command_description.shortcuts:
            self.command_handlers[shortcut] = command_description.func

    def run(self):
        while True:
            user_input = input("User: ")
            user_message = ""
            while user_input:
                user_message += user_input
                user_input = input("... ")

            if user_message.startswith('/'):
                parts = user_message.split(maxsplit=2)
                command = parts[0][1:]
                if command in self.command_handlers:
                    self.command_handlers[command](parts[1:])
                else:
                    print("Invalid command. Try again.")
            else:
                response = self.message_handler(user_message)
                print(f"Bot: {response}")
