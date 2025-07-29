#!/usr/bin/env python3
"""
增强型 HTTP MCP 服务器，具有共享组件

这个 FastMCP HTTP 服务器演示了:
- Streamable HTTP 传输协议
- 上下文感知日志记录和进度报告
- 来自 mcp-shared 库的共享中间件和工具
- HTTP 专用请求检查
- 专业的 async/await 模式
"""

import asyncio
import datetime
import random
from typing import Dict, Any

from fastmcp import FastMCP, Context

# 导入共享组件
from mcp_shared import (
    setup_middleware,
    create_server_info_tool,
    create_math_tool,
    create_string_tool,
    create_data_generator_tool,
    create_data_analysis_prompt,
    create_web_api_prompt,
)

# 初始化 FastMCP 服务器
mcp = FastMCP(
    name="增强型 HTTP MCP 服务器",
    instructions="""
    一个使用 Streamable HTTP 协议的增强型 HTTP MCP 服务器，具有共享组件:
    - 上下文感知日志记录和进度报告
    - 用于错误处理和计时的中间件
    - 来自共享库的可重用工具
    - HTTP 专用请求检查功能
    - LLM 就绪的提示模板
    """,
    on_duplicate_tools="warn",
    on_duplicate_resources="warn",
    on_duplicate_prompts="warn"
)

# 设置标准中间件
setup_middleware(mcp, server_type="http")

# 添加共享工具
create_server_info_tool(mcp, "增强型 HTTP MCP 服务器", "HTTP")
create_math_tool(mcp)
create_string_tool(mcp)
create_data_generator_tool(mcp)

# 添加共享 prompts
create_data_analysis_prompt(mcp)
create_web_api_prompt(mcp)


# HTTP 专用工具
@mcp.tool(description="使用上下文日志记录检查 HTTP 请求详情")
async def inspect_request(ctx: Context) -> dict:
    """检查当前 HTTP 请求详情"""
    await ctx.info("正在检查 HTTP 请求详情")

    try:
        request = ctx.get_http_request()
        headers = dict(request.headers)

        # 过滤敏感信息
        filtered_headers = {
            k: v for k, v in headers.items()
            if not any(sensitive in k.lower()
                       for sensitive in ['authorization', 'cookie', 'token'])
        }

        await ctx.debug(f"请求方法: {request.method}, URL: {request.url}")

        return {
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": filtered_headers,
            "client_host": getattr(request.client, 'host', 'unknown') if request.client else 'unknown',
            "content_type": headers.get('content-type', 'unknown'),
            "user_agent": headers.get('user-agent', 'unknown'),
            "request_id": ctx.request_id,
            "timestamp": datetime.datetime.now().isoformat()
        }
    except Exception as e:
        await ctx.error(f"请求检查失败: {str(e)}")
        return {
            "error": f"请求检查失败: {str(e)}",
            "success": False,
            "request_id": ctx.request_id
        }


@mcp.tool(description="获取天气预报，支持位置和单位")
async def get_weather(location: str, ctx: Context, units: str = "celsius") -> dict:
    """获取特定位置的天气预报"""
    await ctx.info(f"正在获取 {location} 的天气数据，单位: {units}")
    await ctx.report_progress(progress=25, total=100)

    # 模拟天气数据生成
    temperatures = {
        "celsius": random.randint(-10, 35),
        "fahrenheit": random.randint(14, 95)
    }

    conditions = ["sunny", "cloudy", "rainy", "snowy", "foggy", "windy"]

    await ctx.report_progress(progress=50, total=100)

    if units not in temperatures:
        await ctx.warning(f"未知单位: {units}，默认使用 celsius")
        units = "celsius"

    await ctx.report_progress(progress=75, total=100)

    weather_data = {
        "location": location,
        "temperature": temperatures[units],
        "units": units,
        "condition": random.choice(conditions),
        "humidity": random.randint(30, 90),
        "wind_speed": random.randint(0, 30),
        "forecast": {
            "today": f"{random.choice(conditions)}, {temperatures[units]}°",
            "tomorrow": f"{random.choice(conditions)}, {random.randint(-10, 35) if units == 'celsius' else random.randint(14, 95)}°"
        },
        "last_updated": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }

    await ctx.report_progress(progress=100, total=100)
    await ctx.info(f"已生成 {location} 的天气数据")

    return weather_data


@mcp.tool(description="回显消息，支持各种格式化选项")
async def echo_advanced(message: str, ctx: Context, format_type: str = "plain", repeat: int = 1) -> dict:
    """使用各种格式化选项回显消息"""
    await ctx.info(f"正在回显消息，格式: {format_type}，重复次数: {repeat}")

    if repeat > 10:
        await ctx.warning(f"重复次数 {repeat} 过高，限制为 10")
        repeat = 10

    formats = {
        "plain": lambda x: x,
        "upper": lambda x: x.upper(),
        "lower": lambda x: x.lower(),
        "reverse": lambda x: x[::-1],
        "title": lambda x: x.title(),
        "emoji": lambda x: f"🗣️ {x} 🗣️"
    }

    if format_type not in formats:
        await ctx.warning(f"未知格式: {format_type}，使用 plain")
        format_type = "plain"

    formatted_message = formats[format_type](message)
    result = [formatted_message] * repeat

    await ctx.debug(f"消息已格式化并重复 {repeat} 次")

    return {
        "original_message": message,
        "format_type": format_type,
        "repeat_count": repeat,
        "result": result,
        "success": True,
        "timestamp": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }


