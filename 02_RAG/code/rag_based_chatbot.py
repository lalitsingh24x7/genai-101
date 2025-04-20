"""
Retrieval-Augmented Generation (RAG) Chatbot
This code demonstrates how to create a simple RAG-based chatbot using LangChain and OpenAI's GPT-3.5-turbo model.
It uses a small knowledge base and retrieves relevant information to generate responses.

Context:
- Vector: A vector is a mathematical representation of data in a multi-dimensional space. example: [[1, 2, 3], [1, 2, 3]]
- Embeddings: Vector representations of words.
- OpenAIEmbeddings: OpenAIEmbeddings is a class that generates embeddings using OpenAI's API.
- FAISS: FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors.
- CharacterTextSplitter: A class that splits text into smaller chunks based on character count. example: "Hello World" -> ["Hello", "World"]
- RetrievalQA: A class that combines a retriever and a language model to answer questions based on retrieved documents.
"""


from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import openai
import os

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Sample Knowledge Base
documents = [
    "Lalit Singh is a software engineer, who has good experince in Software Development.",
    "Core skils of Lalit Singh are Python, Data Engineering, and AI.",
    "Lalit Singh lives in Delhi, India.",
    "Lalit Singh Lover Driving car."
]

# Convert text into vector embeddings
text_splitter = CharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
    )

split_docs = text_splitter.create_documents(documents)

embeddings = OpenAIEmbeddings()
vector_db = FAISS.from_documents(
    split_docs,
    embeddings
    ) # here we are using FAISS as a vector store to store the embeddings

# Create RAG-based chatbot
retriever = vector_db.as_retriever()

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo"),
    retriever=retriever
    )

print("\n AI Chatbot with RAG! Type 'exit' to quit.\n")
# Enter an infinite loop to interact with the user
while True:
    user_input = input("Me: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    # Process the user's input through the RetrievalQA chain to generate a response
    response = qa_chain.run(user_input)
    print(f"AI: {response}\n")



