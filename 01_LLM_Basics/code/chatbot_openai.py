
"""
This module demonstrates how to create a simple chatbot using OpenAI's API.

Functions:
    chat_with_gpt(prompt: str) -> str:
        Sends a user prompt to the OpenAI API and returns the chatbot's response.

Usage:
    1. Set your OpenAI API key as an environment variable named "OPENAI_API_KEY".
    2. Run the script using the command:
        python chatbot_openai.py
    3. Interact with the chatbot by typing your messages. Type 'exit' or 'quit' to end the session.

Example:
    Me: Hello, how are you?
    AI: I'm just a program, but I'm here to help! How can I assist you today?
This module demonstrates how to create a simple chatbot using OpenAI's API.

"""

import openai
import os

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=api_key)

# Function to chat with GPT
def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Change to "gpt-4o-mini"  or others
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

print("\n AI Chatbot with OPENAI API! Type 'exit' to quit.\n")

# Test the chatbot
while True:
    user_input = input("Me: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    print("\n")
    response = chat_with_gpt(user_input)
    print(f"AI: {response}\n")
