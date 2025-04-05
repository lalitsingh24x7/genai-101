import openai
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Define zero-shot prompts with diverse examples
prompts = [
    "Translate 'How are you today?' into French.",
    "What is the capital of Japan?",
    "Summarize this paragraph: Artificial intelligence is transforming industries by automating tasks, improving efficiency, and enabling new capabilities.",
    "Classify the sentiment of this sentence: 'I absolutely love the new design of your website!'",
    "Extract names from this text: 'Alice and Bob are planning to meet Charlie at the park tomorrow.'"
]

# Function to call OpenAI API and get a response
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Change to "gpt-4" if available
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Execute all prompts and display responses
for i, prompt in enumerate(prompts, 1):
    print(f"Prompt {i}: {prompt}")
    print("Response:", get_response(prompt))
    print("-" * 50)