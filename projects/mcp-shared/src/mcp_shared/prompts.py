"""
FastMCP 服务器的共享提示模板。
"""

from fastmcp import FastMCP


def create_data_analysis_prompt(mcp: FastMCP) -> None:
    """创建数据分析提示模板"""

    @mcp.prompt(
        name="data_analysis_prompt",
        description="生成数据分析查询和指令"
    )
    async def data_analysis_prompt(objective: str, data_format: str = "JSON") -> str:
        return f"""您是一位数据分析专家。帮助分析具有以下目标的数据:

**目标**: {objective}
**数据格式**: {data_format}

请提供:
1. 推荐的分析方法
2. 要检查的关键指标
3. 要寻找的潜在洞察
4. 可视化建议
5. 深入分析的后续步骤

在您的建议中考虑统计分析和数据质量检查。"""


def create_troubleshooting_prompt(mcp: FastMCP) -> None:
    """创建故障排除指南提示"""

    @mcp.prompt(
        name="troubleshooting_guide",
        description="为技术问题生成故障排除步骤"
    )
    async def troubleshooting_guide(issue_type: str, context: str = "general") -> str:
        return f"""技术故障排除指南

**问题类型**: {issue_type}
**上下文**: {context}

按照这个系统性的故障排除方法:

## 步骤 1: 初步评估
- 收集错误消息和症状
- 检查系统状态和最近更改
- 验证基本连接和权限

## 步骤 2: 常见解决方案
- 重启相关服务
- 清除缓存和临时文件
- 检查配置文件
- 验证依赖项

## 步骤 3: 高级诊断
- 启用调试日志
- 监控系统资源
- 在隔离环境中测试
- 检查已知问题

## 步骤 4: 文档记录
- 记录发现和解决方案
- 更新文档
- 创建预防措施

记住记录每个步骤及其结果。"""


def create_web_api_prompt(mcp: FastMCP) -> None:
    """创建 Web API 设计提示"""

    @mcp.prompt(
        name="web_api_request",
        description="生成 Web API 设计和使用指南"
    )
    async def web_api_request(endpoint_purpose: str, method: str = "GET") -> str:
        return f"""Web API 设计指南

**端点目的**: {endpoint_purpose}
**HTTP 方法**: {method}

## 设计考虑因素

### 1. URL 结构
- 使用 RESTful 约定
- 在路径中包含版本 (/api/v1/)
- 使用清晰、描述性的资源名称
- 遵循层次关系

### 2. 请求/响应格式
- 使用 JSON 进行数据交换
- 包含适当的 HTTP 状态码
- 实现一致的错误响应
- 为集合添加分页

### 3. 安全性
- 实现身份验证/授权
- 对所有通信使用 HTTPS
- 验证所有输入参数
- 速率限制和节流

### 4. 文档
- 提供清晰的 API 文档
- 包含请求/响应示例
- 记录错误场景
- 版本变更日志

### 5. 测试
- 所有端点的单元测试
- 集成测试
- 性能负载测试
- 安全测试

设计您的 API 使其直观、安全且可维护。"""
