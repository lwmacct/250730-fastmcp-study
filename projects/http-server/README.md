# HTTP MCP Server

这是一个使用 streamable-http (SSE) 传输协议的 MCP (Model Context Protocol) 服务器示例。

## 功能

这个服务器提供以下工具：

- `get_server_info()`: 获取服务器信息
- `calculate(expression)`: 安全地计算数学表达式
- `echo(message)`: 回显消息
- `get_weather(city)`: 获取模拟天气信息

## 运行

```bash
# 安装依赖
uv sync

# 运行服务器
uv run python main.py
```

服务器将在 `http://localhost:8000` 启动。

## 作为 MCP 客户端使用

在 MCP 客户端配置中，可以这样配置：

```json
{
  "mcpServers": {
    "http-server": {
      "baseUrl": "http://localhost:8000"
    }
  }
}
```

## 协议

- **传输协议**: streamable-http (Server-Sent Events)
- **端口**: 8000
- **地址**: localhost
- **用途**: 适合通过 HTTP 网络访问的 MCP 服务器

## API 端点

- `GET /sse/messages` - MCP 消息流 (SSE)
- `POST /messages` - 发送 MCP 消息
