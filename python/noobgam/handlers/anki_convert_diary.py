import json
from dataclasses import dataclass
from typing import Optional

from noobgam.llm.config import get_anki_chain
from noobgam.llm.llm_retrier import retry_until_valid
from noobgam.llm.prompt.generic_prompts import (
    CONVERT_DIARY_TO_CARDS_EXAMPLES,
    REQUIRED_FORMAT,
)
from noobgam.llm.prompt.japanese_prompts import (
    ANKI_JAPANESE_CONVERT_DIARY_TO_CARDS_EXAMPLES,
    ANKI_JAPANESE_REQUIRED_FORMAT,
)
from noobgam.llm.prompt.prompts import CONVERT_DIARY_TO_CARDS_TEMPLATE


@dataclass
class GenerateCardsFromDiary:
    diary: str
    language: str


def find_first_code_chunk(text_resp: str) -> Optional[str]:
    l = text_resp.find("```")
    if l == -1:
        return None
    r = text_resp.find("```", l + 1)
    if r == -1:
        return None
    chunk = text_resp[l + 3 : r]
    if chunk.startswith("json"):
        chunk = chunk[4:]
    return chunk


def validate_response(text_resp: str) -> Optional[str]:
    chunk = find_first_code_chunk(text_resp)
    if not chunk:
        return "Could not find code, make sure it is escaped properly"
    try:
        val = json.loads(chunk)
    except Exception:
        return "Escaped value is not a valid JSON"

    for note in val:
        if "Expression" not in note:
            return f"No Expression found for {json.dumps(note)}"

    return None


def handler(inp: GenerateCardsFromDiary):
    examples = CONVERT_DIARY_TO_CARDS_EXAMPLES
    rule_format = REQUIRED_FORMAT
    added_initial_prompt: str
    if inp.language.lower() == "japanese":
        examples = ANKI_JAPANESE_CONVERT_DIARY_TO_CARDS_EXAMPLES
        rule_format = ANKI_JAPANESE_REQUIRED_FORMAT
        added_initial_prompt = ANKI_JAPANESE_REQUIRED_FORMAT
    else:
        added_initial_prompt = "If the language contains complicated cases (Cases in German, padeji in russian) try to incorporate them as well"

    anki_chain = get_anki_chain("\n\n" + added_initial_prompt)
    anki_chain.predict(
        input="Repeat the rules to me one by one, explain how the rules are used in the examples."
    )
    text_resp = retry_until_valid(
        retries=3,
        chain=anki_chain,
        prompt=CONVERT_DIARY_TO_CARDS_TEMPLATE.format(
            diary=inp.diary,
            language=inp.language,
            examples=examples,
            rule_format=rule_format,
        ),
        validator=validate_response,
    )

    code_chunk = find_first_code_chunk(text_resp)
    return {"cards": json.loads(code_chunk)}
