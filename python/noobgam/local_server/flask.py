from flask import Flask

from noobgam.handlers.anki_compose_sentence import GenerateCardInput

app = Flask(__name__)


@app.route("/generateAnkiCard", methods=["POST"])
def handler():
    from flask import request

    from noobgam.handlers.anki_compose_sentence import handler

    return handler(GenerateCardInput(**request.json))
