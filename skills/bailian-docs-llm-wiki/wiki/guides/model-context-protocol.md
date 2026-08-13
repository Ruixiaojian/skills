# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等服务）之间建立安全、可扩展的信息交互通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中统一接入和编排多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官方规范](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 支持的模型/功能

MCP 本身不绑定特定模型，而是作为**能力接入层**，供百炼平台内所有支持工具调用的模型使用。当前已在以下两类应用中全面支持：

- **智能体应用**：大模型根据对话上下文自动判断是否调用、调用哪个 MCP 工具及传入参数，支持最多同时配置 5 个 MCP 服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式添加 MCP 节点并手动指定所用工具（如 `maps_weather`），输入参数须由前置节点（如大模型节点）结构化提取，输出参数可传递至后续节点 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

支持的服务类型包括：
- **官方 MCP 服务**：如 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）、QuickChart（图表生成）等，开通即用，部分限时免费 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
- **自定义 MCP 服务**：支持三种部署方式：
  - *脚本部署*（npx/uvx）：适用于 Node.js/Python 开发的开源或自研 MCP Server；
  - *AI 网关导入*：将现有 RESTful API 封装为 MCP 工具；
  - *OpenAPI 导入*：将阿里云产品（如 OSS、ECS）操作封装为 MCP 工具 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 中提到“MCP 服务能在其他 MCP 客户端（Cherry Studio、Cursor）中使用”，而文档 5 明确指出“MCP 服务需集成在智能体或工作流应用中使用，不能直接在调用千问 API 时接入”。二者无矛盾——前者指**外部客户端通过百炼 MCP 服务端接入**，后者强调**百炼 MCP 不支持直连 DashScope Qwen API 的原生调用**，必须经由百炼应用容器（智能体/工作流）调度。

## 关键参数

MCP 服务配置与调用涉及以下核心参数：

| 参数类别 | 参数名 | 说明 | 示例/约束 |
|----------|--------|------|-----------|
| **服务配置** | `service_name` | 服务唯一标识名，仅用于控制台区分，不影响模型调用逻辑 | `"长期记忆"` |
| | `description` | 服务功能描述，供模型理解能力边界 | `"记录个性化信息并在后续交互中调用"` |
| | `type` | 协议传输类型，决定后端连接方式 | `"stdio"`（本地进程）、`"sse"`（Server-Sent Events）、`"streamableHttp"`（HTTP POST `/mcp`） |
| | `url` / `command` / `args` | 远程服务地址 或 本地启动命令及参数 | `https://your-mcp-server/sse` 或 `["npx", "-y", "@your_pkg"]` |
| **工具调用** | `tool_name` | 工具函数名，模型在 `tool_calls` 中指定 | `"maps_weather"` |
| | `inputSchema` | JSON Schema 格式定义输入参数结构 | `{ "type": "object", "properties": { "city": { "type": "string" } } }` |
| | `env` | 环境变量（如 API Key），敏感值需通过 KMS 凭据加密 | `{"AMAP_MAPS_API_KEY": "kms://xxx"}` |

> **注意**：文档 3 的配置模板中 `mcpServers` 对象下 `type` 字段未显式声明（如 `"type": "stdio"`），但文档 5 的错误码说明（11200058）明确要求 `type` 必须与端点路径严格匹配（`"sse"` → `/sse`，`"streamableHttp"` → `/mcp`）。实际部署时务必补全 `type` 字段，否则触发 `MCP_SERVER_HTTP_METHOD_NOT_ALLOWED` 错误 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

## 使用方式

### 1. 开通服务
- 访问 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务卡片 → **立即开通**。
- 敏感凭证（如 API Key）需通过 KMS 凭据加密管理 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 2. 集成到应用
- **智能体**：创建智能体 → 在「MCP 服务」配置页添加已开通服务 → 测试对话触发自动调用。
- **工作流**：创建工作流 → 拖入 MCP 节点 → 选择工具 → 绑定输入（如引用上游节点输出）→ 连接下游节点 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 3. 外部调用
- **第三方应用集成**：在 MCP 服务详情页「外部调用」中选择 Cherry Studio/Cursor → 一键配置或手动导入 JSON 配置。
- **SDK 编码集成**：使用 `mcp` SDK 连接百炼 MCP Server（URL 形如 `https://dashscope.aliyuncs.com/api/v1/mcps/{service}/mcp`），配合 [OpenAI 兼容接口](../concepts/openai-compatibility.md)实现多轮工具调用 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **地域与网络**：自定义 MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 FC IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **本地资源限制**：MCP 服务**无法访问用户本地文件、硬件或数据库**，依赖本地资源的服务需在本地部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **计费模式**：
  - *云部署服务*：部署免费；调用按第三方 API 实际消耗计费（如 WebSearch：2000 次/月免费，超量 29 元/千次）[模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
  - *自定义服务*：基础模式（按调用时长 0.000156 元/秒）；极速模式（另加部署时长 0.000036 元/秒）[模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
- **协议兼容性**：百炼已全面升级至 **Streamable HTTP 协议**（`/mcp` 端点），旧版 SSE（`/sse`）需手动取消再重新开通以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **[Token](../concepts/token.md) 开销**：MCP 返回结果会作为上下文注入模型输入，**显著增加输入 [Token](../concepts/token.md) 数量**；模型响应可能因信息更丰富而变长，间接增加输出 [Token](../concepts/token.md) [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


