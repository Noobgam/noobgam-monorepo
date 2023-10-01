from flask import Flask, Request, abort

from noobgam.handlers.anki_compose_sentence import GenerateCardInput
from noobgam.handlers.anki_convert_diary import GenerateCardsFromDiary
from noobgam.handlers.authorization_check import check_token

app = Flask(__name__)

def check_authorization(request: Request):
    if not request.authorization or not request.authorization.token:
        abort(401)
    if not check_token(request.authorization.token):
        abort(401)


@app.route("/anki/generateExampleSentence", methods=["POST"])
def generateExampleSentence():
    from flask import request

    from noobgam.handlers.anki_compose_sentence import handler
    check_authorization(request)

    return handler(GenerateCardInput(**request.json))


@app.route("/anki/generateCardsFromDiary", methods=["POST"])
def generateCardsFromDiary():
    from flask import request

    from noobgam.handlers.anki_convert_diary import handler
    check_authorization(request)

    return handler(GenerateCardsFromDiary(**request.json))
