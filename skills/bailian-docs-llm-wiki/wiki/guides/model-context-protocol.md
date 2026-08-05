# model context protocol

Model Context Protocol（MCP）是阿里云百炼平台支持的标准化工具调用协议，用于将外部能力（如地图、天气、图表生成等）以结构化方式注入大模型推理流程。它既兼容 Anthropic 提出的开源 [MCP 协议](https://modelcontextprotocol.io/) 标准，又深度集成于百炼的智能体与工作流应用中，支持云托管服务与自定义部署两种模式。开发者可通过控制台一键开通官方 MCP 服务，或自主部署符合协议的第三方/自研服务。

## 支持的模型与功能

- **适用场景**：MCP 服务仅可在百炼平台内的 **智能体应用** 和 **工作流应用** 中使用，不支持直接接入千问 API 调用链（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。  
- **官方服务**：已预置 Amap Maps、Sequential Thinking、QuickChart 等开箱即用的云托管 MCP 服务，部分限时免费（如 Amap Maps），详情参见 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。  
- **自定义服务**：支持通过 `npx`（Node.js）、`uvx`（Python）或 SSE 连接方式部署私有 MCP Server；但要求服务可云端托管、无需本地资源访问（如文件、硬件），且必须发布至公共 npm/PyPI 仓库（私有仓库暂不支持）。

> **注意**：文档 1 称“MCP 服务支持在平台内部（如智能体、工作流）直接集成”，而文档 2 明确指出“MCP 服务**不能在调用千问 API 时接入**”。二者无矛盾，但需强调：MCP 是百炼应用层能力，非底层 API 功能。

## 关键参数

- **传输类型（`type`）**：必须与端点路径严格匹配：
  - `"sse"` → 对应 GET `/sse` 端点；
  - `"streamableHttp"` → 对应 POST `/mcp` 端点。  
  配置错误将触发错误码 `11200058`（HTTP 405）或 `11200059`（HTTP 404）（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **鉴权参数**：云部署服务（如 Amap Maps）默认免填 API Key；但第三方服务（如 Firecrawl）需手动配置有效 `API-Key`，否则报错“请求用量受限/余额不足”或 `MCP_SERVER_HTTP_UNAUTHORIZED`（11200049）。
- **安全参数**：涉及敏感数据（如数据库凭证）的服务，须通过 KMS 凭据加密管理（见 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)）。

## 使用方式

- **智能体应用**：  
  最多可同时添加 5 个 MCP 服务；模型根据对话自动判断是否调用及选择工具（如“从杭州萧山国际机场到西湖”触发 Amap Maps 路径规划）。无需手动指定参数，依赖模型理解力。
- **工作流应用**：  
  每个 MCP 节点**仅能绑定一个工具**（如 `maps_weather`），需显式配置输入参数（如通过前置大模型节点提取城市名），并手动传递输出至下游节点（如“信息总结”节点）。  
- **外部调用**：  
  支持通过 HTTP/SSE 集成至第三方客户端（如 Cherry Studio、Cursor），具体方式参考 [外部调用](https://help.aliyun.com/zh/model-studio/mcp-external-calls)（文档 1 中提及）。

## 限制和注意事项

- **网络与权限**：  
  - MCP 服务托管于函数计算 FC，**无固定出口公网 IP**，访问云数据库等远程资源需配置 IP 白名单或 VPC 打通（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。  
  - **不支持访问本地资源**（如本地文件、数据库、硬件设备），此类服务应在本地部署。
- **[Token](../concepts/token.md) 开销**：  
  调用 MCP 会增加模型输入 [Token](../concepts/token.md)（返回结果作为上下文注入）和潜在输出 [Token](../concepts/token.md)（因上下文更丰富，响应可能更长）。
- **服务可用性**：  
  - 官方服务稳定性由阿里云保障；第三方/自定义服务由提供方负责，百炼仅提供接入渠道，“不保证其一直可用”（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。  
  - 自定义服务版本更新后**不会自动同步**，需手动重新部署。
- **错误排查**：  
  常见错误码（如 `11200044` 连接拒绝、`11200047` 网络错误）均需结合 `curl` 连通性测试、FC 日志及下游服务文档定位（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


