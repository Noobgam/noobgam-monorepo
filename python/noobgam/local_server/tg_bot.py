import logging

from noobgam.telegram_bot.simple_bot import run_tg_bot


def configure_logger():
    logging.basicConfig(
        format="%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler("debug.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    logging.getLogger("asyncio").setLevel(logging.DEBUG)
    logger = logging.getLogger("lcu-driver")
    logger.setLevel(logging.INFO)


if __name__ == "__main__":
    configure_logger()

    run_tg_bot()
