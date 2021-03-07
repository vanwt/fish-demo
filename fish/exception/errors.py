class HttpException(Exception):
    status_msg = ""
    message = ""

    def __init__(self, message=None, status_msg=None, code=None):
        if code:
            self.code = code
        if message:
            self.message = message
        if status_msg:
            self.status_msg = status_msg
        super().__init__(self.message)

    def get_message(self):
        return self.message


class HttpError(HttpException):
    code = 500
    status_code = "Server Error"


class MethodNoteFoundError(HttpException):
    code = 405
    status_msg = "METHOD NOT ALLOWED"
    message = "The method is not allowed for the requested URL"


class NotFoundError(HttpException):
    code = 404
    status_msg = "NOT FOUND"
    message = "The requested URL was not found on the server."


class ValueHttpError(HttpException):
    code = 500
    status_msg = "VALUE ERROR"
    message = "value error"
