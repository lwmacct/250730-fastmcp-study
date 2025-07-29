"""
FastMCP Study - 测试客户端
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
    print(f"🔍 测试 {server_type} 服务器信息...")
    try:
        result = await client.call_tool("get_server_info")
        print(f"✅ 服务器信息: {result}")
        return True
    except Exception as e:
        print(f"❌ 获取服务器信息时出错: {e}")
        return False


async def test_math_operations(client: Client, server_type: str):
    """测试数学运算功能"""
    print(f"🧮 测试 {server_type} 数学运算...")
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
        print(f"✅ 数学运算结果: {result}")
        return True
    except Exception as e:
        print(f"❌ 数学运算出错: {e}")
        return False


async def test_text_operations(client: Client, server_type: str):
    """测试文本处理功能"""
    print(f"📝 测试 {server_type} 文本操作...")
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
        print(f"✅ 文本操作结果: {result}")
        return True
    except Exception as e:
        print(f"❌ 文本操作出错: {e}")
        return False


async def test_advanced_features(client: Client, server_type: str):
    """测试高级功能"""
    print(f"⚡ 测试 {server_type} 高级功能...")
    try:
        if server_type == "stdio":
            # 测试文件操作
            result = await client.call_tool("file_operations", {
                "operation": "list"
            })
            print(
                f"✅ 文件操作: 找到 {len(result.get('files', []))} 个项目")

            # 测试数据处理
            result2 = await client.call_tool("data_processor", {
                "data": [1, 2, 3, 4, 5], "operation": "statistics"
            })
            print(f"✅ 数据处理: {result2}")

        else:
            # 测试数据生成
            result = await client.call_tool("generate_data", {
                "data_type": "numbers", "count": 5
            })
            print(f"✅ 数据生成: {result}")

            # 测试天气功能
            result2 = await client.call_tool("get_weather", {
                "city": "Beijing", "days": 3
            })
            print(f"✅ 天气信息: {result2}")

        return True
    except Exception as e:
        print(f"❌ 高级功能测试出错: {e}")
        return False


async def test_resources(client: Client, server_type: str):
    """测试资源功能"""
    print(f"📚 测试 {server_type} 资源...")
    try:
        # 列出可用资源
        resources = await client.list_resources()
        print(f"📋 可用资源: 找到 {len(resources)} 个")

        if resources:
            # 读取第一个资源
            first_resource = resources[0]
            resource_uri = first_resource.uri
            print(f"🔍 读取资源: {resource_uri}")

            content = await client.read_resource(resource_uri)
            print(f"✅ 资源内容: {len(str(content))} 个字符")
            return True
        else:
            print("ℹ️  没有可测试的资源")
            return True

    except Exception as e:
        print(f"❌ 测试资源时出错: {e}")
        return False


async def run_comprehensive_test(server_type: str, server_path: Optional[str] = None):
    """运行全面的服务器测试"""
    print(f"🚀 开始 {server_type.upper()} 服务器的全面测试")
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
        print(f"❌ 不支持的服务器类型: {server_type}")
        return False

    test_results = []

    try:
        async with client:
            # 测试连接
            print("🏓 测试连接...")
            await client.ping()
            print("✅ 连接成功!")
            print()

            # 列出可用工具
            tools = await client.list_tools()
            print(f"🛠️  可用工具: 找到 {len(tools)} 个")
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
        print(f"❌ 连接错误: {e}")
        if server_type == "http":
            print("💡 提示: 确保 HTTP 服务器在 localhost:8000 上运行")
            print("   运行: uv run python projects/http-server/main.py")
        return False

    # 汇总测试结果
    print("=" * 60)
    passed = sum(test_results)
    total = len(test_results)
    print(f"📊 {server_type.upper()} 服务器测试结果:")
    print(f"   ✅ 通过: {passed}/{total}")
    print(f"   ❌ 失败: {total - passed}/{total}")

    if passed == total:
        print("🎉 所有测试通过!")
        return True
    else:
        print("⚠️  部分测试失败")
        return False


async def run_quick_test(server_type: str, tool_name: str, params: dict):
    """运行快速单个工具测试"""
    print(f"⚡ 快速测试: {tool_name} 在 {server_type.upper()} 服务器上")

    # 创建客户端
    if server_type == "stdio":
        client = Client("projects/stdio-server/main.py")
    elif server_type == "http":
        client = Client("http://localhost:8000/mcp")
    else:
        print(f"❌ 不支持的服务器类型: {server_type}")
        return

    try:
        async with client:
            await client.ping()
            result = await client.call_tool(tool_name, params)
            print(f"✅ 结果: {result}")
    except Exception as e:
        print(f"❌ 错误: {e}")


def main():
    """主函数，解析命令行参数并运行测试"""
    parser = argparse.ArgumentParser(
        description="FastMCP Study - 测试客户端",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py stdio                    # 测试 STDIO 服务器 (全面测试)
  python main.py http                     # 测试 HTTP 服务器 (全面测试)
  python main.py stdio --quick get_server_info
  python main.py http --quick calculate --params '{"expression": "2+2"}'
  python main.py stdio --path "custom_server.py"
        """
    )

    parser.add_argument(
        "server_type",
        choices=["stdio", "http"],
        help="要测试的 MCP 服务器类型"
    )

    parser.add_argument(
        "--quick",
        metavar="TOOL_NAME",
        help="运行特定工具的快速测试"
    )

    parser.add_argument(
        "--params",
        default="{}",
        help="快速测试的 JSON 参数 (默认: {})"
    )

    parser.add_argument(
        "--path",
        help="自定义服务器路径/URL (覆盖默认值)"
    )

    args = parser.parse_args()

    # 检查服务器文件是否存在（对于 stdio）
    if args.server_type == "stdio" and not args.path:
        server_file = Path("projects/stdio-server/main.py")
        if not server_file.exists():
            print(f"❌ 服务器文件未找到: {server_file}")
            print("请确保 STDIO 服务器文件存在")
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
        print("\n🛑 用户中断测试")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 意外错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
