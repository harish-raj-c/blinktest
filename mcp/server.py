from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("Blink Test MCP", host="127.0.0.1", port=8001)

BASE_URL = "http://localhost:8008"

@mcp.tool()
async def get_status():
    """Get Blink Test Status"""

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/api/status"
        )

    return response.json()

@mcp.tool()
async def start_blink_test():
    """Start Blink Test"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/start"
        )

    return response.json()

@mcp.tool()
async def stop_blink_test():
    """Stop Blink Test"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/stop"
        )

    return response.json()

@mcp.tool()
async def reset_blink_test():
    """Reset Blink Test"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/reset"
        )

    return response.json()

if __name__ == "__main__":
    mcp.run(transport="streamable-http")