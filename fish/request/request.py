"""
wsgi -> application -> router -> request -> view
处理 environ 中的参数
data,method...
"""
from .cookie import parser_cookie


class Request(object):
    def __init__(self, environ):
        self.environ = environ
        self.path = environ["PATH_INFO"]
        self.method = environ['REQUEST_METHOD'].upper()
        self.data = {}
        self._cookie = environ.get("HTTP_COOKIE", None)
        #
        # for k, v in environ.items():
        #     print(k, v)

    def parsing(self, parsers):
        """ 根据解析器解析数据 """
        for parser in parsers:

            p = parser(self.environ)
            if p.is_par():
                self.data.update(p.parser())

    # @lazyproperty
    @property
    def cookie(self):
        if self._cookie is None:
            return {}
        # 对cookie格式化
        return parser_cookie(self._cookie)
