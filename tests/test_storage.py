from catalog.library import Item
from catalog.library import Library


def test_json_round_trip(tmp_path):
    library = Library("Аудитории")

    item1 = Item("Лекционная", "101", "Главный корпус")
    item2 = Item("Компьютерная", "202", "Второй корпус")

    library.add(item1)
    library.add(item2)

    file_path = tmp_path / "classrooms.json"

    library.save(str(file_path))

    loaded_items = Library.read(file_path)

    assert len(loaded_items) == 2

    loaded_data = {(item.category, item.class_number, item.campus, item.date) for item in loaded_items}

    original_data = {(item.category, item.class_number, item.campus, item.date) for item in (item1, item2)}

    assert loaded_data == original_data
