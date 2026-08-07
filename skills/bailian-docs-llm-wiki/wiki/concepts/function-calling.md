# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、自主选择并执行外部工具能力的核心机制。它允许大模型在生成响应前，根据对话上下文动态决定是否调用预定义的函数（如搜索、计算、数据库查询、API 调用等），并将结果整合进最终输出，从而实现“思考→决策→行动→反馈”的闭环。

## 在百炼平台的不同场景中，这个概念如何使用

- **文本生成模型（如 `qwen3.7-plus`、`qwen3.8-max`）**：通过 `tools` 参数传入函数定义，模型在推理过程中自动判断是否需要调用、调用哪个函数及传入哪些参数；支持结构化 JSON 输出与联网搜索（二者互斥）。
- **全模态实时模型（如 `qwen3.5-omni-realtime`）**：在 WebSocket 会话中通过 `session.update` 配置 `tools`，模型触发调用后，服务端发送 `tool_call` 事件，客户端需同步回传执行结果（`conversation.item.create`），再由模型继续生成。
- **[OpenAI 兼容接口](openai-compatible-interface.md)（Responses API）**：作为首选 Agent 接口，原生强化函数调用体验——自动管理工具调用链、上下文延续与错误重试；支持内置工具（联网搜索、代码解释器、网页抓取）与自定义工具混合使用。
- **多模态模型（如 `qwen3.5-omni-plus`）**：支持跨模态的函数调用，例如结合图像理解结果后调用天气 API，或解析语音转录文本后触发日程创建函数。

> ⚠️ 注意：函数调用与联网搜索（`enable_search`）互斥，同一请求中不可同时启用；且仅部分模型支持该能力（详见各模型文档的能力矩阵表）。

## 关键参数和配置

- `tools`（必需）：JSON 数组，每个元素为标准 OpenAI-style 工具定义，必须包含：
  - `type`: 固定为 `"function"`
  - `function.name`: 字符串，函数唯一标识（建议小写字母+下划线）
  - `function.description`: 简明功能描述（影响模型调用准确性）
  - `function.parameters`: 符合 JSON Schema 的参数定义（支持 `string`/`number`/`boolean`/`array`/`object` 类型，`required` 字段必填）

- `tool_choice`（可选）：控制调用策略：
  - `"auto"`（默认）：模型自主决定是否及调用哪个工具
  - `"none"`：禁用函数调用
  - `{"type": "function", "function": {"name": "xxx"}}`：强制指定调用某函数（适用于确定性流程）

- `response_format`（推荐配合使用）：设为 `{"type": "json_object"}` 可提升工具参数提取的结构化程度与稳定性。

- 实时 API 中额外约束：
  - `tools` 仅在 `session.update` 时生效，不可在单次 `input_text` 或 `input_audio` 事件中动态变更；
  - 工具执行结果需通过 `conversation.item.create` 以 `type="function_call_output"` 形式提交，格式须严格匹配函数定义中的 `parameters` 类型。

## 面向开发者，简洁实用

- ✅ **最佳实践**：为每个工具提供精准、无歧义的 `description` 和最小必要 `parameters` Schema；避免过度泛化的函数名（如 `"do_something"` → `"get_weather_by_city"`）。
- ✅ **调试技巧**：开启 `stream=true` 时，观察流式响应中的 `delta.tool_calls` 字段，可实时验证模型是否正确识别调用意图。
- ❌ **常见陷阱**：  
  - 未在 `tools` 中声明却在 `tool_choice` 中指定函数 → 返回 400 错误；  
  - 函数返回结果格式与 `parameters` 定义不一致 → 模型可能无法解析，导致后续生成中断；  
  - 在不支持函数调用的模型（如 `qwen-omni-turbo-realtime`）上配置 `tools` → 参数被忽略，无报错但无效果。

函数调用是构建可靠 Agent 的基石能力。请始终以「最小可行工具集 + 清晰语义契约」为设计原则，优先选用 Responses API 或支持 `tools` 的 `qwen3.*` 系列模型，并通过真实请求日志持续优化工具描述与参数 Schema。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [more about models](../api/more-about-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


