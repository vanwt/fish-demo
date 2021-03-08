from ..router import PathRouter
from ..request import Request
from ..exception.errors import HttpException
from ..parsers import BaseParser
from typing import List, Callable, Dict
from functools import wraps
from ..response import HttpErrorResponse, ErrorResponse, Json
from ..parsers import UrlParser
import os
import sys
import traceback

METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]


class RouteInf:
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

    def route(self, *args, **kwargs):
        pass

    def get(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.route(path, "GET", parsers, response)

    def post(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.route(path, "POST", parsers, response)

    def update(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.route(path, "UPDATE", parsers, response)

    def delete(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.route(path, "DELETE", parsers, response)

    def patch(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.route(path, "PATCH", parsers, response)

    def options(self, path: str, parsers: List[BaseParser] = None, response=None):
        return self.route(path, "OPTIONS", parsers, response)


class FishApp(RouteInf):
    request_class = Request
    static_url = ""
    static_dir = None
    DEBUG = True
    ERROR_LOG = sys.stderr

    def __init__(self):
        self.routes = PathRouter()
        self.debug = True
        self.parser_map: dict = {}

    def include_static(self, static_dir_name, static_url):
        path = os.path.join(os.getcwd(), static_dir_name)
        if not os.path.exists(path):
            raise FileNotFoundError("This '{0}' file does not exist".format(static_dir_name))

        self.static_path = path
        self.static_url = static_url

    def _add_routes(self, path: str, view: Callable, method: str, parsers: List[BaseParser], resp_class: Callable):
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

    def route(self, path: str, method: str, parsers: List[BaseParser], response):
        # 解析器默认只有url解析
        parsers = parsers if parsers else (UrlParser,)
        response_class = response if response else Json

        def add_route(func: Callable):
            # 加入到路由表中
            self._add_routes(path=path, view=func, method=method, parsers=parsers, resp_class=response_class)

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
        except HttpException as http_err:
            return HttpErrorResponse(http_err)(environ, start_response)
        except Exception as err:
            if self.DEBUG:
                exc_type, exc_value, exc_traceback_obj = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback_obj, limit=2, file=sys.stderr)

                return ErrorResponse(err, exc_type)(environ, start_response)
            else:
                traceback.print_exc(file=self.ERROR_LOG)
                return ErrorResponse(err)(environ, start_response)

        return resp(environ, start_response)
