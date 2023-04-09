from telegram_api import TelegramBotAPI


class AiogramAPI(TelegramBotAPI):
    def __init__(self, token):
        import aiogram.bot
        self.bot = aiogram.bot.Bot(token=token)

    async def send_message(self, chat_id, text):
        await self.bot.send_message(chat_id=chat_id, text=text)

    async def send_photo(self, chat_id, photo):
        await self.bot.send_photo(chat_id=chat_id, photo=photo)

    # ... other methods ...
