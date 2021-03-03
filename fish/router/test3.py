from time import clock
from functools import reduce


class ViewInfo:
    def __init__(self, path, method, view, parsers, resp_class):
        self.path = path
        self.method = method
        self.view = view
        self.parsers = parsers
        self.resp_class = resp_class

    def __repr__(self):
        return self.path

    def __eq__(self, other):
        return self.method == other

    def equal(self, path, method):
        return self.eq_path(path) and self.method == method

    def eq_path(self, path):
        return self.path == path


class PathRouter:

    def __init__(self):
        self._map = []

    def set_route(self, path, method, view_func, parsers, resp_class):
        for i in iter(self):
            if i.equal(path, method):
                return None
        self._map.append(ViewInfo(path, method, view_func, parsers, resp_class))

    def get_path(self, path, method):
        # print(map(lambda x:x.equal(path,method),iter(self._map)))

        # for i in filter(lambda x: x.equal(path, method), iter(self._map)):
        #     return i
        # return None

        for i in iter(self._map):
            if i.equal(path, method):
                return i
        return None

    def __iter__(self):
        for i in self._map:
            yield i


if __name__ == '__main__':
    """ 
    简单压力测试 
    URL 50 条
    """

    pm = PathRouter()
    pm.set_route("/index", "GET", max, None, None)
    pm.set_route("/index", "POST", abs, None, None)
    pm.set_route("/user", "GET", min, None, None)
    pm.set_route("/user", "POST", min, None, None)
    pm.set_route("/user", "DELETE", min, None, None)
    pm.set_route("/usjgers", "GET", oct, None, None)
    pm.set_route("/uNnser", "V", any, None, None)
    pm.set_route("/uYmser", "C", min, None, None)
    pm.set_route("/use4rs", "D", oct, None, None)
    pm.set_route("/usolEer", "E", any, None, None)
    pm.set_route("/ulsFer", "F", min, None, None)
    pm.set_route("/usloseSrs", "G", oct, None, None)
    pm.set_route("/usolseCr", "V", any, None, None)
    pm.set_route("/usfverA", "B", min, None, None)
    pm.set_route("/uVrsers", "T", oct, None, None)
    pm.set_route("/usolRer", "H", any, None, None)
    pm.set_route("/usoldeSrs", "G", oct, None, None)
    pm.set_route("/usseCr", "V", any, None, None)
    pm.set_route("/uvscerA", "B", min, None, None)
    pm.set_route("/uVvsers", "T", oct, None, None)
    pm.set_route("/usbRer", "H", any, None, None)
    pm.set_route("/usolbeSrs", "G", oct, None, None)
    pm.set_route("/useeCr", "V", any, None, None)
    pm.set_route("/useerA", "B", min, None, None)
    pm.set_route("/uVseyrs", "T", oct, None, None)
    pm.set_route("/usRker", "H", any, None, None)
    pm.set_route("/uscRker", "HU", any, None, None)

    pm.set_route("/usolbeSrs", "GA", oct, None, None)
    pm.set_route("/useeCr", "VC", any, None, None)
    pm.set_route("/useerA", "BV", min, None, None)
    pm.set_route("/uVseyrs", "TT", oct, None, None)
    pm.set_route("/usRker", "HY", any, None, None)
    pm.set_route("/uscRker", "HIU", any, None, None)

    pm.set_route("/ulsFer", "aF", min, None, None)
    pm.set_route("/usloseSrs", "CG", oct, None, None)
    pm.set_route("/usolsseCr", "tV", any, None, None)
    pm.set_route("/usfvesrA", "itdB", min, None, None)
    pm.set_route("/uVrsers", "sdfT", oct, None, None)
    pm.set_route("/usolsRer", "dsH", any, None, None)
    pm.set_route("/usoldeSrs", "Gsd", oct, None, None)

    pm.set_route("/index", "PATH", max, None, None)
    pm.set_route("/index", "UPDATE", abs, None, None)
    pm.set_route("/users", "POST", min, None, None)
    pm.set_route("/user", "DELETE", min, None, None)

    pm.set_route("/ind2ex", "POST", abs, None, None)
    pm.set_route("/us4er", "GET", min, None, None)
    pm.set_route("/WEuser", "POST", min, None, None)
    pm.set_route("/usEer", "DELETE", min, None, None)
    pm.set_route("/us2jgers", "GET", oct, None, None)
    pm.set_route("/uNn2332ser", "V", any, None, None)
    pm.set_route("/uYR45mser", "C", min, None, None)
    pm.set_route("/us6e4rs", "D", oct, None, None)
    pm.set_route("/uso66lEer", "E", any, None, None)

    print([i for i in pm])

    s = clock()
    # s = datetime.datetime.now()
    for i in range(10000):
        cls = pm.get_path("/index", "GET")
        cls2 = pm.get_path("/index", "POST")
        cls3 = pm.get_path("/user", "GET")
        cls4 = pm.get_path("/users", "GET")
        cls5 = pm.get_path("/user", "POST")
        cls6 = pm.get_path("/userRT", "B")
        cls7 = pm.get_path("/useERT", "h")
        cls9 = pm.get_path("/usfvesrA", "itdB")
        path = cls.path
        method = cls5.method
        view = cls9.view
        # print(cls, cls2, cls3, cls4, cls5, cls6, cls7)
    e = clock()
    # e = datetime.datetime.now()
    print(e - s)
