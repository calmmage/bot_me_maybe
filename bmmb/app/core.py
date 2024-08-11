from typing import Type

from pydantic import BaseSettings

from bmmb.logging_utils import get_logger
from bmmb.data import MongoDatabase, MongoTable, MongoItem


class AppConfig(BaseSettings):
    # Add your settings here, for example:
    db_name: str = None  # = "app_db"
    db_alias: str = None  # = "default"
    db_conn_str: str = None  # =
    # "mongodb://localhost:27017/app_db"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class AppBase:
    name = 'app'
    db: MongoDatabase
    logger = get_logger()  # default
    config: AppConfig

    def flag_enabled(self, flag_name: str):
        return hasattr(self, flag_name) and getattr(self, flag_name)


class AppSettingsMixin(AppBase):
    settings_class: Type[AppConfig] = AppConfig
    APP_SETTINGS_ENABLED = True

    def __init__(self, *args, **kwargs):
        # logger.debug("Settings - super")
        super().__init__()
        # logger.debug("Settings - main")
        # load_dotenv()
        self.settings = self.settings_class(*args, **kwargs)


class AppDatabaseMixin(AppBase):
    APP_DATABASE_ENABLED = True

    def __init__(self, *args, **kwargs):
        # logger.debug("Database - super")
        super().__init__(*args, **kwargs)
        # logger.debug("Database - main")
        if self.flag_enabled('APP_SETTINGS_ENABLED'):
            self.db = MongoDatabase(
                db_name=self.config.db_name or self.name,
                db_alias=self.config.db_alias or self.name,
                conn_str=self.config.db_conn_str
            )
        else:
            self.db = MongoDatabase(
                db_name=self.name,
                db_alias='default',
                conn_str=None
            )


class AppLoggingMixin(AppBase):
    APP_LOGGING_ENABLED = True

    def __init__(self, *args, **kwargs):
        # logger.debug("Logging - super")
        super().__init__(*args, **kwargs)
        # logger.debug("Logging - main")
        if self.flag_enabled('APP_DATABASE_ENABLED'):
            self.logger = self.db.get_logger(
                file_path='log.txt',
            )
        else:
            self.logger = get_logger(
                file_path='log.txt',
                to_mongo=False
            )


class AppUsersMixin(AppBase):
    APP_LOGGING_ENABLED = True
    user_class: Type[MongoItem]

    def __init__(self, *args, **kwargs):
        # logger.debug("Users - super")
        super().__init__(*args, **kwargs)
        # logger.debug("Users - main")
        if self.flag_enabled('APP_DATABASE_ENABLED'):
            self.users: MongoTable = self.db.create_table(
                table_name='users',
                item_type=self.user_class
            )
        else:
            raise NotImplementedError(
                'Implement local storage of users to work without database.'
            )

    # def get_user(self, key):
    # option 1: get by id
    # option 2: get by username

    def get_user(self, **kwargs):
        return self.users.get_item(**kwargs)

    def get_user_by_id(self, user_id):
        return self.users.get_item_by_id(user_id)

    # def add_user(self):
    # option 1: add User object
    # option 2: add with kwargs

    def insert_user(self, user):
        return self.users.insert_item(user)

    def add_user(self, **user_data):
        return self.users.add_item(**user_data)


class App(AppUsersMixin, AppLoggingMixin, AppDatabaseMixin, AppSettingsMixin):
    name = 'app'
