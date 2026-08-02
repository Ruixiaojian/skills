# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等服务）之间建立安全、可扩展的信息通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并针对百炼平台进行了工程化增强和托管支持。

## 支持的模型/功能

MCP 本身不绑定特定模型，而是作为**能力接入层**服务于百炼平台上的所有支持工具调用的大模型，当前主要覆盖：

- **智能体应用**：支持自动推理并动态调用已配置的 MCP 服务（如 `maps_route`, `maps_weather`, `web_search`），最多同时启用 5 个服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：支持显式编排 MCP 节点，每个节点需手动指定一个工具（如 `Amap Maps` 的 `maps_weather`），并通过参数传递链路串联上下游 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **外部客户端集成**：支持通过 Streamable HTTP 或 SSE 协议，将百炼托管的 MCP 服务接入 Cherry Studio、Cursor 等第三方 IDE 工具，或通过 SDK 集成至自有项目 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：MCP 服务**不能直接用于调用千问 API**（如 `qwen-max` 的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)），仅限在百炼平台内构建的智能体或工作流应用中使用 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

MCP 服务配置与调用涉及以下核心参数，需在不同环节正确设置：

| 参数类别 | 参数名 | 说明 | 示例值 |
|----------|--------|------|--------|
| **服务元信息** | `服务名称` / `描述` | 仅用于控制台识别，不影响模型调用逻辑 | `"高德天气"` / `"查询城市实时天气预报"` |
| **部署配置** | `安装方式` | 决定运行时环境：`npx`（Node.js）、`uvx`（Python）、`http`（远程 SSE/Streamable HTTP） | `"npx"` |
| | `部署方式` | 影响计费与延迟：`基础模式`（按次计费，有冷启动）、`极速模式`（常驻计费，低延迟） | `"基础模式：按次计费"` |
| | `MCP 服务配置` | JSON 格式定义服务端点，必须严格匹配协议类型与路径 | `{ "mcpServers": { "weather": { "type": "streamableHttp", "url": "https://.../mcp" } } }` |
| **工具调用** | `tool.name` | 模型调用时使用的工具标识符，由 MCP 服务返回的 `list_tools()` 接口提供 | `"maps_weather"` |
| | `inputSchema` | 工具输入参数的 JSON Schema，模型据此生成结构化参数 | `{"type": "object", "properties": {"city": {"type": "string"}}}` |

## 使用方式

### 1. 接入官方 MCP 服务  
前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 `Amap Maps`）→ 点击 **立即开通** → 在智能体/工作流编辑器中添加该服务即可使用。敏感参数（如 API Key）需通过 KMS 凭据加密管理 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 2. 部署自定义 MCP 服务  
支持三种方式：
- **脚本部署**：适用于开源或自研 MCP 服务代码包，通过函数计算 FC 托管，使用 `npx`/`uvx` 启动；
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具；
- **OpenAPI 导入**：将阿里云产品（如 OSS、ECS）操作封装为 MCP 工具 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

### 3. 外部调用集成  
- **第三方应用**：一键配置至 Cherry Studio/Cursor，自动注入 MCP Server 配置；
- **自有项目**：使用 `mcp` SDK（如 `streamablehttp_client`）连接百炼 MCP Endpoint，配合 OpenAI SDK 实现多轮工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与资源限制**：MCP 服务运行于函数计算 FC，**无法访问用户本地数据库或硬件资源**；若需访问云数据库，须配置 FC IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：百炼已全面升级至 **Streamable HTTP 协议**（`/mcp` 端点），旧版 SSE（`/sse`）需手动取消再重新开通以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **部署约束**：
  - 私有 npm/PyPI 包暂不支持直接部署，需发布至公共仓库；
  - `npx`/`uvx` 部署的服务版本更新后**不会自动同步**，需手动重新部署；
  - 本地依赖文件系统或 GUI 的 MCP Server 不适合云端部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **Token 开销**：MCP 返回结果会作为上下文注入模型输入，**直接增加输入 Token 数量**；更丰富的上下文也可能导致输出更详细，间接增加输出 Token [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


