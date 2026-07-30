# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具协同能力，指大语言模型在生成响应过程中，主动识别用户意图并按预定义 Schema 生成结构化工具调用请求（而非自由文本），交由外部系统执行后，再将结果注入后续推理。该机制实现了“思考→规划→执行→整合”的闭环，是构建可靠智能体（Agent）的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用能力在百炼平台中并非全局统一启用，其支持范围、行为细节和配置方式因接入协议与模型而异：

- **DashScope 原生接口**：完全支持自定义函数调用。开发者通过 `tools` 参数传入 OpenAI 风格的工具定义（含 `name`、`description`、`parameters` JSON Schema），模型返回 `output.choices[0].message.tool_calls` 数组，包含 `function.name` 和 `function.arguments` 字符串（需 `json.loads` 解析）。支持多工具并行调用、嵌套调用及调用后自动追加执行结果继续推理（需设置 `enable_tool_choice: "auto"` 或指定 `tool_choice`）。

- **Anthropic 兼容 Messages 接口**：支持 `tool_use` 块输出，使用 Anthropic 原生 `tools` 定义语法（`input_schema` 替代 `parameters`），响应中以 `content` 数组中的 `tool_use` 类型块返回调用请求。注意：`system` 提示词长度受限于 4096 token，可能影响复杂工具描述的完整性。

- **OpenAI 兼容 Chat Completions 接口**：**不支持流式工具调用响应解析**——虽然请求可携带 `tools`，但流式响应（`stream: true`）的 `delta.tool_calls` 可能缺失参数或顺序错乱；建议在非流式模式下使用，并严格校验 `finish_reason == "tool_calls"` 后再解析 `message.tool_calls`。

- **OpenAI 兼容-Responses 模式**：仅支持平台预置的三类内置工具（联网搜索、代码解释器、网页内容提取），**不可自定义 `tools`**。调用逻辑由平台自动触发与编排，开发者只需在 `messages` 中提供自然语言请求，无需声明工具定义。

> ⚠️ 注意：`qwen3.7-max` 等强推理模型默认禁用结构化输出（含函数调用），如需启用，请优先选用 `qwen3.7-plus` 或 `qwen3.7-flash`；同时，联网搜索与函数调用互斥，二者不可同时开启。

## 关键参数和配置

| 参数 | 所属接口 | 说明 | 示例值 |
|------|----------|------|--------|
| `tools` | DashScope、Anthropic 兼容 | 工具定义列表，格式为 OpenAI 或 Anthropic 规范 | `[{"type": "function", "function": {"name": "get_weather", "description": "...", "parameters": {...}}}]` |
| `tool_choice` | DashScope | 控制模型是否调用工具及调用策略 | `"auto"`（默认）、`"none"`、`{"type": "function", "function": {"name": "get_weather"}}` |
| `enable_tool_choice` | DashScope（旧版别名） | 同 `tool_choice`，已逐步被后者替代 | `"auto"` |
| `response_format` | DashScope | 强制结构化输出格式，与函数调用协同使用 | `{"type": "json_object"}`（需配合 `tools` 使用） |
| `enable_search` | DashScope | 启用内置联网搜索（与自定义 `tools` 互斥） | `true` |
| `tools`（OpenAI 兼容） | [OpenAI 兼容接口](openai-compatible-interface.md) | 仅用于非流式请求；流式响应中 `delta.tool_calls` 不可靠 | 同上 |

- **认证与路由**：所有函数调用均需标准鉴权（`Authorization: Bearer <API_KEY>`），且必须使用对应协议的 Endpoint（如 DashScope 原生接口使用 `/api/v1/services/aigc/text-generation/generation`）。
- **输入构造**：工具调用依赖 `messages` 中清晰的用户指令（如“查上海今天天气”），模型据此生成符合 `tools` Schema 的调用请求；避免在 `system` 提示中重复定义工具，应集中于 `tools` 参数。
- **错误处理**：若 `arguments` 解析失败（JSON 格式错误）、工具执行超时或返回异常，需由业务层捕获并构造 error message 追加至 `messages` 后重试。

## 面向开发者，简洁实用

- ✅ **推荐路径**：生产环境首选 **DashScope 原生接口** + `qwen3.7-plus`，它提供最完整的工具定义、调用控制与错误反馈能力。
- ✅ **快速验证**：开发调试阶段可用 **OpenAI 兼容-Responses** 模式，零配置体验内置工具链（搜索/代码执行），但无法扩展自定义能力。
- ❌ **规避陷阱**：勿在 [OpenAI 兼容接口](openai-compatible-interface.md)中依赖流式 `tool_calls`；勿在 `qwen3.7-max` 上启用 `tools`；勿同时设置 `enable_search: true` 和自定义 `tools`。
- 🛠️ **调试技巧**：开启 `stream: false` + `debug: true`（DashScope）可获取完整推理 trace，观察模型何时、为何选择调用某工具；使用 `seed` 固定随机性便于复现问题。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


