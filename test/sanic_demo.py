from sanic import Sanic
from sanic.response import json

app = Sanic("__name__")


@app.route("/index")
def test(request):
    return json({"code": 0, "msg": "Hello World"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
