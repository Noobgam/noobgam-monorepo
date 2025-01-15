import json

from noobgam.llm.config import get_anki_chain
from noobgam.llm.prompt.prompts import ANKI_CORRECT_ERRORS


def handler(event, context):
    anki_chain = get_anki_chain()
    print(
        anki_chain.invoke(
            ANKI_CORRECT_ERRORS.format(
                payload=json.dumps(
                    {
                        "target_languages": ["Japanese"],
                        "card": {
                            "japanese": "新幹線",
                            "japanese_reading": "新幹線[しんかんせん]",
                        },
                    },
                    ensure_ascii=False,
                )
            )
        )
    )