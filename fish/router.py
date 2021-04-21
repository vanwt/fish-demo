import re
from .exception import NotFoundError


class ViewInfo:
    def __init__(self, method, view, parsers, resp_class, path=None, re_path=None):
        self.path_vars = []
        self.temp_vars = None
        self.path = path
        self.re_path = re_path
        self.method = method
        self.view = view
        self.parsers = parsers
        self.resp_class = resp_class
        self.is_re = False

        self.check_path()

    def __repr__(self):
        return self.path

    def check_path(self):
        if self.re_path:
            self.is_re = True
        else:
            path_vars = re.findall(r"/<(int|str):(\w+)>", self.path)
            if path_vars:
                self.is_re = True
                self.re_path = self.replace_path_value(path_vars)

    def replace_path_value(self, path_vars):

        new_path = self.path
        # 添加到参数中,并生成新的url
        for p_type, p_name in path_vars:
            # 添加到参数列
            # 把 <int:x>|<str:x> 替换为正则
            self.path_vars.append(dict(name=p_name, type=p_type))

            if p_type == "int":
                new_path = new_path.replace("<int:%s>" % p_name, "(?P<%s>\d+)" % p_name)
            elif p_type == "str":
                new_path = new_path.replace("<str:%s>" % p_name, "(?P<%s>\w+)" % p_name)

        return "^" + new_path + "$"

    def equal(self, method, path):
        return self.method == method and self.path == path

    def clear(self):
        self.temp_vars = []


class PathRouter:

    def __init__(self):
        self._map = []
        # self.compile = re.compile(r"(^/\w+)/?", re.S)

    def set_route(self, method: str, view_func, parsers, resp_class, path=None, re_path=None):
        if not path and not re_path:
            raise ValueError()

        for i in iter(self._map):
            if i.equal(path, method):
                return None

        self._map.append(ViewInfo(path=path, re_path=re_path, method=method,
                                  view=view_func, parsers=parsers,
                                  resp_class=resp_class))

    def get_route(self, request_path, request_method):
        """
        根据URL匹配
        判断请求类型
        判断是否正则匹配
        """
        for vi in iter(self._map):
            if vi.method == request_method:
                if vi.is_re:
                    result = self.match_path(vi.re_path, request_path)
                    if result:
                        vi.temp_vars = self.get_path_vars(vi.path_vars, result)
                        return vi
                else:
                    if vi.path == request_path:
                        return vi
        else:
            raise NotFoundError("404 Not Found")

    def __iter__(self):
        for i in self._map:
            yield i

    @staticmethod
    def match_path(re_path, request_path):
        return re.search(re_path, request_path)

    @staticmethod
    def get_path_vars(path_vars, search_result):
        """
        返回匹配结果，
        如果定义了路径参数，那么遍历参数对数据格式化
        """
        if path_vars:
            result = {}
            for pv in path_vars:
                var = search_result.group(pv["name"])
                if pv["type"] == "int":
                    var = int(var)
                result[pv["name"]] = var
            return result
        return search_result.groupdict()

    def search_path(self, request_path, request_path_vars, path: str):
        """
        使用正则匹配URL
        """
        result_map = {}
        result = re.search(request_path, path)
        if result:
            for pv in request_path_vars:
                var = result.group(pv["name"])
                if pv["type"] is int:
                    var = int(var)
                result_map[pv["name"]] = var

            return result_map

        return None

