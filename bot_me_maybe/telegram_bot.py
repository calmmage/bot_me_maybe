from enum import Enum

class Engine(Enum):
    """Engines for the bot to use"""
    PTB = "python-telegram-bot"
    AIOGRAM = "aiogram"
    PYROGRAM = "pyrogram"

class TelegramBot:
    """Base class for the bot"""
    def __init__(self, token, engine, base_dir ):
        self.token = token
        self.engine = engine
        # discover plugins

        # load config

        # initialise plugins
        for plugin in self.plugins:
            pass
    # def __init__(self):
    #     self.config = {"property1": "value1", "property2": "value2"}
    #     self.plugins = []
    #
    # def load_plugins(self):
    #     for plugin_class in ... # get the plugin classes
    #         plugin = plugin_class(self)
    #         self.plugins.append(plugin)
    #
    # def add_plugins_from_folder(self, folder_path):
    #     for module_name in os.listdir(folder_path):
    #         if module_name.endswith('.py'):
    #             module = importlib.import_module(module_name[:-3], folder_path)
    #             for name in dir(module):
    #                 obj = getattr(module, name)
    #                 if isinstance(obj, type) and issubclass(obj, PluginBase) and obj != PluginBase:
    #                     self.plugins.append(obj(self))

    #
    # def send_message(self, chat_id, text):
    #     """Sends a message to a chat"""
    #     raise NotImplementedError
    #
    # def send_photo(self, chat_id, photo):
    #     """Sends a photo to a chat"""
    #     raise NotImplementedError
    #
    # # ... other methods ...

