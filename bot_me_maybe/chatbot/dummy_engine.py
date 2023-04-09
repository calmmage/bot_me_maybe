from bot_me_maybe.chatbot import Engine, CLIUserInterface, Chatbot, CommandDescription, register_commands, command
from typing import Dict


@register_commands()
class DummyEngine(Engine):
    def chat(self, message: str) -> str:
        return f"DummyEngine: {message}"

    @command()
    def start(self):
        return "Starting DummyEngine"

    @command()
    def help(self):
        return "DummyEngine help"

    def get_commands(self) -> Dict[str, CommandDescription]:
        return {
            command: CommandDescription.from_func(getattr(self, name))
            for command, name in self.commands.items()
        }

    def run(self):
        pass


if __name__ == '__main__':
    engine = DummyEngine()
    user_interface = CLIUserInterface()
    chatbot = Chatbot(engine, user_interface)
    chatbot.run()
