from fish.application import FishApp

app = FishApp()


@app.get("/index")
def index(req):

    return {"msg": "Hello Word", "code": 0}


if __name__ == '__main__':
    app.run(host="0.0.0.0")
