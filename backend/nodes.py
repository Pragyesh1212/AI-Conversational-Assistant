from backend.config import llm
from backend.tools import tools

# Bind all available tools to the LLM
llm_with_tools = llm.bind_tools(tools)


def chat_node(state):
    """
    Main chatbot node.
    Receives the conversation state,
    invokes the LLM,
    and returns the AI response.
    """

    messages = state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }