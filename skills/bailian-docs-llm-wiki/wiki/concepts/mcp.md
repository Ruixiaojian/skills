# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台提供的标准化工具调用协议层，用于在大语言模型与外部能力（如地理服务、联网搜索、网页爬取、云产品 API 等）之间建立安全、可扩展、声明式的通信通道。它不依赖特定模型，而是作为统一的“工具接入中间件”，让模型能自主规划并调用外部服务，同时屏蔽底层传输、鉴权和序列化细节。

## 在百炼平台的不同场景中如何使用

MCP 协议在百炼三大应用范式中承担不同角色，但均围绕“让模型安全、可靠地使用外部能力”这一核心目标：

- **智能体应用（Agent）**：MCP 服务以“可规划工具”身份直接参与模型决策。开发者在智能体配置页添加已开通的 MCP 服务（最多 5 个），模型将根据用户请求自动判断是否调用、调用哪个服务及传入哪些参数。例如：“查杭州天气”会触发 `weather` MCP 工具；“对比两个 GitHub 仓库的 star 数”可能依次调用 `github_search` 和 `web_crawl`。新版 Agent 2.0 已将知识库与 MCP 统一纳入同一规划调度体系。

- **工作流应用（Workflow）**：MCP 以显式节点形式存在。开发者需手动拖入“MCP 节点”，并从下拉列表中选择具体工具（如 `maps_weather` 或 `firecrawl`），再通过连线方式将上游节点输出（如 `信息提取/result`）绑定为该工具的输入参数。此时调用逻辑由流程编排决定，而非模型自主触发。

- **Managed Agents（托管智能体）**：MCP 是其核心扩展机制之一。在创建 Agent 时，`tools` 字段可包含内置沙箱工具（如 `bash`、`read`）和 MCP 服务标识（如 `"mcp:websearch"`）。所有工具在隔离沙箱中统一调度，MCP 调用结果以结构化事件（`tool_output`）形式返回，供后续步骤消费。

- **高代码应用（Rich Code）**：开发者可通过 `mcp` Python SDK 直接连接 Streamable HTTP 端点（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`），在自定义逻辑中发起工具调用，并与 OpenAI 兼容的 `tool_calls` 响应格式无缝集成，实现细粒度控制。

> ✅ 提示：MCP 服务必须先在 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 开通并启用，才能在上述任一场景中使用。

## 关键参数和配置

MCP 服务的配置分为平台侧管理参数与运行时调用参数两类，开发者需重点关注以下内容：

### 平台侧配置（创建/导入服务时设置）
| 参数 | 说明 | 推荐值/注意事项 |
|------|------|----------------|
| **部署方式** | 决定资源模型与计费模式 | `基础模式`（按次计费，有冷启动延迟）或 `极速模式`（常驻实例，低延迟，适合高频调用） |
| **部署地域** | 影响网络延迟与合规性 | 与主业务同地域（如华东1-杭州） |
| **安装方式** | 启动服务的执行器 | `npx`（Node.js）、`uvx`（Python）、`http`（远程 Streamable HTTP 服务） |
| **`mcpServers` 配置块** | JSON 格式，定义服务映射关系 | 示例：<br>`{ "websearch": { "command": "npx", "args": ["@modelcontextprotocol/server-websearch"] } }` |
| **KMS 凭据** | 敏感凭证（如 API Key）的加密引用方式 | 必须通过 KMS 加密后填入，禁止明文；控制台自动解析为环境变量 |

### 运行时调用参数（模型或代码发起请求时）
- **工具 ID**：在智能体/工作流中引用服务的唯一标识，如 `websearch`、`amap_maps`、`firecrawl`。可在 MCP 广场服务详情页复制。
- **输入参数**：由工具定义 Schema（JSON Schema），模型或 SDK 自动填充。例如 `websearch` 的 `query: string`、`num_results: number`。
- **协议端点**：必须严格匹配类型与路径：<br>• `streamableHttp` → POST `/mcp`（当前默认且推荐）<br>• `sse` → GET `/sse`（已逐步淘汰，不兼容新 SDK）

> ⚠️ 注意：若协议类型与端点不匹配（如配置 `streamableHttp` 却访问 `/sse`），将返回错误码 `11200058`（METHOD_NOT_ALLOWED）或 `11200059`（NOT_FOUND）。

## 面向开发者的实用建议

- **优先使用 Streamable HTTP**：所有新接入服务请基于 `/mcp` 端点开发，旧版 SSE 已停用维护，SDK 和平台内部均已切换。
- **敏感信息务必走 KMS**：API Key、Token 等绝不可硬编码或明文填写，必须通过控制台 KMS 凭据功能注入。
- **自定义服务调试三步法**：① 本地运行 `npx @modelcontextprotocol/server-*` 验证功能；② 上传至函数计算 FC 并配置 KMS 凭据；③ 在控制台“在线调试”页测试输入/输出 Schema 是否匹配。
- **QPS 与额度留意**：官方 MCP 服务（如 WebSearch）有免费额度（2000 次/月）和 QPS 限流（15 QPS，主账号与子账号共享），生产环境请提前评估并申请配额。
- **不要尝试访问本地资源**：自定义 MCP 服务运行于函数计算 FC，无法直连本地数据库、文件系统或硬件设备；需访问云资源（如 RDS）时，请配置 VPC 打通或 IP 白名单。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)


