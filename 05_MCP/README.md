# 05-MCP: Model Context Protocol Example

This project demonstrates a simple Model Context Protocol (MCP) setup using Python, featuring two MCP servers (Math and To-Do) and a command-line client powered by LangChain and OpenAI.

## Architecture

```
+-------------------+        stdio         +-------------------+
|                   | <------------------> |                   |
|   client.py       |                      |   mathserver.py   |
| (LangChain Agent) |                      | (Math MCP Server) |
|                   |                      |                   |
+-------------------+                      +-------------------+
        |
        | streamable-http
        v
+-------------------+
|                   |
|   my_todo.py      |
| (To-Do MCP Server)|
|                   |
+-------------------+
```

- **client.py**: Command-line client that connects to both servers, routes user requests, and displays responses.
- **mathserver.py**: MCP server exposing math tools (`add`, `multiply`) via stdio.
- **my_todo.py**: MCP server exposing a to-do retrieval tool via HTTP.

## Setup

### 1. Install [uv](https://github.com/astral-sh/uv) (fast Python package manager)

```sh
pip install uv
```

### 2. Install dependencies

```sh
uv pip install -r requirements.txt
```

Or, using `pyproject.toml`:

```sh
uv pip install -r requirements.txt
```

### 3. Set your OpenAI API key

Create a `.env` file in the project root with:

```
OPENAI_API_KEY=your-openai-api-key
```

Or export it in your shell:

```sh
export OPENAI_API_KEY=your-openai-api-key
```

## Running the Project

### 1. Start the To-Do MCP Server

```sh
python my_todo.py
```

This will start an HTTP server at `http://localhost:8000/mcp`.

### 2. Run the Client

In a new terminal, run:

```sh
python client.py
```

- The client will automatically start the math server (`mathserver.py`) via stdio.
- It will connect to the to-do server via HTTP.

### 3. Interact

Type your requests at the prompt, for example:

- `What is 5 plus 7?`
- `What are my todos for 05-07-2025?`
- `Multiply 3 and 4`
- Type `exit` to quit.

## File Overview

- [`client.py`](client.py): Command-line client using LangChain, OpenAI, and MCP adapters.
- [`mathserver.py`](mathserver.py): Math MCP server (add, multiply).
- [`my_todo.py`](my_todo.py): To-Do MCP server (date-based to-do retrieval).
- [`requirements.txt`](requirements.txt): Python dependencies.
- [`pyproject.toml`](pyproject.toml): Project metadata and dependencies.

## Notes

- Ensure Python 3.12+ is installed (see [.python-version](.python-version)).
- The math server is started automatically by the client.
- The to-do server must be started manually before running the client.

---

**Note:** MCP stands for **Model Context Protocol**.