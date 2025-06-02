"""Weather tools for MCP Streamable HTTP server using NWS API."""

import uvicorn
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name='weather', json_response=True)


# Add an addition tool
@mcp.tool()
def get_weather(city: str) -> str:
    """获取指定城市天气"""
    return '有雨，12-19度'


if __name__ == '__main__':
    # Start the server with Streamable HTTP transport
    uvicorn.run(mcp.streamable_http_app, host='localhost', port=8000)
