# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具协同能力，指大语言模型在生成响应过程中，主动识别用户意图并按需生成标准化的工具调用请求（而非自由文本），交由外部系统执行后，再将结果注入上下文继续推理。该机制实现了模型与真实世界服务（如搜索、计算、数据库查询等）的安全、可控、可追溯集成。

## 在百炼平台的不同场景中，这个概念如何使用

- **DashScope 原生接口**：通过 `tools` 参数传入 JSON Schema 定义的工具列表，配合 `tool_choice` 控制调用策略（`auto` / `required` / 具体工具名）。模型返回 `output.choices[].message.tool_calls` 字段，含 `id`、`function.name` 和 `function.arguments`，开发者需解析、执行并构造 `tool_result` 回填调用结果。
  
- **Anthropic 兼容 Messages 接口**：使用 `tool_use` 消息类型，模型输出中以 `content` 数组包含 `{"type": "tool_use", "id": "...", "name": "...", "input": {...}}` 结构；需按 Anthropic 协议规范构造 `tool_result` 消息重新提交，支持多轮工具链式调用。

- **OpenAI 兼容 Responses 接口**：**不支持自定义函数调用**，仅内置三类平台托管工具（联网搜索、代码解释器、网页内容提取），由模型自动触发，开发者无需定义 `tools`，也无需手动处理调用逻辑——平台自动完成执行与结果注入，适合快速构建免运维智能助手。

- **Qwen 系列旗舰模型（如 `qwen3.7-plus`）**：原生强化支持函数调用，兼容 OpenAI/Anthropic/DashScope 三种协议，且在长上下文（1M token）、结构化 JSON 输出、多工具并行调用等场景表现更稳定；而 `qwen3.7-max` 等强推理模型默认禁用函数调用，以专注复杂逻辑推演（详见模型选型指南）。

> ⚠️ 注意：函数调用与联网搜索功能互斥——启用 `enable_search: true` 时，`tools` 参数将被忽略，请求将失败。

## 关键参数和配置

| 参数 | 所属接口 | 类型 | 说明 |
|------|----------|------|------|
| `tools` | DashScope、Anthropic 兼容 | array | 工具定义列表，每个元素为 `{ "type": "function", "function": { "name": "...", "description": "...", "parameters": { ... } } }`；`parameters` 必须为合法 JSON Schema（支持 `string`/`number`/`boolean`/`object`/`array` 及嵌套） |
| `tool_choice` | DashScope | string / object | 控制调用行为：<br>`"auto"`（默认，模型自主决定）<br>`"none"`（禁止调用）<br>`{"type": "function", "function": {"name": "xxx"}}`（强制调用指定工具） |
| `tool_choice` | Anthropic 兼容 | string | 仅支持 `"auto"` 或 `"any"`（等效于 `auto`）；不支持强制指定单个工具 |
| `previous_response_id` | OpenAI 兼容 Responses | string | 用于关联上一轮响应（格式 `resp_xxx`），实现多轮对话中工具调用历史的自动维护，**不可用于自定义工具调用** |
| `output_format: "json"` | DashScope | string | 配合函数调用使用，确保模型输出严格遵循 JSON Schema，提升 `arguments` 解析可靠性（推荐开启） |

- **流式响应注意事项**：在 `stream: true` 模式下，`tool_calls` 可能分块返回（尤其 [OpenAI 兼容接口](openai-compatible-interface.md)），建议优先使用非流式模式验证逻辑，或在客户端聚合所有 `delta.tool_calls` 后统一解析。
- **认证与地域**：函数调用能力依赖模型本身支持，调用时仍需标准鉴权（`Authorization: Bearer <api_key>` 或 `X-DashScope-Signature`），且部分模型（如 `qwen-coder-turbo` 的 `completions` 接口）仅限华北2（北京）地域可用。

## 面向开发者：一句话实践建议

> 优先选用 DashScope 原生接口 + `qwen3.7-plus` 模型进行函数调用开发：它提供最完整的工具定义、最稳定的参数解析、最灵活的调用控制，并支持 `output_format: "json"` 强约束，显著降低集成复杂度与出错概率。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)


