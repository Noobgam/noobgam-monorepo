import os

from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import SystemMessage

from noobgam.llm.chain import ConversationHistoryChain
from noobgam.llm.prompt.prompts import ANKI_SYSTEM_PROMPT


def get_anki_chain(added_prompt: str = "") -> ConversationHistoryChain:
    api_key = os.environ["OPENROUTER_API_KEY"]
    common_params = {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": api_key,
        "temperature": 1,
    }
    llm = ChatOpenAI(
        **common_params,
        model="anthropic/claude-sonnet-4",
    )
    chat_history = InMemoryChatMessageHistory(messages=[
        SystemMessage(content=ANKI_SYSTEM_PROMPT + added_prompt),
    ])
    return ConversationHistoryChain(
        chat_history=chat_history,
        llm=llm
    )
