# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配器，即可在智能体或工作流中统一接入和管理各类能力。该协议基于 Anthropic 提出的开源标准 [MCP 官方规范](https://modelcontextprotocol.io/) 实现，并针对百炼平台进行了工程化增强与云服务集成。

## 支持的模型/功能

MCP 本身是协议层，不绑定特定模型，但其调用能力需通过百炼平台的**智能体应用**或**工作流应用**触发。当前支持以下两类使用场景：

- **智能体应用**：大模型根据自然语言输入自动决策是否调用 MCP 工具及选择具体工具（如 `maps_route`, `web_search`），最多可同时配置 5 个 MCP 服务。详见 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式拖入 MCP 节点并手动指定工具（如 `maps_weather`）、输入参数与输出映射，适用于确定性编排任务。

支持的 MCP 服务分为两类：
- **官方 MCP 服务**：由阿里云百炼预部署并托管，包括 Amap Maps、Firecrawl、WebSearch、Sequential Thinking、QuickChart 等，开通即用，部分服务限时免费（如 Amap Maps）[原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **自定义 MCP 服务**：支持三种部署方式：① 使用脚本（npx/uvx）部署开源或自研 MCP Server；② 通过 AI 网关将现有 RESTful API 封装为 MCP；③ 通过 OpenAPI 开发者门户将阿里云产品（如 OSS、ECS）发布为 MCP 服务 [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 3 和文档 5 均提及“Amap Maps 服务限时免费”，但文档 1 的计费说明中未明确标注该服务是否收费。实际以控制台开通页实时显示为准，建议以 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) 中的说明为最新依据。

## 关键参数

MCP 服务配置与调用涉及以下核心参数：

| 参数类别 | 字段名 | 说明 | 示例值 |
|----------|--------|------|--------|
| **服务元信息** | `服务名称`、`描述` | 仅用于平台内标识，不影响模型调用逻辑 | `"高德地图"`、`"提供地理信息与路线规划"` |
| **部署配置** | `安装方式` | 决定启动方式：`npx`（Node.js）、`uvx`（Python）、`http`（远程 SSE） | `"npx"` |
| | `部署方式` | `基础模式`（按次计费，有冷启动延迟）或 `极速模式`（常驻计费，低延迟） | `"基础模式：按次计费"` |
| | `部署地域` | 函数计算 FC 托管地域，影响网络延迟 | `"北京"` |
| **协议端点** | `type` | 必须与后端端点严格匹配：`"sse"` 对应 `/sse`，`"streamableHttp"` 对应 `/mcp` | `"streamableHttp"` |
| | `url` | 远程 MCP Server 地址（HTTP 模式）或本地命令配置（stdio 模式） | `"https://your-server/mcp"` 或 `{ "command": "npx", "args": ["@mcp/server-memory"] }` |
| **鉴权与安全** | `KMS 凭据` | 敏感参数（如 API Key）必须通过 KMS 加密，不可明文填写 | — |
| | `DASHSCOPE_API_KEY` | 外部调用时必需的百炼平台认证凭证 | `"sk-xxx"` |

## 使用方式

### 1. 平台内集成（智能体/工作流）
- **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务卡片 → “立即开通”。
- **添加至应用**：
  - *智能体*：在应用编辑页 → “MCP 服务” → 选择已开通服务 → 保存。
  - *工作流*：从工具栏拖入 “MCP 节点” → 选择服务 → 指定工具 → 配置输入/输出变量映射。
- **测试验证**：在智能体对话框或工作流测试面板中发送符合工具语义的指令（如 `查询杭州天气`），观察是否触发调用 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 2. 外部调用（第三方应用或 SDK）
- **一键集成**：对 Cherry Studio、Cursor 等支持 MCP 的客户端，可在服务详情页选择对应客户端 → “一键配置”，自动注入 `DASHSCOPE_API_KEY` 与服务元数据。
- **SDK 编码集成**：
  - 安装 `mcp` 和 `openai` 客户端库；
  - 使用 `streamablehttp_client` 连接 MCP Server（URL 格式：`https://dashscope.aliyuncs.com/api/v1/mcps/{service-name}/mcp`）；
  - 通过 `ClientSession.list_tools()` 获取工具列表，转换为 OpenAI 兼容格式后传入 `chat.completions.create` 的 `tools` 参数；
  - 在工具调用循环中使用 `session.call_tool()` 执行具体操作。

完整示例见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 文档中的 Python SDK 代码片段。

## 限制和注意事项

- **模型兼容性**：MCP 仅支持集成于百炼平台的**智能体应用**或**工作流应用**，**不可直接用于调用千问 API**（如 `qwen-max` 的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）[原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **网络与权限**：
  - 自定义 MCP 服务托管于函数计算 FC，**无固定出口公网 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通；
  - **不支持访问用户本地资源**（如本地文件、硬件设备），此类服务应在本地部署。
- **部署约束**：
  - 私有 npm/PyPI 仓库的包暂不支持直接 `npx`/`uvx` 部署，需发布至公共仓库或改用 `http` 方式；
  - `npx`/`uvx` 部署的服务版本更新后**不会自动同步**，需手动重新部署。
- **错误处理**：常见错误码（如 `11200044` 连接拒绝、`11200051` 限流、`11200054` 协议解析失败）均有明确排查路径，优先使用 `curl` 测试端点连通性，并检查 `type` 与 URL 路径是否匹配（`/sse` vs `/mcp`）。
- **[Token](../concepts/token.md) 开销**：MCP 调用返回的内容会作为上下文输入模型，**直接增加输入 [Token](../concepts/token.md) 数量**；同时可能因上下文更丰富而间接增加输出 [Token](../concepts/token.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)



