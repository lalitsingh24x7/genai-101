"""
tool_enabled_chatbot_graph.py

LangGraph implementation of a conversational chatbot integrated with external tools.

This example uses:
- OpenAI's GPT model (`gpt-4.1`) for generating assistant responses.
- Tavily (via `langchain_tavily`) for real-time web search functionality.
- LangGraph's `ToolNode` and `tools_condition` for auto-invoking tools when needed.

Flow:
    START → chatbot
               ├── tool_calls? → tools → chatbot → ...
               └── no tool_calls → END (implicit)

Key Components:
- `State`: Holds the list of messages in the conversation.
- `chatbot`: LLM node that responds to user input and may trigger tool calls.
- `ToolNode`: Executes external tools like TavilySearch when needed.
- `tools_condition`: Built-in routing logic to detect tool use from LLM output.

Visualization:
- Uses `utils.show(graph, filename)` to render the graph as an image.

Usage:
    $ python tool_enabled_chatbot_graph.py
    > User: What is the capital of France?
    > Assistant: The capital of France is Paris.

Environment Variables Required:
- `OPENAI_API_KEY`: Your OpenAI key for GPT models.
- `TAVILY_API_KEY`: Your Tavily key for search tool integration.

Author: Lalit Singh
"""


import os
from typing import Annotated
from typing_extensions import TypedDict

from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage
from langchain.chat_models import init_chat_model

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from utils import show  # helper function to visualize the graph

# ------------------------------------------------------
#  Step 1: Set up environment variables for API keys
# ------------------------------------------------------
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')

# ------------------------------------------------------
#  Step 2: Initialize LLM and tools
# ------------------------------------------------------
llm = init_chat_model("openai:gpt-4.1")  # LLM interface
tool = TavilySearch(max_results=2)       # Search tool
tools = [tool]

# Bind tools to the LLM
llm_with_tools = llm.bind_tools(tools)

# ------------------------------------------------------
#  Step 3: Define graph state schema
# ------------------------------------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]  # Tracks chat history

# Initialize the graph builder with state
graph_builder = StateGraph(State)

# ------------------------------------------------------
#  Step 4: Define and add nodes to the graph
# ------------------------------------------------------

# LLM node: handles user input and generates assistant response
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

# Tool node: runs tools if tool_calls exist in the LLM response
tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

# ------------------------------------------------------
#  Step 5: Define flow using conditional edges
# ------------------------------------------------------

# Conditional edge:
# If tool_calls are found → go to tool node,
# else → automatically go to END (handled by `tools_condition`)
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

# Once tools are executed, return to chatbot to continue the loop
graph_builder.add_edge("tools", "chatbot")

# Entry point of the graph
graph_builder.add_edge(START, "chatbot")

# ------------------------------------------------------
#  Step 6: Compile and visualize the graph
# ------------------------------------------------------

graph = graph_builder.compile()

# Save PNG visualization of the graph (optional)
show(graph, "02_graph.png")

# ------------------------------------------------------
#  Step 7: Define streaming chat loop
# ------------------------------------------------------

def stream_graph_updates(user_input: str):
    """
    Streams the assistant response by passing the user's input
    into the compiled LangGraph execution.
    """
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

# ------------------------------------------------------
#  Step 8: CLI loop for interaction
# ------------------------------------------------------

if __name__ == "__main__":
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            stream_graph_updates(user_input)

        except:
            # fallback if input() is not available (e.g., in notebook)
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break
