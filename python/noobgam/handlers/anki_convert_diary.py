import json
from dataclasses import dataclass

from noobgam.llm.config import get_anki_chain
from noobgam.llm.prompts import CONVERT_DIARY_TO_CARDS


@dataclass
class GenerateCardsFromDiary:
    diary: str


def handler(inp: GenerateCardsFromDiary):
    anki_chain = get_anki_chain()
    text_resp = anki_chain.predict(
        input=CONVERT_DIARY_TO_CARDS.format(diary=inp.diary)
    )
    l = text_resp.find('```')
    r = text_resp.find('```', l + 1)
    return {
        "cards": json.loads(text_resp[l + 3:r])
    }
