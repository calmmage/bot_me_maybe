from typing import Any, Dict, Type, Optional, List

# from .database_interface import DatabaseInterface
#
#
# class Table:
#     def __init__(
#             self, database: DatabaseInterface, table_name: str, model: Type):
#         self._database = database
#         self._table_name = table_name
#         self._model = model
#
#     def put(self, key: str, item: Any) -> None:
#         self._database.put(self._table_name, key, item)
#
#     def get(self, key: str) -> Any:
#         result = self._database.get(self._table_name, key)
#         return self._model(**result) if result is not None else None
#
#     def edit(self, key: str, new_value: Any) -> None:
#         self._database.edit(self._table_name, key, new_value)
#
#     def delete(self, key: str) -> None:
#         self._database.delete(self._table_name, key)
#
#     def bulk_put(self, items: Dict[str, Any]) -> None:
#         self._database.bulk_put(self._table_name, items)
#
#     def bulk_get(self, keys: Optional[List[str]] = None) -> Dict[str, Any]:
#         result = self._database.bulk_get(self._table_name, keys)
#         return {key: self._model(**value) for key, value in result.items()}
#
#     def __getitem__(self, key: str) -> Any:
#         return self.get(key)
#
#     def __setitem__(self, key: str, value: Any) -> None:
#         self.put(key, value)
#
#     def __delitem__(self, key: str) -> None:
#         self.delete(key)






#
# # generate tests for the above snippet
# from bmmb.data.database.table import Table
# from bmmb.data.database.database_interface import DatabaseInterface
# from bmmb.data.database.local_database import LocalDatabase
# from bmmb.data.database.mongo_database import MongoDBDatabase
# from bmmb.data.database.config import DatabaseType, Configuration, load_configuration, create_database
#
# import pytest
# from unittest.mock import MagicMock, patch
# from typing import Any, Dict, Type, Optional, List
#
# def test_table_init():
#     database = MagicMock(DatabaseInterface)
#     table_name = "test_table"
#     model = MagicMock()
#     table = Table(database, table_name, model)
#     assert table._database == database
#     assert table._table_name == table_name
#     assert table._model == model