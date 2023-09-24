from langchain import PromptTemplate

ANKI_FORMAT_EXPLANATION = """Anki cards are used to memorize language patterns and words.

User will ask you to modify and create cards, they follow this JSON format:
{{
  "Expression": //the expression in the original language
  "Meaning":    //the expression counterpart in english language
  "Example":    //example sentence in the original language
  "Example sentence meaning": //approximate english translation of the example sentence
  "Example sentence reading": //reading of the example sentence (for Japanese only)
}}

Example 1:
{{
  "Expression": "Leere",
  "Meaning": "empty",
  "Example": "Ich fühlte eine große Leere in mir."
}}
"""

ANKI_CARD_CONVERSATION_TEMPLATE_PROMPT = (
    """You are a helpful language learning assistant.
You know all languages to some extent and should attempt to help the human to the best of your abilities.

"""
    + ANKI_FORMAT_EXPLANATION
    + """

Current conversation:
{history}
Human: {input}
AI:"""
)

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
Target language: English
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
  "Example sentence reading": "日[に]本[ほん]で有[ゆ]名[めい]な新[しん]幹[かん]線[せん]は、東[と]京[きょう]から大[おお]阪[さか]まで早[はや]く移[い]動[どう]できます。"
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
"""

CONVERT_DIARY_TO_CARDS = """You will be given an extract from a lesson notes, your task will be to create Anki cards that will be helpful to memorize notes from the lesson. It could be grammar rules or words, your output should be the JSON formatted like the example:

Example input:
Diary notes, 9.23.2023:

sowohl ... als auch - both ... and
leere - empty

Example output:
```
[{{
  "Expression": "sowohl ... als auch",
  "Meaning": "both ... and",
  "Example sentence": "Ich mag sowohl Schokolade als auch Vanille"
}},
{{
  "Expression": "Leere",
  "Meaning": "empty",
  "Example sentence": "Nach dem Umzug fühlte das Haus sich voller Leere an."
}}]
```

Current notes:
{diary}
"""
