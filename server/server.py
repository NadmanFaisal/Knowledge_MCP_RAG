from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("RAG_MCP")

USER_AGENT = "weather-app/1.0"

@mcp.tool()
def add_numbers(n1: int, n2: int) -> int:
    """
        Add two integers to prodive a sum.
        args:
        n1: The first number
        n2: The second number

        return: returns an integer
    """
    return n1 + n2

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()

