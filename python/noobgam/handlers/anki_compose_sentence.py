import json
from dataclasses import dataclass

from noobgam.llm.config import get_anki_chain
from noobgam.llm.prompts import ANKI_CARD_GENERATE_EXAMPLE_SENTENCE, ANKI_CORRECT_ERRORS


@dataclass
class GenerateCardInput:
    card_fields: dict[str, str]
    target_language: str
    theme: str


def handler(inp: GenerateCardInput):
    anki_chain = get_anki_chain()
    prompt_text = ANKI_CARD_GENERATE_EXAMPLE_SENTENCE.format(
        payload=json.dumps(inp.card_fields, ensure_ascii=False),
        target_language=inp.target_language,
        theme=inp.theme,
    )
    return anki_chain.predict(input=prompt_text)
