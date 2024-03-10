import logging
from multiprocessing import Process
from threading import Thread

from gevent.pywsgi import WSGIServer

from noobgam.discord_bot.chatgpt_bot import run_bot
from noobgam.local_server.core_app import app
from noobgam.telegram_bot.simple_bot import run_tg_bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    run_tg_bot()
