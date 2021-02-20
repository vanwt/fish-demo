from ..parsers import UrlParser
from ..response.response import Json


class Url:

    def __init__(self, view_id):
        self.view_id = view_id
        self.method = None
        self.path = None
        self.view = None
        self.parsers = (UrlParser,)
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

    def add_url_parser(self, view_id, *parsers):
        url_obj = self._get_url_by_id_or_create(view_id)
        url_obj.parsers = parsers

    def get_url(self, path) -> Url or None:
        for url in self.maps:
            if url.path == path:
                return url
        return None

    def out(self):
        print(self.maps)
