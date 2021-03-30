from typing import List, Callable, Dict
from functools import wraps

from .router import PathRouter
from .request import Request, NewRequest
from .exception import HttpException
from .parsers import UrlParams
from .response import ResponseBase, HttpErrorResponse, ErrorResponse, Json
from .response.static import StaticRouter
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

    def get(self, path: str, parsers=None, response=None):
        return self.route(path, "GET", parsers, response)

    def post(self, path: str, parsers=None, response=None):
        return self.route(path, "POST", parsers, response)

    def update(self, path: str, parsers=None, response=None):
        return self.route(path, "UPDATE", parsers, response)

    def delete(self, path: str, parsers=None, response=None):
        return self.route(path, "DELETE", parsers, response)

    def patch(self, path: str, parsers=None, response=None):
        return self.route(path, "PATCH", parsers, response)

    def options(self, path: str, parsers=None, response=None):
        return self.route(path, "OPTIONS", parsers, response)


class FishApp(RouteInf):
    # request_class = Request
    request_class = NewRequest
    static_url = ""
    static_path = None
    DEBUG = True
    ERROR_LOG = sys.stderr

    def __init__(self):
        self.routes = PathRouter()
        self.debug = True
        self.parser_map: dict = {}
        self.static_route = None
        self.static = False

    def include_static(self, static_dir_name, static_url="/static"):
        path = os.path.join(os.getcwd(), static_dir_name)
        if not static_url.startswith("/"):
            raise ValueError("URL must start with /")

        if not os.path.exists(path):
            raise FileNotFoundError("This '{0}' file does not exist".format(static_dir_name))

        self.static_route = StaticRouter(path)
        self.static_url = static_url
        self.static = True

    def _add_routes(self, path: str, view: Callable, method: str, parsers: List[Callable], resp_class: Callable):
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

    def route(self, path: str, method: str, parsers, response):
        # 解析器默认只有url解析
        parsers = parsers if parsers else (UrlParams,)
        response_class = response if response else Json

        def add_route(func: Callable):
            # 加入到路由表中
            self._add_routes(path=path, view=func, method=method, parsers=parsers, resp_class=response_class)

            @wraps(func)
            def wrapper():
                return func

            return wrapper

        return add_route

    def wsgi(self, environ, start_response):
        # 处理 请求参数
        request = self.request_class(environ)

        # 静态文件
        if self.static and request.path.startswith(self.static_url):
            file = self.static_route.check_file(request.path)
            return self.static_route(file, environ, start_response)

        try:
            path_obj = self.routes.get_route(request.path, request.method)
            # 解析
            # request.parsing(path_obj.parsers)
            request.parsing(path_obj.parsers, environ)
            # 执行 resp类的call
            resp_data = path_obj.view(request)
            if isinstance(resp_data, ResponseBase):
                return resp_data

            resp = path_obj.resp_class(resp_data)

        except Exception as err:

            if isinstance(err, HttpException):
                resp = HttpErrorResponse(err)
            else:
                if self.DEBUG:
                    exc_type, exc_value, exc_traceback_obj = sys.exc_info()
                    traceback.print_exception(exc_type, exc_value, exc_traceback_obj, limit=2, file=sys.stderr)
                    resp = ErrorResponse(err, exc_type)
                else:
                    traceback.print_exc(file=self.ERROR_LOG)
                    resp = ErrorResponse(err)

        return resp(environ, start_response)

    def __call__(self, environ: Dict, start_response: Callable):

        return self.wsgi(environ, start_response)
