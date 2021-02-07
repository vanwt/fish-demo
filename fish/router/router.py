from fish.response.errors import MethodNoteFoundError, NotFoundError
from typing import List, Callable


class PathObj:
    def __init__(self, method, view_func: Callable = None, parsers: List = None):
        if type(method) is list:
            self.method_view = self.method_parsers = {}
            for m in method:
                if view_func:
                    self.method_view[m] = view_func
                if parsers:
                    self.method_parsers = parsers
        else:
            self.method_view = {method: view_func} if method and view_func else {}
            self.method_parsers = {method: parsers} if method and parsers else {}

    def set_func_parsers(self, method, view_func=None, parsers=None):
        if view_func:
            self.method_view[method] = view_func

        if parsers:
            self.method_parsers[method] = parsers

    def get_view(self, method):
        return self.method_view.get(method, None)

    def get_parsers(self, method) -> []:
        return self.method_parsers.get(method, None)


class PathRole:
    """
    {
        "/" : PathObj(),
    }
    """

    def __init__(self):
        self.paths = {}

    def add_view(self, path, view_func, method):

        path_obj = self.paths.get(path, None)
        if not path_obj:
            self.paths[path] = PathObj(method, view_func=view_func)
        else:
            path_obj.set_func_parsers(method, view_func=view_func)

    def add_parser(self, path, method, parsers):
        path_obj = self.paths.get(path, None)
        if not path_obj:
            self.paths[path] = PathObj(method=method, parsers=parsers)
        else:
            path_obj.set_func_parsers(method, parsers=parsers)

    def get(self, path) -> PathObj:
        path_obj = self.paths.get(path, None)
        return path_obj

    def __repr__(self):
        return self.paths


class UrlMap:
    """
    {
        "/" : {
            "GET":view,
            "POST":view2
        }
    }
    """

    def __init__(self):
        self.path_map = {}

    def add(self, path: str, view: Callable, methods: List[str]):
        """ 不存在直接创建，已存在用update """
        if path not in self.path_map:
            self.path_map[path] = {method: view for method in methods}
        else:
            self.path_map[path].update({method: view for method in methods})

    def get(self, path: str, method: List[str]):
        """ 根据path查找 method 字典"""
        views = self.path_map.get(path, None)
        # 找不到路由
        if views is None:
            raise NotFoundError()
        # 找不到对应method方法
        func_view = views.get(method, None)
        if func_view is None:
            raise MethodNoteFoundError()
        return func_view

    def __repr__(self):
        return self.path_map


class StaticRoute():
    def __init__(self, request):
        pass

    def readFile(self, filename):
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
        return data
