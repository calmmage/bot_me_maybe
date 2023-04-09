from telegram_api import TelegramBotAPI


class PyrogramAPI(TelegramBotAPI):
    def __init__(self, token):
        import pyrogram
        self.client = pyrogram.Client(token=token)

    def send_message(self, chat_id, text):
        self.client.send_message(chat_id=chat_id, text=text)

    def send_photo(self, chat_id, photo):
        self.client.send_photo(chat_id=chat_id, photo=photo)

    # ... other methods ...
