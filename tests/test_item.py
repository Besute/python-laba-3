import pytest

from catalog.errors import ItemError
from catalog.library import Item


def test_create_item():
    item = Item("Лекционная", "101", "Главный корпус", "2024-09-01")

    assert item.category == "Лекционная"
    assert item.class_number == "101"
    assert item.campus == "Главный корпус"
    assert item.date == "2024-09-01"


def test_generate_unique_id():
    item1 = Item("Лекционная", "101", "Главный корпус")
    item2 = Item("Лекционная", "102", "Главный корпус")

    assert item1.id != item2.id


def test_id_is_string():
    item = Item("Лекционная", "101", "Главный корпус")

    assert isinstance(item.id, str)


def test_auto_generate_date():
    item = Item("Лекционная", "101", "Главный корпус")

    assert item.date is not None
    assert len(item.date) == 10


def test_invalid_class_number():
    with pytest.raises(ItemError):
        Item("Лекционная", "10A", "Главный корпус")


def test_invalid_date_format():
    with pytest.raises(ItemError):
        Item("Лекционная", "101", "Главный корпус", "01-09-2024")


def test_invalid_calendar_date():
    with pytest.raises(ItemError):
        Item("Лекционная", "101", "Главный корпус", "2024-15-40")


def test_copy_item():
    item = Item("Лекционная", "101", "Главный корпус", "2024-09-01")

    copied_item = item.copy()

    assert copied_item.category == item.category
    assert copied_item.class_number == item.class_number
    assert copied_item.campus == item.campus
    assert copied_item.date == item.date
    assert copied_item.id != item.id
