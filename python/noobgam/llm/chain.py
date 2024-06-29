from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, BaseMessage
from pydantic.v1 import BaseModel


class ConversationHistoryChain(BaseModel):
    chat_history: InMemoryChatMessageHistory
    llm: BaseChatModel

    def invoke(self, message: HumanMessage | str) -> BaseMessage:
        if isinstance(message, str):
            message = HumanMessage(content=message)
        resp = self.llm.invoke([*self.chat_history.messages, message])
        self.chat_history.add_messages([message, resp])
        return resp

    def invokes(self, message: HumanMessage | str) -> str:
        return self.invoke(message).content