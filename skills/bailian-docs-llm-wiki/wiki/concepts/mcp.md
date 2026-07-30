# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是阿里云百炼平台提供的标准化、安全、可扩展的工具接入协议，用于在大语言模型与外部能力（如地图、搜索、数据库、图像生成等）之间建立统一通信通道。它基于开源 MCP 规范（[modelcontextprotocol.io](https://modelcontextprotocol.io/)）实现，并深度集成百炼平台的智能体运行时、工作流引擎与云服务基础设施，使开发者无需重复开发适配层即可复用和编排各类工具能力。

## 在百炼平台的不同场景中如何使用

MCP 是百炼平台统一的工具抽象层，已全面替代旧版“插件”机制（见 `llm application` 文档说明），所有外部能力均通过 MCP 协议接入。具体使用方式依应用类型而异：

- **智能体应用（Agent）**：  
  模型根据用户自然语言意图自主决策是否调用 MCP 工具、选择哪个工具、传入哪些参数，并支持多轮动态调用（如先搜索→再解析→最后绘图）。最多可同时启用 5 个 MCP 服务。配置路径：应用编辑页 → “MCP 服务” → 选择已开通服务 → 保存。

- **工作流应用（Workflow）**：  
  需显式拖入 **MCP 节点**，手动指定目标服务、具体工具（如 `maps_weather`）、输入参数映射（如将变量 `city` 映射为工具参数 `location`）及输出结果提取规则。适用于确定性、强编排逻辑的任务。

- **Managed Agents（托管智能体运行时）**：  
  MCP 服务作为可选能力挂载至 Agent 实例，在沙箱环境中与内置工具（`bash`/`read`/`write` 等）协同执行。调用过程通过事件流（`tool_call` / `tool_output`）透出，便于监控与调试。

- **外部 SDK 或第三方客户端（如 Cherry Studio、Cursor）**：  
  通过百炼提供的 MCP 兼容 endpoint（格式：`https://dashscope.aliyuncs.com/api/v1/mcps/{service-name}/mcp`）直接连接，使用标准 `streamablehttp_client` 客户端调用 `list_tools()` 和 `call_tool()`，无缝对接 OpenAI-style `tools` 接口。

> ✅ 提示：所有自定义工具（包括原“插件”）必须先发布为 MCP 服务，再在智能体或工作流中添加——平台内不再支持非 MCP 的直连插件。

## 关键参数和配置

MCP 服务的配置分为元信息、部署、协议端点、安全四类，核心字段如下：

| 类别 | 字段 | 说明 | 示例值 |
|------|------|------|--------|
| **服务元信息** | `服务名称`、`描述` | 仅用于控制台标识，不影响调用逻辑 | `"高德地图"`、`"提供地理编码与路线规划"` |
| **部署配置** | `安装方式` | 启动方式：`npx`（Node.js）、`uvx`（Python）、`http`（远程 SSE） | `"npx"` |
| | `部署模式` | `基础模式`（按次计费，有冷启动延迟）或 `极速模式`（常驻计费，低延迟） | `"极速模式"` |
| | `部署地域` | 函数计算 FC 托管地域，影响网络延迟 | `"北京"` |
| **协议端点** | `type` | 必须与后端严格匹配：`"sse"` 对应 `/sse`，`"streamableHttp"` 对应 `/mcp` | `"streamableHttp"` |
| | `url` | 远程地址（HTTP 模式）或本地命令配置（stdio 模式） | `"https://your-server/mcp"` 或 `{ "command": "npx", "args": ["@mcp/server-memory"] }` |
| **安全与鉴权** | `KMS 凭据` | 所有敏感参数（如 API Key、Secret）**必须**通过 KMS 加密，禁止明文填写 | — |
| | `DASHSCOPE_API_KEY` | 百炼平台认证凭证，调用方必需提供 | `"sk-xxx"` |

> ⚠️ 注意：`Object` 类型输入参数在 `GET` 请求下不支持，仅 `POST` 允许；子属性必须显式定义，否则发布失败（错误码 `130022`）。

## 面向开发者的实用建议

- **快速起步**：优先使用 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 中的官方服务（如 Amap Maps、WebSearch、QuickChart），开通即用，部分限时免费。
- **自建服务**：推荐使用 `npx @mcp/server-memory` 或 `uvx @mcp/server-memory` 快速启动本地 MCP Server；生产环境建议通过 AI 网关封装现有 RESTful API，或通过 OpenAPI 开发者门户将阿里云产品（OSS/ECS）一键发布为 MCP 服务。
- **调试技巧**：在智能体调试窗口发送语义明确指令（如 `查询上海浦东机场实时天气`），观察是否触发 `tool_call` 事件；工作流中启用“节点日志”查看完整输入/输出。
- **权限准备**：确保主账号或 RAM 子账号已授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`，子账号还需 `ram:CreateServiceLinkedRole` 权限。
- **版本管理**：MCP 服务更新后需重新测试并发布，已关联的应用不会自动生效；删除服务将导致所有关联应用立即失效（不可逆）。

MCP 不绑定特定模型，但推荐使用 `qwen-max`、`qwen-plus` 等具备强工具调用与多步规划能力的模型以获得最佳效果。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [managed agents api](../api/managed-agents-api.md)
- [managed agents](../guides/managed-agents.md)


