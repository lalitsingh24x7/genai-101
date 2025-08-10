import os
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch

from utils import show

# ------------------------------------------------------
#  Step 1: Environment setup
# ------------------------------------------------------
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# ------------------------------------------------------
#  Step 2: LLM and Tool initialization
# ------------------------------------------------------
llm = init_chat_model("openai:gpt-4.1")
tool = TavilySearch(max_results=2)
tools = [tool]
llm_with_tool = llm.bind_tools(tools)

# ------------------------------------------------------
#  Step 3: Define graph state schema
# ------------------------------------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# ------------------------------------------------------
#  Step 4: Define nodes
# ------------------------------------------------------
def chatbot(state: State):
    """Main chatbot node that uses the LLM (with tools) to process messages."""
    return {
        "messages": [llm_with_tool.invoke(state["messages"])]
    }

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

# ------------------------------------------------------
#  Step 5: Define edges
# ------------------------------------------------------
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")

# ------------------------------------------------------
#  Step 6: Compile graph with memory
# ------------------------------------------------------
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# ------------------------------------------------------
#  Step 7: Visualization (optional)
# ------------------------------------------------------
show(graph, "03_graph_with_memory.png")

# ------------------------------------------------------
#  Step 8: Streaming helper
# ------------------------------------------------------
def stream_graph_update(user_input: str, config: dict):
    """Stream updates from the graph given a user input."""
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )
    for event in events:
        event["messages"][-1].pretty_print()

# ------------------------------------------------------
#  Step 9: Interactive CLI loop
# ------------------------------------------------------
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1"}}
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_update(user_input, config)
        except Exception as e:
            print(f"Error: {e}")
