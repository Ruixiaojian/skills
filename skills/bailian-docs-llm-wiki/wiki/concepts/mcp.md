# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台提供的标准化工具调用协议，用于在大语言模型与外部能力（如搜索、地图、计算、自定义 API 等）之间建立安全、声明式、可编排的上下文交互通道。它将工具抽象为统一语义接口，使模型能基于自然语言意图自主规划调用，同时支持开发者在工作流中精确控制执行逻辑。

## 在百炼平台的不同场景中如何使用

MCP 是百炼平台统一的工具集成标准，已全面替代旧版“插件”机制（尤其在 Agent 2.0 中），具体使用方式依应用形态而异：

- **智能体应用（Agent 2.0）**：  
  在创建智能体时，于「工具」配置区勾选已开通的 MCP 服务（最多 5 个）。模型根据用户输入自动识别意图、选择工具、生成参数并调用——全程无需显式提示词指令或硬编码工具名。例如：“查上海明天天气”会自动触发 `maps_weather` 工具；“规划从杭州东站到西湖的步行路线”可能协同调用 `amap_geocoding` + `amap_directions`。所有调用过程以 ReAct 形式可视化展示（思考→调用→观察→推理）。

- **工作流应用（Workflow）**：  
  拖入「MCP 节点」，从下拉列表中选择已开通的 MCP 服务，并指定具体工具 ID（如 `web_search`、`firecrawl_fetch`）。输入参数需由上游节点（如大模型节点或变量节点）提供结构化 JSON，支持动态拼接与类型校验。适用于确定性任务，如“先搜索最新政策 → 再提取关键条款 → 最后生成摘要”。

- **高代码应用（Rich Code）**：  
  可通过 SDK（如 `mcp.client.streamable_http`）直接集成 MCP 服务，兼容 OpenAI-style 工具调用格式（`tools`, `tool_calls`, `tool_responses`）。适合需要细粒度控制、多轮状态管理或与自有业务逻辑深度耦合的场景。

> ⚠️ 注意：MCP 服务**不可通过千问原始 API（如 `/v1/chat/completions`）直接调用**，仅限百炼平台内上述三类应用使用。

## 关键参数和配置

MCP 服务在百炼控制台配置时需设置以下核心字段（均在「MCP 服务管理」页填写）：

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `service_name` | ✅ | 服务唯一标识，仅用于控制台显示与区分 | `"高德天气查询"` |
| `type` | ✅ | 通信协议类型，决定连接方式与端点路径 | `"sse"`（对应 `/sse` GET）、`"streamableHttp"`（对应 `/mcp` POST）、`"stdio"`（本地进程） |
| `command` / `url` | ✅ | 启动命令（`stdio`）或远程服务地址（`sse`/`streamableHttp`） | `"npx @aliyun/mcp-amap-weather"` 或 `"https://my-mcp-service.com"` |
| `env` | ❌（但强烈建议） | 敏感环境变量（API Key、[Token](token.md) 等），**必须通过 KMS 凭据加密注入**，禁止明文填写 | `{"AMAP_API_KEY": "{{kms:xxx}}"}` |
| `deployment_mode` | ❌（默认 `basic`） | 部署模式，影响冷启动与计费 | `"basic"`（按次计费，有延迟）、`"ultra"`（常驻实例，低延迟，额外费用） |

> 🔑 配置要点：  
> - `type` 必须与服务端实现的协议严格匹配，否则返回错误码 `11200058`；  
> - 自定义 MCP 服务部署在函数计算（FC），无固定公网出口 IP，访问云数据库等资源需配置 VPC 或白名单；  
> - 所有工具参数定义需符合 [MCP Schema 规范](https://modelcontextprotocol.io/spec)（JSON Schema 格式），百炼控制台提供在线校验。

## 面向开发者：一句话实践指南

> **用 MCP，不是写适配器，而是声明能力**：开通服务 → 配置 `type`+`url`+`env` → 在智能体中勾选，或在工作流中拖入节点并指定工具 ID —— 模型即刻获得该能力，你只需专注 Prompt 设计与业务编排。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)


