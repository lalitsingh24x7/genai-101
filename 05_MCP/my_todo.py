"""
This module defines a simple to-do retrieval service using FastMCP.

Classes:
    None

Functions:
    get_my_todys(date_arg: str) -> list[str]:
        Retrieves the list of to-do items for a given date in "DD-MM-YYYY" format.
        Returns a list of to-do items if found, otherwise returns a default message.

Usage:
    Run this module directly to start the FastMCP server with the to-do retrieval tool enabled.
"""
from mcp.server import FastMCP

mcp = FastMCP("My Todo")

@mcp.tool()
async def get_my_todys(date_arg: str)->list[str]:
    """
    Retrieve the list of to-do items for a given date.

    Args:
        date_arg (str): The date in "DD-MM-YYYY" format for which to fetch to-do items.

    Returns:
        list[str]: A list of to-do items for the specified date. If no items are found for the date,
                   returns a default message indicating nothing to do.
    """

    print("todo-----")
    print(date_arg)
    data = {
        "05-07-2025": ["Cloth cleaning", "medicine purchase"],
        "06-07-2025": ["car service"]
    }

    return data.get(date_arg, ["Nothing to do, Chears!"])


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

