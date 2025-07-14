import os
import asyncio
import gradio as gr
import openai
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

load_dotenv()

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global to be reused in UI function
agent = None

async def setup_agent():
    global agent
    client = MultiServerMCPClient(
        {
            "fastapi-mcp": {
                "url": "http://localhost:8000/mcp",
                "transport": "sse"
            },
            "dateserver": {
                    "command": "python",
                    "args": ["dateserver.py"],
                    "transport": "stdio"
            }
        }
    )
    tools = await client.get_tools()
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    agent = create_react_agent(model, tools)

# UI callable function
async def agent_response(user_input):
    if agent is None:
        return "Agent not ready. Please wait..."
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": user_input}]}
    )
    return response['messages'][-1].content

# Launch Gradio inside async app
async def main():
    await setup_agent()

    demo = gr.Interface(
        fn=agent_response,
        inputs=gr.Textbox(placeholder="Ask something..."),
        outputs= gr.Markdown(), # "text" for simple text output
        title="Async LangGraph Agent",
        allow_flagging="never"
    )

    # Prevent thread blocking in async env
    demo.launch(prevent_thread_lock=True)

    # Keep the app running
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
