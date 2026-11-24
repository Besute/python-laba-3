import pytest

from catalog.errors import DuplicateIDError
from catalog.library import Category
from catalog.library import Item


def test_add_item():
    category = Category("Лекционная")
    item = Item("Лекционная", "101", "Главный корпус")

    category.add(item)

    assert list(category) == [item]


def test_add_multiple_items():
    category = Category("Лекционная")

    item1 = Item("Лекционная", "101", "Главный корпус")
    item2 = Item("Лекционная", "102", "Главный корпус")

    category.add(item1)
    category.add(item2)

    assert len(list(category)) == 2


def test_duplicate_id():
    category = Category("Лекционная")
    item = Item("Лекционная", "101", "Главный корпус")

    category.add(item)

    with pytest.raises(DuplicateIDError):
        category.add(item)


def test_remove_item():
    category = Category("Лекционная")
    item = Item("Лекционная", "101", "Главный корпус")

    category.add(item)
    category.remove(item.id)

    assert list(category) == []


def test_iteration_order():
    category = Category("Лекционная")

    item1 = Item("Лекционная", "101", "Главный корпус")
    item2 = Item("Лекционная", "102", "Главный корпус")

    category.add(item1)
    category.add(item2)

    assert list(category) == [item1, item2]


def test_empty_category():
    category = Category("Лекционная")

    assert list(category) == []
