ANKI_JAPANESE_REQUIRED_FORMAT = """
Rules that are required for the answer to be correct:
1. EVERY kanji must include furigana, even easy ones. EVERY SINGLE ONE. 
2. The furigana must be enclosed in `[]` tags
3. Every kanji must be preceded space and have furigana after it
4. Hiragana and katakana do not need furigana. Never add it
"""

ANKI_JAPANESE_CONVERT_DIARY_TO_CARDS_EXAMPLES = """
[{
  "Meaning": "painful",
  "Expression": "苦[くる]しい",
  "Example sentence": "彼[かれ]は 病[びょう] 気[き]で 苦[くる]しんでいる。",
  "Example sentence meaning": "He is suffering from illness."
},
{
  "Meaning": "traffic lights",
  "Expression": "信[しん] 号[ごう]",
  "Example sentence": "信[しん] 号[ごう]が 青[あお]に 変[か]わった",
  "Example sentence meaning": "The traffic light changed to green"
}]
"""

JLPT_SENSEI_CARD_PROMPT = """
You are a useful language assistant. Your job is to extract text from the pictures and convert them to Anki (Spaced Repetition Software) cards.
You can create multiple cards from one picture if you deem fit, especially if the usage is different for specific cases.
For example for conjugation of verbs to te-form you could create multiple cards for all scenarios (読む->読んで,する->して etc.)

You are encouraged to create your own examples even if they are not present specifically on the card.
"""

JLPT_REFLECT_PROMPT = """
Can you reflect on your answer and make sure that:
1. All of the example sentences are present
2. Furigana/Katakana has no furigana attached to it and all of the kanji do
3. All of the rules from the image have at least one corresponding card created
4. Additional spaces between hiragana are not present. They should only be preceding the Kanji, not Kanas.

Format the response the same way as before, with an explanation of the mistakes done if any and the list of cards escaped with backticks 
"""