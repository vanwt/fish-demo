from random import randint
from time import clock


def get_data1():
    a = randint(1, 10)
    if a % 2 == 0:
        n = {"a": "c", "b": "e"}
        n.update({"AAAAAAA": "EEEEEEEEEEEEE"})
        n.update({"1asdf34d3d3d3": 2392345353524334242})
        return n
    else:
        return False


def get_data2():
    a = randint(1, 10)
    if a % 2 == 0:
        n = {"a": "c", "b": "e"}
        n.update({"AAAAAAA": "EEEEEEEEEEEEE"})
        n.update({"1asdf34d3d3d3": 2392345353524334242})
        n.update({"msg": a})
        return n
    else:
        return {}


def d1():
    start = clock()
    for i in range(10000):
        d = {"1": "2", "2": "3", "3": "4", "4": "5"}
        data = get_data1()
        if isinstance(data, dict):
            d.update(data)
    end = clock()

    print(end - start)


def d2():
    start = clock()
    for i in range(10000):
        d = {"1": "2", "2": "3", "3": "4", "4": "5"}
        data = get_data2()
        d.update(data)
    end = clock()

    print(end - start)


if __name__ == '__main__':
    d1()
    d2()
