"""
mathserver.py

A simple MCP (Modular Command Platform) server exposing basic math operations as tools.
This server provides two tools:
    - add(a: int, b: int): Returns the sum of two integers.
    - multiply(a: int, b: int): Returns the product of two integers.

The server uses FastMCP and communicates via stdio transport.

Usage:
    python mathserver.py

Dependencies:
    - mcp

Author: [Your Name]
Date: [Date]
"""
# ...existing code...
from mcp.server import FastMCP
# ...existing code...

from mcp.server import FastMCP


mcp = FastMCP("Maht")

@mcp.tool()
def add(a: int, b:int)->int:
    """
    Add two numbers
    """
    return  a + b

@mcp.tool()
def multiply(a: int, b: int)-> int:
    """
    Multiplication of two numbers
    """
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
