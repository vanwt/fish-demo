import os
from typing import List
class StaticLoader(object):
    suffix = ["*"]

    types = {
        "css": "text/css",
        "js": "application/javascript",
        "html": "text/html",
        "txt": "text/plan",
        "png": "image/png",
        "json": "application/json",
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
        "jpe": "image/jpeg"
    }

    def __init__(self, directory: str, url: str, suffix: List[str] = None):
        self.cwd = os.getcwd()
        self.request = None
        self.file_path = None
        self.file_name = None
        self.is_exist = False
        self.header = []
        self.static_directory = os.path.join(self.cwd, directory)
        if not os.path.isdir(self.static_directory):
            raise FileExistsError("{dir} Not a directory !".format(dir=directory))
        self.static_url = url if url[-1] == "/" else url + "/"
        if suffix:
            self.suffix = suffix

    def __call__(self, request):
        self.init_request(request)
        msg: str = self.get_status()
        self.get_header()
        data: bytes = self.get_data() if self.is_exist else b"<h1>404 Not Found !</h1>"

        def view(environ, start_response):
            start_response(msg, self.header)
            yield data

        return view

    def init_request(self, request):
        path = request.path[len(self.static_url):]
        path = [p for p in path.split("/") if p]

        self.file_name = path[-1]
        self.file_path = os.path.join(self.static_directory, *path)

    def get_header(self):
        # 判断 path的请求类型返回对应的content-type

        if not self.is_exist or "." not in self.file_name:
            self.header = [("Content-Type", "text/html; charset=utf-8")]
        else:
            suffix = self.file_name.split(".")[-1]
            self.header = [("Content-Type", self.types.get(suffix, "text/html") + "; charset=utf-8")]

    def get_status(self):
        """
        根据判断有没有这个文件返回 404 或200 ok
        :return defalut 404  Not Found Error
        """
        if os.path.isfile(self.file_path):
            self.is_exist = True
            return "200 OK"
        return "404 Not Found Error"

    def get_data(self):
        """
        打开文件( rb encode="utf-8")，返回文件内容
        """
        f = open(self.file_path, "rb")
        data = f.read()
        f.close()
        self.header.append(("content-length", str(len(data))))
        return data

