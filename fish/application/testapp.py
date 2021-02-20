from ..router import UrlMap
from ..request import Request
from ..response.http import NotFoundResponse, MethodNotAllowResponse
from ..response.errors import MethodNoteFoundError, NotFoundError
from ..serve import make_server
from typing import List, Callable, Dict


class TestApp:
    request_class = Request

    def __init__(self):
        self.url_map = UrlMap()

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

    def run(self, host="127.0.0.1", port=8000, thread=False):

        make_server((host, port), self, thread)

    def __call__(self, environ: Dict, start_response: Callable):

        # 此处要返回一个handler
        request = self.request_class(environ)

        # 查找路由
        url_obj = self.url_map.get_url(request.path)
        if not url_obj:
            resp = NotFoundResponse()()
            return resp(environ, start_response)

        # 对请求进行解析
        request.parsing(url_obj.parsers)

        try:
            # 返回结果是resp 类
            # 执行 resp类的call
            response_data = url_obj.view(request)
            resp = url_obj.response(response_data)()
        except NotFoundError:
            resp = NotFoundResponse()()
        except MethodNoteFoundError:
            resp = MethodNotAllowResponse()()
        return resp(environ, start_response)
