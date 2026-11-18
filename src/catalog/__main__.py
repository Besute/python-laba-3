from .library import Item, Library

def main():
    lib = Library("123")
    lib.add(Item(name="HELLO", category="python"))
    lib.add(Item(name="HELLO2", category="python2"))

    print(Library.__dict__)

    for i in lib:
        print(i)


if __name__ == "__main__":
    main()