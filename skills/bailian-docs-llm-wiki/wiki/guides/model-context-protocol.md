# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的上下文传递通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配层，即可在智能体或工作流中声明式接入多种能力。MCP 协议本身遵循 [Anthropic 提出的开源标准](https://modelcontextprotocol.io/)，百炼在此基础上提供了云托管、自定义部署和外部集成全链路支持。

## 支持的模型/功能

MCP 服务**不直接绑定特定大模型**，而是作为独立能力模块被智能体（Agent）或工作流（Workflow）调用。当前百炼平台支持以下两类 MCP 服务：

- **官方 MCP 服务**：由阿里云预部署并维护，开箱即用，包括 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）、Sequential Thinking（逻辑推理）、QuickChart（图表生成）等。其中 Amap Maps 服务限时免费，[联网搜索MCP服务](https://bailian.console.aliyun.com/cn-beijing?tab=app#/mcp-market/detail/WebSearch)提供 2000 次/月免费额度 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
- **自定义 MCP 服务**：支持三种部署方式：
  - **使用脚本部署**（`npx`/`uvx`）：适用于已发布至 npm 或 PyPI 的开源或自研 MCP Server；
  - **从 AI 网关导入**：将现有 RESTful API 封装为 MCP 接口；
  - **从阿里云 OpenAPI 导入**：将 OSS、ECS 等云产品 OpenAPI 快速转为 MCP 工具 [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 3 明确指出“阿里云百炼 MCP 服务不能在调用千问 API 时直接接入”，即 MCP 仅支持集成于百炼平台内的智能体或工作流应用，**不可用于直连 `dashscope` SDK 的纯 API 调用场景** [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

MCP 服务配置的核心参数均在创建/导入时指定，关键项如下：

| 参数 | 说明 | 示例值 |
|--------|------|---------|
| `service name` / `description` | 仅用于控制台识别，不影响模型调用逻辑 | `"长期记忆"`, `"该服务使大模型能够记录个性化信息..."` |
| `install method` | 决定运行环境与启动方式 | `npx`, `uvx`, `http`（对应 `stdio` 或 `sse/streamableHttp` 类型） |
| `deployment mode` | 影响计费与延迟 | `基础模式：按次计费`（冷启动延迟）、`极速模式`（常驻，需额外部署费） |
| `mcpServers` 配置块 | 定义实际服务端点，必须严格匹配协议类型 | `{"memory": {"command": "npx", "args": ["@modelcontextprotocol/server-memory"]}}` |
| `url`（HTTP/SSE 模式） | 必须与 `type` 字段一致：`"sse"` → `GET /sse`；`"streamableHttp"` → `POST /mcp` | `"https://your-server/sse"` |

所有自定义服务均需确保其符合 MCP 协议规范，否则会触发 `11200054 - MCP_PROTOCOL_ERROR` 等错误码 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 使用方式

### 在平台内集成
- **智能体应用**：最多可同时启用 5 个 MCP 服务。模型根据提示词自动判断是否调用及调用哪个工具，例如输入“从杭州萧山国际机场到杭州西湖景区”将触发 Amap Maps 的路径规划 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：每个 MCP 节点需**手动指定具体工具名**（如 `maps_weather`）和输入参数（支持变量引用），适用于确定性编排场景。

### 外部调用
- **第三方应用集成**：支持一键配置至 Cherry Studio、Cursor 等工具，自动注入 `DASHSCOPE_API_KEY` 和服务地址。
- **SDK 编程集成**：推荐使用 `mcp` Python SDK + `OpenAI` 兼容客户端，通过 `streamablehttp_client` 连接 `/mcp` 端点，实现工具发现（`list_tools`）与调用（`call_tool`）全流程 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与资源限制**：MCP 服务运行于函数计算（FC），**无法访问用户本地资源（如本地数据库、文件）**；若需访问云数据库，必须配置 FC 出口 IP 白名单或 VPC 打通 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：百炼已全面升级至 **Streamable HTTP 协议**（`POST /mcp`），旧版 SSE（`GET /sse`）需手动取消再重新开通以完成升级 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **版本与更新**：通过 `npx`/`uvx` 部署的服务**不会自动更新**，包版本变更后必须手动重新部署 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **安全要求**：部署自定义 MCP 服务前，务必核实源代码可信度；涉及敏感参数（如 API Key）必须通过 KMS 凭据加密，禁止明文配置。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)


