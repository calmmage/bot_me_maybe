import os
import toml
from typing import Optional


class Configuration:
    def __init__(self, toml_path: Optional[str] = None):
        if not toml_path:
            toml_path = self.discover_config_file()
        with open(toml_path, "r") as f:
            self.config = toml.load(f)

    @staticmethod
    def discover_config_file(config_filenames: Optional[list] = None,
                             search_directories: Optional[list] = None) -> str:
        if config_filenames is None:
            config_filenames = ["config.toml", "app_config.toml"]
        if search_directories is None:
            search_directories = [".", "app_data", os.path.expanduser("~")]

        for directory in search_directories:
            for filename in config_filenames:
                path = os.path.join(directory, filename)
                if os.path.isfile(path):
                    return path

        raise FileNotFoundError("No configuration file found")
