from collections import UserDict


class Url(UserDict):
    def __setitem__(self, key, value):
        print("__setitem__")
        super().__setitem__(key, value)

    def __getitem__(self, item):
        print("__getitem__")

        return self.data[item]


if __name__ == '__main__':
    u = Url()
    u["s"] = 1
    print(u)
    print(u["s"])
