from mongoengine import StringField, EmbeddedDocumentField, BooleanField

from bmmb.app.core import App, AppConfig
from bmmb.data import MongoItem
from bmmb.data.mongo_utils import MongoSubItem


class ChatSummaryConfig(AppConfig):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "CHAT_SUMMARY_"


class UserConfig(MongoSubItem):
    # todo: create template __repr__ for embedded documents
    disabled = BooleanField(default=False)


class User(MongoItem):
    username = StringField(required=True, unique=True)
    email = StringField()
    full_name = StringField()
    config = EmbeddedDocumentField(UserConfig, default=UserConfig())


class ChatSummary(App):
    name = "chat_summary"
    settings_class = ChatSummaryConfig
    user_class = User


if __name__ == '__main__':
    app = ChatSummary()
# app.settings.debug
