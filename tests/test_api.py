import pytest

from src.api import AeroplanesAPI


def test_get_country_bounds():
    api = AeroplanesAPI()
    bounds = api.get_country_bounds("Russia")
    assert "south" in bounds
    assert "north" in bounds
    assert "west" in bounds
    assert "east" in bounds
    assert bounds["south"] < bounds["north"]
    assert bounds["west"] < bounds["east"]


def test_get_aeroplanes():
    api = AeroplanesAPI()
    planes = api.get_aeroplanes("France")
    assert isinstance(planes, list)
    if planes:
        assert "callsign" in planes[0]
