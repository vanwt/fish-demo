"""
wsgi -> application -> router -> request -> view
处理 environ 中的参数
data,method...
"""


def parser_cookie(cookie):
    """ 转换cookie字符串至 字典 """
    data = {}
    for c in cookie.split(";"):
        key, *value = c.strip().split("=")
        if '[' in value and ']' in value or "{" in value and "}" in value:
            value = eval(value.replace("null", "None").replace("undefined", "None"))
            data.update(value)
        else:
            data.update({key: value})

    return data


class NewRequest:
    def __init__(self, environ, session_poll=None):
        self.path = environ["PATH_INFO"]
        self.method = environ['REQUEST_METHOD'].upper()
        self.data = {}
        self._cookie = environ.get("HTTP_COOKIE", None)
        self.resp_cookie = []
        self.cookie_data = None
        self._session = session_poll
        self.session_id = None
        self.clear_session = False
        self.set_session = False
        self.vars = []

    def parsing(self, parsers, environ):
        """ 根据解析器解析数据 """
        if not parsers:
            return None

        for parser in parsers:
            p_data = parser("wsgi.input", environ)
            if type(p_data) == dict:
                self.data.update(p_data)

    @property
    def cookie(self):
        """ 读取原始cookie 转换为dict """
        if self._cookie is None:
            return {}
        if self.cookie_data:
            return self.cookie_data

        cookie = parser_cookie(self._cookie)

        for key in cookie.keys():
            value = cookie[key]
            if isinstance(value, list):
                if len(value) == 1:
                    cookie[key] = value[0]
                elif len(value) < 1:
                    cookie[key] = None
        self.cookie_data = cookie
        return cookie

    @cookie.setter
    def cookie(self, value):

        if isinstance(value, dict):
            self.cookie_data = value
        raise ValueError("Cookie type must be Dict !")

    @property
    def session(self):
        """读取 cookie中的session """
        self.session_id = self.cookie.get("SESSION_ID")

        if not self.session_id:
            return None

        data = self._session.get_session(self.session_id)
        # 清除无效session
        if data is None:
            self.clear_session = True
            self.session_id = None
        return data

    @session.setter
    def session(self, value):
        """
        获取session 并写入到字典 ,若没有则新建新的字典空间，并写入cookie
        """
        if isinstance(value, dict):
            if not self.session_id:
                self.set_session = True
                self.clear_session = False
                self.session_id = self._session.create_session()
            self._session.set_value(self.session_id, value)

    def get_header_param(self):
        """ 设置cookie 和session """

        if self.cookie_data:
            for key, value in self.cookie_data.items():
                if key == "SESSION_ID":
                    continue
                self.resp_cookie.append({"name": key, "value": value, "date": None})

        if self.set_session:
            self.resp_cookie.append({"name": "SESSION_ID", "value": self.session_id, "date": None})

        if self.clear_session:
            self.resp_cookie.append({"name": "SESSION_ID", "value": "xxxx", "date": 0})

        return self.resp_cookie

    def set_path_value(self, value):
        self.vars = value
