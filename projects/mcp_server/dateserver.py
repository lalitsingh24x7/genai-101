from mcp.server import FastMCP

from datetime import datetime, timedelta
from typing import Optional

mcp = FastMCP("Maht")

@mcp.tool()
def get_date_from_input(date_input: str) -> Optional[str]:
    """
    Returns a date string (YYYY-MM-DD) based on natural language input.
    Examples:
        "today" -> current date
        "yesterday" -> current date - 1
        "tomorrow" -> current date + 1
        "5 days ago" -> current date - 5
        "in 3 days" -> current date + 3
        "10 days before" -> current date - 10
        "after 7 days" -> current date + 7

    Args:
        date_input (str): Natural language date input.

    Returns:
        str: Date in YYYY-MM-DD format, or None if input is not recognized.
    """
    date_input = date_input.strip().lower()
    today = datetime.now().date()

    if date_input == "today":
        return today.isoformat()
    elif date_input == "yesterday":
        return (today - timedelta(days=1)).isoformat()
    elif date_input == "tomorrow":
        return (today + timedelta(days=1)).isoformat()
    else:
        import re
        # Matches: "5 days ago", "in 3 days", "10 days before", "after 7 days"
        patterns = [
            (r"(\d+)\s+days?\s+ago", -1),
            (r"in\s+(\d+)\s+days?", 1),
            (r"(\d+)\s+days?\s+before", -1),
            (r"after\s+(\d+)\s+days?", 1),
        ]
        for pattern, direction in patterns:
            match = re.match(pattern, date_input)
            if match:
                days = int(match.group(1))
                return (today + timedelta(days=days * direction)).isoformat()
    return None


if __name__ == "__main__":
    mcp.run(transport="stdio")