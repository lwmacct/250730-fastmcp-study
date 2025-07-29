"""
Shared middleware components for FastMCP servers.
"""

from fastmcp import FastMCP


def setup_middleware(mcp: FastMCP, server_type: str = "unknown") -> None:
    """Setup standard middleware for a FastMCP server"""
    print(f"Setting up middleware for {server_type} server...")
    # 注意：当前版本的 FastMCP 可能不直接支持中间件
    # 这里保留接口用于未来扩展
    pass
