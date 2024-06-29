from langchain.prompts import PromptTemplate

ANKI_FORMAT_EXPLANATION = """Anki cards are used to memorize language patterns and words.

User will ask you to modify and create cards, they follow this JSON format:
{{
  "Expression": //the expression in the original language
  "Meaning":    //the expression counterpart in english language
  "Example sentence":    //example sentence in the original language, in case of japanese with furigana
  "Example sentence meaning": //approximate english translation of the example sentence
}}

Example 1:
{{
  "Expression": "くそ",
  "Meaning": "damn",
  "Example sentence": "くそ、 遅[おく]れた！",
  "Example sentence meaning": "Damn, I'm late!"
}}
"""

ANKI_CARD_CONVERSATION_TEMPLATE_PROMPT = (
    """You are a helpful language learning assistant.
    You know all languages and should attempt to help the human to the best of your abilities.
    
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

ANKI_SYSTEM_PROMPT = f"""\
You are a helpful language learning assistant.
You know all languages and should attempt to help the human to the best of your abilities.

{ANKI_FORMAT_EXPLANATION}
"""

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

{examples}

{rule_format}

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

CONVERT_DIARY_TO_CARDS_TEMPLATE = """You will be given an extract from a lesson notes, your task will be to create Anki cards that will be helpful to memorize notes from the lesson. It could be grammar rules or words, your output should be the JSON formatted like the example:

Example output:
```
{examples}
```

{rule_format}

Try to fill the gaps and fix any mistakes inferring context from sentences around and do not skip cards if there is something you can create.
Do not forget about reading

Create as many cards as you can.
Current note is supposed to be a note about {language}, if there are placeholders - replace them with {language} words.
If current diary notes seem to follow some grammatical concept include it in sentences.

Current notes:
{diary}
"""
