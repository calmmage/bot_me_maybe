from .engine import Engine
from .user_interface import UserInterface


class Chatbot:
    def __init__(self, engine: Engine, user_interface: UserInterface):
        self.engine = engine
        self.user_interface = user_interface
        # register commands from
        commands = engine.get_commands()
        for command in commands.values():
            user_interface.register_command_handler(command)

        # register message handler
        message_handler = engine.chat
        user_interface.register_message_handler(message_handler)

    def run(self):
        self.engine.run()
        self.user_interface.run()

# code to run the chatbot
