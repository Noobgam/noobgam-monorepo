
import base64
import os.path

import anthropic

from noobgam.llm.prompt.japanese_prompts import ANKI_JAPANESE_REQUIRED_FORMAT, \
    ANKI_JAPANESE_CONVERT_DIARY_TO_CARDS_EXAMPLES, JLPT_SENSEI_CARD_PROMPT, JLPT_REFLECT_PROMPT


# we will be using claude here because gpt-4-vision is shit, just to test whether claude is better?
def convert_file_to_anki(file_path: str):
    client = anthropic.Anthropic()
    with open(file_path, 'rb') as f:
        bb = base64.b64encode(f.read()).decode('utf-8')
        system_prompt = '\n'.join([
            JLPT_SENSEI_CARD_PROMPT,
            ANKI_JAPANESE_REQUIRED_FORMAT,
            "Here are the examples of properly formatted anki cards",
            ANKI_JAPANESE_CONVERT_DIARY_TO_CARDS_EXAMPLES,
            "Tell me what is on the picture first and then output the resulting cards.",
            "Escape them with the backticks like a code block"
        ])

        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2500,
            temperature=0.3,
            system=system_prompt,
            messages=[
                {"role": "user", "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": bb,
                        }
                    },
                    {
                        "type": "text",
                        "text": f"This flashcard is named {os.path.basename(file_path)}"
                    }
                ]}
            ]
        )

        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2500,
            temperature=0.0,
            system=system_prompt,
            messages=[
                {"role": "user", "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": bb,
                        }
                    },
                    {
                        "type": "text",
                        "text": f"This flashcard is named {os.path.basename(file_path)}"
                    },
                ]},
                {
                    "role": "assistant",
                    "content": [{
                        "type": "text",
                        "text": message.content[0].text,
                    }]
                },
                {
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": JLPT_REFLECT_PROMPT,
                    }]

                }
            ]
        )
        print(message.content[0].text)


