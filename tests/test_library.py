import pytest

from catalog.errors import DuplicateIDError
from catalog.errors import EntityNotFound
from catalog.errors import ItemError
from catalog.library import Item
from catalog.library import Library


def test_add_item():
    library = Library("Библиотека")

    item = Item("Лекционная", "101", "Главный корпус")

    library.add(item)

    assert library.get(item.id) == item


def test_get_item():
    library = Library("Библиотека")

    item = Item("Лекционная", "101", "Главный корпус")
    library.add(item)

    result = library.get(item.id)

    assert result == item


def test_get_nonexistent_item():
    library = Library("Библиотека")

    with pytest.raises(EntityNotFound):
        library.get("999")


def test_remove_item():
    library = Library("Библиотека")

    item = Item("Лекционная", "101", "Главный корпус")
    library.add(item)

    library.remove(item.id)

    with pytest.raises(EntityNotFound):
        library.get(item.id)


def test_remove_nonexistent_item():
    library = Library("Библиотека")

    with pytest.raises(EntityNotFound):
        library.remove("999")


def test_duplicate_id():
    library = Library("Библиотека")

    item = Item("Лекционная", "101", "Главный корпус")
    library.add(item)

    with pytest.raises(DuplicateIDError):
        library.add(item)


def test_find_by_number():
    library = Library("Библиотека")

    item1 = Item("Лекционная", "101", "Главный корпус")
    item2 = Item("Компьютерная", "201", "Второй корпус")

    library.add(item1)
    library.add(item2)

    result = library.find_by_number("101")

    assert len(result) == 1
    assert result[0] == item1


def test_find_nonexistent_number():
    library = Library("Библиотека")

    result = library.find_by_number("999")

    assert result == ()


def test_library_contains():
    library = Library("Библиотека")

    item = Item("Лекционная", "101", "Главный корпус")
    library.add(item)

    assert item.id in library


def test_library_length():
    library = Library("Библиотека")

    item1 = Item("Лекционная", "101", "Главный корпус")
    item2 = Item("Лекционная", "102", "Главный корпус")
    item3 = Item("Компьютерная", "201", "Второй корпус")

    library.add(item1)
    library.add(item2)
    library.add(item3)

    assert len(library) == 3


def test_iteration_order():
    library = Library("Библиотека")

    item1 = Item("Лекционная", "101", "Главный корпус")
    item2 = Item("Лекционная", "102", "Главный корпус")
    item3 = Item("Компьютерная", "201", "Второй корпус")

    library.add(item1)
    library.add(item2)
    library.add(item3)

    result = []

    for category in library:
        result.extend(list(category))

    assert result == [item1, item2, item3]


def test_undo_add():
    library = Library("Библиотека")

    item = Item("Лекционная", "101", "Главный корпус")
    library.add(item)

    library.undo_last()

    with pytest.raises(EntityNotFound):
        library.get(item.id)


def test_undo_empty_library():
    library = Library("Библиотека")

    with pytest.raises(ItemError):
        library.undo_last()
