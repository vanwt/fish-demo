# from ..router import PathRole
# from ..request import Request
# from ..response.http import NotFoundResponse, MethodNotAllowResponse
# from ..response.errors import MethodNoteFoundError, NotFoundError
# from ..serve import make_server
# from ..parsers import BaseParser
# from ..loader import StaticLoader
# from ..config import METHODS
# from typing import List, Callable, Dict
# from functools import wraps
# from ..response import Json
#
#
# class BaseApp:
#     request_class = Request
#     static_url = ""
#     static_dir = None
#
#     def __init__(self):
#         self.routes = PathRole()
#         self.debug = True
#         self.parser_map: dict = {}
#
#     def add_routes(self, path: str, view: Callable, methods: List[str]):
#         """
#         添加路由
#         :param path: url
#         :param options:  methods 目前只有请求类型
#         :return: None
#         """
#         # check methods
#         for m in methods:
#             if m not in METHODS:
#                 raise AttributeError("method must in {0!r}".format(METHODS))
#
#         self.routes.add_view(path, view, methods)
#
#     def route(self, path: str, methods: List[str], parsers: List[BaseParser] = None):
#         """
#         装饰器
#         @app.route("/",["GET"])
#         def test(req):
#             return "ok"
#
#         @app.route("/",["POST"])
#         def test2(req):
#             return "ok"
#         加入到路由表中
#
#         """
#
#         # 解析器默认只有url解析
#         parsers = parsers if parsers else ()
#
#         # 存入解析器
#         self.parser_map[path] = parsers
#
#         def add_route(func: Callable):
#             # 加入到路由表中
#             self.add_routes(path, func, methods)
#
#             @wraps(func)
#             def wrapper():
#                 return func
#
#             return wrapper
#
#         return add_route
#
#     def response(self, resp: Callable):
#
#         def set_resp(func):
#             print(func)
#
#             @wraps(func)
#             def wrapper():
#                 return func
#
#             return wrapper
#
#         return set_resp
#
#     def run(self, host="127.0.0.1", port=8000, thread=False):
#
#         make_server((host, port), self, thread)
#
#     def __call__(self, environ: Dict, start_response: Callable):
#
#         # 此处要返回一个handler
#         request = self.request_class(environ)
#
#         # 静态文件
#         if self.static_dir and request.path.startswith(self.static_url):
#             resp = StaticLoader(directory=self.static_dir, url=self.static_url)(request)
#             return resp(environ, start_response)
#
#         # 查找存储的解析器
#         # 没有就404
#         func_parser = self.parser_map.get(request.path, None)
#         # 对请求进行解析
#         if func_parser:
#             request.parsing(func_parser)
#
#         try:
#             path_obj = self.routes.get(request.path)
#
#             # 返回结果是resp 类
#             view_func = path_obj.get_view(request.method)
#             # 执行 resp类的call
#             response_data = view_func(request)
#             resp = Json(response_data)()
#         except NotFoundError:
#             resp = NotFoundResponse()()
#         except MethodNoteFoundError:
#             resp = MethodNotAllowResponse()()
#         return resp(environ, start_response)
