from telegram_api import TelegramBotAPI

class PythonTelegramBotAPI(TelegramBotAPI):
    def __init__(self, token):
        import telegram
        self.bot = telegram.Bot(token=token)

    def send_message(self, chat_id, text):
        self.bot.send_message(chat_id=chat_id, text=text)

    def send_photo(self, chat_id, photo):
        self.bot.send_photo(chat_id=chat_id, photo=photo)

    # ... other methods ...
