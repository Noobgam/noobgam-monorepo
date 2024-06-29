import json
from dataclasses import dataclass

from noobgam.llm.config import get_anki_chain
from noobgam.llm.prompt.japanese_prompts import ANKI_JAPANESE_REQUIRED_FORMAT
from noobgam.llm.prompt.prompts import ANKI_CARD_GENERATE_EXAMPLE_SENTENCE


@dataclass
class GenerateCardInput:
    card_fields: dict[str, str]
    target_language: str
    theme: str


def handler(inp: GenerateCardInput):
    examples = ""
    rule_format = ""
    if inp.target_language.lower() == "japanese":
        rule_format = ANKI_JAPANESE_REQUIRED_FORMAT

    anki_chain = get_anki_chain()
    prompt_text = ANKI_CARD_GENERATE_EXAMPLE_SENTENCE.format(
        payload=json.dumps(inp.card_fields, ensure_ascii=False),
        target_language=inp.target_language,
        theme=inp.theme,
        examples=examples,
        rule_format=rule_format,
    )
    return anki_chain.invoke(prompt_text)
