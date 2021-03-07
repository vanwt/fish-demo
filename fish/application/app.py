from ..router import PathRouter
from ..request import Request
from ..exception.errors import HttpException
from ..parsers import BaseParser
from ..config import METHODS
from typing import List, Callable, Dict
from functools import wraps
from ..response import ErrorResponse, Json
from ..parsers import UrlParser


class RouteInf:
    def at_route(self, *args, **kwargs):
        pass

    def get(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.at_route(path, "GET", parsers, response)

    def post(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.at_route(path, "POST", parsers, response)

    def update(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.at_route(path, "UPDATE", parsers, response)

    def delete(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.at_route(path, "DELETE", parsers, response)

    def patch(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.at_route(path, "PATCH", parsers, response)

    def options(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.at_route(path, "OPTIONS", parsers, response)


class FishApp(RouteInf):
    request_class = Request
    static_url = ""
    static_dir = None

    def __init__(self):
        self.routes = PathRouter()
        self.debug = True
        self.parser_map: dict = {}

    def add_routes(self, path: str, view: Callable, method: str, parsers: List[BaseParser], resp_class: Callable):
        """
        添加路由
        :param path: url
        :param options:  methods 目前只有请求类型
        :return: None
        """
        # check methods

        if method not in METHODS:
            raise AttributeError("method must in {0!r}".format(METHODS))

        self.routes.set_route(path=path, view_func=view, method=method, resp_class=resp_class, parsers=parsers)

    def route(self, path: str, method: str, parsers: List[BaseParser] = None, response=None):
        """
        装饰器
        @app.route("/",["GET"])
        def test(req):
            return "ok"

        @app.route("/",["POST"])
        def test2(req):
            return "ok"
        加入到路由表中

        """
        return self.at_route(path, method, parsers, response)

    def at_route(self, path: str, method: str, parsers: List[BaseParser], response):
        # 解析器默认只有url解析
        parsers = parsers if parsers else (UrlParser,)
        response_class = response if response else Json

        def add_route(func: Callable):
            # 加入到路由表中
            self.add_routes(path=path, view=func, method=method, parsers=parsers, resp_class=response_class)

            @wraps(func)
            def wrapper():
                return func

            return wrapper

        return add_route

    def run(self, host="127.0.0.1", port=8000, **options):
        from werkzeug.serving import run_simple
        options.setdefault("threaded", True)
        run_simple(host, port, self, **options)

    def __call__(self, environ: Dict, start_response: Callable):
        # 此处要返回一个handler
        request = self.request_class(environ)
        try:
            path_obj = self.routes.get_route(request.path, request.method)
            # 解析
            request.parsing(path_obj.parsers)
            # 执行 resp类的call
            response_data = path_obj.view(request)
            resp = Json(response_data)
        except HttpException as e:
            return ErrorResponse(e)(environ, start_response)
        return resp(environ, start_response)
