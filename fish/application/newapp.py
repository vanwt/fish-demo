from ..request import Request
from ..response.http import NotFoundResponse, MethodNotAllowResponse
from ..response.errors import MethodNoteFoundError, NotFoundError
from ..serve import make_server
from ..config import METHODS
from typing import List, Callable, Dict
from functools import wraps
from collections import UserDict
from ..response import Json


class UrlMap(UserDict):
    def add(self, path, view_func, method):
        self.data[(path, method)] = view_func


class NewApp:
    request_class = Request
    view_options = {}
    debug = True

    def __init__(self):
        self.routes = UrlMap()

    def add_routes(self, path: str, view: Callable, method: str):
        """
        添加路由
        :param path: url
        :param options:  methods 目前只有请求类型
        :return: None
        """

        if method not in METHODS:
            raise AttributeError("method must in {0!r}".format(METHODS))

        self.routes.add(path, view, method)

    def route(self, path: str, method: str):
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

        def add_route(func: Callable):
            # 加入到路由表中
            self.add_routes(path, func, method)

            @wraps(func)
            def wrapper():
                return func

            return wrapper

        return add_route

    def parsers(self, *parsers):
        def parser_fun(func):
            key = id(func)
            if key in self.view_options:
                # 存入解析器
                self.view_options[key]["p"] = parsers
            else:
                self.view_options[key] = {"p": parsers}
            return func

        return parser_fun

    def response(self, resp):
        def set_resp(func):
            key = id(func)
            if key in self.view_options:
                self.view_options[key]["r"] = resp
            else:
                self.view_options[key] = {"r": resp}
            return func

        return set_resp

    def run(self, host="127.0.0.1", port=8000, **options):
        from werkzeug.serving import run_simple
        # options.setdefault("use_reloader", self.debug)
        # options.setdefault("use_debugger", self.debug)
        options.setdefault("threaded", True)

        run_simple(host, port, self, **options)

    def run2(self, host="127.0.0.1", port=8000, thread=False):

        make_server((host, port), self, thread)

    def wsgi(self, environ, start_response):
        # 此处要返回一个handler
        request = self.request_class(environ)

        view = self.routes.get((request.path, request.method))
        if not view:
            resp = NotFoundResponse()()
            return resp(environ, start_response)

        view_id = id(view)

        Response = Json
        if view_id in self.view_options:
            # 查找存储的解析器
            # 没有就404
            func_opt = self.view_options.get(view_id)
            # 对请求进行解析
            request.parsing(func_opt["p"])

            Response = func_opt.get("r", Json)
        try:

            # 返回结果是resp 类
            # 执行 resp类的call
            data = view(request)
            resp = Response(data)()


        except NotFoundError:
            resp = NotFoundResponse()()
        except MethodNoteFoundError:
            resp = MethodNotAllowResponse()()
        return resp(environ, start_response)

    def __call__(self, environ: Dict, start_response: Callable):

        return self.wsgi(environ, start_response)
