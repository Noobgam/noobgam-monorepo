import logging

from gevent.pywsgi import WSGIServer

from noobgam.local_server.core_app import app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    http_server = WSGIServer(("", 5000), app)
    http_server.serve_forever()
