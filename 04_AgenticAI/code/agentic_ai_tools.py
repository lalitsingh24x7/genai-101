"""
agentic_ai_tools.py

This script demonstrates how to build an agentic AI chatbot using LangChain with multiple tools:
- DuckDuckGo search
- Wikipedia lookup
- Math calculator
- Python code executor

The agent uses OpenAI's GPT-4o-mini model and maintains conversation memory for context-aware responses.
You can ask general questions, request calculations, or run Python code interactively.

Dependencies:
    - langchain_openai
    - langchain
    - langchain_community
    - duckduckgo-search
    - wikipedia


Usage:
    Ensure a valid OpenAI API key is set in the .env file as OPENAI_API_KEY.
    Run the script and interact with the agent via the terminal.
"""

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.memory import ConversationBufferMemory
import math

# Initialize DuckDuckGo search tool for web queries
search_tool = DuckDuckGoSearchRun()

# Initialize Wikipedia retriever and tool for Wikipedia queries
wiki_retriver = WikipediaAPIWrapper()
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_retriver)

# Safe math evaluation function, only exposes 'math' module
def safe_eval(expression: str):
    return eval(
        expression,
        {"__builtins__": None},
        {"math": math}
    )

# Tool for mathematical calculations
math_tool = Tool(
    name="calculator",
    func=safe_eval,
    description="Use this tool for math."
)

# Function to safely execute Python code and return 'result' variable if present
def run_python_code(code):
    exec_globals = {}
    exec(code, exec_globals)
    return exec_globals.get("result", "Code executed successfully, but no result vairale found.")

# Tool for running Python code snippets
python_executor = Tool(
    name="python_code_runner",
    func=run_python_code,
    description="To run python code."
)

# List of all tools available to the agent
tools = [search_tool, wiki_tool, math_tool, python_executor]

# Initialize the OpenAI chat model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Conversation memory to maintain chat history for context
memory = ConversationBufferMemory(return_messages=True)

# Initialize the agent with tools, LLM, agent type, and memory
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory
)

# Main interactive loop for user queries
while True:
    query = input("Ask: ")
    if query.lower() in ["exit", "quit"]:
        print("byyy")
        break
    # Pass user input to the agent and print the response
    response = agent.invoke(
        {"input": query}
    )
    print("\n AI:", response["output"])


"""
Example usage:

Ask: sum of 120 and 20
AI: The sum of 120 and 20 is 140.

Ask: who is Elon musk
AI: Elon Reeve Musk, born on June 28, 1971,
is a prominent businessman known for his leadership roles in several high-profile companies, 
including Tesla, SpaceX, and X (formerly Twitter). He has been recognized as one of 
the wealthiest individuals in the world, with an estimated net worth of approximately $424.7 billion as of May 2025.

Ask: run this python code : sum(range(3))  
AI: The result of the code `sum(range(3))` is 3.

"""