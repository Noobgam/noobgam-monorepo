import json

from noobgam.handlers.anki_compose_sentence import GenerateCardInput, handler

if __name__ == "__main__":
    raw = json.loads(
        """
    {
    "target_language": "Japanese",
    "card_fields": {
        "Expression": "高校",
        "Meaning": "high school",
        "Reading": "高校[こうこう]",
        "Lesson Number": "",
        "Example sentence": "",
        "Example sentence meaning": "",
        "Example sentence reading": ""
    },
    "theme": "Jojo's bizarre adventures"
}"""
    )
    print(handler(GenerateCardInput(**raw)))
