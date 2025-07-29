"""
Shared prompt templates for FastMCP servers.
"""

from fastmcp import FastMCP


def create_data_analysis_prompt(mcp: FastMCP) -> None:
    """Create a data analysis prompt template"""

    @mcp.prompt(
        name="data_analysis_prompt",
        description="Generate data analysis queries and instructions"
    )
    async def data_analysis_prompt(objective: str, data_format: str = "JSON") -> str:
        return f"""You are a data analysis expert. Help analyze data with the following objective:

**Objective**: {objective}
**Data Format**: {data_format}

Please provide:
1. Recommended analysis approach
2. Key metrics to examine
3. Potential insights to look for
4. Visualization suggestions
5. Next steps for deeper analysis

Consider both statistical analysis and data quality checks in your recommendations."""


def create_troubleshooting_prompt(mcp: FastMCP) -> None:
    """Create a troubleshooting guide prompt"""

    @mcp.prompt(
        name="troubleshooting_guide",
        description="Generate troubleshooting steps for technical issues"
    )
    async def troubleshooting_guide(issue_type: str, context: str = "general") -> str:
        return f"""Technical Troubleshooting Guide

**Issue Type**: {issue_type}
**Context**: {context}

Follow this systematic troubleshooting approach:

## Step 1: Initial Assessment
- Gather error messages and symptoms
- Check system status and recent changes
- Verify basic connectivity and permissions

## Step 2: Common Resolutions
- Restart relevant services
- Clear caches and temporary files
- Check configuration files
- Verify dependencies

## Step 3: Advanced Diagnostics
- Enable debug logging
- Monitor system resources
- Test in isolated environment
- Check for known issues

## Step 4: Documentation
- Record findings and solutions
- Update documentation
- Create preventive measures

Remember to document each step and its outcome."""


def create_web_api_prompt(mcp: FastMCP) -> None:
    """Create a web API design prompt"""

    @mcp.prompt(
        name="web_api_request",
        description="Generate web API design and usage guidelines"
    )
    async def web_api_request(endpoint_purpose: str, method: str = "GET") -> str:
        return f"""Web API Design Guidelines

**Endpoint Purpose**: {endpoint_purpose}
**HTTP Method**: {method}

## Design Considerations

### 1. URL Structure
- Use RESTful conventions
- Include version in path (/api/v1/)
- Use clear, descriptive resource names
- Follow hierarchical relationships

### 2. Request/Response Format
- Use JSON for data exchange
- Include proper HTTP status codes
- Implement consistent error responses
- Add pagination for collections

### 3. Security
- Implement authentication/authorization
- Use HTTPS for all communications
- Validate all input parameters
- Rate limiting and throttling

### 4. Documentation
- Provide clear API documentation
- Include request/response examples
- Document error scenarios
- Version changelog

### 5. Testing
- Unit tests for all endpoints
- Integration testing
- Load testing for performance
- Security testing

Design your API to be intuitive, secure, and maintainable."""
