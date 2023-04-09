class PluginBase:
    def __init__(self, main_instance):
        self.main = main_instance

class MainClass:
    def __init__(self):
        self.plugins = []

    def add_plugin(self, plugin):
        plugin_instance = plugin(self)
        self.plugins.append(plugin_instance)

import importlib

class PluginBase:
    def __init__(self, main_instance):
        self.main = main_instance


# Main configuration

import toml

with open("config.toml", "r") as f:
    config = toml.load(f)

main_config = config["main"]
plugins_config = config["plugins"]


class PluginClass:
    def __init__(self, main_class):
        self.main_class = main_class

    def do_something(self):
        config = self.main_class.config
        # access the configuration stored in the main class
        ...
