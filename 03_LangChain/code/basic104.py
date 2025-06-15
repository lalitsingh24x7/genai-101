"""
basic104.py

This script demonstrates how to use LangChain's ConversationBufferMemory with LLMChain
to maintain conversation context across multiple prompts. It shows how memory enables
the model to use previous conversation history for more context-aware responses.

Dependencies:
    - python-dotenv
    - langchain_openai

Usage:
    Ensure a valid OpenAI API key is set in the .env file as OPENAI_API_KEY.
    Run the script to see how conversation memory affects the model's responses.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from pprint import pprint

# Load environment variables from .env file (for API keys, etc.)
load_dotenv()

# Initialize the OpenAI chat model with specified parameters
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# Create a conversation memory object to store chat history
memory = ConversationBufferMemory(
    memory_key="chat_history",  # Key for storing conversation history
    input_key="term"            # Input key to track in memory
)

# Define the first prompt template for a SWOT analysis
define_format = "Do a {lines} SWAT analys for the {term}"
define_prompt = PromptTemplate(
    input_variables=["term", "lines"],
    template=define_format
)

# Create the first conversation chain with memory
conversion_chain = LLMChain(
    llm=llm,
    prompt=define_prompt,
    memory=memory
)

# Define the second prompt template that uses chat history
define_format_2 = (
    "Conversation so far:\n{chat_history}\n"
    "Now, which sector will be the most benefitted by {term}? "
    "I need a list of companies in that sector, based on the country or context above."
)

"""
The memory object will automatically fill in the {chat_history} variable in your prompt template using the conversation so far.
"""
define_prompt_2 = PromptTemplate(
    input_variables=["term", "chat_history"],
    template=define_format_2
)

# Create the second conversation chain, also using memory
conversion_chain_2 = LLMChain(
    llm=llm,
    prompt=define_prompt_2,
    memory=memory
)

print("-------First Interaction-------")
# First interaction: perform a SWOT analysis for 'indian economy'
response1 = conversion_chain.invoke(
    {
        "term": "indian economy",
        "lines": 3
    }
)
print(response1["text"])

print("-------Second Interaction-------")
# Second interaction: ask which sector will benefit, using conversation memory for context
response2 = conversion_chain_2.invoke(
    {
        "term": "health sector"
    }
)
print(response2["text"])

print("----------Memory after first interaction-----------")
# Print the current state of the conversation memory
pprint(memory.load_memory_variables({}))