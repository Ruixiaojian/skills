# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等服务）之间建立安全、可扩展的信息交换通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官方规范](https://modelcontextprotocol.io/) 实现，并针对百炼平台进行了生产级增强与托管支持。

## 支持的模型/功能

MCP 本身不绑定特定模型，而是作为**能力接入层**服务于百炼平台上的所有支持工具调用的模型，当前主要覆盖：

- **智能体应用**：支持自动推理并调用已配置的 MCP 服务（如 `Amap Maps`、`WebSearch`、`Sequential Thinking`），最多同时启用 5 个服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：支持显式编排 MCP 节点，每个节点绑定一个具体工具（如 `maps_weather`），需手动传递输入参数并处理输出 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **外部客户端**：支持通过 Streamable HTTP 或 SSE 协议被 Cherry Studio、Cursor 等第三方 MCP 客户端直接集成，亦可通过 MCP SDK 在自有项目中调用 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：MCP 服务**不能**在直接调用千问 API（如 `qwen-max` 的 RESTful 接口）时接入；必须部署于百炼智能体或工作流应用内，或通过外部 MCP 客户端调用 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `type` | MCP 服务传输类型，决定通信协议和端点路径 | `"sse"`（对应 `/sse`）、`"streamableHttp"`（对应 `/mcp`） | [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| `url` | 远程 MCP Server 地址（仅 `http` 模式） | `"https://your-mcp-server/sse"` | [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `command` / `args` | 本地脚本启动命令（`npx`/`uvx` 模式） | `"npx"`, `["-y", "@modelcontextprotocol/server-memory"]` | [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `env` | 启动环境变量（如 API Key、密钥） | `{"AMAP_MAPS_API_KEY": "xxx"}` | [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `deploymentMode` | 部署模式：`basic`（按次计费）或 `ultra`（极速模式） | `"basic"` | [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md) |

## 使用方式

1. **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择官方服务（如 `Amap Maps`）或自定义服务，点击“立即开通”。
2. **配置应用**：
   - *智能体*：在应用编辑页 → “MCP 服务” → 添加已开通服务，无需指定工具，模型自动调度。
   - *工作流*：拖入“MCP 节点”，选择服务及具体工具（如 `maps_weather`），手动配置输入参数（常引用上游节点输出）。
3. **外部调用**：
   - 第三方客户端（Cherry Studio/Cursor）：在 MCP 服务详情页选择对应客户端，一键配置或手动导入 JSON。
   - 自有项目：使用 `mcp` SDK（如 `streamablehttp_client`）连接 `https://dashscope.aliyuncs.com/api/v1/mcps/{service}/mcp`，配合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)完成工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与资源限制**：MCP 服务托管于函数计算 FC，**无法访问用户本地数据库或文件系统**；若需访问云数据库等远程资源，必须配置 FC 的 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：百炼已全面升级至 **Streamable HTTP 协议**（旧版 SSE 已弃用），新用户默认使用；存量用户需主动取消再重新开通以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **版本与更新**：通过 `npx`/`uvx` 部署的服务，**不会自动同步上游包更新**，版本变更后需手动重新部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **[Token](../concepts/token.md) 开销**：MCP 返回结果将作为上下文注入模型输入，**直接增加输入 [Token](../concepts/token.md) 数量**；更丰富的上下文也可能导致模型生成更长响应，间接增加输出 [Token](../concepts/token.md) [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **错误排查**：常见错误码（如 `11200044` 连接拒绝、`11200059` 404 Not Found）均需结合 `curl` 测试、FC 日志及下游服务文档定位，详见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) 中的错误码表。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)


