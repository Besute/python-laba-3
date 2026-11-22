from .library import Item
from .library import Library


def main():
    lib = Library("Audience")

    loaded = lib.read("classrooms.jsonl")
    for data in loaded:
        lib.add(data)

    item1 = Item("SKIBIDI", "67", "CAMPUS")
    lib.add(item1)

    lib.save("saved/classrooms.jsonl")


if __name__ == "__main__":
    main()
