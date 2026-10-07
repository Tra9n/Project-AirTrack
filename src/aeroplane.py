from typing import Any, Dict, List, Optional


class Aeroplane:
    """Класс для представления информации о самолёте."""

    def __init__(
        self,
        callsign: str,
        origin_country: str,
        velocity: float,
        baro_altitude: float,
        geo_altitude: float = 0.0,
    ):
        self.callsign = callsign
        self.origin_country = origin_country
        self.velocity = velocity
        self.baro_altitude = baro_altitude
        self.geo_altitude = geo_altitude

        self._validate()

    def _validate(self):
        """Валидация данных."""
        if not isinstance(self.callsign, str) or not self.callsign:
            raise ValueError("Позывной должен быть непустой строкой")
        if not isinstance(self.origin_country, str) or not self.origin_country:
            raise ValueError("Страна регистрации должна быть непустой строкой")
        if not isinstance(self.velocity, (int, float)) or self.velocity < 0:
            raise ValueError("Скорость должна быть неотрицательным числом")
        if not isinstance(self.baro_altitude, (int, float)) or self.baro_altitude < 0:
            raise ValueError(
                "Барометрическая высота должна быть неотрицательным числом"
            )
        if not isinstance(self.geo_altitude, (int, float)) or self.geo_altitude < 0:
            raise ValueError("Геометрическая высота должна быть неотрицательным числом")

    def __repr__(self):
        return (
            f"Aeroplane(callsign='{self.callsign}', origin_country='{self.origin_country}', "
            f"velocity={self.velocity}, baro_altitude={self.baro_altitude}, "
            f"geo_altitude={self.geo_altitude})"
        )

    def __str__(self):
        return (
            f"Самолёт {self.callsign} ({self.origin_country}): "
            f"скорость {self.velocity} м/с, высота {self.baro_altitude} м"
        )

    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнение по скорости (для сортировки по возрастанию)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity < other.velocity

    def __le__(self, other):
        return self.velocity <= other.velocity

    def __eq__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (
            self.callsign == other.callsign
            and self.origin_country == other.origin_country
            and self.velocity == other.velocity
            and self.baro_altitude == other.baro_altitude
        )

    @classmethod
    def cast_to_object_list(cls, data_list: List[Dict[str, Any]]) -> List["Aeroplane"]:
        """Преобразует список словарей в список объектов Aeroplane."""
        objects = []
        for item in data_list:
            try:
                obj = cls(
                    callsign=item.get("callsign", ""),
                    origin_country=item.get("origin_country", "Unknown"),
                    velocity=item.get("velocity", 0.0),
                    baro_altitude=item.get("baro_altitude", 0.0),
                    geo_altitude=item.get("geo_altitude", 0.0),
                )
                objects.append(obj)
            except ValueError as e:
                print(f"Пропуск некорректных данных: {e} -> {item}")
                continue
        return objects
