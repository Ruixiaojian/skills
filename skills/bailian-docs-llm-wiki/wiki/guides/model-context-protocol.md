# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等）之间建立安全、可扩展的上下文传递通道。它屏蔽了底层工具接入的复杂性，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式调用第三方能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，同时兼容 Streamable HTTP 和 SSE 两种传输方式。

## 支持的模型/功能

MCP 协议本身不绑定特定模型，但其调用能力需通过百炼平台的**智能体应用**或**工作流应用**触发。当前支持以下两类使用场景：

- **智能体应用**：大模型根据对话上下文自动判断是否调用、调用哪个 MCP 工具及传入参数。支持单次调用多个 MCP 服务（最多 5 个），适用于自然语言驱动的动态工具选择，例如路径规划、逐步推理、多源信息融合（如天气+图表）[原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：MCP 节点需手动指定具体工具（如 `maps_weather`），并显式配置输入/输出参数映射。适用于确定性流程编排，例如“解析城市名 → 查询天气 → 总结结果”链路 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

> **注意**：MCP 服务**不能直接接入千问 API 的原始调用**，仅限集成于百炼平台内的智能体或工作流应用中使用 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

| 参数 | 说明 | 取值示例 | 来源 |
|------|------|----------|------|
| `type` | 传输协议类型 | `"sse"`（Server-Sent Events）或 `"streamableHttp"`（POST `/mcp`） | [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| `url` | MCP 服务接入地址 | `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`（Streamable HTTP）<br>`https://dashscope.aliyuncs.com/api/v1/mcps/AmapMaps/sse`（SSE） | [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) |
| `headers.Authorization` | 外部调用必需认证头 | `Bearer ${DASHSCOPE_API_KEY}` | [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) |
| `mcpServers.<name>.type` | 自定义部署时服务类型 | `"stdio"`（本地进程）、`"sse"`、`"streamableHttp"` | [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |

## 使用方式

### 1. 接入官方 MCP 服务
- 前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 Amap Maps、WebSearch）→ 点击“立即开通”。
- 敏感参数（如 API Key）需通过 KMS 凭据加密管理 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 2. 配置至应用
- **智能体**：创建后，在“MCP 服务”配置页添加已开通的服务，无需指定工具，由模型自主调度。
- **工作流**：拖入 MCP 节点，从下拉列表选择具体工具（如 `maps_weather`），并手动绑定输入参数（如引用上游节点输出）。

### 3. 外部调用
- **第三方应用集成**：在 MCP 服务详情页的“外部调用”界面，一键配置至 Cherry Studio 或 Cursor。
- **SDK 编程集成**：使用 `mcp` SDK（如 `streamablehttp_client`）连接服务端点，配合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)实现工具调用循环 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络限制**：自定义 MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等远程资源时需配置 IP 白名单或 VPC 打通 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **本地资源不可达**：MCP 服务无法访问用户本地文件、硬件或数据库；依赖本地资源的服务应本地部署 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **版本更新**：通过 `npx`/`uvx` 部署的服务，**不会自动同步新版本**，需手动重新部署 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **[Token](../concepts/token.md) 开销**：MCP 返回内容作为上下文注入模型，会增加输入 [Token](../concepts/token.md)；更丰富的上下文可能导致输出 [Token](../concepts/token.md) 间接增长 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议升级**：已开通用户需主动取消再重开，才能将旧版 SSE 服务升级至新版 Streamable HTTP 协议 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)


