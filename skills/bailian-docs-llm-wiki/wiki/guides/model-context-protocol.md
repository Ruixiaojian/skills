# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息交互通道。它屏蔽了底层工具的实现差异，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中统一接入和编排多种能力。该协议基于开源 MCP 标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部调用 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用行为由百炼平台内的**智能体应用**和**工作流应用**驱动，当前支持以下两类核心使用场景：

- **智能体应用**：模型根据自然语言输入自动判断是否调用、调用哪个 MCP 工具及传入参数，支持最多同时配置 5 个 MCP 服务 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。典型用例包括路径规划（Amap Maps）、逻辑推理（Sequential Thinking）、多工具协同（天气+图表绘制）。
- **工作流应用**：需显式配置 MCP 节点并手动指定所用工具（如 `maps_weather`），输入参数需通过前置大模型节点解析生成，输出参数可传递至后续节点。适用于确定性、可编排的业务流程。

支持的服务类型分为两类：
- **官方 MCP 服务**：由阿里云百炼直接部署并托管，如 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）等，开通即用，部分服务限时免费 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **自定义 MCP 服务**：支持三种部署方式：① 使用脚本（npx/uvx）托管开源或自研 MCP Server；② 通过 AI 网关将现有 RESTful API 封装为 MCP 服务；③ 通过 OpenAPI 开发者门户将阿里云产品（如 OSS、ECS）能力发布为 MCP 服务 [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 明确指出 MCP 协议已从旧版 SSE 升级为新版 Streamable HTTP 协议，而文档 3 的示例截图仍显示 SSE 类型（如 Cherry Studio 配置中类型为 `服务器发送事件 (sse)`）。实际部署和外部调用应以 `streamableHttp` 为准，SSE 仅作为历史兼容模式存在，新集成请优先采用 `/mcp` 端点。

## 关键参数

MCP 服务配置涉及以下关键参数，不同部署方式下字段略有差异：

| 参数 | 说明 | 常见值/约束 |
|------|------|-------------|
| `type` | 通信协议类型 | 必须与端点路径严格匹配：`"sse"` 对应 `/sse`；`"streamableHttp"` 对应 `/mcp`（[原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) 中错误码 11200058/11200059 强调此匹配规则） |
| `command` / `url` | 启动方式或服务地址 | `npx`（Node.js）、`uvx`（Python）或 `http` + 远程 URL |
| `env` | 环境变量 | 用于注入 API Key、密钥等敏感信息，建议配合 KMS 凭据加密 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) |
| `deploymentMode` | 部署模式 | `基础模式（按次计费）`：无部署费，有调用时按秒计费（0.000156 元/秒）；`极速模式`：额外收取部署费（0.000036 元/秒），适合高频调用 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md) |

## 使用方式

### 平台内集成（智能体/工作流）
1. **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务卡片点击“立即开通”。
2. **添加到应用**：
   - *智能体*：在应用编辑页 > “工具” > “添加 MCP 服务”，从已开通列表中选择。
   - *工作流*：从工具栏拖入“MCP 节点”，在配置中选择具体工具（如 `maps_weather`），并通过变量引用（如 `信息提取/result`）传入参数。
3. **提示词优化**：模型调用依赖明确指令。若调用失败，需在 System Prompt 中清晰描述工具名称、功能及输入/输出格式 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

### 外部调用（第三方应用/SDK）
- **一键集成**：支持 Cherry Studio、Cursor 等客户端，通过控制台“外部调用”页选择目标平台，点击“一键配置”自动注入 API Key 和服务地址。
- **SDK 编码集成**：使用 `mcp` Python SDK（如 `streamablehttp_client`）连接 `/mcp` 端点，结合 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)实现多轮工具调用循环 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限限制**：自定义 MCP 服务运行于函数计算 FC，**无法访问用户本地资源（如本地文件、硬件）**，也**暂不支持直接访问本地数据库** [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。若需访问云数据库，必须配置 FC IP 白名单或 VPC 打通。
- **协议与版本兼容性**：npx/uvx 部署的服务版本更新后**不会自动同步**，需手动重新部署 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；私有 npm 仓库包暂不支持直接部署，需发布至公共仓库或改用 SSE 连接。
- **计费与限流**：
  - 官方服务如 WebSearch：免费额度 2000 次/月，超量后 29 元/千次；限流 15 QPS（主账号与 RAM 子账号共享）。
  - 自定义服务：基础模式冷启动延迟明显，高频场景建议启用极速模式；所有模式均按调用时长（秒）计费。
- **错误排查重点**：常见失败原因包括协议类型与端点不匹配（错误码 11200058/11200059）、HTTP 状态码异常（401/403/429）、SSL 证书问题（11200048）及初始化超时（11200057）。推荐使用 `curl` 测试端点连通性，并开启 FC 日志服务定位问题 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


