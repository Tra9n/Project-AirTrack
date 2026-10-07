import pytest

from src.aeroplane import Aeroplane


def test_aeroplane_creation_valid():
    p = Aeroplane("UAL1621", "United States", 268.79, 10203.18, 10250.0)
    assert p.callsign == "UAL1621"
    assert p.velocity == 268.79


def test_aeroplane_validation_fails():
    with pytest.raises(ValueError, match="Позывной должен быть непустой строкой"):
        Aeroplane("", "US", 100, 1000)
    with pytest.raises(ValueError, match="Скорость должна быть неотрицательным числом"):
        Aeroplane("A123", "US", -5, 1000)


def test_aeroplane_comparison():
    p1 = Aeroplane("A1", "RU", 200, 5000)
    p2 = Aeroplane("A2", "US", 300, 6000)
    assert p1 < p2
    assert p2 > p1
    assert p1 != p2


def test_cast_to_object_list():
    data = [
        {
            "callsign": "A1",
            "origin_country": "RU",
            "velocity": 200,
            "baro_altitude": 5000,
        }
    ]
    objects = Aeroplane.cast_to_object_list(data)
    assert len(objects) == 1
    assert isinstance(objects[0], Aeroplane)