#
# if __name__ == '__main__':
#     from time import clock
#
#     """
#     简单测试
#     URL 50 条
#     """
#
#     pm = PathRouter()
#     pm.set_route("/index", "GET", max, None, None)
#     pm.set_route("/index", "POST", abs, None, None)
#     pm.set_route("/user", "GET", min, None, None)
#     pm.set_route("/user", "POST", min, None, None)
#     pm.set_route("/user", "DELETE", min, None, None)
#     pm.set_route("/usjgers", "GET", oct, None, None)
#     pm.set_route("/uNnser", "V", any, None, None)
#     pm.set_route("/uYmser", "C", min, None, None)
#     pm.set_route("/use4rs", "D", oct, None, None)
#     pm.set_route("/usolEer", "E", any, None, None)
#     pm.set_route("/ulsFer", "F", min, None, None)
#     pm.set_route("/usloseSrs", "G", oct, None, None)
#     pm.set_route("/usolseCr", "V", any, None, None)
#     pm.set_route("/usfverA", "B", min, None, None)
#     pm.set_route("/uVrsers", "T", oct, None, None)
#     pm.set_route("/usolRer", "H", any, None, None)
#     pm.set_route("/usoldeSrs", "G", oct, None, None)
#     pm.set_route("/usseCr", "V", any, None, None)
#     pm.set_route("/uvscerA", "B", min, None, None)
#     pm.set_route("/uVvsers", "T", oct, None, None)
#     pm.set_route("/usbRer", "H", any, None, None)
#     pm.set_route("/usolbeSrs", "G", oct, None, None)
#     pm.set_route("/useeCr", "V", any, None, None)
#     pm.set_route("/useerA", "B", min, None, None)
#     pm.set_route("/uVseyrs", "T", oct, None, None)
#     pm.set_route("/usRker", "H", any, None, None)
#     pm.set_route("/uscRker", "HU", any, None, None)
#
#     pm.set_route("/usolbeSrs", "GA", oct, None, None)
#     pm.set_route("/useeCr/<int:id>", "VCany", max, None, None)
#     pm.set_route("/useerA", "BV", min, None, None)
#     pm.set_route("/uVseyrs", "TT", oct, None, None)
#     pm.set_route("/usRker", "HY", any, None, None)
#     pm.set_route("/uscRker", "HIU", any, None, None)
#
#     pm.set_route("/ulsFer", "aF", min, None, None)
#     pm.set_route("/usloseSrs", "CG", oct, None, None)
#     pm.set_route("/usolsseCr", "tV", any, None, None)
#     pm.set_route("/usfvesrA", "itdB", min, None, None)
#     pm.set_route("/uVrsers", "sdfT", oct, None, None)
#     pm.set_route("/usolsRer", "dsH", any, None, None)
#     pm.set_route("/usoldeSrs", "Gsd", oct, None, None)
#
#     pm.set_route("/index", "PATH", max, None, None)
#     pm.set_route("/index", "UPDATE", abs, None, None)
#     pm.set_route("/users", "POST", min, None, None)
#     pm.set_route("/user", "DELETE", min, None, None)
#
#     pm.set_route("/ind2ex", "POST", abs, None, None)
#     pm.set_route("/us4er", "GET", min, None, None)
#     pm.set_route("/WEuser", "POST", min, None, None)
#     pm.set_route("/usEer", "DELETE", min, None, None)
#     pm.set_route("/us2jgers", "GET", oct, None, None)
#     pm.set_route("/uNn2332ser", "V", any, None, None)
#     pm.set_route("/uYR45mser", "C", min, None, None)
#     pm.set_route("/us6e4rs", "D", oct, None, None)
#     pm.set_route("/uso66lEer", "E", any, None, None)
#
#     print([i for i in pm])
#
#     s = clock()
#     # s = datetime.datetime.now()
#     for i in range(10000):
#         cls = pm.get_route("/index", "GET")
#         cls2 = pm.get_route("/index", "POST")
#         cls3 = pm.get_route("/user", "GET")
#         cls4 = pm.get_route("/users", "GET")
#         cls5 = pm.get_route("/user", "POST")
#         cls6 = pm.get_route("/userRT", "B")
#         cls7 = pm.get_route("/useERT", "h")
#         cls9 = pm.get_route("/usfvesrA", "itdB")
#         path = cls.path
#         method = cls5.method
#         view = cls9.view
#         # print(cls, cls2, cls3, cls4, cls5, cls6, cls7)
#     e = clock()
#     # e = datetime.datetime.now()
#     print(e - s)
