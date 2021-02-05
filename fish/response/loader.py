from .response import ResponseBase


class CssLoader(ResponseBase):
    content_type = "text/css"
    encoding = "utf-8"


class ImageLoader(ResponseBase):
    pass
