import os

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import SystemMessage

from noobgam.llm.chain import ConversationHistoryChain
from noobgam.llm.prompt.prompts import ANKI_SYSTEM_PROMPT


def _get_openai_llm() -> ChatOpenAI:
    org = os.getenv("OPENAI_ORGANIZATION")
    api_key = os.getenv("OPENAI_API_KEY")
    if not org or not api_key:
        raise ValueError("openai misconfiguration")
    return ChatOpenAI(
        temperature=0.1,
        openai_api_key=api_key,
        model_name="gpt-4o-2024-08-06",
    )


def _get_anthropic_llm() -> ChatAnthropic:
    return ChatAnthropic(
        temperature=0.1,
        model_name="claude-3-5-sonnet-20241022",
        max_tokens_to_sample=4096,
    )


def get_anki_chain(added_prompt: str = "") -> ConversationHistoryChain:
    llm = _get_anthropic_llm()
    chat_history = InMemoryChatMessageHistory(messages=[
        SystemMessage(content=ANKI_SYSTEM_PROMPT + added_prompt),
    ])
    return ConversationHistoryChain(
        chat_history=chat_history,
        llm=llm
    )
