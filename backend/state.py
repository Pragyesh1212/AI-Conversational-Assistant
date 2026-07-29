from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ChatState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    messages: Annotated[list[BaseMessage], add_messages]