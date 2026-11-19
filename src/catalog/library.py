import time
from dataclasses import dataclass, field
from .errors import EntityNotFound, DuplicateIDError

@dataclass
class Item:
    __next_id = "0"

    name: str
    __id: str = field(init=False)
    category: str
    date: str | None = field(default=None)

    def __new__(cls, *args, **kwargs):
        cls.__next_id = str(int(cls.__next_id) + 1)

        return super().__new__(cls)

    def __post_init__(self):
        if self.date is None:
            self.date = time.strftime("%d %m %Y")

        self.__id = Item.__next_id

    @property
    def id(self) -> str:
        """Getter for __id"""

        return self.__id

@dataclass(frozen=True)
class Category:
    category: str
    __container: dict[str, list[Item]] = field(default_factory=dict)

    def add(self, item) -> None:
        """Add item to category"""

        if item.id not in self.__container:
            self.__container[item.id] = item
        else:
            raise DuplicateIDError("ID was duplicated")

    def __iter__(self):
        return iter(self.__container.values())

@dataclass(frozen=True)
class Library:
    __name: str
    __container: dict[str, Category] = field(default_factory=dict, init=False)

    def add(self, item: Item) -> None:
        """Add item to library"""

        if item.category not in self.__container:
            self.__container[item.category] = Category(item.category)

        self.__container[item.category].add(item)

    def get(self, item_id: str) -> Item:
        """Get item from library"""

        return self.__container[item_id]

    def remove(self, item_id: str) -> int:
        """Remove item from library"""

        if item_id in self.__container:
            del self.__container[item_id]

            return 0

        raise EntityNotFound("ID was not found")

    def find_by_category(self, category: str) -> Category:
        """Find item by category"""

        if category not in self.__container:
            return self.__container[category]

        return Category(category)

    def find_by_name(self, name: str) -> tuple:
        """Find item by name"""

        found = []
        for cat in self.__container:
            for item in self.__container[cat]:
                if item.name == name:
                    found.append(item)

        return tuple(found)

    def __len__(self) -> int:
        return len(self.__container)

    def __iter__(self):
        return iter(self.__container.values())

    def __contains__(self, item_id: str) -> bool:
        return item_id in self.__container
