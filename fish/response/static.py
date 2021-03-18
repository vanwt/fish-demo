from .response import ResponseBase
from ..exception import FileNotFoundHttpError
import os, re
from pathlib import Path
from ._static_dict import type_map


class StaticLoader(ResponseBase):

    def __init__(self, static_path, url, head_url):
        rep = r"{0}/(\S+)".format(head_url)
        filename = re.findall(rep, url)[0]
        file_path = os.path.join(static_path, filename)
        if not os.path.isfile(file_path):
            raise FileNotFoundHttpError()

        self.path = file_path
        super().__init__(content_type="application/octet-stream")

    def encode_response(self):
        with open(self.path, "rb") as f:
            return f.read()


class StaticRouter:

    def __init__(self, static_path, encode="utf-8"):
        self.path: Path = Path(static_path)
        self.encode = encode

    def check_file(self, url):
        filename = url.split("/")[-1]
        file = self.path / filename
        if not file.is_file():
            raise FileNotFoundHttpError()
        return file

    @staticmethod
    def get_content_type(suffix):
        return type_map.get(suffix, "text/plain")

    def __call__(self, file, environ, start_response):
        content_type = self.get_content_type(file.suffix) + "; charset={0}".format(self.encode)
        start_response("200 OK", [("Content-Type", content_type)])

        fio = file.open(mode="rb")
        data = fio.read()
        fio.close()
        yield data
