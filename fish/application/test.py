from fish.request import Request
from fish.serve import make_server
from fish.parsers import UrlParser, BaseParser, FormParser
from fish.response import Text
from typing import Dict, Callable



class TestApp:
    request_class = Request

    def run(self, host="127.0.0.1", port=8000, thread=False):
        make_server((host, port), self, thread)

    def __call__(self, environ: Dict, start_response: Callable):
        from time import clock
        # 此处要返回一个handler
        request = self.request_class(environ)

        # 对请求进行解析

        request.parsing((UrlParser,))
        print(request.data)
        resp = Text("OK")()

        return resp(environ, start_response)


if __name__ == '__main__':
    app = TestApp()

    app.run()
