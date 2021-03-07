import json
from typing import List


class ResponseBase:
    status_code: int = 200
    content_type: str = "text/plain"
    # 状态值
    status_msg: str = "OK"
    content: str = ""
    encoding = "utf-8"

    def __init__(self, content=None, content_type: str = None, status: int = None, status_msg: str = None,
                 encoding: str = None):
        self.headers = []
        if content:
            self.content = content
        if content_type:
            self.content_type = content_type
        if encoding:
            self.encoding = encoding

        if status_msg:
            self.status_msg = status_msg

        if status is not None:
            try:
                self.status_code = int(status)
            except (ValueError, TypeError):
                raise TypeError('HTTP status code must be an integer.')

        if not 100 <= self.status_code <= 599:
            raise ValueError('HTTP status code must be an integer from 100 to 599.')

    def encode_response(self):
        """ 数据进行转码 """
        return self.content.encode(self.encoding)

    def set_cookie(self, name: str, value, second: int = None, path: str = "/"):
        """
        Set-Cookie: name=yunwei; Expires=Thu, 01 Jan 1970 00:00:01 GMT; Path=/;
        "%a, %d %b %Y %H:%M:%S GMT"
        datetime.utcnow().strftime(f)
        """
        fmt = "{name}={value}; Path={path};".format(name=name, value=value, path=path)
        if second:
            fmt += " Expires={date}".format(date=second)

        # 加入请求头
        self.headers.append(("Set-Cookie", fmt))

    def __call__(self, environ, start_response):
        msg = "{0} {1}".format(self.status_code, self.status_msg)
        # headers 最后生成
        self.headers.append(("Content-Type", "{0}; charset={1}".format(self.content_type, self.encoding)))

        start_response(msg, self.headers)
        yield self.encode_response()


class ErrorResponse(ResponseBase):
    encoding = "utf-8"
    content_type = "application/json"

    def __init__(self, error):
        self.err = error
        super().__init__(content=error.message, status=error.code, status_msg=error.status_msg)

    def encode_response(self):
        resp = {
            "code": self.err.code,
            "message": self.err.message
        }
        return json.dumps(resp, ensure_ascii=False).encode(self.encoding)


class TemplateResponse(ResponseBase):
    content_type = "text/html"

    def __init__(self, template_name: str = None, encoding: str = None):
        super(TemplateResponse, self).__init__(status=200)
        if encoding:
            self.encoding = encoding
        if template_name:
            self.file_to_response(template_name)

    def file_to_response(self, name):
        with open(name, "r", encoding="UTF-8", errors="ignore") as f:
            self.content = f.read()


class Text(ResponseBase):
    pass


class Json(ResponseBase):
    content_type = "application/json"

    def encode_response(self):
        return json.dumps(self.content, ensure_ascii=False).encode(self.encoding)


class Xml(ResponseBase):
    content_type = "application/xml"


class Html(ResponseBase):
    content_type = "text/html"
