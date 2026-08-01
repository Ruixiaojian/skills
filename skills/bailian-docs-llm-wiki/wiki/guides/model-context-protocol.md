# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化工具集成机制，用于在大模型应用（如智能体、工作流）与外部服务之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，使开发者无需为每个工具单独编写适配代码即可调用地理信息、网页爬取、天气查询等能力。MCP 同时支持官方托管服务与自定义部署，并可通过外部 SDK 集成至第三方客户端。

## 支持的模型/功能

MCP 本身不绑定特定大模型，但其调用行为高度依赖所配置的推理模型能力：
- **智能体应用**：自动识别用户意图并动态选择、调用已接入的 MCP 服务（最多同时启用 5 个），适用于多步推理（如“鸡兔同笼”）、路径规划、多源数据聚合（如“气温趋势+图表绘制”）等场景 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式指定 MCP 节点使用的具体工具（如 `maps_weather`），并通过前置大模型节点解析自然语言输入为结构化参数，再将输出传递至后续节点进行结果整合 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **外部调用**：支持通过标准 Streamable HTTP 协议或 SSE 协议接入 Cherry Studio、Cursor 等第三方客户端，也可使用 `mcp` Python SDK 进行深度定制开发 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：文档 4 明确指出“MCP 服务不能在调用千问 API 时直接接入”，即 MCP 仅限于百炼平台内智能体/工作流应用或通过外部 SDK 调用，**不支持作为参数传入 `dashscope.ChatCompletion.create()` 等原生千问 API 调用中**。

## 关键参数

| 参数类别 | 名称 | 说明 | 示例/约束 |
|----------|------|------|-----------|
| **服务配置** | `type` | 指定通信协议类型，必须与后端端点严格匹配 | `"sse"`（对应 `/sse`）、`"streamableHttp"`（对应 `/mcp`）；配置错误将导致 `11200058` 错误 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| | `url` | MCP Server 的访问地址 | 必须可公网访问；若使用函数计算托管，需确保下游服务开放相应端口并配置 IP 白名单 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| | `env` | 环境变量注入（仅 `npx`/`uvx` 部署） | 用于传递 API Key、密钥等敏感信息，**禁止明文写入配置代码**，应通过 KMS 凭据加密 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) |
| **工具调用** | `tool.name` | 工具唯一标识符 | 在智能体中由模型自动匹配；工作流中需手动选择，如 `maps_weather` |
| | `inputSchema` | JSON Schema 定义的输入参数结构 | 决定模型生成参数的格式，System Prompt 中需准确描述该 schema 以约束大模型输出 |

## 使用方式

1. **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 Amap Maps）并点击“立即开通”。敏感参数（如 `AMAP_MAPS_API_KEY`）需通过 KMS 凭据加密管理 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
2. **集成至智能体**：创建智能体应用 → “添加 MCP 服务” → 从已开通列表中勾选（最多 5 个）→ 测试对话触发自动调用。
3. **集成至工作流**：创建工作流 → 拖入 MCP 节点 → 手动选择工具 → 通过上游大模型节点（如“信息提取”）将 `query` 解析为工具所需参数（如 `city: "杭州"`）→ 将输出 `result` 传递至下游节点。
4. **外部调用**：
   - 第三方客户端：在 MCP 服务详情页选择 Cherry Studio/Cursor → 点击“一键配置”。
   - 自定义开发：使用 `mcp` SDK（如 `streamablehttp_client`）连接 `https://dashscope.aliyuncs.com/api/v1/mcps/{service}/mcp`，配合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)实现工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与资源限制**：MCP 服务托管于函数计算（FC），**无法访问用户本地数据库或文件系统**；若需访问云数据库，必须配置 FC 的 VPC 网络打通或 IP 白名单 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：百炼已全面升级至 Streamable HTTP 协议，旧版 SSE 用户需先“取消开通”再“重新开通”以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **Token 开销**：MCP 返回结果会作为上下文注入模型输入，**显著增加输入 Token 数量**；复杂响应也可能间接提升输出 Token [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **版本与维护**：通过 `npx`/`uvx` 部署的自定义服务，**版本更新后需手动重新部署**；第三方 MCP 服务（如 Firecrawl）的可用性及权限由服务商控制，百炼不保证长期稳定 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **安全边界**：所有自定义 MCP 服务仅对当前阿里云主账号及授权 RAM 用户可见，私有 npm 仓库包暂不支持直接部署，需发布至公共仓库或改用 SSE 远程连接 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)


