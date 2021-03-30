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

    def parsing(self, parsers):
        """ 根据解析器解析数据 """
        [self.data.update(p.parser()) for parser in parsers]
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


class NewRequest:
    def __init__(self, environ):
        self.path = environ["PATH_INFO"]
        self.method = environ['REQUEST_METHOD'].upper()
        self.data = {}
        self._cookie = environ.get("HTTP_COOKIE", None)

    def parsing(self, parsers, environ):
        """ 根据解析器解析数据 """

        for parser in parsers:
            p_data = parser("wsgi.input", environ)
            if type(p_data) == dict:
                self.data.update(p_data)

    @property
    def cookie(self):
        if self._cookie is None:
            return {}

        return parser_cookie(self._cookie)
