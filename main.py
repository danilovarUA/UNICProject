from database import Database


def main(test_mode=False):
    local_storage = {"sessions": []}
    db = Database()
    if test_mode:
        test()
    else:
        pass


def test():
    pass


if __name__ == "__main__":
    main()
