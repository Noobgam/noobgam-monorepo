from dataclasses import dataclass

from noobgam.llm.config import get_anki_chain
from noobgam.llm.prompts import CONVERT_DIARY_TO_CARDS


@dataclass
class GenerateCardsFromDiary:
    diary: str


def handler(inp: GenerateCardsFromDiary):
    anki_chain = get_anki_chain()
    return anki_chain.predict(input=CONVERT_DIARY_TO_CARDS.format(diary=inp.diary))
