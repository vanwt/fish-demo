from .response import Json


class MethodNotAllowResponse(Json):
    status_code = 405
    msg = "Method Not Found"
    content = {"error": "Method Not Found"}


class NotFoundResponse(Json):
    status_code = 404
    msg = "Not Found Error"
    content = {"error": "404 Not Found !"}
