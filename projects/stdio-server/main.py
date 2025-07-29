#!/usr/bin/env python3
"""
增强型 STDIO MCP 服务器，具有共享组件

这个 FastMCP 服务器演示了:
- 上下文感知日志记录和进度报告
- 中间件集成
- 来自共享库的可重用工具模式
- 结构化提示模板
- 专业的 async/await 模式
"""

import asyncio
import datetime
import os
import pathlib
import random
from typing import Dict, List, Any

from fastmcp import FastMCP, Context

# 导入共享组件
from mcp_shared import (
    setup_middleware,
    create_server_info_tool,
    create_math_tool,
    create_string_tool,
    create_data_generator_tool,
    create_data_analysis_prompt,
    create_troubleshooting_prompt,
)

# 初始化 FastMCP 服务器
mcp = FastMCP(
    name="增强型 STDIO MCP 服务器",
    instructions="""
    一个展示 FastMCP 功能的增强型 STDIO MCP 服务器，具有共享组件:
    - 上下文感知日志记录和进度报告
    - 用于错误处理和计时的中间件
    - 来自共享库的可重用工具
    - LLM 就绪的提示模板
    - 专业开发模式
    """,
    on_duplicate_tools="warn",
    on_duplicate_resources="warn",
    on_duplicate_prompts="warn"
)

# 设置标准中间件
setup_middleware(mcp, server_type="stdio")

# 添加共享工具
create_server_info_tool(mcp, "增强型 STDIO MCP 服务器", "STDIO")
create_math_tool(mcp)
create_string_tool(mcp)
create_data_generator_tool(mcp)


# 添加共享 prompts
create_data_analysis_prompt(mcp)
create_troubleshooting_prompt(mcp)


# STDIO 专用工具
@mcp.tool(description="获取当前系统时间，包含时区信息")
async def get_current_time(ctx: Context, timezone: str = "UTC") -> dict:
    """获取当前时间，支持增强的时区功能"""
    await ctx.info(f"正在获取时区 {timezone} 的当前时间")

    current_time = datetime.datetime.now()

    return {
        "current_time": current_time.isoformat(),
        "timezone": timezone,
        "timestamp": current_time.timestamp(),
        "formatted": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "request_id": ctx.request_id
    }


