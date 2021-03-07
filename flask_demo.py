from flask import Flask, request, jsonify
import json

app = Flask("__name__")


@app.route("/index", methods=["POST", "GET"])
def req():
    print(request.form)
    return jsonify({"code": 0, "msg": "hello word"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
