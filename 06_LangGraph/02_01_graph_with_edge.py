"""
conditional_branch_graph.py

A simple LangGraph example to demonstrate conditional edges and branching logic.

This graph routes the flow based on whether a given input number is even or odd.

Flow:
    START → check_number → (even_node | odd_node) → END

Nodes:
- check_number: Evaluates the number and routes accordingly.
- even_node: Handles even numbers.
- odd_node: Handles odd numbers.

Key Concepts:
- add_conditional_edges(): Used to create dynamic routing logic.
- StateGraph: Maintains the execution graph.
- START and END: Entry and exit points in the LangGraph.

Visualization:
- Uses utils.show() to render the graph as 'edge_graph.png'.

Usage:
    $ python conditional_branch_graph.py
    > User (number): 5
    It's odd!

    > User (number): 10
    It's even!

Author: Lalit Singh
"""


from langgraph.graph import StateGraph, START, END

from utils import show


# State just has a number
class State(dict):
    pass

# Create the graph
graph_builder = StateGraph(State)

# Step 1: A simple decision node
def check_number(state: State):
    return state  # just pass the state forward

graph_builder.add_node("check_number", check_number)

# Step 2: Two target nodes for branching
def even_node(state: State):
    print("It's even!")
    return state

def odd_node(state: State):
    print("It's odd!")
    return state

graph_builder.add_node("even_node", even_node)
graph_builder.add_node("odd_node", odd_node)

# Step 3: Conditional function
def route_based_on_even_or_odd(state: State):
    num = state.get("number", 0)
    if num % 2 == 0:
        return "even_node"
    else:
        return "odd_node"

# Step 4: Add conditional edge
graph_builder.add_conditional_edges(
    "check_number",
    route_based_on_even_or_odd,
    {
        "even_node": "even_node",
        "odd_node": "odd_node"
    }
)

# Step 5: Connect the flow
graph_builder.add_edge(START, "check_number")
graph_builder.add_edge("even_node", END)
graph_builder.add_edge("odd_node", END)

# Step 6: Compile and run
graph = graph_builder.compile()

# Step 7: Visualize the graph
show(graph, 'edge_graph.png')

# Run interactively
if __name__ == "__main__":
    while True:
        try:
            user_input = input("User (number): ")
            if user_input.lower() in ["quit", "exit", "q"]:
                break
            number = int(user_input)

            # Uncomment the following line to stream events, it will print visited nodes and their states
            # for event in graph.stream({"number": number}):
            #     for node, state in event.items():
            #         print(f" Visited node: {node} | State: {state}")

            # Invoke the graph with the number
            graph.invoke({"number": number})

        except Exception as e:
            print("Invalid input:", e)
