# from typing import Any, Dict, List, Optional
# from pymongo import MongoClient
# from .database import Database
#
#
# class MongoDBDatabase(Database):
#     def __init__(self, connection_string: str, db_name: str):
#         super().__init__()
#         self.client = MongoClient(connection_string)
#         self.db = self.client[db_name]
#
#     def put(self, table: str, key: str, value: Any) -> None:
#         self.db[table].update_one({"_id": key}, {"$set": value}, upsert=True)
#
#     def get(self, table: str, key: str) -> Any:
#         result = self.db[table].find_one({"_id": key})
#         if result:
#             del result["_id"]
#         return result
#
#     def edit(self, table: str, key: str, new_value: Any) -> None:
#         self.put(table, key, new_value)
#
#     def delete(self, table: str, key: str) -> None:
#         self.db[table].delete_one({"_id": key})
#
#     def bulk_put(self, table: str, items: Dict[str, Any]) -> None:
#         for key, value in items.items():
#             self.put(table, key, value)
#
#     def bulk_get(self, table: str, keys: Optional[List[str]] = None) -> Dict[
#         str, Any]:
#         query = {} if keys is None else {"_id": {"$in": keys}}
#         result = {item["_id"]: {k: v for k, v in item.items() if k != "_id"} for
#                   item in self.db[table].find(query)}
#         return result
