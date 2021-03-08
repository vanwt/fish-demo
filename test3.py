from fish import FishApp
from fish.response import Text
from fish.parsers import UrlParser, FormParser

app = FishApp()
app.include_static("static", "/static")


def ccc(a):
    return int(a)


@app.get("/index", response=Text)
def index(req):
    ccc(req.data["a"])
    return {"msg": "Hello Word", "code": 0}


@app.post("/index", parsers=(UrlParser, FormParser))
def index_post(req):
    print(req.data)
    return req.data


if __name__ == '__main__':
    app.run(host="0.0.0.0")
