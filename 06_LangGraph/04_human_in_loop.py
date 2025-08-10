"""
LangGraph Example: Single-File Demo with Human-in-the-Loop

Flow:
1. Start with normal AI conversation.
2. If the AI decides to call the `human_assistance` tool, execution will pause.
3. The human provides input.
4. The graph resumes from the paused point and continues the conversation.

Requirements:
- OPENAI_API_KEY and TAVILY_API_KEY must be set in the environment.
"""

import os
from typing import Annotated
from typing_extensions import TypedDict

# LangGraph core
from langgraph.graph import StateGraph, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, interrupt

# LangChain core
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch

# Optional: Graph visualization helper (custom utility)
from utils import show


# ------------------------------------------------------
# Step 1: Environment setup
# ------------------------------------------------------
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")


# ------------------------------------------------------
# Step 2: Define tools
# ------------------------------------------------------

@tool
def human_assistance(query: str) -> str:
    """
    Request assistance from a human during the AI's execution.
    This function uses LangGraph's `interrupt` to pause execution
    and wait for human input.
    """
    human_response = interrupt({"query": query})
    return human_response["data"]


# Tavily Search API as a tool
tavily_tool = TavilySearch(max_results=2)

# Combine tools
tools = [tavily_tool, human_assistance]


# ------------------------------------------------------
# Step 3: Initialize the LLM bound with tools
# ------------------------------------------------------
llm = init_chat_model("openai:gpt-4.1")
llm_with_tools = llm.bind_tools(tools)


# ------------------------------------------------------
# Step 4: Define graph state schema
# ------------------------------------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]  # Holds conversation messages


graph_builder = StateGraph(State)


# ------------------------------------------------------
# Step 5: Define graph nodes
# ------------------------------------------------------
def chatbot(state: State):
    """
    Node for the chatbot:
    - Calls the LLM (with tools bound).
    - Ensures at most one tool is called at a time (important for interrupts).
    """
    message = llm_with_tools.invoke(state["messages"])
    assert len(message.tool_calls) <= 1  # Avoid multiple tool calls in parallel
    return {"messages": [message]}


graph_builder.add_node("chatbot", chatbot)

# Node that handles tool execution
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)


# ------------------------------------------------------
# Step 6: Define graph edges
# ------------------------------------------------------
graph_builder.add_conditional_edges("chatbot", tools_condition)  # Route if tool is needed
graph_builder.add_edge("tools", "chatbot")  # After tool execution, return to chatbot
graph_builder.set_entry_point("chatbot")  # Start at chatbot


# ------------------------------------------------------
# Step 7: Compile graph with in-memory checkpoint
# ------------------------------------------------------
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)


# ------------------------------------------------------
# Step 8: (Optional) Save graph visualization
# ------------------------------------------------------
show(graph, "03_graph_with_human_in_loop.png")


# ------------------------------------------------------
# Step 9: Run a sample conversation
# ------------------------------------------------------
if __name__ == "__main__":
    # Thread/session configuration
    config = {"configurable": {"thread_id": "1"}}

    #  Initial user message
    user_input = "I need some expert guidance for building an AI agent. Could you request assistance for me?"

    # Run the graph with the first message
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )

    # Print events until we hit an interrupt
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()

    # 2 Human provides the assistance (resuming the interrupt)
    human_response = (
        "We, the experts, are here to help! "
        "We recommend using LangGraph to build your agent, "
        "as it's more reliable and extensible than simple autonomous agents."
    )

    # Command to resume the graph with the human's response
    human_command = Command(resume={"data": human_response})

    # Continue execution after human assistance
    events = graph.stream(human_command, config, stream_mode="values")

    # Print remaining messages
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()
