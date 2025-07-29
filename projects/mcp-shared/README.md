# MCP Shared

FastMCP 服务器的共享工具和组件库。

## 功能

这个共享库提供：

- 标准中间件设置
- 可重用的工具实现
- 提示模板
- 上下文感知日志记录

## 使用

在 FastMCP 服务器中导入和使用共享组件：

```python
from mcp_shared import (
    setup_middleware,
    create_server_info_tool,
    create_math_tool,
    create_string_tool,
    create_data_generator_tool,
    create_data_analysis_prompt,
    create_troubleshooting_prompt,
    create_web_api_prompt,
)
```
