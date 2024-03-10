import logging
from threading import Thread

from gevent.pywsgi import WSGIServer

from noobgam.discord_bot.chatgpt_bot import run_bot
from noobgam.local_server.core_app import app
from noobgam.telegram_bot.simple_bot import run_tg_bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    http_server = WSGIServer(("", 5000), app)

    discord_bot_thread = Thread(target=run_bot)
    discord_bot_thread.start()

    tg_bot_thread = Thread(target=run_tg_bot)
    tg_bot_thread.start()
    tg_bot_thread.join()

    http_server.serve_forever()
