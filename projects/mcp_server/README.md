# 🧪 Model Context Protocol (MCP) Demo with FastAPI

This project demonstrates the integration of **Model Context Protocol (MCP)** using **FastAPI** and other components for simulating a modular, multi-client AI service ecosystem.

## 🔧 Project Overview

This demo setup includes multiple services working together to illustrate how the **Model Context Protocol** can be used for model-to-model and client-server interactions. Below are the key components and their respective endpoints.

---

## 🔌 Available Services & URLs

### 🚀 FastAPI MCP Server

The main service exposing the MCP endpoint.

* **URL**: [`http://0.0.0.0:8080`](http://0.0.0.0:8080)

### 📡 MCP Core Server

A standalone MCP server that communicates using the protocol.

* **URL**: [`http://0.0.0.0:8000`](http://0.0.0.0:8000)

### 💬 Chat UI (Gradio)

A simple conversational interface to test communication with the MCP endpoint.

* **URL**: [`http://127.0.0.1:7860`](http://127.0.0.1:7860)

### ✅ TODO UI (Streamlit)

A demo Streamlit-based frontend (e.g., task list) to interact with or simulate use cases.

* **URL**: [`http://localhost:8501`](http://localhost:8501)

---

## 🧠 About Model Context Protocol (MCP)

MCP is a communication protocol that enables different AI models and services to interact in a shared context, allowing dynamic task routing, modularity, and composability of LLM-based services.
