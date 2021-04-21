from typing import List, Callable, Dict
from functools import wraps
from .request.session import DictSession
from .router import PathRouter
from .request import NewRequest
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

    def route(self, path: str, method: str, parsers=None, response=None, is_re=False):
        pass

    def get(self, path: str, parsers=None, response=None, re=False):
        return self.route(path, "GET", parsers, response, is_re=re)

    def post(self, path: str, parsers=None, response=None, re=False):
        return self.route(path, "POST", parsers, response, is_re=re)

    def update(self, path: str, parsers=None, response=None, re=False):
        return self.route(path, "UPDATE", parsers, response, is_re=re)

    def delete(self, path: str, parsers=None, response=None, re=False):
        return self.route(path, "DELETE", parsers, response, is_re=re)

    def patch(self, path: str, parsers=None, response=None, re=False):
        return self.route(path, "PATCH", parsers, response, is_re=re)

    def options(self, path: str, parsers=None, response=None, re=False):
        return self.route(path, "OPTIONS", parsers, response, is_re=re)


class FishApp(RouteInf):
    request_class = NewRequest

    DEBUG = True
    ERROR_LOG = sys.stderr

    def __init__(self, session=DictSession):
        self._routes = PathRouter()

        # static
        self._static_route = None
        self._static_url = "&!#"

        # session
        self._session_pool = session()

    def include_static(self, static_dir_name, static_url="/static"):
        path = os.path.join(os.getcwd(), static_dir_name)
        if not static_url.startswith("/"):
            raise ValueError("URL must start with /")

        if not os.path.exists(path):
            raise FileNotFoundError("This '{0}' file does not exist".format(static_dir_name))

        self._static_route = StaticRouter(path)
        self._static_url = static_url

    def route(self, path: str, method: str, parsers=None, response=None, is_re=False):
        if method not in METHODS:
            raise AttributeError("method must in {0!r}".format(METHODS))
        # 解析器默认只有url解析
        response = response if response else Json

        def add_route(func: Callable):
            # 加入到路由表中
            if is_re:
                self._routes.set_route(re_path=path, view_func=func, method=method, resp_class=response,
                                       parsers=parsers)
            else:
                self._routes.set_route(path=path, view_func=func, method=method, resp_class=response, parsers=parsers)

            @wraps(func)
            def wrapper():
                return func

            return wrapper

        return add_route

    def wsgi(self, environ, start_response):
        # 处理 请求参数
        request = self.request_class(environ, self._session_pool)

        # 静态文件
        if request.path.startswith(self._static_url):
            file = self._static_route.check_file(request.path)
            return self._static_route(file, environ, start_response)

        try:
            path_obj = self._routes.get_route(request.path, request.method)
            # 解析

            request.parsing(path_obj.parsers, environ)
            request.set_path_value(path_obj.temp_vars)
            # 执行 resp类的call
            response = path_obj.view(request)
            if not isinstance(response, ResponseBase):
                response = path_obj.resp_class(response)

            path_obj.clear()
            response.set_header(request.get_header_param())
        except Exception as err:
            response = self.get_exception_resp(err)
        # 设置cookie session
        finally:
            del request
        return response(environ, start_response)

    def __call__(self, environ: Dict, start_response: Callable):

        return self.wsgi(environ, start_response)

    def get_exception_resp(self, err):
        if isinstance(err, HttpException):
            return HttpErrorResponse(err)
        else:
            if self.DEBUG:
                exc_type, exc_value, exc_traceback_obj = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback_obj, limit=2, file=self.ERROR_LOG)
                return ErrorResponse(err, exc_type)
            else:
                traceback.print_exc(file=self.ERROR_LOG)
                return ErrorResponse(err)