@mcp.tool(description="高级数学运算，包含详细分析")
async def math_operations(numbers: List[float], operation: str, ctx: Context) -> dict:
    """对数字列表执行数学运算"""
    await ctx.info(f"正在对 {len(numbers)} 个数字执行 {operation} 运算")
    await ctx.report_progress(progress=25, total=100)

    if not numbers:
        await ctx.error("提供的数字列表为空")
        return {"error": "未提供数字", "success": False}

    operations = {
        "sum": sum(numbers),
        "average": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "median": sorted(numbers)[len(numbers) // 2],
        "count": len(numbers)
    }

    await ctx.report_progress(progress=75, total=100)

    if operation not in operations:
        await ctx.warning(f"未知运算: {operation}")
        return {
            "error": f"未知运算: {operation}",
            "available_operations": list(operations.keys()),
            "success": False
        }

    result = operations[operation]
    await ctx.info(f"运算 {operation} 完成: {result}")
    await ctx.report_progress(progress=100, total=100)

    return {
        "operation": operation,
        "result": result,
        "input_count": len(numbers),
        "success": True,
        "timestamp": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }


@mcp.tool(description="使用综合统计和洞察分析文本")
async def text_analyzer(text: str, analysis_type: str, ctx: Context) -> dict:
    """综合文本分析工具"""
    await ctx.info(f"正在使用 {analysis_type} 分析分析文本")
    await ctx.report_progress(progress=20, total=100)

    # 基础统计
    word_count = len(text.split())
    char_count = len(text)
    line_count = len(text.splitlines())

    await ctx.report_progress(progress=50, total=100)

    analyses = {
        "basic": {
            "character_count": char_count,
            "word_count": word_count,
            "line_count": line_count,
            "average_word_length": sum(len(word) for word in text.split()) / word_count if word_count > 0 else 0
        },
        "detailed": {
            "character_count": char_count,
            "word_count": word_count,
            "line_count": line_count,
            "unique_words": len(set(text.lower().split())),
            "sentences": len([s for s in text.split('.') if s.strip()]),
            "paragraphs": len([p for p in text.split('\n\n') if p.strip()])
        }
    }

    await ctx.report_progress(progress=80, total=100)

    if analysis_type not in analyses:
        await ctx.warning(f"未知分析类型: {analysis_type}")
        return {
            "error": f"未知分析类型: {analysis_type}",
            "available_types": list(analyses.keys()),
            "success": False
        }

    result = analyses[analysis_type]
    await ctx.info("文本分析成功完成")
    await ctx.report_progress(progress=100, total=100)

    return {
        "analysis_type": analysis_type,
        "results": result,
        "text_preview": text[:100] + "..." if len(text) > 100 else text,
        "success": True,
        "timestamp": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }


@mcp.tool(description="处理和分析数据集合，支持过滤和排序")
async def data_processor(data: List[Any], operation: str, ctx: Context) -> dict:
    """使用各种操作处理数据集合"""
    await ctx.info(f"正在对 {len(data)} 个项目执行 {operation} 操作")
    await ctx.report_progress(progress=30, total=100)

    # 将所有数据转换为字符串以避免类型错误
    str_data = [str(item) for item in data]

    operations = {
        "sort": sorted(str_data),
        "reverse": list(reversed(str_data)),
        "unique": list(set(str_data)),
        "frequency": {item: str_data.count(item) for item in set(str_data)},
        "sample": random.sample(str_data, min(5, len(str_data))) if str_data else []
    }

    await ctx.report_progress(progress=70, total=100)

    if operation not in operations:
        await ctx.error(f"未知操作: {operation}")
        return {
            "error": f"未知操作: {operation}",
            "available_operations": list(operations.keys()),
            "success": False
        }

    result = operations[operation]
    await ctx.info("数据处理成功完成")
    await ctx.report_progress(progress=100, total=100)

    return {
        "operation": operation,
        "result": result,
        "input_count": len(data),
        "output_count": len(result) if isinstance(result, list) else 1,
        "success": True,
        "timestamp": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }


@mcp.tool(description="增强型问候，支持个性化和上下文")
async def greet_advanced(name: str, style: str, ctx: Context,
                         language: str = "en") -> dict:
    """以不同风格和语言生成个性化问候"""
    await ctx.info(f"正在为 {name} 生成 {style} 风格的问候，语言: {language}")

    greetings = {
        "en": {
            "formal": f"Good day, {name}. It is a pleasure to make your acquaintance.",
            "casual": f"Hey {name}! How's it going?",
            "professional": f"Hello {name}, I hope you're having a productive day.",
            "friendly": f"Hi there {name}! Great to see you!"
        },
        "es": {
            "formal": f"Buenos días, {name}. Es un placer conocerle.",
            "casual": f"¡Hola {name}! ¿Cómo estás?",
            "professional": f"Hola {name}, espero que tengas un día productivo.",
            "friendly": f"¡Hola {name}! ¡Qué bueno verte!"
        }
    }

    if language not in greetings or style not in greetings[language]:
        await ctx.warning(f"不支持的组合: {language}/{style}")
        return {
            "error": "不支持的语言或风格",
            "available_languages": list(greetings.keys()),
            "available_styles": list(greetings.get("en", {}).keys()),
            "success": False
        }

    greeting = greetings[language][style]
    await ctx.info("问候生成成功")

    return {
        "greeting": greeting,
        "name": name,
        "style": style,
        "language": language,
        "success": True,
        "timestamp": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }


# 资源
@mcp.resource(uri="mcp://server/status")
async def server_status_resource(ctx: Context) -> str:
    """综合服务器状态信息"""
    await ctx.info("正在生成综合服务器状态报告")

    return {
        "server_name": "增强型 STDIO MCP 服务器",
        "server_type": "stdio",
        "status": "running",
        "uptime": "active session",
        "capabilities": [
            "mathematical_operations",
            "text_analysis",
            "data_processing",
            "personalized_greetings",
            "context_logging",
            "progress_reporting",
            "middleware_support"
        ],
        "features": {
            "shared_components": True,
            "middleware_enabled": True,
            "context_aware": True,
            "progress_tracking": True
        },
        "timestamp": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }


@mcp.resource(uri="mcp://data/sample/{data_type}")
async def sample_data_resource(data_type: str, ctx: Context) -> Dict[str, Any]:
    """使用共享组件生成示例数据资源"""
    await ctx.info(f"正在生成 {data_type} 类型的示例数据资源")

    # 重用共享库的数据生成逻辑
    sample_generators = {
        "users": lambda: [
            {"id": i, "name": f"User{i}", "email": f"user{i}@example.com"}
            for i in range(1, 6)
        ],
        "tasks": lambda: [
            {"id": i, "title": f"Task {i}",
                "completed": random.choice([True, False])}
            for i in range(1, 6)
        ],
        "logs": lambda: [
            {"timestamp": datetime.datetime.now().isoformat(), "level": random.choice(
                ["INFO", "WARN", "ERROR"]), "message": f"Log entry {i}"}
            for i in range(1, 6)
        ]
    }

    if data_type not in sample_generators:
        await ctx.warning(f"未知数据类型: {data_type}")
        return {
            "error": f"未知数据类型: {data_type}",
            "available_types": list(sample_generators.keys())
        }

    data = sample_generators[data_type]()
    await ctx.info(f"已生成 {len(data)} 个 {data_type} 类型的示例项目")

    return {
        "resource_type": "sample_data",
        "data_type": data_type,
        "count": len(data),
        "data": data,
        "generated_at": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }


@mcp.resource(uri="mcp://system/info")
async def system_info_resource(ctx: Context) -> Dict[str, Any]:
    """系统信息资源，过滤敏感数据"""
    await ctx.info("正在收集系统信息")

    # 过滤敏感环境变量
    safe_env = {k: v for k, v in os.environ.items()
                if not any(sensitive in k.lower()
                           for sensitive in ['password', 'token', 'key', 'secret'])}

    return {
        "python_version": "3.12+",
        "working_directory": str(pathlib.Path.cwd()),
        "environment_variables": safe_env,
        "server_type": "stdio",
        "capabilities": {
            "context_logging": True,
            "progress_reporting": True,
            "middleware_enabled": True,
            "shared_components": True
        },
        "timestamp": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }


async def main():
    """STDIO 服务器的主入口点"""
    print("🚀 正在启动具有共享组件的增强型 STDIO MCP 服务器...")
    print("📦 功能: 上下文日志记录、进度报告、中间件")
    print("🔧 架构: 来自 mcp-shared 库的共享组件")
    print("📡 传输: STDIO (标准输入/输出)")
    print("✅ 服务器已准备好接受 MCP 客户端连接")

    # 使用 run_async 避免事件循环冲突
    await mcp.run_async(transport="stdio")


if __name__ == "__main__":
    asyncio.run(main())
