import asyncio
import logging
from functools import wraps
from typing import List, Tuple

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot_me_maybe.chatbot import UserInterface, Chatbot, CommandDescription
from bot_me_maybe.chatbot.dummy_engine import DummyEngine
from defaultenv import ENVCD as env

# lib_path = os.path.expanduser('/')
# if lib_path not in sys.path:
#     sys.path.append(lib_path)

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def argument_parser(command_text: str):
    """Parse the command text into a list of arguments"""
    from projects.active.chatgpt_enhancer_bot.chatgpt_enhancer_bot.utils import parse_query
    # todo: finish the updated implementation drafted at bot_me_maybe/chatbot/drafts/command_parser.py
    _, args, kwargs = parse_query(command_text)
    return args, kwargs


def add_argument_parser(func):
    """Decorator to add the argument parser to the telegram function"""

    @wraps(func)
    async def wrapper(update: Update, context):
        args, kwargs = argument_parser(update.message.text)
        result = func(*args, **kwargs)
        if not result:
            result = f"Command {func.__name__} finished successfully"
        await update.message.reply_text(result)

    return wrapper


def pass_update_text(func):
    """Decorator to pass the update text to the function"""

    @wraps(func)
    async def wrapper(update: Update, context):
        result = func(update.message.text)
        await update.message.reply_text(result)

    return wrapper


class PTBUserInterface(UserInterface):
    """Single User PTB interface """

    def __init__(self, token: str, username: str):
        # Create the Application and pass it your bot's token.
        self.application = Application.builder().token(token).build()
        self.username = username
        self.commands: List[Tuple[str, str]] = []

    def register_command_handler(self, command_description: CommandDescription):
        commands = [command_description.name] + command_description.shortcuts

        callback = add_argument_parser(command_description.func)
        # on different commands - answer in Telegram
        for command in commands:
            self.application.add_handler(CommandHandler(
                command,
                callback=callback,
                filters=filters.User(username=self.username)
            ))
            self.commands.append((command, command_description.doc.splitlines()[0]))

    def register_message_handler(self, chat: callable):
        # on non command i.e message - echo the message on Telegram
        callback = pass_update_text(chat)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, callback))

    def _update_commands(self):
        """Update the commands list"""
        asyncio.run(self.application.bot.set_my_commands(self.commands))

    def run(self):
        self._update_commands()
        # Run the bot until the user presses Ctrl-C
        self.application.run_polling()


# try a simple ptb bot
if __name__ == '__main__':
    # test ptb ui.
    ui = PTBUserInterface(token=env.telegram_token, username=env.telegram_username)
    engine = DummyEngine()
    chatbot = Chatbot(engine, ui)
    chatbot.run()

# bot = GptOnPoint()
#
# # simple CLI:
# while True:
#     user_message = input('User: ')
#     if user_message == '/next_stage':
#         bot.next_stage()
#     elif user_message.startswith("/set_scenario"):
#         goal = input("Specify the goal: ")  # todo - check not empty. fancy input utils? ~require not empty
#         print("Specify the scenario steps")  # , starting each with '-'")
#         stages = []
#         step = input("Next step or empty to finish: ").lstrip('- ')
#         while step:
#             stages.append(step)
#             step = input("Next step or empty to finish: ").lstrip('- ')
#
#         bot.set_scenario(stages, goal)
#     # elif user_message == '/previous_stage':
#     #     scenario.previous_stage()
#     else:
#         response = bot.chat(user_message)
#         print(f'Bot: {response}')
