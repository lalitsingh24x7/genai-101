from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from app import app

mcp = FastApiMCP(app)
mcp.mount()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)