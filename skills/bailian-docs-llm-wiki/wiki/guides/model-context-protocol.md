# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息交互通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配层，即可将第三方或自研服务统一接入智能体与工作流应用。该协议基于开源 [MCP 官方规范](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议（替代旧版 SSE），支持更稳定的长连接与结构化工具调用。

## 支持的模型/功能

MCP 本身不绑定特定模型，而是作为**工具调用协议层**，服务于百炼平台内的所有支持工具调用的大模型，包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 等通义千问系列模型。其核心能力体现在两类应用场景中：

- **智能体应用**：模型根据自然语言输入自动判断是否及何时调用 MCP 工具（如 `maps_route`、`web_search`），支持多工具协同与多轮调用。单个智能体最多可配置 5 个 MCP 服务 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：MCP 以显式节点形式嵌入流程图，每个 MCP 节点必须指定具体工具（如 `maps_weather`），并手动配置输入参数来源与输出参数传递路径，适用于确定性、可编排的任务链 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

> **注意**：文档 5 明确指出“MCP 服务不能在调用千问 API 时直接接入”，即 MCP 仅在百炼平台内建的智能体/工作流应用中生效，**不支持通过 `dashscope` SDK 直接调用千问模型时动态注入 MCP 工具**。外部 SDK 集成（见下文）是独立于模型 API 的 MCP Server 调用，而非模型侧工具增强。

## 关键参数

MCP 服务配置与调用涉及以下关键参数，需在不同环节正确设置：

| 参数类别 | 参数名 | 说明 | 示例值 |
|----------|--------|------|--------|
| **服务部署** | `type` | 通信协议类型，决定后端连接方式 | `"stdio"`（npx/uvx）、`"sse"`（旧版）、`"streamableHttp"`（新版推荐） |
| | `command` / `url` | 启动命令或远程服务地址 | `"npx"` 或 `"https://your-server/mcp"` |
| | `args` | 启动参数（Node.js/Python） | `["-y", "@modelcontextprotocol/server-memory"]` |
| **工具调用** | `tool.name` | 工具唯一标识符，由 MCP Server 提供 | `"web_search"`、`"maps_route"` |
| | `tool.inputSchema` | JSON Schema 描述输入参数结构 | `{"type": "object", "properties": {"query": {"type": "string"}}}` |
| | `DASHSCOPE_API_KEY` | 外部调用必需的身份凭证 | `sk-xxx`（需配置为环境变量或请求头） |
| **安全与计费** | KMS 凭据 | 敏感配置（如 API Key）的加密存储方式 | 在控制台创建并关联 KMS 密钥 |
| | 计费模式 | 自定义服务分“基础模式”（按调用时长计费）和“极速模式”（按部署+调用时长计费） | 基础模式费率：0.000156 元/秒 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md) |

## 使用方式

### 1. 接入官方 MCP 服务  
前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 `Amap Maps`、`WebSearch`），点击“立即开通”。开通后即可在智能体或工作流中直接添加使用，无需额外配置密钥（试用版）[原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 2. 部署自定义 MCP 服务  
支持三种方式：
- **脚本部署**：适用于开源或自研的 Node.js/Python MCP Server，通过函数计算 FC 托管，使用 `npx` 或 `uvx` 启动；
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 服务，需提前在 AI 网关完成托管；
- **OpenAPI 导入**：将阿里云产品（如 OSS、ECS）的 OpenAPI 快速发布为 MCP 工具 [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

### 3. 外部调用集成  
支持两种外部集成路径：
- **第三方 IDE 配置**：一键对接 Cherry Studio、Cursor，自动注入 MCP Server 配置；
- **SDK 编程集成**：使用 `mcp` Python SDK 连接 MCP Server，获取工具列表，并与 `openai` SDK 协同实现多轮工具调用循环（示例代码见文档 3）。

## 限制和注意事项

- **网络与资源限制**：MCP 服务运行于函数计算 FC，**无法访问用户本地资源（如本地文件、数据库）**；若需访问云数据库，必须配置 FC 的 VPC 网络打通或 IP 白名单 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：务必确认 `type` 字段与服务端端点路径严格匹配——`"sse"` 对应 `/sse`，`"streamableHttp"` 对应 `/mcp`；配置错误将导致 `11200058`（HTTP 405）或 `11200059`（HTTP 404）错误 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **版本与更新**：通过 `npx`/`uvx` 部署的服务**不会自动同步上游包更新**，版本变更后需手动重新部署；私有 npm/PyPI 包暂不支持直接部署 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **限流与额度**：部分服务（如 WebSearch）有明确调用限额（2000 次/月）和 QPS 限制（15 QPS），超限将返回 `11200051` 错误，需联系服务商申请扩容。
- **安全要求**：所有敏感配置（如第三方 API Key）必须通过 KMS 凭据加密，禁止明文写入配置代码。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


