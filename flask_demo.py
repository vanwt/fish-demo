from flask import Flask, request, jsonify
import json

app = Flask("__name__")


@app.route("/index/<int:id>", methods=["POST", "GET"])
def req(id):
    print(id)
    return jsonify({"code": 0, "msg": "hello word"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
