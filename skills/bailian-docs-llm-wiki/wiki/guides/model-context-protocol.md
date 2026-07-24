# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化机制，用于在大语言模型与外部工具（如地图、搜索、图表生成等服务）之间建立安全、可扩展的上下文交互通道。它屏蔽了底层接口差异，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式接入第三方能力。该协议基于 Anthropic 提出的开源标准 [MCP 官方规范](https://modelcontextprotocol.io/) 实现，并针对百炼平台进行了生产级增强与托管支持。

## 支持的模型/功能

MCP 本身不绑定特定模型，而是作为**上下文增强层**服务于百炼平台上的所有支持工具调用的大模型应用，当前主要覆盖：

- **智能体应用**：支持自动推理并动态调用已配置的 MCP 服务（如 `maps_route`, `maps_weather`, `web_search`），最多同时启用 5 个服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：支持显式编排 MCP 节点，每个节点绑定一个具体工具（如 `amap-maps/maps_weather`），需手动传递输入参数并处理输出 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **外部调用场景**：支持通过 Streamable HTTP 协议（推荐）或 SSE 协议，集成至 Cherry Studio、Cursor 等第三方客户端，或通过 `mcp` SDK 在自有项目中编程调用 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：MCP 服务**不能直接接入千问 API 的原始调用链路**，仅限百炼平台内智能体/工作流应用或通过外部调用协议集成。详见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) 第三节第3条。

## 关键参数

| 参数 | 说明 | 示例/取值 |
|------|------|-----------|
| `service_name` | 服务唯一标识，仅用于控制台区分，不影响模型调用逻辑 | `"长期记忆"`, `"Amap Maps"` |
| `tool_name` | 工具名称，模型在 function calling 中实际引用的名称 | `"maps_weather"`, `"web_search"` |
| `inputSchema` | JSON Schema 格式定义的工具输入参数结构，影响模型参数生成准确性 | `{ "type": "object", "properties": { "city": { "type": "string" } } }` |
| `transport_type` | 传输协议类型，决定连接方式与端点路径 | `"streamableHttp"`（对应 `/mcp` POST）、`"sse"`（对应 `/sse` GET） |
| `env` | 运行时环境变量，用于注入 API Key、密钥等敏感配置（需配合 KMS 加密） | `{ "AMAP_MAPS_API_KEY": "xxx" }` |

## 使用方式

### 1. 接入官方 MCP 服务  
前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 Amap Maps）→ 点击“立即开通” → 在智能体/工作流编辑器中添加该服务即可使用。试用版无需填写 API Key；商业化定制需配置个人 Key 并通过 KMS 加密 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 2. 部署自定义 MCP 服务  
支持三种方式：
- **脚本部署（npx/uvx）**：适用于已发布至 npm/PyPI 的开源或自研 MCP Server，通过函数计算 FC 托管；
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具；
- **OpenAPI 导入**：将阿里云产品 OpenAPI 快速转化为 MCP 工具 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

### 3. 外部调用  
获取 MCP 服务的 `mcp_url` 和 `DASHSCOPE_API_KEY`，使用 `mcp` SDK（如 `streamablehttp_client`）建立会话，调用 `list_tools()` 获取工具列表，再以 OpenAI 兼容格式传入 LLM 的 `tools` 参数进行 function calling [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与资源限制**：MCP 服务运行于函数计算 FC，**无法访问本地文件、硬件或数据库**；访问远程云资源（如 RDS）需配置 FC 出口 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：百炼已全面升级至 **Streamable HTTP 协议**（旧版 SSE 已弃用），新部署必须使用 `/mcp` 端点；已开通用户需取消再重开以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **[Token](../concepts/token.md) 开销**：MCP 返回结果会作为上下文注入模型输入，**显著增加输入 [Token](../concepts/token.md) 消耗**；复杂响应也可能间接提升输出 [Token](../concepts/token.md) 量 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **版本与维护**：通过 `npx/uvx` 部署的服务**不会自动更新**，需手动重新部署新版本；第三方 MCP 服务可用性由服务商自行维护，百炼不保证其持续可用 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)


