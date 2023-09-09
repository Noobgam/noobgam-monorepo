from langchain import PromptTemplate

ANKI_CARD_CONVERSATION_TEMPLATE_PROMPT = """You are a helpful language learning assistant.
You know all languages to some extent and should attempt to help the human to the best of your abilities.

Current conversation:
{history}
Human: {input}
AI:"""

ANKI_CARD_CONVERSATION_TEMPLATE = PromptTemplate(
    input_variables=["history", "input"],
    template=ANKI_CARD_CONVERSATION_TEMPLATE_PROMPT,
)

ANKI_CORRECT_ERRORS = """
You will be given a card that contains information, your task will be to correct existing errors in the card if there are any, or return the card as it is.
Specific errors may differ by language, but generally speaking the card should contain grammatically correct word/sentence/template for sentence.

Example input 1:
```
{{
  "russian": "Акно",
  "english": "Window"
}}
```

Example output 1:
```
{{
  "russian": "Окно",
  "english": "Window"
}}
```

Example input 2:
```
{{
  "english": "traffic lights",
  "japanese": "信号",
  "japanese_reading": "信号[しんがう]"
}}
```

Example output 2:
```
{{
  "english": "traffic lights",
  "japanese": "信号",
  "japanese_reading": "信[しん]号[ごう]"
}}
```

If the card is correct do not change anything in it, just return it unchanged.
Your current card to check for errors is
```
{payload}
```

Conform strictly to the JSON format and do not add additional comments.
"""

ANKI_CARD_GENERATE_EXAMPLE_SENTENCE = """
You will be given a card field containing information information, your task is to compose an example sentence that can be used with this word/phrase.

Example input 1:
Target language: Уnglish
```
{{
  "Meaning": "Окно",
  "Expression": "Window"
}}
```

Example output 1:
```
{{
  "Example sentence": "Close the window, it is cold outside!"
  "Example sentence meaning": "Закрой окно, снаружи холодно!",
}}
```

Example input 2:
Target language: japanese
```
{{
  "Meaning": "the Shinkansen, the bullet train"
  "Expression": "新幹線",
  "Reading": "新幹線[しんかんせん]"
}}

Example output 2:
```
{{
  "Example sentence": "日本で有名な新幹線は、東京から大阪まで早く移動できます。",
  "Example sentence meaning": "Japan's famous Shinkansen is a fast way to travel from Tokyo to Osaka.",
  "Example sentence reading": "日[に]本[ほん]で有[ゆ]名[め]な新[しん]幹[かん]線[せん]は、東[と]京[きょう]から大[おお]阪[さか]まで早[はや]く移[い]動[どう]できます。"
}}
```

Your current task:
Target language: {target_language}
```
{payload}
```

Try to come up with an easy sentence that shows a good example of how the content of this card could be used.
Today's sentence theme: {theme}
Try to think of a sentence corresponding to that theme 

For Japanese remember to add furigana to kanji for reading, do not add furigana if it is not needed
If there is a separate attribute for reading, only include furigana there, do not include furigana in example sentence 
Conform strictly to the JSON format and do not add additional comments.
"""
