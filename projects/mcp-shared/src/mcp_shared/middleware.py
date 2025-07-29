"""
FastMCP 服务器的共享中间件组件。
"""

from fastmcp import FastMCP


def setup_middleware(mcp: FastMCP, server_type: str = "unknown") -> None:
    """为 FastMCP 服务器设置标准中间件"""
    print(f"正在为 {server_type} 服务器设置中间件...")
    # 注意：当前版本的 FastMCP 可能不直接支持中间件
    # 这里保留接口用于未来扩展
    pass
