# Stdio MCP 服务器

这是一个使用 stdio 传输协议的 MCP (Model Context Protocol) 服务器示例。

## 功能

这个服务器提供以下工具：

- `get_current_time()`: 获取当前时间
- `add_numbers(a, b)`: 计算两个数字的和
- `greet(name)`: 按名字问候

## 运行

```bash
# 安装依赖
uv sync

# 运行服务器
uv run python main.py
```

## 作为 MCP 客户端使用

在 MCP 客户端配置中，可以这样配置：

```json
{
  "mcpServers": {
    "stdio-server": {
      "command": "uv",
      "args": ["run", "python", "/path/to/servers/stdio-server/main.py"]
    }
  }
}
```

## 协议

- **传输协议**: stdio
- **通信方式**: 标准输入/输出流
- **用途**: 适合作为子进程运行的 MCP 服务器
