from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mojeek")


@mcp.tool()
async def get_search(state: str) -> str:
    """Get mojeek search results.
    Mojeek is a web search engine that provides unbiased, fast, and relevant search results combined with a no tracking privacy policy.

    Args:
        state: word or words to search for.
    """

    return ""


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
