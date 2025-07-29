"""
FastMCP 服务器的共享工具实现。
"""

import random
import datetime
from typing import Optional
from fastmcp import FastMCP, Context


def create_server_info_tool(mcp: FastMCP, server_name: str, server_type: str) -> None:
    """创建具有通用功能的服务器信息工具"""

    @mcp.tool(description=f"获取此 {server_type} MCP 服务器的综合信息")
    async def get_server_info(ctx: Context) -> dict:
        await ctx.info(f"正在获取 {server_type} 服务器信息")
        await ctx.debug("正在收集系统详情和功能")

        return {
            "name": server_name,
            "type": server_type,
            "version": "0.1.0",
            "description": f"具有中间件和上下文支持的增强型 {server_type} FastMCP 服务器",
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
    """创建数学计算工具"""

    @mcp.tool(description="安全地评估数学表达式，支持进度跟踪")
    async def calculate(expression: str, ctx: Context) -> dict:
        await ctx.info(f"正在评估数学表达式: {expression}")
        await ctx.report_progress(progress=25, total=100)

        try:
            # 只允许基本的数学运算，确保安全
            allowed_chars = set('0123456789+-*/().,e ')
            if not all(c in allowed_chars for c in expression):
                await ctx.error(f"表达式中包含无效字符: {expression}")
                return {
                    "error": "表达式包含无效字符",
                    "expression": expression,
                    "success": False
                }

            await ctx.report_progress(progress=50, total=100)

            # 安全评估表达式
            result = eval(expression)

            await ctx.report_progress(progress=75, total=100)
            await ctx.info(f"成功评估: {expression} = {result}")

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
            await ctx.error(f"评估表达式失败: {str(e)}")
            return {
                "error": str(e),
                "expression": expression,
                "success": False,
                "request_id": ctx.request_id
            }


def create_string_tool(mcp: FastMCP) -> None:
    """创建字符串操作工具"""

    @mcp.tool(description="高级字符串操作，支持进度报告")
    async def string_operations(text: str, operation: str, ctx: Context,
                                target: Optional[str] = None,
                                replacement: Optional[str] = None) -> dict:
        await ctx.info(f"正在对长度为 {len(text)} 的文本执行 {operation} 操作")
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
            await ctx.warning(f"未知操作: {operation}")
            return {
                "error": f"未知操作: {operation}",
                "available_operations": list(operations.keys()),
                "success": False
            }

        await ctx.report_progress(progress=80, total=100)
        result = operations[operation]
        await ctx.info(f"字符串操作 {operation} 成功完成")

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
    """创建数据生成工具"""

    @mcp.tool(description="生成各种类型的示例数据，支持进度跟踪")
    async def generate_data(data_type: str, count: int, ctx: Context) -> dict:
        await ctx.info(f"正在生成 {count} 个 {data_type} 类型的项目")
        await ctx.report_progress(progress=10, total=100)

        if count > 100:
            await ctx.warning(f"数量 {count} 过大，限制为 100")
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
            await ctx.error(f"未知数据类型: {data_type}")
            return {
                "error": f"未知数据类型: {data_type}",
                "available_types": list(generators.keys()),
                "success": False
            }

        await ctx.report_progress(progress=70, total=100)
        data = generators[data_type]()

        await ctx.report_progress(progress=90, total=100)
        await ctx.info(f"成功生成 {len(data)} 个 {data_type} 类型的项目")

        await ctx.report_progress(progress=100, total=100)
        return {
            "data_type": data_type,
            "count": len(data),
            "data": data,
            "success": True,
            "timestamp": datetime.datetime.now().isoformat(),
            "request_id": ctx.request_id
        }
