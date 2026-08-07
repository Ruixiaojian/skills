# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等）之间建立可互操作的信息通道。它屏蔽了工具接入的底层差异，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式调用能力。该协议基于 Anthropic 提出的开源标准 [MCP 官方规范](https://modelcontextprotocol.io/) 实现，并由百炼平台提供云部署、自定义部署及外部 SDK 集成支持。

## 支持的模型/功能

MCP 本身不绑定特定模型，而是作为**能力调度层**，服务于百炼平台上的所有支持工具调用的模型。当前已在以下两类应用中全面启用：

- **智能体应用**：支持自动推理并调用最多 5 个已配置的 MCP 服务（如 `Amap Maps` 的路径规划、`Sequential Thinking` 的逻辑推理、`QuickChart` 的图表生成），无需显式指定工具名 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：支持手动编排 MCP 节点，每个节点绑定一个具体工具（如 `maps_weather`），需通过前置大模型节点提取参数、后置节点解析结果 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

> **注意**：MCP 服务**不能直接接入千问 API 调用链**（如 `dashscope.ChatCompletion.create`），仅限百炼平台内智能体/工作流应用使用 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

| 参数 | 说明 | 示例/取值 |
|------|------|-----------|
| `type` | 协议传输类型，决定连接方式与端点路径 | `"sse"`（对应 `/sse`）、`"streamableHttp"`（对应 `/mcp`）；配置错误将导致 `11200058` 或 `11200059` 错误 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| `command` / `url` | 启动方式或远程地址 | `npx`（Node.js）、`uvx`（Python）、`http`（远程 SSE）；`url` 必须指向有效 MCP Server 端点 |
| `env` | 环境变量注入 | 用于传递 API Key、密钥等敏感信息（建议配合 KMS 凭据加密） |
| `inputSchema` | 工具输入参数 Schema | JSON Schema 格式，影响大模型参数生成准确性；缺失或错误将导致 `11200060` 错误 |

## 使用方式

### 1. 接入官方 MCP 服务  
前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，开通即用（如 Amap Maps、WebSearch）。开通后，在智能体/工作流的「添加 MCP 服务」界面选择并配置 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 2. 部署自定义 MCP 服务  
支持三种方式：
- **脚本部署**：适用于开源或自研 MCP Server（如 `@modelcontextprotocol/server-memory`），通过函数计算 FC 托管，需提供 `npx`/`uvx` 启动配置 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)；
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具；
- **OpenAPI 导入**：将阿里云产品（OSS/ECS）能力一键发布为 MCP 服务。

### 3. 外部调用  
支持两种集成模式：
- **第三方应用集成**：一键配置至 Cherry Studio、Cursor 等客户端；
- **SDK 编码集成**：使用 `mcp` Python SDK + [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，需设置 `DASHSCOPE_API_KEY` 及 `streamablehttp_client` 连接地址 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限**：自定义 MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通；**无法访问本地文件或硬件** [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议升级**：已从旧版 SSE 升级为 Streamable HTTP 协议，旧用户需重新开通以生效 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **计费模式**：
  - 云部署服务：调用费用由第三方收取（如 WebSearch 29 元/千次），百炼不收服务费；
  - 自定义服务：基础模式按调用时长计费（0.000156 元/秒），极速模式另加部署费（0.000036 元/秒） [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
- **调试建议**：遇到连接失败（如 `11200044`）、超时（`11200045`）或协议错误（`11200054`），优先执行 `curl <服务地址>` 测试连通性，并检查 `type` 与端点路径是否匹配 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


