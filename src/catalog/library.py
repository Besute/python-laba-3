import time
from dataclasses import dataclass, field
from .errors import EntityNotFound

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


@dataclass
class Library:
    __name: str
    __container: dict = field(default_factory=dict, init=False)

    def add(self, item: Item) -> None:
        """Add item to library"""
        self.__container[item.id] = item

    def get(self, item_id: str) -> Item:
        """Get item from library"""

        return self.__container[item_id]

    def remove(self, item_id: str) -> int:
        """Remove item from library"""

        if item_id in self.__container:
            del self.__container[item_id]

            return 0

        raise EntityNotFound("ID was not found")

    def find_by_category(self, category: str) -> tuple:
        """Find item by category"""

        found = []
        for data in self.__container.values():
            if data.category == category:
                found.append(data)

        return tuple(found)

    def find_by_name(self, name: str) -> tuple:
        """Find item by name"""

        found = []
        for data in self.__container.values():
            if data.name == name:
                found.append(data)

        return tuple(found)

    def __len__(self) -> int:
        return len(self.__container)

    def __iter__(self):
        return iter(self.__container.values())

    def __contains__(self, item_id: str) -> bool:
        return item_id in self.__container
