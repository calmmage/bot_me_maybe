import os
import json
from typing import Any, Dict, List, Optional, Type
from .database import Database
from pathlib import Path


class LocalDatabase(Database):
    def __init__(self, data_path: str):
        super().__init__()
        self.data_path = Path(data_path)
        os.makedirs(data_path, exist_ok=True)

    def _get_table_path(self, table: str) -> Path:
        return self.data_path / table

    def _get_file_path(self, table: str, key: str) -> Path:
        return self._get_table_path(table) / f"{key}.json"

    def register_model(self, table_name: str, model: Type):
        super().register_model(table_name, model)
        self._get_table_path(table_name).mkdir(parents=True, exist_ok=True)

    def put(self, table: str, key: str, value: Any) -> None:
        with open(self._get_file_path(table, key), "w") as f:
            json.dump(value, f)

    def get(self, table: str, key: str) -> Any:
        file_path = self._get_file_path(table, key)
        if not file_path.exists():
            return None

        with open(file_path, "r") as f:
            return json.load(f)

    def edit(self, table: str, key: str, new_value: Any) -> None:
        self.put(table, key, new_value)

    def delete(self, table: str, key: str) -> None:
        file_path = self._get_file_path(table, key)
        if file_path.exists():
            file_path.unlink()

    def bulk_put(self, table: str, items: Dict[str, Any]) -> None:
        for key, value in items.items():
            self.put(table, key, value)

    def bulk_get(self, table: str, keys: Optional[List[str]] = None
                 ) -> Dict[str, Any]:
        if keys is None:
            keys = [file.stem for file in self._get_table_path(table).iterdir()
                    if file.suffix == ".json"]

        result = {}
        for key in keys:
            value = self.get(table, key)
            if value is not None:
                result[key] = value
        return result
