import toml
from enum import Enum
from typing import Any, Dict
from injector import Module, provider, singleton

from .database import Database
from .local_database import LocalDatabase
from .mongo_database import MongoDBDatabase


class DatabaseType(Enum):
    LOCAL = "local"
    MONGODB = "mongodb"


class DatabaseConfig:
    def __init__(self, database_type: DatabaseType,
                 connection_data: Dict[str, Any]):
        self.database_type = database_type
        self.connection_data = connection_data


# def create_database(config: DatabaseConfig) -> Database:
#     if config.database_type == DatabaseType.LOCAL:
#         return LocalDatabase(config.connection_data["data_path"])
#     elif config.database_type == DatabaseType.MONGODB:
#         return MongoDBDatabase(
#             config.connection_data["connection_string"],
#             config.connection_data["db_name"]
#         )
#     else:
#         raise ValueError(f"Unknown database type: {config.database_type}")


class DatabaseModule(Module):
    @singleton
    @provider
    def provide_database(self, configuration: DatabaseConfig) -> Database:
        # return create_database(configuration)
        if config.database_type == DatabaseType.LOCAL:
            return LocalDatabase(config.connection_data["data_path"])
        elif config.database_type == DatabaseType.MONGODB:
            return MongoDBDatabase(
                config.connection_data["connection_string"],
                config.connection_data["db_name"]
            )
        else:
            raise ValueError(f"Unknown database type: {config.database_type}")


if __name__ == '__main__':
    # test code
    config = load_configuration()
