import os

from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from noobgam.llm.prompts import ANKI_CARD_CONVERSATION_TEMPLATE


def _get_openai_llm() -> ChatOpenAI:
    org = os.getenv("OPENAI_ORGANIZATION")
    api_key = os.getenv("OPENAI_API_KEY")
    if not org or not api_key:
        raise ValueError("openai misconfiguration")
    return ChatOpenAI(
        temperature=0.1,
        openai_api_key=api_key,
        model_name="gpt-4",
    )


def get_anki_chain():
    memory = ConversationBufferMemory()
    return ConversationChain(
        llm=_get_openai_llm(),
        prompt=ANKI_CARD_CONVERSATION_TEMPLATE,
        verbose=True,
        memory=memory,
    )
