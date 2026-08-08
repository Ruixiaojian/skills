# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化工具集成机制，用于在大模型应用（如智能体、工作流）与外部服务之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，支持官方托管服务与自定义服务统一接入，并兼容 Anthropic 提出的开源 MCP 协议标准 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。开发者无需为每个工具单独开发适配逻辑，即可实现多工具协同调用。

## 支持的模型/功能

- **适用应用类型**：仅限百炼平台内的 **智能体应用** 和 **工作流应用**，不支持直接在千问 API 调用中接入 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **服务来源**：
  - **官方 MCP 服务**：由阿里云百炼预部署并托管，如 `Amap Maps`（地理信息）、`WebSearch`（联网搜索）、`Sequential Thinking`（逻辑推理）、`QuickChart`（图表生成）等，开通后即开即用 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
  - **自定义 MCP 服务**：支持通过 `npx`（Node.js）、`uvx`（Python）部署公共仓库包，或通过 SSE 连接已托管的远程服务；但**不支持私有 npm 仓库或需访问本地资源的服务**（如本地文件、硬件）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：已从旧版 SSE 协议升级为 **Streamable HTTP 协议**（对应 `/mcp` 端点），新用户默认使用该协议；已开通用户需手动取消再重新开通以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：文档 2 中提及“智能体和工作流应用已支持接入两种 MCP 服务”，表述模糊且易引发歧义；实际指“官方”与“自定义”两类服务形态，而非仅限两种具体服务。应以文档 1 和文档 4 的明确分类为准。

## 关键参数

| 参数名 | 说明 | 来源/约束 |
|--------|------|-----------|
| `tool name` | 工具唯一标识符（如 `maps_weather`），用于模型识别与调用 | 必须与 MCP 服务注册的工具名完全一致；工作流中需手动指定 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) |
| `inputSchema` | 工具输入参数 JSON Schema，定义 `city: string` 等字段类型与必填性 | 模型依赖此 Schema 生成合法参数；若 Schema 缺失或错误，可能导致调用失败或参数解析异常 |
| `DASHSCOPE_API_KEY` | 外部调用时必需的身份凭证，用于鉴权 | 需配置为环境变量或显式传入 SDK；API Key 错误将导致 `MCP_SERVER_HTTP_UNAUTHORIZED (11200049)` 错误 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| `KMS 凭据` | 用于加密敏感配置（如第三方 API Key） | 仅云部署服务支持；自定义服务需自行处理密钥安全 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) |

## 使用方式

### 平台内集成（智能体/工作流）
- **智能体应用**：最多可同时添加 **5 个 MCP 服务**；模型根据对话自动判断是否及何时调用，无需显式指定工具 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：每个 MCP 节点**仅绑定一个工具**，需手动配置输入参数（如引用上游节点输出 `信息提取/result`）和输出映射 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 外部调用
- **第三方 IDE 集成**：支持一键配置至 Cherry Studio（SSE 类型）或 Cursor（stdio 类型），自动注入服务元信息 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **SDK 编码集成**：推荐使用 `mcp` 官方 SDK + `OpenAI` 兼容客户端，通过 `streamablehttp_client` 连接 `/mcp` 端点，动态获取工具列表并执行多轮工具调用 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限限制**：
  - MCP 服务运行于函数计算 FC 环境，**无固定出口公网 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - **不支持访问用户本地资源**（如本地数据库、文件系统）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  
- **计费与额度**：
  - 云部署服务：部署免费；调用费用由第三方 API 提供方收取（如高德地图），百炼不额外收费 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
  - 联网搜索服务：免费额度 **2000 次/月**，超限后 **29 元/千次**；限流 **15 QPS**（主账号与 RAM 子账号共享）[模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

- **调试与排错**：
  - 模型无法调用 MCP 的首要原因是**提示词未明确指令**（如未提及工具名称或能力），应优化 Prompt 或更换更强模型 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - 常见错误码（如 `11200044` 连接拒绝、`11200058` 方法不被允许）均与协议端点匹配相关，务必确认 `type`（`sse`/`streamableHttp`）与 URL 路径（`/sse`/`/mcp`）严格一致 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


