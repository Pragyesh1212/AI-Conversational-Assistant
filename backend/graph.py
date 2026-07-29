from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

from backend.state import ChatState
from backend.nodes import chat_node
from backend.tools import tools
from backend.memory import memory


# Create the graph
graph = StateGraph(ChatState)

# Add nodes
graph.add_node("chat", chat_node)
graph.add_node("tools", ToolNode(tools))

# Starting point
graph.add_edge(START, "chat")

# Decide whether a tool is needed
graph.add_conditional_edges(
    "chat",
    tools_condition,
)

# After tool execution, return to chat
graph.add_edge("tools", "chat")

# Compile graph
chatbot = graph.compile(
    checkpointer=memory
)