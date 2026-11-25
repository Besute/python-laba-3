from .library import Item
from .library import Library


def main():
    lib = Library("Audience")
    try:
        loaded = lib.read("C:/Users/Boris/OneDrive/Desktop/python-laba-3/src/catalog/data/classrooms.jsonl")
        for data in loaded:
            lib.add(data)

        item1 = Item("SKIBIDI", "67", "CAMPUS")
        lib.add(item1)
        print(lib.find_by_category("SKIBIDI"))
    except Exception as e:
        print("Exception:", e)
    finally:
        lib.save("saved/classrooms.jsonl")


if __name__ == "__main__":
    main()
