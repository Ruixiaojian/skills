# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大模型应用（如智能体、工作流）与外部工具服务之间建立安全、可扩展的上下文交互通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配层，即可复用官方或自定义的 MCP 服务。该协议基于 Anthropic 提出的开源标准实现，当前在百炼中以 Streamable HTTP 和 SSE 两种传输方式落地 [MCP 协议](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 支持的模型/功能

MCP 协议本身不绑定特定模型，但其能力需通过百炼平台的**智能体应用**和**工作流应用**触发和编排：

- **智能体应用**：支持自动决策调用（基于提示词理解），最多同时接入 5 个 MCP 服务；适用于多步推理、动态工具选择场景（如路径规划、气温趋势分析）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式配置 MCP 节点并指定具体工具（如 `maps_weather`），适合确定性、单步调用流程；常配合大模型节点完成参数提取与结果总结 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **不支持直接接入千问 API**：MCP 服务无法在调用 `qwen-*` 等基础模型 API 时启用，仅限平台内智能体/工作流应用使用 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

> **注意**：文档 3 提到“百炼 MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议”，但文档 4 的错误码表（如 `11200058`）仍明确要求区分 `"sse"` 与 `"streamableHttp"` 类型配置，且文档 5 的脚本部署模板也保留 `type: "sse/streamableHttp"` 字段。这表明两种协议并存，**并非完全替代关系**，实际部署需严格匹配服务端端点（`/sse` 或 `/mcp`）。

## 关键参数

| 参数 | 说明 | 示例值 | 来源依据 |
|------|------|--------|----------|
| `type` | 传输协议类型，决定请求方法与端点路径 | `"sse"`（GET `/sse`）或 `"streamableHttp"`（POST `/mcp`） | [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) 错误码 11200058/11200059 |
| `url` | MCP 服务接入地址 | `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp` | [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) SDK 示例 |
| `Authorization` | 认证头，值为 `Bearer <DASHSCOPE_API_KEY>` | `Bearer sk-xxx` | [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) SDK 示例 |
| `command` / `args` | 自定义部署时启动命令（`npx`/`uvx`）及参数 | `"npx", ["-y", "@modelcontextprotocol/server-memory"]` | [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |

## 使用方式

### 1. 接入官方 MCP 服务
- **开通**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击服务卡片（如 Amap Maps）→ “立即开通” → “确认开通”。
- **配置到智能体**：创建智能体 → “添加 MCP 服务” → 从已开通列表选择，最多 5 个。
- **配置到工作流**：拖入 MCP 节点 → 选择具体工具（如 `maps_weather`）→ 手动绑定输入参数（如引用上游节点输出）。

### 2. 外部调用集成
- **第三方工具**：支持 Cherry Studio、Cursor 一键配置，自动注入 `DASHSCOPE_API_KEY` 和服务元信息。
- **自有项目**：使用 MCP SDK（如 `mcp.client.streamable_http`）连接，配合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)实现工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

### 3. 部署自定义 MCP 服务
支持三种方式：
- **脚本部署**：上传 `npx`/`uvx` 启动配置（如 `@modelcontextprotocol/server-memory`），托管至函数计算 FC；
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 服务后，从 AI 网关导入；
- **OpenAPI 导入**：将阿里云产品 OpenAPI（如 OSS、ECS）快速发布为 MCP 工具 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

## 限制和注意事项

- **网络与权限**：自定义 MCP 服务运行在函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通；**不支持访问本地资源**（文件、硬件、本地数据库）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **[Token](../concepts/token.md) 消耗**：MCP 返回内容作为上下文输入模型，**直接增加输入 [Token](../concepts/token.md) 数量**；模型响应可能因信息更丰富而间接增加输出 [Token](../concepts/token.md) [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：若服务返回非标准 JSON-RPC 格式或版本不匹配，将触发 `MCP_PROTOCOL_ERROR`（错误码 11200054），需检查服务端实现是否符合 [MCP 官网](https://modelcontextprotocol.io/) 规范 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **部署约束**：私有 npm 仓库包暂不支持 `npx` 部署；自定义服务版本更新后需手动重新部署，不会自动同步 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)


