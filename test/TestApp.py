from typing import List, Callable, Dict
from functools import wraps
from weakref import ref

from fish.parsers import UrlParser
from fish.response.response import Json


def html():
    return "AA"


class UrlTest:

    def __init__(self, view_id):
        self.view_id = view_id
        self.method = None
        self.path = None
        self.view = None
        self.parsers = UrlParser
        self.response = Json

    def set_path(self, path, method):
        self.method = method
        self.path = path

    def set_resp(self, resp_class):
        self.response = resp_class

    def set_parsers(self, parsers):
        self.parsers = parsers

    def __str__(self):
        return "%s.%s" % (self.view.__name__, self.path)

    def __repr__(self):
        return "%s.%s" % (self.path, self.method)


class UrlMapTest:
    METHODS = ["GET", "POST", "PUT", "DELETE"]

    def __init__(self):
        self.maps = []
        self.view_funcs = []

    def _get_url_by_id_or_create(self, view_id):
        for url in self.maps:
            if url.view_id == view_id:
                return url
        url = UrlTest(view_id)
        self.maps.append(url)
        return url

    def check_method_and_path(self, path, method):

        if method not in self.METHODS:
            raise AttributeError("method must in {0!r}".format(self.METHODS))
        for url in self.maps:
            if url.path == path and url.method == method:
                raise AttributeError("同一个url与请求类型只能声明一次")

    def add_route(self, path, view, method, resp_class, parsers):
        url_obj = self._get_url_by_id_or_create(id(view))
        url_obj.path = path
        url_obj.method = method
        url_obj.response = resp_class
        url_obj.parsers = parsers

    def add_url_route(self, path, view, method):
        url_obj = self._get_url_by_id_or_create(id(view))
        url_obj.path = path
        url_obj.method = method
        url_obj.view = view

    def add_url_response(self, view_id, resp_class):
        url_obj = self._get_url_by_id_or_create(view_id)
        url_obj.response = resp_class

    def add_url_parser(self, view_id, parsers):
        url_obj = self._get_url_by_id_or_create(view_id)
        url_obj.parsers = parsers

    def get_url(self, path) -> UrlTest or None:
        for url in self.maps:
            if url.path == path:
                return url
        return None

    def out(self):
        print(self.maps)


class UrlInitDict:
    url_data = {}

    def init_key(self, key):
        if key not in self.url_data:
            self.url_data[key] = {}

    def set_route(self, key, path, view, method):
        self.init_key(key)
        self.url_data[key]["path"] = path
        self.url_data[key]["view"] = view
        self.url_data[key]["method"] = method

    def set_response(self, key, response_class):
        self.init_key(key)
        self.url_data[key]["response"] = response_class

    def set_parsers(self, key, parsers):
        self.init_key(key)
        self.url_data[key]["parsers"] = parsers

    def set_url_value(self, key, name, value):
        self.url_data[key][name] = value

    def out(self):
        for k, v in self.url_data.items():
            print(k, v)


class TestApp1:
    def __init__(self):
        self.url_map = UrlMapTest()

    def route(self, path: str, method: str):
        def add_route(func):
            self.url_map.check_method_and_path(path, method)
            self.url_map.add_url_route(path, func, method)

            return func

        return add_route

    def parsers(self, *parsers):
        def parser_fun(func):
            self.url_map.add_url_parser(id(func), parsers)
            return func

        return parser_fun

    def response(self, resp):
        def set_resp(func):
            self.url_map.add_url_response(id(func), resp)

            return func

        return set_resp

    def run(self):
        self.url_map.out()


if __name__ == '__main__':
    app = TestApp1()


    @app.route("/", "GET")
    @app.response(html)
    @app.parsers(1, 2, 3)
    def index():
        """ 这是测试2 """
        print("index view")


    @app.route("/", "POST")
    @app.response(html)
    def index():
        """ 则是测试 """
        print("index2 view")


    @app.route("/s", "POST")
    @app.response(html)
    def index2():
        """ 则是测试 """
        print("index2 view")


    @app.route("/s", "DELETE")
    @app.response(html)
    def index2():
        """ 则是测试 """
        print("index2 view")


    app.run()
