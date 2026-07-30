# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是阿里云百炼平台提供的标准化、可扩展的工具调用协议，用于在大语言模型与外部能力（如地图、搜索、数据库、代码执行等）之间建立安全、统一的通信通道。它基于开源 MCP 规范实现，并深度集成百炼平台的智能体运行时、工作流引擎与云服务基础设施，使开发者无需为每个工具重复开发适配逻辑，即可声明式接入和编排各类能力。

## 在百炼平台的不同场景中如何使用

- **智能体应用（Agent 2.0）**：MCP 是智能体调用外部工具的**唯一标准协议**。模型根据用户意图自动决策是否调用、调用哪个工具（如 `maps_route` 或 `web_search`），并动态构造参数。最多支持同时配置 5 个 MCP 服务，适用于开放式、意图不确定的任务（如“规划从上海到杭州的自驾路线并查沿途天气”）。

- **工作流应用（Workflow）**：通过拖拽 MCP 节点显式编排工具调用，需手动指定工具 ID（如 `maps_weather`）、输入参数映射与输出解析规则。适用于确定性、步骤明确的业务流程（如“先查天气 → 再生成图表 → 最后发送邮件”）。

- **高代码集成（SDK / REST API）**：开发者可通过 Python/Java SDK 或直接调用百炼 MCP 网关（`https://dashscope.aliyuncs.com/api/v1/mcps/{service-name}/mcp`）接入外部客户端（如 Cherry Studio、Cursor）或自有系统。支持将工具列表动态注入 OpenAI 兼容的 `tools` 参数，无缝对接现有 LLM 应用栈。

> ⚠️ 注意：百炼平台已全面迁移至 MCP 架构，旧版“插件”机制（如 `quark_search`、`code_interpreter`）在新智能体中均以 MCP 协议封装提供；新建应用请统一使用 MCP 接入方式。

## 关键参数和配置

| 类别 | 参数 | 说明 | 开发提示 |
|------|------|------|----------|
| **服务标识** | `服务名称`、`描述` | 仅用于控制台管理，不影响调用逻辑 | 建议命名清晰（如 `"amap-weather-v1"`），便于多版本区分 |
| **部署配置** | `安装方式` | `npx`（Node.js）、`uvx`（Python）、`http`（远程 SSE） | 本地调试推荐 `npx @mcp/server-memory`；生产环境建议 `uvx` 或托管 HTTP |
| | `部署模式` | `基础模式`（按次计费，冷启动延迟约 1–3s）或 `极速模式`（常驻实例，毫秒级响应） | 高频调用场景必选 `极速模式` |
| | `部署地域` | 函数计算 FC 托管区域（如 `cn-beijing`） | 应与智能体/工作流所在地域一致，降低网络延迟 |
| **协议端点** | `type` | 必须匹配后端协议：`"sse"`（对应 `/sse`）或 `"streamableHttp"`（对应 `/mcp`） | 百炼网关仅支持 `streamableHttp`；自建 Server 需严格遵循此约定 |
| | `url` | 远程地址（HTTP 模式）或本地命令配置（stdio 模式） | 示例：<br>`"https://your-mcp-server.com/mcp"`<br>`{ "command": "uvx", "args": ["@mcp/server-http"] }` |
| **安全与鉴权** | `KMS 凭据` | 所有敏感字段（如 API Key、Secret）必须通过 KMS 加密后填入 | **禁止明文填写任何密钥**；控制台会自动加密解密 |
| | `DASHSCOPE_API_KEY` | 外部调用百炼 MCP 网关时必需的认证凭证 | 从 [API 密钥管理](https://ram.console.aliyun.com/manage/ak) 获取，需归属目标工作空间 |

## 面向开发者的实用建议

- ✅ **快速起步**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，开通官方服务（如 Amap Maps、WebSearch），一键添加至智能体即可测试。
- ✅ **自定义服务三步走**：① 用 `npx`/`uvx` 启动开源 MCP Server；② 在控制台创建服务，选择 `http` 模式并填写 URL；③ 在智能体中启用该服务，无需改写模型提示词。
- ✅ **调试技巧**：在智能体调试窗口发送语义明确指令（如“查询北京今日气温”），观察日志中是否出现 `tool_call` 事件及返回结果；失败时优先检查 `type` 与端点路径是否匹配、KMS 凭据是否生效。
- ❌ **避坑提醒**：  
  - 不要混用旧版插件参数（如 `biz_params`）与 MCP 配置；  
  - `Object` 类型输入参数在自定义 MCP 中必须显式定义所有子字段（不能为空）；  
  - 工作流中 MCP 节点的输出变量名需与工具返回 JSON 字段严格一致（区分大小写）。  

MCP 的核心价值在于**协议即契约**——只要符合规范，任何语言、任何部署方式的服务均可被百炼智能体识别与调度。专注你的业务逻辑，让协议处理连接。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [managed agents api](../api/managed-agents-api.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)


