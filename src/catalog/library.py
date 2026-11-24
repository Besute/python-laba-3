from dataclasses import dataclass
from dataclasses import field
from json import dumps
from json import loads
from pathlib import Path
from time import strftime
from time import strptime

from .errors import DuplicateIDError
from .errors import EntityNotFound
from .errors import ItemError
from .errors import UnsupportedFormatError


@dataclass
class Item:
    VALID_NUMBERS = "0123456789 "
    VALID_DATE_FORMAT = "0123456789 :-"

    __next_id = "0"

    __id: str = field(init=False)
    category: str
    class_number: str
    campus: str
    date: str | None = field(default=None)

    def __new__(cls, *args, **kwargs):
        cls.__next_id = str(int(cls.__next_id) + 1)

        return super().__new__(cls)

    def __post_init__(self):
        self.__check_class_number(self.class_number)
        if self.date is None:
            self.date = strftime("%Y-%m-%d")
        else:
            self.__check_date(self.date)

        self.__id = Item.__next_id

    @classmethod
    def __check_class_number(cls, class_number: str) -> None:
        for c in class_number:
            if c not in cls.VALID_NUMBERS:
                raise ItemError("Class number must be a valid number")

    @classmethod
    def __check_date(cls, date: str) -> None:
        try:
            strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ItemError("Invalid date format")

    @property
    def id(self) -> str:
        """Getter for __id"""

        return self.__id

    @id.deleter
    def id(self) -> None:
        del self.__id

    def copy(self):
        """Copy item"""

        return Item(self.category, self.class_number, self.campus, self.date)


@dataclass(frozen=True)
class Category:
    category: str
    __container: dict[str, Item] = field(default_factory=dict)

    def add(self, item) -> None:
        """Add item to category"""

        if item.id not in self.__container:
            self.__container[item.id] = item
        else:
            raise DuplicateIDError("ID was duplicated")

    def __iter__(self):

        return iter(self.__container.values())

    def remove(self, item_id: str) -> None:
        del self.__container[item_id]

    def __len__(self) -> int:

        return len(self.__container.keys())


@dataclass(frozen=True)
class Library:
    __name: str
    __container: dict[str, Category] = field(default_factory=dict, init=False)
    __operations: dict[str, dict[str, Item | str]] = field(default_factory=dict, init=False)

    VALID_EXTENSION = ("json", "jsonl")

    def save(self, path: str) -> None:
        """Save library to file"""

        path = Path(__file__).parent / path
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="UTF-8") as f:
            for category in self.__container:
                for item in self.__container[category]:
                    curr_data = item.copy()
                    curr_data.__delattr__("id")
                    curr_data = curr_data.__dict__
                    f.write(dumps(curr_data, ensure_ascii=False) + "\n")

    @classmethod
    def save_operation(cls, operations: dict[str, str]) -> None:
        """Saves last operation"""
        pass

    @classmethod
    def read(cls, filename):
        """Reads data from JSON"""

        path = Path(filename)
        filename_extention = path.suffix[1:]

        if filename_extention not in cls.VALID_EXTENSION:
            raise UnsupportedFormatError("Такой формат не поддерживается!")

        data = []
        try:
            with open(path, "r", encoding="UTF-8") as f:
                for line in f:
                    curr_data = loads(line)
                    data.append(
                        Item(
                            curr_data["category"],
                            curr_data["class_number"],
                            curr_data["campus"],
                            curr_data["date"],
                        )
                    )
        except Exception as e:
            raise Exception(f"Что-то пошло не так: {e}")

        return data

    def undo_last(self):
        if len(self.__operations) > 0:
            last = self.__operations.popitem()
            id_ = last[0]
            operation = last[1]["operation"]
            item = last[1]["item"]
            if operation == "removed":
                self.add(item)
            elif operation == "added":
                self.remove(id_)

            return 0

        raise ItemError("You didn't add or remove")

    def add(self, item: Item) -> None:
        """Add item to library"""

        if item.category not in self.__container:
            self.__container[item.category] = Category(item.category)

        self.__operations[item.id] = {
            "operation": "added",
            "item": item.copy(),
        }
        self.__container[item.category].add(item)

    def get(self, item_id: str) -> Item:
        """Get item from library by ID"""

        for catalog in self.__container:
            for item in self.__container[catalog]:
                if item.id == item_id:
                    return item

        raise EntityNotFound("Item was not found")

    def remove(self, item_id: str) -> int:
        """Remove item from library by ID"""

        for category in self.__container.keys():
            for item in self.__container[category]:
                if item.id == item_id:
                    self.__operations[item_id] = {
                        "operation": "removed",
                        "item": item,
                    }
                    self.__container[category].remove(item_id)
                    return 0
        raise EntityNotFound("ID was not found")

    def find_by_category(self, category: str) -> Category:
        """Find item by category"""

        if category not in self.__container:
            return self.__container[category]

        return Category(category)

    def find_by_number(self, name: str) -> tuple:
        """Find item by name"""

        found = []
        for cat in self.__container:
            for item in self.__container[cat]:
                if item.class_number == name:
                    found.append(item)

        return tuple(found)

    def __len__(self) -> int:
        acc = 0
        for cat in self.__container.keys():
            acc += len(self.__container[cat])

        return acc

    def __iter__(self):

        return iter(self.__container.values())

    def __contains__(self, item_id: str) -> bool:
        for category in self.__container.values():
            for item in category:
                if item.id == item_id:
                    return True

        return False
