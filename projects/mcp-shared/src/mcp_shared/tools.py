"""
Shared tool implementations for FastMCP servers.
"""

import random
import datetime
from typing import Optional
from fastmcp import FastMCP, Context


def create_server_info_tool(mcp: FastMCP, server_name: str, server_type: str) -> None:
    """Create a server info tool with common capabilities"""

    @mcp.tool(description=f"Get comprehensive information about this {server_type} MCP server")
    async def get_server_info(ctx: Context) -> dict:
        await ctx.info(f"Fetching {server_type} server information")
        await ctx.debug("Collecting system details and capabilities")

        return {
            "name": server_name,
            "type": server_type,
            "version": "0.1.0",
            "description": f"Enhanced {server_type} FastMCP Server with middleware and context support",
            "capabilities": {
                "context_logging": True,
                "progress_reporting": True,
                "middleware_enabled": True,
                "has_prompts": True,
                "request_tracking": True,
            },
            "status": "running",
            "timestamp": datetime.datetime.now().isoformat(),
            "request_id": ctx.request_id,
        }


def create_math_tool(mcp: FastMCP) -> None:
    """Create a mathematical calculation tool"""

    @mcp.tool(description="Safely evaluate mathematical expressions with progress tracking")
    async def calculate(expression: str, ctx: Context) -> dict:
        await ctx.info(f"Evaluating mathematical expression: {expression}")
        await ctx.report_progress(progress=25, total=100)

        try:
            # 只允许基本的数学运算，确保安全
            allowed_chars = set('0123456789+-*/().,e ')
            if not all(c in allowed_chars for c in expression):
                await ctx.error(f"Invalid characters in expression: {expression}")
                return {
                    "error": "Expression contains invalid characters",
                    "expression": expression,
                    "success": False
                }

            await ctx.report_progress(progress=50, total=100)

            # 安全评估表达式
            result = eval(expression)

            await ctx.report_progress(progress=75, total=100)
            await ctx.info(f"Successfully evaluated: {expression} = {result}")

            response = {
                "expression": expression,
                "result": result,
                "type": type(result).__name__,
                "success": True,
                "timestamp": datetime.datetime.now().isoformat(),
                "request_id": ctx.request_id
            }

            await ctx.report_progress(progress=100, total=100)
            return response

        except Exception as e:
            await ctx.error(f"Failed to evaluate expression: {str(e)}")
            return {
                "error": str(e),
                "expression": expression,
                "success": False,
                "request_id": ctx.request_id
            }


def create_string_tool(mcp: FastMCP) -> None:
    """Create a string operations tool"""

    @mcp.tool(description="Advanced string operations with progress reporting")
    async def string_operations(text: str, operation: str, ctx: Context,
                                target: Optional[str] = None,
                                replacement: Optional[str] = None) -> dict:
        await ctx.info(f"Performing {operation} on text of length {len(text)}")
        await ctx.report_progress(progress=20, total=100)

        operations = {
            "upper": text.upper(),
            "lower": text.lower(),
            "title": text.title(),
            "reverse": text[::-1],
            "length": len(text),
            "strip": text.strip(),
            "capitalize": text.capitalize()
        }

        # 高级操作
        if operation == "replace" and target and replacement:
            operations["replace"] = text.replace(target, replacement)

        await ctx.report_progress(progress=60, total=100)

        if operation not in operations:
            await ctx.warning(f"Unknown operation: {operation}")
            return {
                "error": f"Unknown operation: {operation}",
                "available_operations": list(operations.keys()),
                "success": False
            }

        await ctx.report_progress(progress=80, total=100)
        result = operations[operation]
        await ctx.info(f"String operation {operation} completed successfully")

        await ctx.report_progress(progress=100, total=100)
        return {
            "original_text": text,
            "operation": operation,
            "result": result,
            "success": True,
            "timestamp": datetime.datetime.now().isoformat(),
            "request_id": ctx.request_id
        }


def create_data_generator_tool(mcp: FastMCP) -> None:
    """Create a data generation tool"""

    @mcp.tool(description="Generate sample data with various types and progress tracking")
    async def generate_data(data_type: str, count: int, ctx: Context) -> dict:
        await ctx.info(f"Generating {count} items of type {data_type}")
        await ctx.report_progress(progress=10, total=100)

        if count > 100:
            await ctx.warning(f"Count {count} too large, limiting to 100")
            count = 100

        await ctx.report_progress(progress=30, total=100)

        generators = {
            "numbers": lambda: [random.randint(1, 1000) for _ in range(count)],
            "floats": lambda: [round(random.uniform(0, 100), 2) for _ in range(count)],
            "strings": lambda: [f"item_{i}_{random.randint(100, 999)}" for i in range(count)],
            "booleans": lambda: [random.choice([True, False]) for _ in range(count)],
            "dates": lambda: [
                (datetime.datetime.now(
                ) - datetime.timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
                for _ in range(count)
            ],
            "colors": lambda: [
                random.choice(
                    ["red", "blue", "green", "yellow", "purple", "orange"])
                for _ in range(count)
            ]
        }

        await ctx.report_progress(progress=50, total=100)

        if data_type not in generators:
            await ctx.error(f"Unknown data type: {data_type}")
            return {
                "error": f"Unknown data type: {data_type}",
                "available_types": list(generators.keys()),
                "success": False
            }

        await ctx.report_progress(progress=70, total=100)
        data = generators[data_type]()

        await ctx.report_progress(progress=90, total=100)
        await ctx.info(f"Successfully generated {len(data)} items of type {data_type}")

        await ctx.report_progress(progress=100, total=100)
        return {
            "data_type": data_type,
            "count": len(data),
            "data": data,
            "success": True,
            "timestamp": datetime.datetime.now().isoformat(),
            "request_id": ctx.request_id
        }
