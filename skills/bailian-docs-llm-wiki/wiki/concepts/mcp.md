# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台提供的标准化、可扩展的工具调用协议，用于在大语言模型与外部能力（如地图、搜索、数据库、代码执行等）之间建立安全、统一的通信通道。它基于开源 MCP 规范实现，并深度集成阿里云基础设施，屏蔽底层适配差异，使开发者能以一致方式接入和编排各类能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用（Agent 2.0）**：MCP 是默认且唯一的外部能力接入机制。模型根据用户意图自动决策是否调用、调用哪个 MCP 工具（如 `maps_route` 或 `web_search`），支持最多 5 个 MCP 服务并行配置。无需显式编写调用逻辑，由模型自主规划工具链（ReAct 流程），适用于开放式、意图不确定的任务。

- **工作流应用（Workflow）**：通过拖拽“MCP 节点”显式编排工具调用。开发者需手动指定服务、工具名、输入参数映射与输出解析规则，适用于确定性、强流程控制的业务场景（如“先查天气 → 再规划路线 → 最后生成行程卡片”）。

- **高代码应用（Managed Agents API / Assistant API）**：MCP 服务以标准 `tools` 格式注入 Agent 或 Session。SDK 中可通过 `ClientSession.list_tools()` 获取工具列表，并转换为 OpenAI 兼容格式传入 `chat.completions.create`；外部系统亦可直接调用百炼托管的 MCP 端点（如 `https://dashscope.aliyuncs.com/api/v1/mcps/{service-name}/mcp`）。

- **文件自定义处理**：当选择“自定义处理”模式时，文件内容（如图片、PDF）可作为输入参数传递给特定 MCP 工具（如图像风格迁移、文档结构化提取），实现端到端的非文本智能处理。

> ⚠️ 注意：百炼平台已全面统一为 MCP 架构，旧版“插件”概念已下线。所有新接入的外部能力（含官方、三方及自定义）均须通过 MCP 协议注册与调用。

## 关键参数和配置

| 类别 | 参数 | 说明 | 示例值 |
|------|------|------|--------|
| **服务标识** | `服务名称`、`描述` | 仅用于控制台识别，不影响调用逻辑 | `"高德地图"`、`"提供实时路况与导航"` |
| **部署方式** | `安装方式` | 决定启动命令：`npx`（Node.js）、`uvx`（Python）、`http`（远程 SSE） | `"npx"` |
| | `部署模式` | `基础模式`（按次计费，有冷启动延迟）或 `极速模式`（常驻实例，低延迟） | `"极速模式"` |
| | `部署地域` | 函数计算托管地域，影响网络延迟 | `"cn-beijing"` |
| **协议端点** | `type` | 必须与后端严格匹配：`"sse"`（对应 `/sse`）、`"streamableHttp"`（对应 `/mcp`） | `"streamableHttp"` |
| | `url` | 远程地址（HTTP 模式）或本地命令配置（stdio 模式） | `"https://your-server/mcp"` 或 `{ "command": "npx", "args": ["@mcp/server-memory"] }` |
| **安全与鉴权** | `KMS 凭据` | 所有敏感字段（如 API Key、[Token](token.md)）必须通过 KMS 加密，禁止明文填写 | — |
| | `DASHSCOPE_API_KEY` | 百炼平台认证凭证，用于服务间调用与 SDK 鉴权 | `"sk-xxx"` |

## 面向开发者，简洁实用

- ✅ **开通即用**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击“立即开通”即可启用官方服务（如 Amap Maps、WebSearch），部分服务限时免费。
- ✅ **快速自定义**：三种零门槛部署方式：① 一行命令 `npx @mcp/server-memory` 启动内存服务；② 用 AI 网关将现有 REST API 封装为 MCP；③ 通过 OpenAPI 开发者门户一键发布阿里云产品为 MCP 服务。
- ✅ **调试友好**：所有 MCP 工具支持在线“测试工具”，输入 JSON 参数即可验证响应结构与鉴权有效性；失败时返回明确错误码（如 `130022` 表示 Object 子属性未定义）。
- ✅ **生产就绪**：支持多版本管理、KMS 加密凭据、跨地域部署、QPS 限流与调用日志审计，满足企业级安全与可观测性要求。
- ❌ **避坑提示**：  
  - 不要将 `DASHSCOPE_API_KEY` 明文写入代码或配置文件；  
  - `Object` 类型输入参数在 `GET` 请求中不被支持，务必使用 `POST`；  
  - 删除 MCP 服务会导致所有关联应用立即失效，操作前请确认依赖关系。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)
- [llm application](../guides/llm-application.md)


