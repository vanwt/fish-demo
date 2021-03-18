from fish import FishApp
from fish.serve import run
from fish.parsers import UrlParser, FormParser

app = FishApp()
app.include_static("static", "/s")


def ccc(a):
    return int(a)


@app.get("/index")
def index(req):
    # return Html("<h1>Hello Word</h1>")
    return {"msg": "Hello Word", "code": 0}


@app.post("/index", parsers=(UrlParser, FormParser))
def index_post(req):
    print(req.data)
    return req.data


if __name__ == '__main__':
    run(app,host="0.0.0.0")
