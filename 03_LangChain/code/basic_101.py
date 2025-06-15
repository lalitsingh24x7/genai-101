"""
basic_101.py

This script demonstrates a basic usage of the LangChain library with OpenAI's GPT-4o-mini model.
It loads environment variables (such as API keys) from a .env file, initializes a chat-based language model,
sends a simple prompt ("What is Math in one sentence?"), and prints the model's response.

Dependencies:
    - python-dotenv
    - langchain_openai

Usage:
    Ensure a valid OpenAI API key is set in the .env file as OPENAI_API_KEY.
    Run the script to see the model's response to the prompt.

"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file (for API keys, etc.)
load_dotenv()

# Initialize the OpenAI chat model with specified parameters
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# Define a simple prompt to send to the language model
basic_prompt = "What is Math in one sentence?"

# Invoke the language model with the prompt and get the response
response = llm.invoke(basic_prompt)

# Print the prompt and the model's response
print("----------------------------------------\n")
print(f"Prompt: {basic_prompt}")
print(f"Response: {response.content}")
print("----------------------------------------\n")