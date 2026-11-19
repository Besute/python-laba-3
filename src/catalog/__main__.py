from .library import Item, Library

def main():
    lib = Library("Audience")

    loaded = lib.read_from_json("classrooms.jsonl")
    for data in loaded:
        lib.add(data)



if __name__ == "__main__":
    main()