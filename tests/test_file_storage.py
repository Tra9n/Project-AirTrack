import os

import pytest

from src.aeroplane import Aeroplane
from src.file_storage import JSONStorage


@pytest.fixture
def temp_storage(tmp_path):
    filepath = tmp_path / "test.json"
    return JSONStorage(str(filepath))


def test_add_and_get(temp_storage):
    p = Aeroplane("A1", "RU", 100, 2000)
    temp_storage.add_aeroplane(p)
    result = temp_storage.get_aeroplanes(origin_country="RU")
    assert len(result) == 1
    assert result[0].callsign == "A1"


def test_delete(temp_storage):
    p = Aeroplane("A1", "RU", 100, 2000)
    temp_storage.add_aeroplane(p)
    temp_storage.delete_aeroplane(p)
    result = temp_storage.get_aeroplanes()
    assert len(result) == 0


def test_duplicate_add(temp_storage):
    p = Aeroplane("A1", "RU", 100, 2000)
    temp_storage.add_aeroplane(p)
    temp_storage.add_aeroplane(p)  # не добавится дубликат
    result = temp_storage.get_aeroplanes()
    assert len(result) == 1
