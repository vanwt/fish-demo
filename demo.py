from fish import FishApp
from fish.serve import run
from fish.parsers import UrlParams, JsonParams, FormParams, XmlParams

app = FishApp()
app.include_static("static", "/s")


def ccc(a):
    return int(a)


@app.get("/index", parsers=[UrlParams, ])
def index(req):
    print("demo1", req.session)

    req.session = {1: 1, 2: 21}
    return {"msg": "Hello Word", "code": 0}


@app.get("/index2", parsers=[UrlParams, ])
def index(req):
    print("demo2:", req.session)
    return {"msg": "Hello index2", "code": 0}


if __name__ == '__main__':
    run(app, host="0.0.0.0")
