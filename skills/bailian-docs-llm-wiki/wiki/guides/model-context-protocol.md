# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地理服务、网页爬取、天气查询等）之间建立安全、可扩展的信息通道。通过 MCP，开发者无需为每个工具单独开发适配层，即可在智能体或工作流中声明式接入官方或自定义工具服务。该协议基于开源 MCP 标准实现，当前采用 Streamable HTTP 协议（替代旧版 SSE），并深度集成于百炼应用架构中。

## 支持的模型/功能

MCP 本身不绑定特定模型，而是作为**工具调用协议层**，服务于百炼平台内的两类核心应用：
- **智能体应用**：支持自动决策调用（最多同时配置 5 个 MCP 服务），例如根据用户提问“从杭州萧山国际机场到西湖景区提供三种公交方案”自动触发 Amap Maps MCP 服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)；
- **工作流应用**：需手动指定 MCP 节点使用的具体工具（如 `maps_weather`），并显式连接输入/输出参数，适用于确定性任务编排 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

支持的服务类型包括：
- **官方 MCP 服务**：由阿里云预部署并托管，如 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）等，开通即用；
- **自定义 MCP 服务**：支持三种部署方式：① 使用脚本（npx/uvx）部署开源或自研 MCP Server；② 通过 AI 网关将现有 RESTful API 封装为 MCP 工具；③ 通过 OpenAPI 开发者门户将阿里云产品（如 OSS、ECS）能力发布为 MCP 服务 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 提到“百炼 MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议”，而文档 2 的示例截图及部分描述仍沿用 SSE 术语（如“服务器发送事件 (sse)”）。实际部署和 SDK 调用应以 Streamable HTTP（`/mcp` 端点）为准，SSE 模式已逐步淘汰。

## 关键参数

MCP 服务配置涉及以下关键参数，需在创建或导入时明确指定：

| 参数类别 | 参数名 | 说明 | 示例值 |
|----------|--------|------|--------|
| **基础信息** | 服务名称、描述 | 仅用于控制台标识，不影响模型调用逻辑 | `"长期记忆"`、`"记录个性化信息"` |
| **部署配置** | 安装方式 | 决定启动机制：`npx`（Node.js）、`uvx`（Python）、`http`（远程 SSE/Streamable HTTP） | `"npx"` |
| | 部署方式 | `基础模式`（按次计费，有冷启动延迟）或 `极速模式`（常驻计费，低延迟） | `"基础模式：按次计费"` |
| | 部署地域 | 影响网络延迟，推荐与主业务同地域 | `"北京"` |
| **服务地址** | `mcpServers` 配置块 | JSON 格式，定义服务类型、命令、参数及环境变量 | `{ "memory": { "command": "npx", "args": ["@modelcontextprotocol/server-memory"] } }` |
| **安全凭证** | KMS 凭据 | 敏感参数（如 API Key）必须通过 KMS 加密管理，不可明文填写 | `AMAP_MAPS_API_KEY`（加密后引用） |

## 使用方式

### 1. 平台内集成（智能体/工作流）
- **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务卡片点击“立即开通”；
- **添加至智能体**：在智能体编辑页 → “MCP 服务” → 点击“添加服务”，选择已开通服务；
- **配置工作流节点**：拖入 MCP 节点 → 选择具体工具（如 `maps_weather`）→ 在输入参数中引用上游节点输出（如 `引用：信息提取/result`）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 2. 外部调用（第三方应用/SDK）
- **一键集成**：支持 Cherry Studio、Cursor 等客户端，通过控制台“外部调用”页点击“一键配置”自动注入配置；
- **SDK 编码集成**：使用 `mcp` Python SDK 连接 Streamable HTTP 端点（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`），配合 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)完成多轮工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与资源限制**：
  - 自定义 MCP 服务运行于函数计算 FC，**无法访问用户本地数据库或硬件资源**；
  - 访问远程云资源（如 RDS）需配置 FC IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；
  - 云部署服务（如 WebSearch）有 QPS 限流（15 QPS，主账号与 RAM 子账号共享）及免费额度（2000 次/月）。

- **协议与兼容性**：
  - 必须严格匹配 `type` 与端点路径：`"streamableHttp"` 对应 POST `/mcp`，`"sse"` 对应 GET `/sse`，否则报错 `11200058`（METHOD_NOT_ALLOWED）或 `11200059`（NOT_FOUND） [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；
  - 私有 npm/PyPI 包暂不支持直接部署，需发布至公共仓库或改用 SSE 连接。

- **运维与调试**：
  - 自定义服务版本更新后**不会自动同步**，需手动重新部署；
  - 排查连接失败（如 `11200044`）时，优先执行 `curl <服务地址>` 测试连通性，并检查下游服务日志；
  - 模型 Token 消耗会因 MCP 返回内容增加：返回结果作为上下文输入模型，直接增加输入 Token，间接影响输出长度。

- **安全与权限**：
  - 敏感参数（如 API Key）必须通过 KMS 凭据加密，禁止明文配置；
  - 自定义 MCP 服务仅对创建账号及授权 RAM 用户可见，不对外暴露。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


