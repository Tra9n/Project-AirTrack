import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from src.aeroplane import Aeroplane


class BaseStorage(ABC):
    """Абстрактный класс для работы с хранилищем данных о самолётах."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет информацию о самолёте в хранилище."""
        pass

    @abstractmethod
    def get_aeroplanes(self, **filters) -> List[Aeroplane]:
        """Возвращает список самолётов по заданным фильтрам (например, по стране регистрации)."""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет информацию о самолёте из хранилища."""
        pass


class JSONStorage(BaseStorage):
    """Хранилище в JSON-файле."""

    def __init__(self, filepath: str = "data/aeroplanes.json"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Создаёт файл и папку, если их нет."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _read_data(self) -> List[Dict[str, Any]]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_data(self, data: List[Dict[str, Any]]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._read_data()
        for item in data:
            if (
                item.get("callsign") == aeroplane.callsign
                and item.get("origin_country") == aeroplane.origin_country
            ):
                return
        data.append(
            {
                "callsign": aeroplane.callsign,
                "origin_country": aeroplane.origin_country,
                "velocity": aeroplane.velocity,
                "baro_altitude": aeroplane.baro_altitude,
                "geo_altitude": aeroplane.geo_altitude,
            }
        )
        self._write_data(data)

    def get_aeroplanes(self, **filters) -> List[Aeroplane]:
        data = self._read_data()
        result = []
        for item in data:
            match = True
            for key, value in filters.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                try:
                    result.append(Aeroplane(**item))
                except ValueError:
                    continue
        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._read_data()
        new_data = [
            item
            for item in data
            if not (
                item.get("callsign") == aeroplane.callsign
                and item.get("origin_country") == aeroplane.origin_country
            )
        ]
        if len(new_data) == len(data):
            print("Самолёт не найден, удаление не выполнено.")
        self._write_data(new_data)
