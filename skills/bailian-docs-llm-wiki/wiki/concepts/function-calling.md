# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化工具请求，并协同外部能力完成复杂任务的核心机制。它不是简单的 API 转发，而是模型基于对话上下文自主决策“是否调用”“调用哪个函数”“传入哪些参数”的端到端推理过程，最终由平台调度执行并注入结果回模型继续生成。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口能力，而是贯穿多个服务层级的统一语义能力，具体体现为以下四类场景：

- **Qwen 系列模型 API（OpenAI/Anthropic 兼容 & DashScope 原生）**：通过 `tools` 参数声明可用函数列表，配合 `tool_choice` 控制调用策略（`auto`/`required`/`none`）。模型返回 `tool_calls` 数组（DashScope）或 `function_call` 字段（OpenAI 兼容），开发者需解析、执行并以 `tool_result` 或 `tool_use` 消息形式回传结果，形成完整调用闭环。

- **Managed Agents（托管智能体）**：函数调用由 Agent 运行时自动管理。当 Session 中模型输出 `tool_calls` 事件时，平台根据绑定的 Skill（ZIP 工具包）或 MCP 服务自动分发执行；执行结果经沙箱安全校验后，作为 `tool_result` 事件注入会话，无需应用层手动拼接消息。

- **Omni Realtime（实时多模态）**：在 WebSocket 会话中，模型可基于语音/文本输入动态触发 `tool_calls`，客户端通过 `conversation.item.create` 回填结果。该场景强调低延迟与状态连续性，VAD 检测与工具响应需协同优化，避免打断自然对话流。

- **插件（Plug-in）与 MCP（Model Context Protocol）**：二者是函数调用的**能力供给层**。插件定义 HTTP 工具的结构化契约（`input_params`/`output_params`），MCP 提供标准化上下文传输协议（SSE/Streamable HTTP）。它们不直接暴露调用入口，而是被上述上层服务（API/Agent/Omni）引用和调度，实现“模型决策 → 平台路由 → 插件/MCP 执行 → 结果注入”的解耦链路。

> ⚠️ 注意：函数调用能力**不可跨服务混用**。例如，Qwen API 的 `tools` 无法调用 Managed Agents 中注册的 Skill；MCP 服务也不能直接接入 Qwen 原始 API —— 必须通过智能体或工作流应用作为统一入口。

## 关键参数和配置

函数调用的启用与行为由以下关键参数控制，不同接口存在差异，请按实际场景选用：

| 参数 | 位置 | 说明 | 典型值 | 注意事项 |
|------|------|------|--------|----------|
| `tools` | 请求 body | 工具定义数组，含 `name`、`description`、`parameters`（JSON Schema） | `[{"name":"get_weather","description":"查询城市天气","parameters":{"type":"object","properties":{"city":{"type":"string"}}}}]` | DashScope 和 [OpenAI 兼容接口](openai-compatible-interface.md)均支持；MCP/插件需先发布为工具才能在此声明 |
| `tool_choice` | 请求 body | 控制模型是否及如何调用工具 | `"auto"`（默认）、`"required"`（强制调用）、`{"type":"function","function":{"name":"xxx"}}`（指定函数） | [OpenAI 兼容接口](openai-compatible-interface.md)使用 `function_call` 字段，语义等价 |
| `enable_search` | Omni Realtime `session.update` | 启用联网搜索（与 `tools` 互斥） | `true` | 仅 `qwen3.5-omni-realtime` 系列支持 |
| `mcpServers` | 智能体/工作流配置页 | MCP 服务注册表，声明可用 MCP 端点 | `{"websearch": {"url": "https://.../sse", "type": "sse"}}` | 配置后由模型或工作流节点自动调度，无需在 API 请求中重复传 `tools` |
| `skill_ids` | Managed Agents `POST /agents` | 绑定已审核的 Skill（ZIP 工具包）ID 列表 | `["skill_xxx"]` | Skill 版本锁定，更新需重新挂载 |

## 面向开发者，简洁实用

- ✅ **必做三步**：1）在控制台开通并授权插件/MCP/Skill；2）在请求中正确声明 `tools`（或配置对应服务）；3）实现工具执行逻辑 + 结果回填（注意字段名：DashScope 用 `tool_results`，OpenAI 兼容用 `function_call` + `tool_calls`）。
- 🚫 **避坑提示**：
  - 不要将 `tools` 参数与 `enable_search: true` 同时设置（Omni Realtime）；
  - [OpenAI 兼容接口](openai-compatible-interface.md)返回的 `function_call` 是单对象，DashScope 返回的 `tool_calls` 是数组，解析逻辑需区分；
  - 流式响应中，工具调用事件（如 `tool_calls`）可能出现在任意 chunk，需持续监听直至 `finish_reason="tool_calls"`；
  - 所有工具返回内容计入模型输入 token，长响应可能导致超 context window，建议对工具输出做摘要裁剪。
- 🔧 **调试建议**：开启 `stream=false` + `debug=true`（DashScope 支持）查看完整推理链；使用 `dashscope` SDK 的 `ToolCallHandler` 自动处理解析与回填，减少胶水代码。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [more about models](../api/more-about-models.md)


