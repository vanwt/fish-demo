from time import clock


class Url:

    def __init__(self, view_id):
        self.view_id = view_id
        self.method = None
        self.path = None
        self.view = None
        self.parsers = None
        self.response = None

    def set_path(self, path, method):
        self.method = method
        self.path = path

    def set_resp(self, resp_class):
        self.response = resp_class

    def set_parsers(self, parsers):
        self.parsers = parsers

    def __repr__(self):
        return "%s.%s" % (self.path, self.method)


class UrlMap:
    METHODS = ["GET", "POST", "PUT", "DELETE"]

    def __init__(self):
        self.maps = []
        self.view_funcs = []

    def _get_url_by_id_or_create(self, view_id):
        for url in self.maps:
            if url.view_id == view_id:
                return url
        url = Url(view_id)
        self.maps.append(url)
        return url

    def check_method_and_path(self, path, method):

        if method not in self.METHODS:
            raise AttributeError("method must in {0!r}".format(self.METHODS))
        for url in self.maps:
            if url.path == path and url.method == method:
                raise AttributeError("同一个url与请求类型只能声明一次")

    def add_route(self, path, method, view, resp_class, parsers):
        # url_obj = self._get_url_by_id_or_create(id(view))
        url_obj = Url(id(view))
        print(url_obj.method)
        url_obj.path = path
        url_obj.method = method
        url_obj.response = resp_class
        url_obj.parsers = parsers
        self.maps.append(url_obj)

    def add_url_route(self, path, view, method):
        url_obj = self._get_url_by_id_or_create(id(view))
        url_obj.path = path
        url_obj.method = method
        url_obj.view = view

    def add_url_response(self, view_id, resp_class):
        url_obj = self._get_url_by_id_or_create(view_id)
        url_obj.response = resp_class

    def add_url_parser(self, view_id, *parsers):
        url_obj = self._get_url_by_id_or_create(view_id)
        url_obj.parsers = parsers

    def get_url(self, path, method) -> Url or None:
        for url in self.maps:
            if url.path == path and method == url.method:
                return url
        return None

    def out(self):
        print(self.maps)

    def __iter__(self):
        for i in self.maps:
            yield i


class A():
    pass


if __name__ == '__main__':
    pm = UrlMap()

    pm.add_route("/index", "GET", A(), None, None)
    pm.add_route("/index", "POST", A(), None, None)
    pm.add_route("/user", "GET", A(), None, None)
    pm.add_route("/user", "POST", A(), None, None)
    pm.add_route("/user", "DELETE", A(), None, None)
    pm.add_route("/usjgers", "GET", A(), None, None)
    pm.add_route("/uNnser", "V", A(), None, None)
    pm.add_route("/uYmser", "C", A(), None, None)
    pm.add_route("/use4rs", "D", A(), None, None)
    pm.add_route("/usolEer", "E", A(), None, None)
    pm.add_route("/ulsFer", "F", A(), None, None)
    pm.add_route("/usloseSrs", "G", A(), None, None)
    pm.add_route("/usolseCr", "V", A(), None, None)
    pm.add_route("/usfverA", "B", A(), None, None)
    pm.add_route("/uVrsers", "T", A(), None, None)
    pm.add_route("/usolRer", "H", A(), None, None)
    pm.add_route("/usoldeSrs", "G", A(), None, None)
    pm.add_route("/usseCr", "V", A(), None, None)
    pm.add_route("/uvscerA", "B", A(), None, None)
    pm.add_route("/uVvsers", "T", A(), None, None)
    pm.add_route("/usbRer", "H", A(), None, None)
    pm.add_route("/usolbeSrs", "G", A(), None, None)
    pm.add_route("/useeCr", "V", A(), None, None)
    pm.add_route("/useerA", "B", A(), None, None)
    pm.add_route("/uVseyrs", "T", A(), None, None)
    pm.add_route("/usRker", "H", A(), None, None)
    pm.add_route("/uscRker", "HU", A(), None, None)

    pm.add_route("/usolbeSrs", "GA", A(), None, None)
    pm.add_route("/useeCr/<int:id>", "VCA()", A(), None, None)
    pm.add_route("/useerA", "BV", A(), None, None)
    pm.add_route("/uVseyrs", "TT", A(), None, None)
    pm.add_route("/usRker", "HY", A(), None, None)
    pm.add_route("/uscRker", "HIU", A(), None, None)

    pm.add_route("/ulsFer", "aF", A(), None, None)
    pm.add_route("/usloseSrs", "CG", A(), None, None)
    pm.add_route("/usolsseCr", "tV", A(), None, None)
    pm.add_route("/usfvesrA", "itdB", A(), None, None)
    pm.add_route("/uVrsers", "sdfT", A(), None, None)
    pm.add_route("/usolsRer", "dsH", A(), None, None)
    pm.add_route("/usoldeSrs", "Gsd", A(), None, None)

    pm.add_route("/index", "PATH", A(), None, None)
    pm.add_route("/index", "UPDATE", A(), None, None)
    pm.add_route("/users", "POST", A(), None, None)
    pm.add_route("/user", "DELETE", A(), None, None)

    pm.add_route("/ind2ex", "POST", A(), None, None)
    pm.add_route("/us4er", "GET", A(), None, None)
    pm.add_route("/WEuser", "POST", A(), None, None)
    pm.add_route("/usEer", "DELETE", A(), None, None)
    pm.add_route("/us2jgers", "GET", A(), None, None)
    pm.add_route("/uNn2332ser", "V", A(), None, None)
    pm.add_route("/uYR45mser", "C", A(), None, None)
    pm.add_route("/us6e4rs", "D", A(), None, None)
    pm.add_route("/uso66lEer", "E", A(), None, None)

    print([i for i in pm])

    s = clock()
    # s = datetime.datetime.now()
    for i in range(10000):
        cls = pm.get_url("/index", "GET")
        cls2 = pm.get_url("/usolbeSrs", "POST")
        cls3 = pm.get_url("/user", "GET")
        cls4 = pm.get_url("/users", "GET")
        cls5 = pm.get_url("/usolbeSrs", "POST")
        cls6 = pm.get_url("/userRT", "B")
        cls7 = pm.get_url("/useERT", "h")
        cls9 = pm.get_url("/usfvesrA", "itdB")

        path = cls.path
        method = cls5.method
        view = cls9.view
        print(path)
        print(method)
        print(view)
        # print(cls, cls2, cls3, cls4, cls5, cls6, cls7)
    e = clock()
    # e = datetime.datetime.now()
    print(e - s)
