from wsgiref.simple_server import WSGIRequestHandler
from .wsgi import WSGIServer, ThreadWSGIServer

from werkzeug.serving import run_simple


def run(app, host="127.0.0.1", port=8000, **options):
    options.setdefault("threaded", True)
    run_simple(host, port, app, **options)


def run2(address, application, thread):
    print("Fish framework demo v0.1")

    if thread:
        server = ThreadWSGIServer(address, WSGIRequestHandler)
        print("MultiThreaded Server version v0.1 ")
    else:
        server = WSGIServer(address, WSGIRequestHandler)
        print("SimpleTCP Server version v0.1 ")

    print("Server on %d" % address[1])
    print("Default url: http://%s:%d" % address)
    server.set_app(application)
    server.serve_forever()
