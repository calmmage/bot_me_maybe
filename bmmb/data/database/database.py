from typing import Type
from abc import ABC

from .database_interface import DatabaseInterface
from .table import Table


class Database(DatabaseInterface, ABC):
    def __init__(self):
        self._tables = {}

    def register_model(self, table_name: str, model: Type):
        self._tables[table_name] = Table(self, table_name, model)

    def get_table(self, table_name: str) -> Table:
        return self._tables.get(table_name)

    def __getattr__(self, table_name: str) -> Table:
        return self.get_table(table_name)
