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
        if not path_obj:
            raise NotFoundError()
        return path_obj

    def __repr__(self):
        return self.paths


class StaticRoute():
    def __init__(self, request):
        pass

    def readFile(self, filename):
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
        return data
