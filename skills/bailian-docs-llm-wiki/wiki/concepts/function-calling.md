# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、自主选择并执行外部工具能力的核心机制。它使大模型不仅能生成文本，还能在运行时动态调用搜索、代码解释、网页提取等预定义工具，实现“思考→决策→执行”的闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用不是独立接口，而是嵌入在多种模型调用协议中的**能力模式**，其启用方式和行为因协议而异：

- **OpenAI 兼容 Chat Completions 接口**：需显式传入 `tools` 数组（定义工具 schema）并设置 `tool_choice="auto"`（或指定工具名）。模型返回 `tool_calls` 字段，开发者需解析后同步调用对应工具，再将结果以 `tool_message` 形式拼入下一轮 `messages` 提交。  
  ✅ 支持模型：`qwen-max`、`qwen-plus`、`qwen-turbo` 等文本模型（需 DashScope 原生或 OpenAI 兼容 v1.3+）  
  ❌ 不支持：`qwen-turbo` 在 Anthropic Messages 接口下不可用；纯 `completions` 接口（如代码补全）不支持函数调用。

- **Anthropic 兼容 Messages 接口**：使用 `tool_use` 结构化输出，模型直接返回 `content` 中嵌套的 `{"type": "tool_use", "name": "...", "input": {...}}` 对象。开发者按标准 tool use 协议处理，无需手动构造 `tool_message`。  
  ✅ 支持模型：`qwen3.7-plus`、`qwen3.5-omni-plus` 等旗舰文本/全模态模型  
  ⚠️ 注意：该接口暂不支持 `qwen-turbo`，且流式响应格式与 OpenAI 不兼容。

- **DashScope 原生接口**：通过 `enable_search=true`、`enable_code_interpreter=true` 等布尔开关启用内置工具；也可通过 `tools` + `tool_choice` 实现自定义工具调度。返回字段为 `output.choices[0].message.tool_calls`（同步）或 `task_result.tool_calls`（异步）。  
  ✅ 最高控制粒度，支持调试字段（如 `tool_call_id`、`tool_name`）、细粒度错误码（`InvalidToolCall`）及失败重试策略。

- **Responses 接口（OpenAI Responses）**：开箱即用——无需传 `tools`，模型自动判断是否调用联网搜索、代码解释器或网页提取。开发者只需关注最终 `output.text` 或结构化 `output.data`，底层工具调用完全透明。  
  ✅ 适合轻量级应用，降低集成复杂度；默认启用全部内置工具，无需额外配置。

> 💡 关键区别：OpenAI/Anthropic 接口要求开发者**显式管理工具调用生命周期**（解析→执行→回填），而 Responses 接口由平台**全自动托管**，二者不可混用。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 适用协议 |
|------|------|------|------|----------|
| `tools` | array | 否（启用时必填） | 工具定义列表，每个对象含 `type`（`function`）、`function.name`、`function.description`、`function.parameters`（JSON Schema） | OpenAI Chat, Anthropic Messages, DashScope 原生 |
| `tool_choice` | string / object | 否 | 控制调用策略：`"auto"`（模型自主决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | OpenAI Chat, DashScope 原生 |
| `enable_search` | boolean | 否 | 启用内置联网搜索工具（返回实时网页摘要） | DashScope 原生 |
| `enable_code_interpreter` | boolean | 否 | 启用内置代码解释器（支持 Python 执行与文件 I/O） | DashScope 原生 |
| `previous_response_id` | string | 否（Responses 接口推荐） | 上一轮响应的顶层 `id`，用于自动关联上下文及工具调用历史 | Responses 接口 |

⚠️ 注意事项：
- 工具 schema 中 `parameters` 必须为严格 JSON Schema（不支持 `anyOf`/`oneOf`），建议使用 [JSON Schema Validator](https://json-schema.org/) 校验；
- `tool_call_id` 由模型生成，**不可自行构造**，必须原样透传至工具执行结果回填；
- 所有工具调用均计入请求 token 消耗，`tools` 定义本身也占用 [prompt](../guides/prompt.md) token；
- 异步任务（如文生图）不支持函数调用，仅同步文本/多模态模型支持。

## 面向开发者，简洁实用

- ✅ **快速上手**：用 Responses 接口 + `qwen3.7-plus`，零配置即可获得搜索+代码能力；  
- ✅ **精细控制**：选 DashScope 原生接口 + `tools` + `enable_search`，调试时查看 `output.usage.tool_tokens` 分析开销；  
- ✅ **生产就绪**：在 OpenAI 兼容 SDK 中，用 `openai` v1.42+ 的 `client.chat.completions.create(..., tool_choice="auto")`，自动处理 `tool_calls` 解析与回填逻辑；  
- ❌ **避免踩坑**：不要在 `completions` 接口或 `qwen-audio` 模型中尝试函数调用——它们根本不支持该能力；  
- 🛠️ **调试技巧**：开启 `debug=true`（DashScope 原生）或检查 `error.code == "InvalidToolCall"` 快速定位 schema 错误。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)


