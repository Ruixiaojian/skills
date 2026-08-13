# 函数调用

函数调用（Function Calling）是百炼平台中大语言模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行的关键能力。它不是简单的 API 请求转发，而是模型在推理过程中自主规划、参数提取、格式校验并输出标准化 `tool_calls` 的闭环过程，是实现“模型驱动自动化”的核心机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口特性，而是贯穿多个能力层的横切能力，具体体现为：

- **DashScope 原生模型 API**：通过 `tools` 参数传入 JSON Schema 定义的工具列表，模型在响应中返回 `output.tool_calls` 字段（含 `id`、`function.name`、`function.arguments`），开发者需解析后同步调用对应工具，并将结果以 `tool_result` 形式回填至下一轮 `messages` 继续推理。
- **Managed Agents（托管智能体）**：函数调用由 Agent 运行时自动接管——模型输出 `tool_calls` 后，平台在沙箱内安全执行已挂载的 Skill 或插件，无需开发者手动解析或调度；事件流中会推送 `tool_call_started` 和 `tool_call_finished` 事件，便于监控与调试。
- **插件（Plug-in）系统**：所有官方/三方/自定义插件均以函数调用形式接入。模型根据 `tool_id` 和高级配置（如典型参数样例）生成调用请求，平台负责鉴权、参数透传（`biz_params`）、超时控制与结果归一化，屏蔽底层协议差异。
- **Application Call（应用调用）**：当智能体应用配置了插件或工作流中嵌入了插件节点时，函数调用在内部自动触发；开发者仅需在 `input` 中提供自然语言指令，无需显式构造 `tools`，平台在应用编排层完成调用链路。
- **[OpenAI 兼容接口](openai-compatibility.md)（Responses 模式）**：该模式内置函数调用能力（区别于标准 Chat Completions），模型可自主触发搜索、代码解释等能力，响应中直接包含 `choices[0].message.tool_calls`，且支持多轮自动续调，适合快速构建免编排的智能助手。

> ⚠️ 注意：OpenAI 兼容的 `chat/completions` 接口（非 Responses 模式）**不支持函数调用**；`qwen-vl` 等[多模态](multimodal.md)模型仅在 DashScope 原生接口中支持函数调用，[OpenAI 兼容接口](openai-compatibility.md)暂不支持。

## 关键参数和配置

| 参数/配置 | 说明 | 开发者须知 |
|-----------|------|------------|
| `tools`（数组） | 必填（除 Responses 模式外）。每个元素为 `{ "type": "function", "function": { "name": "...", "description": "...", "parameters": { ... } } }`，需严格遵循 JSON Schema 规范（支持 `string`/`number`/`boolean`/`object`/`array`，`null` 不支持）。 | Schema 中 `required` 字段必须存在，`properties` 中 Object 类型子字段**不可为空**，否则模型可能无法生成有效参数。 |
| `tool_choice`（字符串或对象） | 控制调用策略：`"auto"`（默认，模型自主决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定）。 | 生产环境建议显式设为 `"auto"` 或精确函数名，避免模型跳过必要工具。 |
| `tool_id`（插件专用） | 插件内工具的唯一标识符，非 Schema 中的 `name`。在插件市场或控制台复制获取，用于 `tools` 定义及 SDK 调用。 | `tool_id` 与 `function.name` 是两个不同概念：前者是平台侧注册 ID，后者是模型推理时使用的逻辑名，二者需在插件发布时映射一致。 |
| `enable_search` / `code_interpreter` 等布尔开关 | Responses 模式下的快捷开关，等价于预置特定 `tools`。 | 开关开启后，模型仍需自主判断是否调用；若需强约束（如必须执行搜索），应改用 `tools` + `tool_choice` 显式控制。 |
| `stream` 与 `tool_calls` 解析 | 流式响应中，`delta.content` 可能为空，关键信息在 `delta.tool_calls` 中分 chunk 返回。 | 必须累积 `delta.tool_calls` 的所有 chunk 后再 JSON.parse，不可对单个 chunk 直接解析；SDK 已内置聚合逻辑，推荐优先使用。 |

## 面向开发者，简洁实用

- ✅ **首选 DashScope 原生接口**：功能最全、控制最细、[多模态](multimodal.md)支持完备，是生产环境函数调用的唯一推荐路径。
- ✅ **Schema 设计要克制**：参数越少、类型越明确（避免嵌套过深的 `object`），模型提取准确率越高；为复杂参数提供 `examples`（高级配置）可显著提升鲁棒性。
- ✅ **始终校验 `tool_calls` 再执行**：模型可能返回无效 `arguments`（如 JSON 格式错误、缺失必填字段），务必在调用外部工具前做 `JSON.parse()` + 字段校验。
- ✅ **结果回填需严格匹配 `id`**：调用工具后，必须将结果以 `{"tool_call_id": "...", "role": "tool", "content": "..."}` 格式加入下一轮 `messages`，`tool_call_id` 必须与模型返回的 `id` 完全一致。
- ❌ **不要在 OpenAI 兼容 `chat/completions` 中尝试 `tools`**：该字段会被忽略，且无任何报错提示。
- ❌ **不要复用未发布的插件或禁用状态的 Skill**：函数调用会直接失败，错误码通常为 `InvalidToolId` 或 `ToolNotAvailable`。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [plug in](../guides/plug-in.md)
- [application call](../api/application-call.md)
- [more about models](../api/more-about-models.md)


