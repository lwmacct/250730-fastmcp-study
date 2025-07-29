"""
MCP Shared - Shared utilities and components for FastMCP servers.
"""

__version__ = "0.1.0"

from .middleware import setup_middleware
from .tools import (
    create_server_info_tool,
    create_math_tool,
    create_string_tool,
    create_data_generator_tool,
)
from .prompts import (
    create_data_analysis_prompt,
    create_troubleshooting_prompt,
    create_web_api_prompt,
)

__all__ = [
    "setup_middleware", 
    "create_server_info_tool",
    "create_math_tool",
    "create_string_tool",
    "create_data_generator_tool",
    "create_data_analysis_prompt",
    "create_troubleshooting_prompt",
    "create_web_api_prompt",
]
