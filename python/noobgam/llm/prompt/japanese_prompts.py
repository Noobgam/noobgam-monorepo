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

JLPT_SENSEI_CARD_EXAMPLES = """
[{
  "Meaning": "while; during~ something happened",
  "Expression": "間[あいだ]に",
  "Usage": "Verb (casual, non-past) + 間に",
  "Example sentence": "彼[かれ]を 待[ま]っている 間[あいだ]にYouTubeを 見[み]ていた。",
  "Example sentence meaning": "I watched YouTube while I waited for him."
},
{
  "Meaning": "while; during~ something happened",
  "Expression": "間[あいだ]に",
  "Usage": "Noun + の + 間に",
  "Example sentence": "夜[よる]の 間[あいだ]に 火[か] 事[じ]が 起[お]こった。",
  "Example sentence meaning": "A fire broke out during the night."
},
{
  "Meaning": "while; during~ something happened",
  "Expression": "間[あいだ]に",
  "Usage": "な-adjective + な + 間に",
  "Example sentence": "元[げん] 気[き]な 間[あいだ]に 旅[りょ] 行[こう]に 行[い]った。",
  "Example sentence meaning": "I went on a trip while I was healthy."
},
{
  "Meaning": "while; during~ something happened",
  "Expression": "間[あいだ]に",
  "Usage": "い-adjective + 間に",
  "Example sentence": "若[わか]い 間[あいだ]にたくさん 勉[べん] 強[きょう]した。",
  "Example sentence meaning": "I studied a lot while I was young."
}]
"""

JLPT_SENSEI_CARD_PROMPT = """
You are a useful language assistant. Your job is to extract text from the pictures and convert them to Anki (Spaced Repetition Software) cards.
You can create multiple cards from one picture if you deem fit, especially if the usage is different for specific cases.
For example for conjugation of verbs to te-form you could create multiple cards for all scenarios (読む->読んで,する->して etc.)
You are allowed to combine furigana for consecutive kanji. For example: 勝手[かって].

You are encouraged to create your own examples even if they are not present specifically on the card, but all the card examples should be present.
"""

JLPT_SENSEI_HUMAN_MESSAGE = f"""
This flashcard is named {{file_name}}
Tell me what is on the picture first and then output the resulting cards.
Escape them with the backticks like a code block
"""

JLPT_REFLECT_PROMPT = """
Can you reflect on your answer and make sure that:
1. All of the example sentences from the image are present and at least one additional is added.
2. Furigana/Katakana has no furigana attached to it and all of the kanji do
3. All of the rules from the image have at least one corresponding card created
4. Additional spaces between hiragana are not present. They should only be preceding the Kanji, not Kanas.
5. Ensure that usage of the card is correct and contains the expression in the same form as example sentence does.
6. The sentences do not contain grammatical mistakes neither in the original, nor in the explanation.

Format the response the same way as before, with an explanation of the mistakes done if any and the list of cards escaped with backticks 
"""

JLPT_SENSEI_CORRECT_CARDS_PROMPT = f"""
Previously you were asked to generate the following:
<original_prompt>
{JLPT_SENSEI_CARD_PROMPT}
</original_prompt>
and then reflect on your answer by
<reflection_prompt>
{JLPT_REFLECT_PROMPT}
</reflection_prompt>
the answer you came up with is
<claude_answer>
{{llm_answer}}
</claude_answer>
It was incorrect because of the following error:
<error>
{{validation_error}}
</error>

Can you attempt to fix it and respond in the same format?
"""
