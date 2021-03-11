from .response import ResponseBase
from ..exception import FileNotFoundHttpError
import os, re


class StaticLoader(ResponseBase):

    def __init__(self, static_path, url, head_url):
        rep = r"{0}/(\S+)".format(head_url)
        filename = re.findall(rep, url)[0]
        file_path = os.path.join(static_path, filename)
        if not os.path.isfile(file_path):
            raise FileNotFoundHttpError()

        self.path = file_path
        super().__init__(content_type="text/plain")

    def encode_response(self):
        with open(self.path, "rb") as f:
            return f.read()


class CssLoader(ResponseBase):
    content_type = "text/css"
    encoding = "utf-8"


class ImageLoader(ResponseBase):
    pass
