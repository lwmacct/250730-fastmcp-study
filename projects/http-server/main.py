#!/usr/bin/env python3
"""
Enhanced HTTP MCP Server with shared components

This FastMCP HTTP server demonstrates:
- Streamable HTTP transport protocol
- Context-aware logging and progress reporting
- Shared middleware and tools from mcp-shared library  
- HTTP-specific request inspection
- Professional async/await patterns
"""

import asyncio
import datetime
import random
from typing import Dict, Any

from fastmcp import FastMCP, Context

# Import shared components
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
    name="Enhanced HTTP MCP Server",
    instructions="""
    An enhanced HTTP MCP server using Streamable HTTP protocol with shared components:
    - Context-aware logging and progress reporting
    - Middleware for error handling and timing
    - Reusable tools from shared library
    - HTTP-specific request inspection capabilities
    - LLM-ready prompt templates
    """,
    on_duplicate_tools="warn",
    on_duplicate_resources="warn",
    on_duplicate_prompts="warn"
)

# 设置标准中间件
setup_middleware(mcp, server_type="http")

# 添加共享工具
create_server_info_tool(mcp, "Enhanced HTTP MCP Server", "HTTP")
create_math_tool(mcp)
create_string_tool(mcp)
create_data_generator_tool(mcp)

# 添加共享 prompts
create_data_analysis_prompt(mcp)
create_web_api_prompt(mcp)


# HTTP 专用工具
@mcp.tool(description="Inspect HTTP request details with context logging")
async def inspect_request(ctx: Context) -> dict:
    """Inspect the current HTTP request details"""
    await ctx.info("Inspecting HTTP request details")
    
    try:
        request = ctx.get_http_request()
        headers = dict(request.headers)
        
        # 过滤敏感信息
        filtered_headers = {k: v for k, v in headers.items()
                           if not any(sensitive in k.lower()
                                     for sensitive in ['authorization', 'cookie', 'token'])}
        
        await ctx.debug(f"Request method: {request.method}, URL: {request.url}")
        
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
        await ctx.error(f"Failed to inspect request: {str(e)}")
        return {
            "error": f"Request inspection failed: {str(e)}",
            "success": False,
            "request_id": ctx.request_id
        }


@mcp.tool(description="Get weather forecast with location and units")
async def get_weather(location: str, ctx: Context, units: str = "celsius") -> dict:
    """Get weather forecast for a specific location"""
    await ctx.info(f"Fetching weather data for {location} in {units}")
    await ctx.report_progress(progress=25, total=100)
    
    # 模拟天气数据生成
    temperatures = {
        "celsius": random.randint(-10, 35),
        "fahrenheit": random.randint(14, 95)
    }
    
    conditions = ["sunny", "cloudy", "rainy", "snowy", "foggy", "windy"]
    
    await ctx.report_progress(progress=50, total=100)
    
    if units not in temperatures:
        await ctx.warning(f"Unknown units: {units}, defaulting to celsius")
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
    await ctx.info(f"Weather data generated for {location}")
    
    return weather_data


@mcp.tool(description="Echo message with various formatting options")
async def echo_advanced(message: str, ctx: Context, format_type: str = "plain", repeat: int = 1) -> dict:
    """Echo a message with various formatting options"""
    await ctx.info(f"Echoing message with format: {format_type}, repeat: {repeat}")
    
    if repeat > 10:
        await ctx.warning(f"Repeat count {repeat} too high, limiting to 10")
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
        await ctx.warning(f"Unknown format: {format_type}, using plain")
        format_type = "plain"
    
    formatted_message = formats[format_type](message)
    result = [formatted_message] * repeat
    
    await ctx.debug(f"Message formatted and repeated {repeat} times")
    
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
    description="Generate HTTP debugging and troubleshooting guide"
)
async def http_debugging_guide(issue_type: str, status_code: str = "unknown") -> str:
    return f"""HTTP Debugging Guide

**Issue Type**: {issue_type}
**Status Code**: {status_code}

## Common HTTP Issues and Solutions

### 1. Connection Issues
- Check network connectivity
- Verify server is running and accessible
- Check firewall settings
- Validate SSL/TLS certificates

### 2. Request Issues
- Verify HTTP method (GET, POST, PUT, DELETE)
- Check request headers and content-type
- Validate request body format
- Ensure proper URL encoding

### 3. Response Issues
- Check response status codes
- Verify response headers
- Validate response body format
- Check for CORS issues

### 4. Performance Issues
- Monitor response times
- Check for timeouts
- Analyze server load
- Review caching strategies

### 5. Authentication Issues
- Verify credentials and tokens
- Check authorization headers
- Validate API keys
- Review session management

Use browser developer tools and HTTP clients for detailed debugging."""


# 资源
@mcp.resource(uri="mcp://server/info")
async def server_info_resource(ctx: Context) -> dict:
    """Comprehensive server information resource"""
    await ctx.info("Generating comprehensive server status report")
    
    return {
        "server_name": "Enhanced HTTP MCP Server",
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
    """Generate sample data resource"""
    await ctx.info(f"Generating sample data resource for type: {data_type}")
    
    sample_generators = {
        "users": lambda: [
            {"id": i, "name": f"User{i}", "email": f"user{i}@example.com", "active": random.choice([True, False])}
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


@mcp.resource(uri="mcp://weather/forecast/{city}")
async def weather_forecast_resource(city: str, ctx: Context) -> Dict[str, Any]:
    """Weather forecast resource for a specific city"""
    await ctx.info(f"Generating weather forecast for {city}")
    
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
    
    await ctx.info(f"Weather forecast generated for {city}")
    return forecast


async def main():
    """Main entry point for the HTTP server"""
    print("🚀 Starting Enhanced HTTP MCP Server with shared components...")
    print("📦 Features: Context logging, progress reporting, middleware")
    print("🔧 Architecture: Shared components from mcp-shared library")
    print("📡 Transport: Streamable HTTP (localhost:8000/mcp)")
    print("🌐 HTTP-specific: Request inspection, weather API, debugging tools")
    print("✅ Server ready for MCP client connections")
    
    # 使用 run_async 以支持异步环境
    await mcp.run_async(transport="streamable-http", host="localhost", port=8000, path="/mcp")


if __name__ == "__main__":
    asyncio.run(main())
