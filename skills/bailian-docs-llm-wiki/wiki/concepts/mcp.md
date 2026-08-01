# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol, MCP）是百炼平台统一的、标准化的外部工具集成协议，用于在大模型应用（如智能体、工作流）与外部服务之间建立安全、可扩展、模型友好的双向通信通道。它将工具能力抽象为声明式接口，由平台自动完成意图识别、参数生成、调用编排与结果注入，使大模型能像调用内置函数一样使用地理、天气、搜索、数据库等外部能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用（Agent 2.0）**：MCP 服务以“能力插槽”形式接入，最多同时启用 5 个。模型根据用户自然语言指令（如“查上海今天气温并画趋势图”）自动推理所需工具、生成结构化参数，并串联调用多个 MCP 服务。整个过程无需人工编排，支持 ReAct 多轮规划与可视化回溯。

- **工作流应用（Workflow）**：MCP 作为独立节点存在，需显式选择具体工具（如 `maps_weather` 或 `news_search`），并依赖上游大模型节点（如“信息提取”）将用户输入解析为符合 `inputSchema` 的 JSON 参数。适合流程确定、结果需精确控制的业务场景（如审批链+数据校验+通知推送）。

- **高代码/自定义应用**：通过 `mcp` Python SDK（如 `streamablehttp_client`）直接连接 MCP Server 地址（`https://dashscope.aliyuncs.com/api/v1/mcps/{service}/mcp`），实现细粒度调用控制、错误重试与结果后处理，适用于需要深度定制或与现有系统集成的场景。

- **第三方客户端集成**：支持 Cherry Studio、Cursor 等 IDE 工具一键配置，通过标准 Streamable HTTP 或 SSE 协议接入，无需修改客户端核心逻辑，即可复用百炼托管的 MCP 服务生态。

> ⚠️ 注意：MCP **不支持**作为参数直接传入 `dashscope.ChatCompletion.create()` 等原生千问 API 调用；仅限百炼平台内应用或通过官方 SDK/协议接入。

## 关键参数和配置

| 类别 | 参数名 | 说明 | 实用提示 |
|--------|---------|------|-----------|
| **服务注册** | `type` | 协议类型，必须与后端端点严格匹配 | 必填；仅支持 `"streamableHttp"`（推荐，对应 `/mcp`）或 `"sse"`（旧版，对应 `/sse`）；错配将返回 `11200058` 错误 |
| | `url` | MCP Server 公网可访问地址 | 若部署在函数计算（FC），需确保下游服务开放端口，并配置 IP 白名单或 VPC 打通 |
| | `env` | 环境变量注入（仅 `npx`/`uvx` 部署方式） | **禁止明文写密钥**；敏感信息（如 `API_KEY`）必须通过 KMS 凭据加密管理 |
| **工具定义** | `tool.name` | 工具唯一标识符 | 智能体中由模型自动匹配；工作流中需手动选择（如 `amap_geocode`） |
| | `inputSchema` | JSON Schema 定义的输入参数结构 | **决定模型能否正确生成参数**；System Prompt 中需清晰描述该 schema（例如：“城市名必须为字符串，不可为空”） |
| | `description` | 工具功能简述（面向模型） | 影响模型调用准确性；应包含典型输入、输出、限制条件（如“仅支持中国境内城市”） |

## 面向开发者，简洁实用

- ✅ **快速上手**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，开通服务 → 在智能体/工作流中勾选/拖入 → 测试对话即生效。  
- ✅ **调试要点**：  
  - 检查 `url` 是否可公网 `curl -v {url}/mcp`；  
  - 验证 `inputSchema` 是否与模型实际输出字段完全一致（大小写、嵌套层级）；  
  - 使用 `streamableHttp` 协议时，响应体必须为 `application/json`，且含 `result` 字段。  
- ✅ **性能注意**：MCP 返回内容将作为上下文注入模型输入，显著增加 Token 消耗；对长响应，建议在服务端做摘要或分页。  
- ✅ **安全红线**：MCP 服务运行于函数计算，**无法访问本地文件、数据库或内网资源**；如需访问云数据库，请配置 FC 的 VPC 及白名单。  
- ❌ **避坑提醒**：旧版 SSE 服务需先“取消开通”再“重新开通”才能升级至 Streamable HTTP；自定义 MCP 服务发布前，务必通过控制台“测试工具”验证成功。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [application support](../guides/application-support.md)


