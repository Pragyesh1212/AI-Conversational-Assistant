from langchain_core.messages import SystemMessage

from backend.config import llm
from backend.tools import tools


SYSTEM_PROMPT = """
You are a helpful AI Assistant.

Follow these rules:

1. Answer the user's question directly and naturally.
2. When you use a tool, NEVER expose the raw tool output, JSON, API response,
   or internal tool data to the user.
3. Interpret tool results and convert them into a clean, human-readable answer.
4. Use Markdown formatting when it improves readability.
5. Use headings, bullet points, and bold labels for structured information.
6. For stock-price questions, clearly present the company/ticker, current price,
   change, percentage change, previous close, day high, day low, volume,
   and trading date when those fields are available.
7. If a tool returns an error, explain the error clearly and briefly.
8. Do not mention internal tools, LangGraph, tool calls, APIs, or implementation
   details unless the user explicitly asks about them.
9. Keep simple answers concise. Give more detail only when the user asks for it.
10. Do not repeat information unnecessarily.
"""

llm_with_tools = llm.bind_tools(tools)


def chat_node(state):
    """
    Main chatbot node.

    The system prompt is included on every invocation so that both normal
    responses and post-tool responses follow the same formatting rules.
    """

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }
