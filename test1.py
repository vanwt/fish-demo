from fish import SimpleApp
from fish.response import Json, Text

app = SimpleApp()


@app.get("/index")
def index(req):
    return Json({"code": 0, "msg": "Hello Word"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", thread=True)
