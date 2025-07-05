"""
client.py

A command-line client for interacting with MCP (Modular Command Platform) servers using LangChain and OpenAI.

Features:
    - Connects to two MCP servers: a math server (local, stdio) and a to-do server (HTTP).
    - Uses a React-style agent to process user requests and route them to the appropriate tool.
    - Continuously prompts the user for input and displays the agent's response.
    - Exits gracefully when the user types 'exit'.

Usage:
    python client.py

"""

import os
import asyncio

import openai
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio"
            },
            "my_todo": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http"
            }
        }
    )
    
    tools = await client.get_tools()
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    agent = create_react_agent(
        model, tools
    )

    while True:
        user_input = input("Enter your request (type 'exit' to quit): ")
        if user_input.strip().lower() == "exit":
            print("Exiting...")
            break
        todo_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        print("Todo's response:", todo_response['messages'][-1].content)

asyncio.run(main())