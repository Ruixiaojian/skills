# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、自主规划并执行外部工具（如搜索、计算、代码解释、文生图等）的关键能力。它通过结构化工具定义与模型推理协同，将自然语言请求转化为确定性 API 调用，实现“说即所得”的智能交互。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非独立服务，而是**模型能力 + 工具集成 + 接口协议**三者协同的结果，主要应用于以下三类场景：

- **文本生成模型的自主工具调度**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-omni-plus` 等支持 Function Calling 的文本/多模态模型，在接收到含工具需求的用户输入（如“查一下今天北京的天气”或“画一只戴墨镜的熊猫”）时，可自动输出符合 OpenAI 兼容格式的 `tool_calls`，无需工作流显式编排。该能力需配合 `tools` 参数传入工具定义，并通过 `tool_choice` 控制调用策略（`auto`/`required`/具体工具名）。

- **[插件](plugin.md)（Plug-in）系统的底层执行机制**：所有官方、三方及自定义[插件](plugin.md)在被调用时，其实际触发依赖于模型的函数调用能力。例如，当启用 `quark_search` [插件](plugin.md)后，模型若决定调用搜索，会生成对应 `tool_call`，平台自动解析并转发至插件网关；插件返回结果后，模型继续生成最终回复。**插件本身不提供函数调用能力，而是被函数调用所驱动**。

- **Assistant API 与兼容接口的标准交互范式**：百炼完全兼容 OpenAI Assistant API 的 `tools`、`tool_choice`、`tool_calls`、`tool_responses` 字段语义。开发者可通过统一 SDK（如 OpenAI Python SDK）调用 `chat.completions.create`，只需设置 `base_url` 指向百炼兼容端点，即可复用现有函数调用逻辑，无缝迁移。

> ⚠️ 注意：并非所有模型都支持函数调用。例如 `qwen-long` 明确不支持 Function Calling 和内置工具，仅适用于纯长文档摘要；`qwen3.5-omni-flash` 在 WebSocket 流式模式下也不支持。实际使用前请以控制台模型详情页的「功能支持」栏为准。

## 关键参数和配置

| 参数 | 类型 | 说明 | 百炼特有约束 |
|------|------|------|--------------|
| `tools` | array of object | 定义可用工具列表，每个对象包含 `type`（固定为 `"function"`）、`function.name`、`function.description`、`function.parameters`（JSON Schema 格式） | `parameters` 必须为合法 JSON Schema，不支持 `anyOf`/`oneOf`；`required` 字段必须显式声明，否则模型可能遗漏必填参数 |
| `tool_choice` | string / object | 控制模型是否及如何调用工具：<br>• `"auto"`（默认）：模型自主决策<br>• `"none"`：禁用调用<br>• `"required"`：必须调用一个工具<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定工具 | 百炼对 `required` 模式支持稳定；若工具定义缺失或 schema 不合法，模型可能返回普通文本而非 `tool_calls` |
| `enable_thinking` | boolean | 是否启用模型内部推理链路（影响 `tool_calls` 的规划质量） | 默认 `true`；关闭（`false`）可降低 token 成本，但可能降低复杂工具链的调用准确率；仅 Responses/Batch 接口支持，WebSocket 流式暂不支持 |
| `response_format` | object | 强制结构化输出格式 | 若同时启用 `tool_calls` 和 `{"type": "json_object"}`，模型优先保证工具调用完整性，JSON 输出可能被延迟至工具响应后生成 |

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `qwen3.7-plus` + `quark_search` 插件 + `tool_choice="auto"` 即可跑通首个函数调用 Demo；无需额外部署。
- ✅ **调试建议**：首次集成时，先关闭 `stream=true`，查看完整响应体中的 `choices[0].message.tool_calls` 字段，确认模型是否正确识别意图并生成有效调用。
- ✅ **错误排查**：若模型未触发 `tool_calls`，检查三项：① 模型是否在[支持列表](#支持的模型)中；② `tools` 参数是否 JSON 格式合法且 `parameters` 定义清晰；③ 用户 query 是否明确包含工具可解决的任务（避免模糊表述如“帮我处理一下”）。
- ❌ **避坑提示**：不要在 `qwen-long` 或 `qwen3.5-omni-flash`（WebSocket 模式）上尝试函数调用——它们不支持，会静默降级为普通文本生成。
- 📦 **生产就绪**：函数调用产生的 `tool_calls` 和后续 `tool_responses` 构成完整 trace，可在百炼控制台「调用日志」中按 `request_id` 追踪全链路，便于问题定位与效果分析。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)


