import logging
from threading import Thread

from gevent.pywsgi import WSGIServer

from noobgam.discord_bot.chatgpt_bot import run_bot
from noobgam.local_server.core_app import app

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    http_server = WSGIServer(("", 5000), app)

    discord_bot_proc = Thread(target=run_bot)
    discord_bot_proc.start()

    http_server.serve_forever()
