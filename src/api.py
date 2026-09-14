import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()


class BaseAPI(ABC):
    """Абстрактный класс для работы с внешними API."""

    @abstractmethod
    def get_country_bounds(self, country: str) -> Dict[str, float]:
        """Получает bounding box страны через nominatim."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """Получает данные о самолётах через opensky для заданной страны."""
        pass


class AeroplanesAPI(BaseAPI):
    """Реализация API для nominatim и opensky."""

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"
    APP_NAME = "AirTrack-CourseWork"
    APP_VERSION = "1.0"

    def __init__(self):
        self.nominatim_contact = os.getenv("NOMINATIM_CONTACT", "").strip()

        if not self.nominatim_contact:
            print(
                "  NOMINATIM_CONTACT не задан в .env.\n"
                "   Nominatim может блокировать запросы.\n"
                "   Скопируйте .env.example в .env и укажите свой контакт."
            )

    def _user_agent(self) -> str:
        """Формирует User-Agent. Если contact пустой — используем заглушку."""
        contact = self.nominatim_contact or "(+https://github.com/your-username)"
        return f"{self.APP_NAME}/{self.APP_VERSION} {contact}"

    def get_country_bounds(self, country: str) -> Dict[str, float]:
        """Запрос к nominatim, возвращает {'south': ..., 'north': ..., 'west': ..., 'east': ...}."""
        params = {"q": country, "format": "json", "limit": 1}
        headers = {"User-Agent": self._user_agent()}

        try:
            response = requests.get(
                self.NOMINATIM_URL, params=params, headers=headers, timeout=30
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                raise ValueError(f"Страна '{country}' не найдена")
            bbox = data[0]["boundingbox"]
            return {
                "south": float(bbox[0]),
                "north": float(bbox[1]),
                "west": float(bbox[2]),
                "east": float(bbox[3]),
            }
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка запроса к nominatim: {e}")

    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """Получает список самолётов в границах страны через opensky."""
        bounds = self.get_country_bounds(country)
        params = {
            "lamin": bounds["south"],
            "lamax": bounds["north"],
            "lomin": bounds["west"],
            "lomax": bounds["east"],
        }

        try:
            response = requests.get(self.OPENSKY_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            states = data.get("states", [])

            result = []
            for state in states:
                aeroplane_dict = {
                    "icao24": state[0],
                    "callsign": state[1].strip() if state[1] else "",
                    "origin_country": state[2] or "Unknown",
                    "time_position": state[3],
                    "last_contact": state[4],
                    "longitude": state[5],
                    "latitude": state[6],
                    "baro_altitude": state[7] or 0.0,
                    "on_ground": state[8],
                    "velocity": state[9] or 0.0,
                    "true_track": state[10],
                    "vertical_rate": state[11],
                    "sensors": state[12],
                    "geo_altitude": state[13] or 0.0,
                    "squawk": state[14],
                    "spi": state[15],
                    "position_source": state[16],
                }
                result.append(aeroplane_dict)

            return result
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка запроса к opensky: {e}")
