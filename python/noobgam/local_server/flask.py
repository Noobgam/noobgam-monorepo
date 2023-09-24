from flask import Flask

from noobgam.handlers.anki_compose_sentence import GenerateCardInput
from noobgam.handlers.anki_fix_error import GenerateCardsFromDiary

app = Flask(__name__)


@app.route("/anki/generateExampleSentence", methods=["POST"])
def generateExampleSentence():
    from flask import request

    from noobgam.handlers.anki_compose_sentence import handler

    return handler(GenerateCardInput(**request.json))


@app.route("/anki/generateCardsFromDiary", methods=["POST"])
def generateCardsFromDiary():
    from flask import request

    from noobgam.handlers.anki_fix_error import handler

    return handler(GenerateCardsFromDiary(**request.json))
