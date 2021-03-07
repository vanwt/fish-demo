from time import clock
from functools import reduce
import re


class ViewInfo:
    def __init__(self, path, method, view, parsers, resp_class):
        self.parameter = []
        self.path = path
        self.method = method
        self.view = view
        self.parsers = parsers
        self.resp_class = resp_class
        self.re_path = False
        self.check_path()

    def __repr__(self):
        return self.path

    def check_path(self):
        d = re.findall("/(<int:\w+>|<str:\w+>)/?", self.path)
        if len(d):
            self.re_path = True

    def equal(self, method, path):
        return self.method == method and self.path == path


class PathRouter:

    def __init__(self):
        self._map = []
        self.compile = re.compile(r"(^/\w+)/?", re.S)

    def set_route(self, path: str, method: str, view_func, parsers, resp_class):
        for i in iter(self._map):
            if i.equal(path, method):
                return None
        self._map.append(ViewInfo(path=path, method=method, view=view_func, parsers=parsers, resp_class=resp_class))

    def get_route(self, path, method):
        """
        根据URL匹配
        判断请求类型
        判断是否正则匹配
        """
        for vi in iter(self._map):
            if vi.method == method:
                if vi.re_path:

                    resp, param = self.search_path(vi.path, path)
                    if resp:
                        vi.parameter.append(param)
                        return vi
                else:
                    if vi.path == path:
                        return vi
        return None

    def __iter__(self):
        for i in self._map:
            yield i

    def search_path(self, v_path: str, path: str) -> (bool, None):
        """
        使用正则匹配URL
        """
        d = self.compile.findall(path)
        if len(d):
            return v_path == d[0]
        return False, None


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
    pm.set_route("/useeCr/<int:id>", "VCany", max, None, None)
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
        cls = pm.get_route("/index", "GET")
        cls2 = pm.get_route("/index", "POST")
        cls3 = pm.get_route("/user", "GET")
        cls4 = pm.get_route("/users", "GET")
        cls5 = pm.get_route("/user", "POST")
        cls6 = pm.get_route("/userRT", "B")
        cls7 = pm.get_route("/useERT", "h")
        cls9 = pm.get_route("/usfvesrA", "itdB")
        path = cls.path
        method = cls5.method
        view = cls9.view
        # print(cls, cls2, cls3, cls4, cls5, cls6, cls7)
    e = clock()
    # e = datetime.datetime.now()
    print(e - s)
