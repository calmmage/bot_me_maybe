from abc import ABC, abstractmethod

class TelegramBotAPI(ABC):
    @abstractmethod
    def send_message(self, chat_id, text):
        pass

    @abstractmethod
    def send_photo(self, chat_id, photo):
        pass

    # ... other methods ...
