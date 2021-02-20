from fish.application.newapp import NewApp
from fish.response import Json, Text

# app = BaseApp()
app = NewApp()


@app.response(Json)
@app.route("/index", "GET")
def index(req):
    return {"code": 0, "msg": "Hello Word"}


if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=8000)
    app.run2(host="0.0.0.0", port=8000, thread=True)
