# FastMCP Study Project - Code Reuse with Shared Components

本项目演示了如何使用 `uv` 工作空间和共享库来消除 FastMCP 服务器之间的重复代码。

## 🏗️ 项目架构

### 工作空间结构
```
250730-fastmcp-study/
├── main.py                    # 测试客户端
├── pyproject.toml             # 根工作空间配置
├── packages/
│   └── mcp-shared/           # 共享组件库
│       ├── src/mcp_shared/
│       │   ├── __init__.py
│       │   ├── middleware.py  # 中间件组件
│       │   ├── tools.py      # 可复用工具
│       │   └── prompts.py    # 提示模板
│       └── pyproject.toml
└── servers/
    ├── stdio-server/         # STDIO 传输服务器
    │   ├── main.py
    │   └── pyproject.toml
    └── http-server/          # HTTP 传输服务器
        ├── main.py
        └── pyproject.toml
```

### 🔄 代码复用设计

#### 共享组件库 (`packages/mcp-shared`)

**1. 共享工具 (`tools.py`)**
- `create_server_info_tool()` - 服务器信息工具
- `create_math_tool()` - 数学计算工具
- `create_string_tool()` - 字符串操作工具  
- `create_data_generator_tool()` - 数据生成工具

**2. 共享提示模板 (`prompts.py`)**
- `create_data_analysis_prompt()` - 数据分析提示
- `create_troubleshooting_prompt()` - 故障排除提示
- `create_web_api_prompt()` - Web API 提示

**3. 中间件支持 (`middleware.py`)**
- `setup_middleware()` - 标准中间件设置（为未来扩展保留）

#### 服务器实现

**STDIO 服务器特性:**
- 使用所有共享工具和提示
- 专用工具：时间获取、数学操作、文本分析、数据处理、多语言问候
- 动态资源：服务器状态、示例数据、系统信息

**HTTP 服务器特性:**
- 使用所有共享工具和提示
- 专用工具：HTTP 请求检查、天气模拟、消息回声
- HTTP 调试提示模板
- 动态资源：服务器信息、示例数据、天气预报

## 🚀 使用方法

### 安装依赖
```bash
uv sync
```

### 测试服务器

**快速测试:**
```bash
# 测试 STDIO 服务器
uv run python main.py stdio --quick get_server_info

# 测试共享数学工具
uv run python main.py stdio --quick calculate --params '{"expression": "2+3*4"}'

# 测试共享字符串工具
uv run python main.py stdio --quick string_operations --params '{"text": "Hello", "operation": "upper"}'
```

**完整测试:**
```bash
# 运行所有 STDIO 测试
uv run python main.py stdio

# 运行所有 HTTP 测试
uv run python main.py http
```

## 📊 代码复用效果

### 消除的重复代码
- **中间件设置** - 统一的错误处理和日志记录
- **核心工具** - 数学、字符串、数据生成等通用功能
- **提示模板** - LLM 交互的结构化模板
- **Context 注入** - 标准化的上下文感知日志记录

### 架构优势
1. **DRY 原则** - 不重复代码，单一数据源
2. **易维护性** - 共享组件的修改自动影响所有服务器
3. **一致性** - 所有服务器使用相同的工具行为
4. **可扩展性** - 新服务器可轻松重用现有组件

### 工作空间配置 (`pyproject.toml`)
```toml
[tool.uv.workspace]
members = [
    "servers/stdio-server",
    "servers/http-server", 
    "packages/mcp-shared",
]
```

服务器通过以下方式引用共享库:
```toml
dependencies = ["mcp-shared"]

[tool.uv.sources]
mcp-shared = { workspace = true }
```

## 🛠️ 技术栈

- **uv** - Python 包管理和工作空间
- **FastMCP 2.10.6** - MCP 服务器框架
- **工作空间成员** - stdio-server, http-server, mcp-shared
- **传输协议** - STDIO, Streamable HTTP

## 📈 测试状态

✅ **STDIO 服务器** - 完全工作，所有工具和资源正常  
⚠️ **HTTP 服务器** - 共享组件工作，HTTP 特定功能需要进一步调试  
✅ **共享库** - 成功消除代码重复，所有工具正常运行

这个架构演示了如何在 FastMCP 项目中有效实现代码复用，大大减少了维护成本并提高了代码质量。
