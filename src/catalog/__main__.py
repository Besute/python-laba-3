from .library import Item, Library

def main():
    lib = Library("123")
    lib.add(Item(name="HELLO", category="python"))
    lib.add(Item(name="HELLO2", category="python2"))

    # print(lib)

    # for i in lib:
    #     print(i)

    print(lib.find_by_name("HELLO"))


if __name__ == "__main__":
    main()