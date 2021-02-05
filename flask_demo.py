from flask import Flask

app = Flask("__name__")


@app.route("/index")
def req():
    return {"code": 0, "msg": "Hello Word"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
