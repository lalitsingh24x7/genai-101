"""
basic102.py

This script demonstrates how to use LangChain's PromptTemplate and chaining with the OpenAI GPT-4o-mini model.
It loads environment variables, initializes the language model, defines a prompt template for a SWOT analysis,
and uses the modern chaining syntax to generate and print a concise SWOT analysis for a given term.

Dependencies:
    - python-dotenv
    - langchain_openai

Usage:
    Ensure a valid OpenAI API key is set in the .env file as OPENAI_API_KEY.
    Run the script to see the model's response to the SWOT analysis prompt.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables from .env file (for API keys, etc.)
load_dotenv()

# Initialize the OpenAI chat model with specified parameters
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
print("LLM Initialized.")

# Define a prompt template for a SWOT analysis with placeholders for 'term' and 'lines'
deinfe_template = "Do a {lines} liner SWOT analysis for the term: {term}"
define_prompt = PromptTemplate(input_variables=["term", "lines"], template=deinfe_template)

# Create a chain by piping the prompt template into the language model (modern chaining syntax)
# define_chain = LLMChain(llm=llm, prompt=define_prompt) # This is the old way of chaining
define_chain = define_prompt | llm  # (| is bitwise OR operator for chaining)

# Set the term and number of lines for the SWOT analysis
term_to_define = "Large Language Model"
lines_to_generate = 1

# Invoke the chain with the specified inputs and get the response
definition = define_chain.invoke({"term": term_to_define, "lines": lines_to_generate})

# Print the results
print("-----------------------------------------\n")
print(f"Defining '{term_to_define}' in {lines_to_generate} lines:")
print(definition.content)
print("-----------------------------------------\n")