"""
FastMCP Study - Test Client
测试客户端，支持连接不同类型的 MCP 服务器进行功能测试
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import Optional
from fastmcp import Client


async def test_server_info(client: Client, server_type: str):
    """测试服务器信息工具"""
    print(f"🔍 Testing {server_type} server info...")
    try:
        result = await client.call_tool("get_server_info")
        print(f"✅ Server Info: {result}")
        return True
    except Exception as e:
        print(f"❌ Error getting server info: {e}")
        return False


async def test_math_operations(client: Client, server_type: str):
    """测试数学运算功能"""
    print(f"🧮 Testing {server_type} math operations...")
    try:
        if server_type == "stdio":
            # STDIO 服务器使用 math_operations
            result = await client.call_tool("math_operations", {
                "a": 10, "b": 5, "operation": "add"
            })
        else:
            # HTTP 服务器使用 calculate
            result = await client.call_tool("calculate", {
                "expression": "10 + 5 * 2"
            })
        print(f"✅ Math Result: {result}")
        return True
    except Exception as e:
        print(f"❌ Error in math operations: {e}")
        return False


async def test_text_operations(client: Client, server_type: str):
    """测试文本处理功能"""
    print(f"📝 Testing {server_type} text operations...")
    try:
        if server_type == "stdio":
            # STDIO 服务器使用 text_analyzer
            result = await client.call_tool("text_analyzer", {
                "text": "Hello FastMCP! This is a test message for analysis."
            })
        else:
            # HTTP 服务器使用 string_operations
            result = await client.call_tool("string_operations", {
                "text": "Hello FastMCP", "operation": "upper"
            })
        print(f"✅ Text Result: {result}")
        return True
    except Exception as e:
        print(f"❌ Error in text operations: {e}")
        return False


async def test_advanced_features(client: Client, server_type: str):
    """测试高级功能"""
    print(f"⚡ Testing {server_type} advanced features...")
    try:
        if server_type == "stdio":
            # 测试文件操作
            result = await client.call_tool("file_operations", {
                "operation": "list"
            })
            print(
                f"✅ File Operations: Found {len(result.get('files', []))} items")

            # 测试数据处理
            result2 = await client.call_tool("data_processor", {
                "data": [1, 2, 3, 4, 5], "operation": "statistics"
            })
            print(f"✅ Data Processing: {result2}")

        else:
            # 测试数据生成
            result = await client.call_tool("generate_data", {
                "data_type": "numbers", "count": 5
            })
            print(f"✅ Data Generation: {result}")

            # 测试天气功能
            result2 = await client.call_tool("get_weather", {
                "city": "Beijing", "days": 3
            })
            print(f"✅ Weather: {result2}")

        return True
    except Exception as e:
        print(f"❌ Error in advanced features: {e}")
        return False


async def test_resources(client: Client, server_type: str):
    """测试资源功能"""
    print(f"📚 Testing {server_type} resources...")
    try:
        # 列出可用资源
        resources = await client.list_resources()
        print(f"📋 Available resources: {len(resources)} found")

        if resources:
            # 读取第一个资源
            first_resource = resources[0]
            resource_uri = first_resource.uri
            print(f"🔍 Reading resource: {resource_uri}")

            content = await client.read_resource(resource_uri)
            print(f"✅ Resource content: {len(str(content))} characters")
            return True
        else:
            print("ℹ️  No resources available to test")
            return True

    except Exception as e:
        print(f"❌ Error testing resources: {e}")
        return False


async def run_comprehensive_test(server_type: str, server_path: Optional[str] = None):
    """运行全面的服务器测试"""
    print(f"🚀 Starting comprehensive test for {server_type.upper()} server")
    print("=" * 60)

    # 根据服务器类型创建客户端
    if server_type == "stdio":
        if server_path:
            client = Client(server_path)
        else:
            client = Client("projects/stdio-server/main.py")
    elif server_type == "http":
        if server_path:
            client = Client(server_path)
        else:
            client = Client("http://localhost:8000/mcp")
    else:
        print(f"❌ Unsupported server type: {server_type}")
        return False

    test_results = []

    try:
        async with client:
            # 测试连接
            print("🏓 Testing connection...")
            await client.ping()
            print("✅ Connection successful!")
            print()

            # 列出可用工具
            tools = await client.list_tools()
            print(f"🛠️  Available tools: {len(tools)} found")
            for tool in tools:
                print(f"   - {tool.name}: {tool.description}")
            print()

            # 运行各项测试
            test_results.append(await test_server_info(client, server_type))
            print()

            test_results.append(await test_math_operations(client, server_type))
            print()

            test_results.append(await test_text_operations(client, server_type))
            print()

            test_results.append(await test_advanced_features(client, server_type))
            print()

            test_results.append(await test_resources(client, server_type))
            print()

    except Exception as e:
        print(f"❌ Connection error: {e}")
        if server_type == "http":
            print("💡 Hint: Make sure the HTTP server is running on localhost:8000")
            print("   Run: uv run python projects/http-server/main.py")
        return False

    # 汇总测试结果
    print("=" * 60)
    passed = sum(test_results)
    total = len(test_results)
    print(f"📊 Test Results for {server_type.upper()} server:")
    print(f"   ✅ Passed: {passed}/{total}")
    print(f"   ❌ Failed: {total - passed}/{total}")

    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False


async def run_quick_test(server_type: str, tool_name: str, params: dict):
    """运行快速单个工具测试"""
    print(f"⚡ Quick test: {tool_name} on {server_type.upper()} server")

    # 创建客户端
    if server_type == "stdio":
        client = Client("projects/stdio-server/main.py")
    elif server_type == "http":
        client = Client("http://localhost:8000/mcp")
    else:
        print(f"❌ Unsupported server type: {server_type}")
        return

    try:
        async with client:
            await client.ping()
            result = await client.call_tool(tool_name, params)
            print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """主函数，解析命令行参数并运行测试"""
    parser = argparse.ArgumentParser(
        description="FastMCP Study - Test Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py stdio                    # Test STDIO server (comprehensive)
  python main.py http                     # Test HTTP server (comprehensive)
  python main.py stdio --quick get_server_info
  python main.py http --quick calculate --params '{"expression": "2+2"}'
  python main.py stdio --path "custom_server.py"
        """
    )

    parser.add_argument(
        "server_type",
        choices=["stdio", "http"],
        help="Type of MCP server to test"
    )

    parser.add_argument(
        "--quick",
        metavar="TOOL_NAME",
        help="Run quick test for a specific tool"
    )

    parser.add_argument(
        "--params",
        default="{}",
        help="JSON parameters for quick test (default: {})"
    )

    parser.add_argument(
        "--path",
        help="Custom server path/URL (overrides default)"
    )

    args = parser.parse_args()

    # 检查服务器文件是否存在（对于 stdio）
    if args.server_type == "stdio" and not args.path:
        server_file = Path("projects/stdio-server/main.py")
        if not server_file.exists():
            print(f"❌ Server file not found: {server_file}")
            print("Please make sure the STDIO server file exists")
            sys.exit(1)

    try:
        if args.quick:
            # 快速测试模式
            import json
            params = json.loads(args.params)
            asyncio.run(run_quick_test(args.server_type, args.quick, params))
        else:
            # 全面测试模式
            success = asyncio.run(run_comprehensive_test(
                args.server_type, args.path))
            sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
