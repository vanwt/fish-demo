from fish.application.baseapp import BaseApp
from fish.application.testapp import TestApp
from fish.response import Json, Text

# app = BaseApp()
app = TestApp()


@app.response(Json)
@app.route("/index", "GET")
def index(req):
    return {"code": 0, "msg": "Hello Word"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", thread=True)