from fish.application.newapp import NewApp
from fish.response import Json, Text

# app = BaseApp()
app = NewApp()


@app.response(Json)
@app.route("/index", "GET", parsers=(1, 2, 3, 4), resp=Json)
def index(req):
    return {"code": 0, "msg": "Hello Word"}


if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=8000)
    app.run2(host="0.0.0.0", port=8000, thread=True)


@Router("/", sdfsff)
class A:
    @Response(Text)
    @Parser(Json, Text)
    def get(self):
        pass
