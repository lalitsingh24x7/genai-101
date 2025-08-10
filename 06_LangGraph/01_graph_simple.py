"""
simple_chatbot_graph.py

A minimal LangGraph implementation of a chatbot workflow using OpenAI's GPT model.
This script demonstrates how to:

1. Define a simple conversational state structure.
2. Add an LLM-based chatbot node.
3. Create a graph with a basic START → chatbot → END flow.
4. Compile and visualize the LangGraph.
5. Stream user input and display assistant responses in a CLI loop.

Dependencies:
- langchain
- langgraph
- OpenAI-compatible API key (OPENAI_API_KEY env var)
- utils.show() for graph visualization

Usage:
    $ python simple_chatbot_graph.py
    > User: Hello
    > Assistant: Hi! How can I help you today?

Author: Lalit Singh
"""

import os
from typing import Annotated
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from utils import show  # Helper to visualize the graph

# ------------------------------------------------------
#  Step 0: Set environment variables
# ------------------------------------------------------
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# ------------------------------------------------------
#  Step 1: Define the conversation state structure
# ------------------------------------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ------------------------------------------------------
#  Step 2: Initialize the graph with state
# ------------------------------------------------------
graph = StateGraph(State)

# ------------------------------------------------------
#  Step 3: Add chatbot node using LLM
# ------------------------------------------------------
llm = init_chat_model("openai:gpt-4.1")

def chatbot(state: State):
    """
    Main chatbot logic that receives messages
    and invokes the LLM to generate a response.
    """
    return {
        "messages": [llm.invoke(state["messages"])]
    }

graph.add_node("chatbot", chatbot)

# ------------------------------------------------------
#  Step 4: Define the execution flow
# ------------------------------------------------------
graph.add_edge(START, "chatbot")  # Start → chatbot
graph.add_edge("chatbot", END)    # chatbot → End

# ------------------------------------------------------
#  Step 5: Compile the graph
# ------------------------------------------------------
app = graph.compile()

# ------------------------------------------------------
#  Step 6: Visualize the graph
# ------------------------------------------------------
show(app, "simple_graph.png")

# ------------------------------------------------------
#  Step 7: Streaming logic to process conversation
# ------------------------------------------------------
def stream_graph_updates(user_input: str):
    """
    Handles streaming updates by invoking the graph
    and printing the assistant's response.
    """
    for event in app.stream({
        "messages": [{"role": "user", "content": user_input}]
    }):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

# ------------------------------------------------------
#  Step 8: Interactive command-line loop
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
            # fallback for notebook or input-less environments
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break
