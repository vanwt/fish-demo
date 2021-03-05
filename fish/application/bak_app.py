from typing import List, Callable, Dict
from .baseapp import BaseApp
from ..parsers import BaseParser


class SimpleApp(BaseApp):
    def get(self, path: str, parsers: List[BaseParser] = None):
        """
            装饰器
            @app.get("/")
            def test(request):
                return "ok"

            @app.post("/")
            def test2(request):
                return "ok"
            加入到路由表中
        """
        # 解析器默认只有url解析
        parsers = parsers if parsers else ()

        # 存入解析器
        self.parser_map[path] = parsers

        def add_route(func):
            # 加入到路由表中
            self.add_routes(path, func, ["GET"])
            return func

        return add_route

    def post(self, path: str, parsers: List[BaseParser] = None):
        parsers = parsers if parsers else ()
        # 存入解析器
        self.parser_map[path] = parsers

        def add_route(func):
            # 加入到路由表中
            self.add_routes(path, func, ["POST"])
            return func

        return add_route

    def put(self, path: str, parsers: List[BaseParser] = None):
        parsers = parsers if parsers else ()

        # 存入解析器
        self.parser_map[path] = parsers

        def add_route(func):
            # 加入到路由表中
            self.add_routes(path, func, ["PUT"])
            return func

        return add_route

    def delete(self, path: str, parsers: List[BaseParser] = None):
        parsers = parsers if parsers else ()

        # 存入解析器
        self.parser_map[path] = parsers

        def add_route(func):
            # 加入到路由表中
            self.add_routes(path, func, ["DELETE"])
            return func

        return add_route
