# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、结构化提取参数，并按预定义规范调用外部工具或内部能力的核心机制。它不是简单的 API 请求封装，而是模型在推理过程中自主决策“何时调用、调用哪个、传什么参数”的闭环能力，支撑智能体、工作流及高级文本生成等场景的自动化执行。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼中并非独立接口，而是深度集成于多个能力层，其触发方式与执行上下文因场景而异：

- **文本生成模型（如 `qwen3.7-plus`、`qwen3.8-max`）**：通过 `tools` 字段声明可用函数（含 `name`、`description`、`parameters` JSON Schema），并在请求中设置 `enable_thinking: true`（默认开启）。模型自动判断是否需调用、选择工具、生成符合 Schema 的 `tool_calls`，返回结构化 `function_call` 或 `tool_calls` 数组。适用于联网搜索、代码解释、计算器等内置工具，也支持自定义[插件](plugin.md)接入。

- **[插件](plugin.md)（Plug-in）场景**：函数调用是[插件](plugin.md)调度的底层协议。当智能体或工作流配置了 `quark_search`、`code_interpreter` 等插件后，模型输出即为标准 `tool_calls` 格式；平台自动解析并路由至对应插件服务，执行结果再注入下一轮推理。注意：`quark_search` 是显式工具调用，与模型内部 `enable_search` 机制互斥，不可共存。

- **Managed Agents API**：函数调用由 Agent 运行时统一托管。开发者在创建 Agent 时通过 `skills` 字段挂载 Skill（即函数包），Session 执行中模型生成 `tool_calls` 后，平台沙箱自动调用对应 Skill 并回填 `tool_result`，全程事件驱动、无需手动轮询。

- **Application Call（应用调用）**：新版智能体应用默认启用函数调用能力。调用时只需在 `input` 中提供自然语言指令（如“查杭州今天天气”），无需显式传 `tools` —— 因为函数集合已在应用发布时固化。平台自动注入工具定义，模型完成规划与调用，最终返回整合结果。

- **[OpenAI 兼容接口](openai-compatible-api.md)（Responses API）**：完全兼容 OpenAI 的 `functions` / `function_call` 参数语法，可复用现有 SDK 代码。但需注意：`qwen-coder-turbo` 等部分模型**不支持**该协议，仅限 `completions` 接口，调用前务必核对模型文档支持列表。

> ⚠️ 关键约束：所有函数调用均要求模型具备明确的 `tools` 定义（或应用已预置），且 `parameters` 必须为严格 JSON Schema（Object 类型子属性不能为空）；未匹配到有效工具或参数校验失败时，模型将拒绝调用并返回普通文本响应。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 必填 |
|------|------|------|------|------|
| `tools` | 请求体顶层 | array | 工具定义列表，每个元素含 `type: "function"`、`function.name`、`function.description`、`function.parameters`（JSON Schema） | 同步调用需显式声明；应用调用中由平台隐式注入 |
| `tool_choice` | 请求体顶层 | string \| object | 控制调用策略：<br>`"auto"`（默认，模型自主决策）<br>`"none"`（禁用调用）<br>`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | 否 |
| `enable_thinking` | `parameters` 内 | boolean | 是否启用模型推理链（含函数调用规划）。`qwen3.5+` 系列默认 `true`；设为 `false` 可跳过 planning 阶段，节省 token | 否（但影响调用行为） |
| `response_format` | 请求体顶层 | object | 强制结构化输出，如 `{"type": "json_object"}`。与函数调用协同时，确保 `parameters` Schema 与期望 JSON 结构一致 | 否（推荐配合使用） |

- **Schema 注意事项**：`parameters` 必须是合法 JSON Schema，`required` 字段需显式列出；`string` 类型建议加 `description` 辅助模型理解；避免嵌套过深或使用 `anyOf`/`oneOf` 等复杂关键字（兼容性风险高）。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `qwen3.7-plus` + 最简 `tools`（如单个 `calculator`）发起一次请求，观察响应中是否出现 `tool_calls` 字段及 `name`/`arguments`。
- ✅ **调试技巧**：开启 `debug: { "return_prompt": true }`（Application Call）或 `enable_debug: true`（Managed Agents），查看模型思考过程中的原始 [prompt](../guides/prompt.md) 和 tool call 指令。
- ✅ **错误排查**：
  - `invalid_tool_call`：检查 `tools` 中 `name` 是否与模型实际调用名完全一致（大小写敏感）；
  - `parameter_validation_failed`：用 [JSON Schema Validator](https://jsonschemalint.com/) 校验 `parameters`；
  - 无 `tool_calls` 返回：确认模型支持函数调用（查[模型体验文档](guides/model-experience.md)）、`enable_thinking` 未被关闭、输入指令足够明确。
- ✅ **生产建议**：高频调用场景下，优先使用 Managed Agents API 或 Application Call（v1），避免手动解析 `tool_calls` 并二次请求；自定义插件务必通过“测试工具”验证后再发布。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model experience](../guides/model-experience.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)
- [application call](../api/application-call.md)


