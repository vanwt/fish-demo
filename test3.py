from fish import FishApp
from fish.serve import run
from fish.parsers import UrlParams, JsonParams, FormParams, XmlParams

app = FishApp()
app.include_static("static", "/s")


def ccc(a):
    return int(a)


@app.get("/index", parsers=[UrlParams, ])
def index(req):
    # print(req.data)
    # return Html("<h1>Hello Word</h1>")
    # print(req.data)
    return {"msg": "Hello Word", "code": 0}


@app.post("/index", parsers=(UrlParams, FormParams, JsonParams, XmlParams))
def index_post(req):
    print(req.data)
    return req.data


if __name__ == '__main__':
    run(app, host="0.0.0.0")
