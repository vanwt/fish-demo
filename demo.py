from fish import FishApp
from fish.serve import run
from fish.parsers import UrlParams, JsonParams, FormParams, XmlParams
import pymysql

app = FishApp()
app.include_static("static", "/s")


def ccc(a):
    return int(a)


@app.get("/index/<int:id>/<str:id2>")
def index(req):
    # connect = pymysql.connections.Connection(host="127.0.0.1", user="root", password="root123", db="springdb",
    #                                          charset="utf8")
    # cur = connect.cursor()
    #
    # cur.execute("select * from student")
    # data = [{"id": i[0], "name": i[1], "age": i[2], "email": i[3]} for i in cur.fetchall()]
    # cur.close()
    # connect.close()
    # return data
    print(req.vars)
    return {"ok": 1}


@app.get("/index/<str:id2>")
def index1(req):
    print(req.vars)
    return {"ok": 1}


@app.get("/index")
def index2(req):
    print(req.vars)
    return {"ok": 1}


@app.get(r"^/index/sb-\d+$", re=True)
def index2(req):
    return {"ok": 233}


if __name__ == '__main__':
    run(app, host="0.0.0.0")
