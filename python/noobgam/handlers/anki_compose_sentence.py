import json

from noobgam.llm.config import get_anki_chain
from noobgam.llm.prompts import ANKI_CARD_GENERATE_EXAMPLE_SENTENCE, ANKI_CORRECT_ERRORS


def handler(event, context):
    anki_chain = get_anki_chain()
    print(
        anki_chain.predict(
            input=ANKI_CARD_GENERATE_EXAMPLE_SENTENCE.format(
                payload=json.dumps(
                    {
                        "target_languages": "Japanese",
                        "card": {
                            "Expression": "向かって",
                            "Meaning": "towards",
                            "Reading": "向[む]かって",
                            "Lesson Number": "",
                            "Example sentence": "",
                            "Example sentence meaning": "",
                            "Example sentence reading": "",
                        },
                    },
                    ensure_ascii=False,
                )
            )
        )
    )
