# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等服务）之间建立安全、可扩展的信息交互通道。通过 MCP，开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中统一接入官方或自定义工具服务。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

- **适用场景**：MCP 仅支持在百炼平台的 **智能体应用** 和 **工作流应用** 中使用，不支持直接在调用千问 API（如 `qwen-max` 接口）时接入 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **官方服务**：已预置 Amap Maps、Firecrawl、WebSearch（联网搜索）、Sequential Thinking、QuickChart 等官方 MCP 服务，开通后即可在应用中配置使用 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **自定义服务**：支持三种部署方式：
  - **脚本部署**（npx/uvx）：适用于 Node.js 或 Python 编写的开源或自研 MCP 服务；
  - **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具；
  - **OpenAPI 导入**：将阿里云产品（如 OSS、ECS）的 OpenAPI 快速发布为 MCP 服务 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 1 中称“智能体和工作流应用已支持接入两种 MCP 服务”，但文档 2 和文档 4 明确列出多个官方服务（如 Amap Maps、WebSearch、Sequential Thinking 等），且文档 3 描述了多种自定义服务类型。此处“两种”应为过时表述，实际支持数量远超两种，以 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) 和 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) 列表为准。

## 关键参数

| 参数 | 说明 | 示例/约束 |
|------|------|-----------|
| `service_name` | 服务唯一标识，仅用于管理区分，不影响模型调用逻辑 | `"长期记忆"`（自定义服务） |
| `tool_name` | 工具名称，模型在 function calling 中实际引用的名称 | `"maps_weather"`（Amap Maps 的天气查询工具） |
| `inputSchema` | JSON Schema 格式定义输入参数结构，影响模型参数生成准确性 | 必须严格匹配下游服务要求，否则触发 `MCP_SERVER_HTTP_BAD_REQUEST`（错误码 11200060） |
| `type` | 协议传输类型，决定端点路径和请求方式 | `"sse"` → `/sse`（GET）；`"streamableHttp"` → `/mcp`（POST）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| `env` | 环境变量配置，用于传递 API Key 等敏感信息 | 需配合 KMS 凭据加密，不可明文写入配置代码 |

## 使用方式

1. **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务并点击「立即开通」。涉及敏感信息（如 `AMAP_MAPS_API_KEY`）需通过 KMS 凭据加密 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
2. **在智能体中配置**：
   - 最多可添加 5 个 MCP 服务；
   - 模型根据对话自动判断是否调用及选择工具，无需显式指令（但提示词优化可提升准确率）；
   - 示例：发送“从杭州萧山国际机场到杭州西湖景区”即可触发 Amap Maps 路径规划 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
3. **在工作流中配置**：
   - 每个 MCP 节点仅绑定一个工具（如 `maps_weather`），需手动指定输入参数来源（如引用上游节点输出）；
   - 典型模式：大模型节点 → 提取城市名 → MCP 节点 → 大模型节点 → 总结结果 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
4. **外部调用**：
   - 支持集成至 Cherry Studio、Cursor 等第三方 IDE，提供一键自动配置；
   - 支持通过 MCP SDK 编程调用，示例代码使用 `streamablehttp_client` 连接 WebSearch 服务 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限**：
  - 自定义 MCP 服务托管于函数计算 FC，无固定出口 IP，访问云数据库等资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；
  - 不支持访问用户本地资源（如本地文件、硬件设备）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：
  - 百炼已全面升级至 Streamable HTTP 协议（`/mcp` 端点），旧版 SSE（`/sse`）需手动取消再重新开通以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)；
  - 配置中 `type` 必须与端点路径严格匹配，否则触发 `MCP_SERVER_HTTP_METHOD_NOT_ALLOWED`（11200058）或 `MCP_SERVER_HTTP_NOT_FOUND`（11200059）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **计费与限流**：
  - 官方服务如 WebSearch：免费额度 2000 次/月，超量后 29 元/千次；限流 15 QPS（主账号与 RAM 子账号共享）[模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)；
  - 自定义服务按部署模式计费：基础模式（按调用时长，0.000156 元/秒）或极速模式（另加部署费 0.000036 元/秒）[模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
- **调试建议**：
  - 工具调用失败时，优先检查 `curl <MCP_URL>` 连通性及响应状态码；
  - 启用函数计算 FC 日志服务，结合错误码（如 `MCP_CONNECTION_TIMEOUT` 11200045）定位网络或下游服务问题 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