# HTTP 专用 prompt
@mcp.prompt(
    name="http_debugging_guide",
    description="生成 HTTP 调试和故障排除指南"
)
async def http_debugging_guide(issue_type: str, status_code: str = "unknown") -> str:
    return f"""HTTP 调试指南

**问题类型**: {issue_type}
**状态码**: {status_code}

## 常见 HTTP 问题和解决方案

### 1. 连接问题
- 检查网络连接
- 验证服务器是否运行且可访问
- 检查防火墙设置
- 验证 SSL/TLS 证书

### 2. 请求问题
- 验证 HTTP 方法 (GET, POST, PUT, DELETE)
- 检查请求头和内容类型
- 验证请求体格式
- 确保正确的 URL 编码

### 3. 响应问题
- 检查响应状态码
- 验证响应头
- 验证响应体格式
- 检查 CORS 问题

### 4. 性能问题
- 监控响应时间
- 检查超时设置
- 分析服务器负载
- 审查缓存策略

### 5. 认证问题
- 验证凭据和令牌
- 检查授权头
- 验证 API 密钥
- 审查会话管理

使用浏览器开发者工具和 HTTP 客户端进行详细调试。"""


# 资源
@mcp.resource(uri="mcp://server/info")
async def server_info_resource(ctx: Context) -> dict:
    """综合服务器信息资源"""
    await ctx.info("正在生成综合服务器状态报告")

    return {
        "server_name": "增强型 HTTP MCP 服务器",
        "server_type": "http",
        "transport": "streamable-http",
        "status": "running",
        "host": "localhost",
        "port": 8000,
        "path": "/mcp",
        "capabilities": [
            "mathematical_calculations",
            "string_operations",
            "data_generation",
            "weather_simulation",
            "http_request_inspection",
            "message_echo",
            "context_logging",
            "progress_reporting"
        ],
        "features": {
            "shared_components": True,
            "middleware_enabled": True,
            "context_aware": True,
            "http_specific": True
        },
        "timestamp": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }


@mcp.resource(uri="mcp://data/sample/{data_type}")
async def sample_data_resource(data_type: str, ctx: Context) -> Dict[str, Any]:
    """生成示例数据资源"""
    await ctx.info(f"正在生成 {data_type} 类型的示例数据资源")

    sample_generators = {
        "users": lambda: [
            {"id": i, "name": f"User{i}", "email": f"user{i}@example.com",
                "active": random.choice([True, False])}
            for i in range(1, 6)
        ],
        "products": lambda: [
            {"id": i, "name": f"Product{i}",
             "price": round(random.uniform(10, 100), 2)}
            for i in range(1, 6)
        ],
        "orders": lambda: [
            {"id": i, "user_id": random.randint(1, 5),
             "total": round(random.uniform(20, 200), 2)}
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


@mcp.resource(uri="mcp://weather/forecast/{city}")
async def weather_forecast_resource(city: str, ctx: Context) -> Dict[str, Any]:
    """特定城市的天气预报资源"""
    await ctx.info(f"正在生成 {city} 的天气预报")

    # 模拟天气预报数据
    conditions = ["sunny", "cloudy", "rainy", "snowy", "foggy"]

    forecast = {
        "city": city,
        "current_weather": {
            "temperature": random.randint(-10, 35),
            "condition": random.choice(conditions),
            "humidity": random.randint(30, 90),
            "wind_speed": random.randint(0, 30)
        },
        "forecast_days": [
            {
                "day": i + 1,
                "condition": random.choice(conditions),
                "high": random.randint(20, 35),
                "low": random.randint(-5, 15)
            }
            for i in range(5)
        ],
        "last_updated": datetime.datetime.now().isoformat(),
        "request_id": ctx.request_id
    }

    await ctx.info(f"已生成 {city} 的天气预报")
    return forecast


async def main():
    """HTTP 服务器的主入口点"""
    print("🚀 正在启动具有共享组件的增强型 HTTP MCP 服务器...")
    print("📦 功能: 上下文日志记录、进度报告、中间件")
    print("🔧 架构: 来自 mcp-shared 库的共享组件")
    print("📡 传输: Streamable HTTP (localhost:8000/mcp)")
    print("🌐 HTTP 专用: 请求检查、天气 API、调试工具")
    print("✅ 服务器已准备好接受 MCP 客户端连接")

    # 使用 run_async 以支持异步环境
    await mcp.run_async(transport="streamable-http", host="localhost", port=8000, path="/mcp")


if __name__ == "__main__":
    asyncio.run(main())
