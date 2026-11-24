from .library import Item
from .library import Library


def main():
    lib = Library("Audience")
    try:
        # loaded = lib.read("classrooms.jsonl")
        # for data in loaded:
        #     lib.add(data)

        item1 = Item("SKIBIDI", "67", "CAMPUS")
        lib.add(item1)
        lib.undo_last()

        lib.save("saved/classrooms.jsonl")
    except Exception as e:
        print("Exception:", e)
    finally:
        lib.save("saved/classrooms.jsonl")


if __name__ == "__main__":
    main()
