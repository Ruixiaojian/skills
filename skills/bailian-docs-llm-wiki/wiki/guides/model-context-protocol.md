# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配逻辑，即可将第三方或自研服务统一接入智能体和工作流应用。该协议基于开源 MCP 标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部调用 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 支持的模型/功能

MCP 服务**不直接绑定特定大模型**，而是通过百炼平台的智能体（Agent）和工作流（Workflow）两类应用承载：

- **智能体应用**：支持自动推理调用，大模型根据对话上下文自主判断是否及何时调用已配置的 MCP 服务（最多同时启用 5 个），适用于路径规划、逐步思考等动态决策场景 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：采用显式编排，每个 MCP 节点必须手动指定具体工具（如 `maps_weather`），并严格配置输入/输出参数传递链路，适用于确定性任务（如城市天气查询）。

当前支持两类服务来源：
- **官方 MCP 服务**：由百炼预部署并托管，包括 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）等，开通即用，部分服务限时免费 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
- **自定义 MCP 服务**：支持三种部署方式：① 使用脚本（npx/uvx）托管开源或自研服务；② 通过 AI 网关将现有 RESTful API 封装为 MCP；③ 通过 OpenAPI 开发者门户将阿里云产品（如 OSS、ECS）能力发布为 MCP [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 明确指出 MCP 协议已从旧版 SSE 升级为新版 Streamable HTTP 协议，而文档 3 和文档 5 中部分示例仍提及 SSE（如 Cherry Studio 配置中显示类型为 `sse`）。实际生产环境应优先使用 `/mcp` 端点的 Streamable HTTP 模式，SSE 仅作为兼容选项存在。

## 关键参数

MCP 服务配置的核心参数取决于部署方式：

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `type` | 通信协议类型 | `"stdio"`（本地）、`"sse/streamableHttp"`（远程） | [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `command` / `args` | 本地服务启动命令 | `"npx"`, `["-y", "@modelcontextprotocol/server-memory"]` | [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `url` | 远程服务地址 | `"https://your-mcp-server/sse"`（SSE）或 `"https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp"`（Streamable HTTP） | [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) |
| `deploymentMode` | 部署模式 | `"basic"`（按次计费）、`"ultra"`（极速模式，常驻） | [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md) |
| `region` | 部署地域 | `"cn-beijing"` | [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |

所有远程服务必须确保 `type` 与端点路径严格匹配：`"sse"` 对应 GET `/sse`，`"streamableHttp"` 对应 POST `/mcp`；否则将触发错误码 `11200058`（HTTP 405）[原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 使用方式

### 1. 服务开通与管理
- 官方服务：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务卡片 → 点击“立即开通” → 完成 KMS 加密（如需）。
- 自定义服务：进入 [MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage) → “创建 MCP 服务” → 选择部署方式（脚本/AI 网关/OpenAPI）→ 填写配置 → 提交部署。

### 2. 在智能体中集成
- 创建智能体后，在“工具”页添加已开通的 MCP 服务；
- 无需额外配置参数，模型根据提示词自动调用（如发送“从杭州萧山国际机场到杭州西湖景区”将触发 Amap Maps 服务）。

### 3. 在工作流中集成
- 添加 MCP 节点后，**必须手动指定工具名**（如 `maps_weather`）；
- 通过变量引用（如 `引用：信息提取/result`）将上游节点输出映射为 MCP 输入；
- 输出结果需经大模型节点二次处理才能生成自然语言响应。

### 4. 外部调用（SDK/第三方工具）
- 获取 DASHSCOPE_API_KEY 及服务 URL（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`）；
- 使用 `mcp.client.streamable_http` 客户端连接，配合 OpenAI SDK 的 `tools` 参数实现[函数调用](../concepts/function-calling.md)循环 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)；
- 支持一键配置至 Cherry Studio、Cursor 等主流 IDE。

## 限制和注意事项

- **网络与权限**：自定义 MCP 服务运行于函数计算 FC，无固定公网出口 IP，访问云数据库等资源需配置 IP 白名单或 VPC 打通；无法访问用户本地文件或硬件 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **版本与更新**：通过 `npx/uvx` 部署的服务版本固化，MCP Server 更新后需手动重新部署；私有 npm/PyPI 包暂不支持直接部署 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **[Token](../concepts/token.md) 消耗**：MCP 返回结果会作为上下文注入模型输入，显著增加输入 [Token](../concepts/token.md)；模型可能因信息更丰富而生成更长响应，间接增加输出 [Token](../concepts/token.md) [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **错误排查**：常见错误码（如 `11200044` 连接拒绝、`11200051` 限流）需结合 `curl` 测试、FC 日志及下游服务文档定位，详见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **模型兼容性**：MCP 仅支持集成于百炼智能体/工作流应用，**不可直接用于调用千问 API 的独立请求** [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


