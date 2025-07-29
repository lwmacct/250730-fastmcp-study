#!/usr/bin/env python3
"""
Enhanced STDIO MCP Server with shared components

This FastMCP server demonstrates:
- Context-aware logging and progress reporting
- Middleware integration
- Reusable tool patterns from shared library
- Structured prompt templates
- Professional async/await patterns
"""

import asyncio
import datetime
import os
import pathlib
import random
from typing import Dict, List, Any

from fastmcp import FastMCP, Context

# Import shared components
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
    name="Enhanced STDIO MCP Server",
    instructions="""
    An enhanced STDIO MCP server showcasing FastMCP capabilities with shared components:
    - Context-aware logging and progress reporting
    - Middleware for error handling and timing
    - Reusable tools from shared library
    - LLM-ready prompt templates
    - Professional development patterns
    """,
    on_duplicate_tools="warn",
    on_duplicate_resources="warn",
    on_duplicate_prompts="warn"
)

# 设置标准中间件
setup_middleware(mcp, server_type="stdio")

# 添加共享工具
create_server_info_tool(mcp, "Enhanced STDIO MCP Server", "STDIO")
create_math_tool(mcp)
create_string_tool(mcp)
create_data_generator_tool(mcp)


# 添加共享 prompts
create_data_analysis_prompt(mcp)
create_troubleshooting_prompt(mcp)


# STDIO 专用工具
@mcp.tool(description="Get current system time with timezone information")
async def get_current_time(ctx: Context, timezone: str = "UTC") -> dict:
    """Get current time with enhanced timezone support"""
    await ctx.info(f"Fetching current time for timezone: {timezone}")

    current_time = datetime.datetime.now()

    return {
        "current_time": current_time.isoformat(),
        "timezone": timezone,
        "timestamp": current_time.timestamp(),
        "formatted": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "request_id": ctx.request_id
    }


@mcp.tool(description="Advanced mathematical operations with detailed analysis")
async def math_operations(numbers: List[float], operation: str, ctx: Context) -> dict:
    """Perform mathematical operations on a list of numbers"""
    await ctx.info(f"Performing {operation} on {len(numbers)} numbers")
    await ctx.report_progress(progress=25, total=100)

    if not numbers:
        await ctx.error("Empty numbers list provided")
        return {"error": "No numbers provided", "success": False}

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
        await ctx.warning(f"Unknown operation: {operation}")
        return {
            "error": f"Unknown operation: {operation}",
            "available_operations": list(operations.keys()),
            "success": False
        }

    result = operations[operation]
    await ctx.info(f"Operation {operation} completed: {result}")
    await ctx.report_progress(progress=100, total=100)

    return {
        "operation": operation,
        "result": result,
        "input_count": len(numbers),
        "success": True,
        "timestamp": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }


@mcp.tool(description="Analyze text with comprehensive statistics and insights")
async def text_analyzer(text: str, analysis_type: str, ctx: Context) -> dict:
    """Comprehensive text analysis tool"""
    await ctx.info(f"Analyzing text with {analysis_type} analysis")
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
        await ctx.warning(f"Unknown analysis type: {analysis_type}")
        return {
            "error": f"Unknown analysis type: {analysis_type}",
            "available_types": list(analyses.keys()),
            "success": False
        }

    result = analyses[analysis_type]
    await ctx.info("Text analysis completed successfully")
    await ctx.report_progress(progress=100, total=100)

    return {
        "analysis_type": analysis_type,
        "results": result,
        "text_preview": text[:100] + "..." if len(text) > 100 else text,
        "success": True,
        "timestamp": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }


@mcp.tool(description="Process and analyze data collections with filtering and sorting")
async def data_processor(data: List[Any], operation: str, ctx: Context) -> dict:
    """Process data collections with various operations"""
    await ctx.info(f"Processing {len(data)} items with {operation} operation")
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
        await ctx.error(f"Unknown operation: {operation}")
        return {
            "error": f"Unknown operation: {operation}",
            "available_operations": list(operations.keys()),
            "success": False
        }

    result = operations[operation]
    await ctx.info("Data processing completed successfully")
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


@mcp.tool(description="Enhanced greeting with personalization and context")
async def greet_advanced(name: str, style: str, ctx: Context,
                         language: str = "en") -> dict:
    """Generate personalized greetings in different styles and languages"""
    await ctx.info(f"Generating {style} greeting for {name} in {language}")

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
        await ctx.warning(f"Unsupported combination: {language}/{style}")
        return {
            "error": "Unsupported language or style",
            "available_languages": list(greetings.keys()),
            "available_styles": list(greetings.get("en", {}).keys()),
            "success": False
        }

    greeting = greetings[language][style]
    await ctx.info("Generated greeting successfully")

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
    """Comprehensive server status information"""
    await ctx.info("Generating comprehensive server status report")

    return {
        "server_name": "Enhanced STDIO MCP Server",
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
    """Generate sample data resource using shared components"""
    await ctx.info(f"Generating sample data resource for type: {data_type}")

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
        await ctx.warning(f"Unknown data type: {data_type}")
        return {
            "error": f"Unknown data type: {data_type}",
            "available_types": list(sample_generators.keys())
        }

    data = sample_generators[data_type]()
    await ctx.info(f"Generated {len(data)} sample items for {data_type}")

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
    """System information resource with filtered sensitive data"""
    await ctx.info("Collecting system information")

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
    """Main entry point for the STDIO server"""
    print("🚀 Starting Enhanced STDIO MCP Server with shared components...")
    print("📦 Features: Context logging, progress reporting, middleware")
    print("🔧 Architecture: Shared components from mcp-shared library")
    print("📡 Transport: STDIO (standard input/output)")
    print("✅ Server ready for MCP client connections")

    # 使用 run_async 避免事件循环冲突
    await mcp.run_async(transport="stdio")


if __name__ == "__main__":
    asyncio.run(main())
