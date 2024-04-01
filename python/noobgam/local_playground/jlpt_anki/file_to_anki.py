import base64
import json
import logging
import os.path
import typing

import anthropic

from noobgam.handlers.anki_convert_diary import find_first_code_chunk
from noobgam.llm.prompt.japanese_prompts import (
    ANKI_JAPANESE_REQUIRED_FORMAT,
    JLPT_SENSEI_CARD_PROMPT,
    JLPT_REFLECT_PROMPT,
    JLPT_SENSEI_CARD_EXAMPLES,
    JLPT_SENSEI_HUMAN_MESSAGE,
    JLPT_SENSEI_CORRECT_CARDS_PROMPT,
)

EXAMPLE_CLAUDE_RESPONSE = """
Thank you for the feedback. I have reviewed the answer and made the necessary corrections. Here are the updated Anki cards:

```
[{
  "Meaning": "to be (am, is, are, were, used to)",
  "Expression": "だ / です",
  "Usage": "Noun + だ / です",
  "Example sentence": "私[わたし]の 名[な] 前[まえ]は クリス です。",
  "Example sentence meaning": "My name is Chris."
},
{
  "Meaning": "to be (am, is, are, were, used to)",
  "Expression": "だった / でした",
  "Usage": "Noun + だった / でした",
  "Example sentence": "彼[かれ]は 学[がく] 生[せい]でした。",
  "Example sentence meaning": "He was a student."
},
{
  "Meaning": "to be (am, is, are, were, used to)",
  "Expression": "ではない",
  "Usage": "Noun + ではない",
  "Example sentence": "これは 私[わたし]の 本[ほん]ではない。",
  "Example sentence meaning": "This is not my book."
},
{
  "Meaning": "to be (am, is, are, were, used to)",
  "Expression": "ではなかった / ではありませんでした",
  "Usage": "Noun + ではなかった / ではありませんでした",
  "Example sentence": "昨日[きのう]の 天[てん] 気[き]は 良[よ]くありませんでした。",
  "Example sentence meaning": "The weather yesterday was not good."
},
{
  "Meaning": "to be (am, is, are, were, used to)",
  "Expression": "だ / です",
  "Usage": "な-adjective + だ / です",
  "Example sentence": "日[に] 本[ほん]の 文[ぶん] 化[か]が 好[す]きです。",
  "Example sentence meaning": "I like Japanese culture."
}]
```

Corrections made:
1. Added example sentences for all usage cases from the image and one additional example.
2. Removed furigana from hiragana and katakana while ensuring all kanji have furigana.
3. Created cards for all usage rules from the image.
4. Removed extra spaces between hiragana.
5. Ensured the usage in each card matches the example sentence.
6. Corrected grammatical mistakes in the example sentences and their explanations.
"""

client = anthropic.Anthropic()

jlpt_sensei_card_schema = {
    "type": "object",
    "properties": {
        "Meaning": {"type": "string"},
        "Expression": {"type": "string"},
        "Usage": {"type": "string"},
        "Example sentence": {"type": "string"},
        "Example sentence meaning": {"type": "string"},
    },
    "required": [
        "Meaning",
        "Expression",
        "Usage",
        "Example sentence",
        "Example sentence meaning",
    ],
}

claude_response_schema = {"type": "array", "items": jlpt_sensei_card_schema}

jlpt_sensei_system_prompt = "\n".join(
    [
        JLPT_SENSEI_CARD_PROMPT,
        ANKI_JAPANESE_REQUIRED_FORMAT,
        "Here are the examples of properly formatted anki cards",
        JLPT_SENSEI_CARD_EXAMPLES,
    ]
)


def get_refined_response_from_claude(image_content: str, file_name: str):
    jlpt_messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_content,
                    },
                },
                {
                    "type": "text",
                    "text": JLPT_SENSEI_HUMAN_MESSAGE.format(file_name=file_name),
                },
            ],
        }
    ]

    logging.info("Prompting claude")
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2500,
        temperature=0.3,
        system=jlpt_sensei_system_prompt,
        messages=jlpt_messages,
    )

    logging.info("Got original resp from claude")

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2500,
        temperature=0.0,
        system=jlpt_sensei_system_prompt,
        messages=jlpt_messages
        + [
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": message.content[0].text,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": JLPT_REFLECT_PROMPT,
                    }
                ],
            },
        ],
    )
    logging.info("Got refined response from claude")
    return message.content[0].text


def validate_claude_response(response: str) -> [typing.Any, typing.Optional[str]]:
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError

    try:
        code_chunk = find_first_code_chunk(response)
        if not code_chunk:
            raise ValidationError(
                message="No valid code chunk found. Make sure the response is valid"
            )
        thing = json.loads(code_chunk)
        validate(instance=json.loads(code_chunk), schema=claude_response_schema)
        return thing, None
    except ValidationError as e:
        return None, str(e)


# we will be using claude here because gpt-4-vision is shit, just to test whether claude is better?
def convert_file_to_anki(file_path: str):
    with open(file_path, "rb") as f:
        bb = base64.b64encode(f.read()).decode("utf-8")
    claude_resp = get_refined_response_from_claude(
        image_content=bb, file_name=os.path.basename(file_path)
    )
    err: typing.Optional[str] = "No attempts to fix were done"
    for i in range(3):
        r, err = validate_claude_response(claude_resp)
        if err is None:
            return r
        logging.info(f"Trying to correct {err}")
        new_resp = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2500,
            temperature=0.0,
            system=jlpt_sensei_system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": JLPT_SENSEI_CORRECT_CARDS_PROMPT.format(
                                llm_answer=claude_resp,
                                validation_error=err,
                            ),
                        }
                    ],
                }
            ],
        )
        claude_resp = new_resp.content[0].text
        logging.info(f"Got new response from claude")
    raise Exception(err)
