# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、自主触发外部工具并结构化传递参数的核心能力。它使模型不仅能生成文本，还能在推理过程中决策是否需要调用特定工具（如计算器、搜索、代码执行、图像生成等），并将结果无缝整合进最终响应。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口能力，而是贯穿多个技术路径的横切机制，具体体现为：

- **Omni Realtime API（实时语音交互场景）**：  
  在 `qwen3.5-omni-realtime` 等实时多模态模型中，函数调用通过 `tools` 字段声明支持的工具列表（`type: "function"`），模型在流式推理过程中可自主触发工具调用，并返回标准化的 `tool_calls` 事件；客户端需执行对应逻辑后，将结果通过 `response.create` 回传，继续后续对话流。该模式严格依赖 WebSocket 事件驱动，适用于低延迟语音助手、智能客服等场景。

- **[插件](plugin.md)（Plug-in）体系（智能体/工作流场景）**：  
  [插件](plugin.md)本质即函数调用的工程化封装。开发者定义工具（Tool）后，模型（如 `qwen-plus`、`qwen-max`）根据用户输入自动规划调用序列；在智能体（Agent）中由模型自主决策，在工作流（Workflow）中可显式编排节点顺序。所有[插件](plugin.md)均需配置 `tool_id`、输入/输出 Schema 和鉴权方式，调用过程对上层应用透明。

- **[OpenAI 兼容接口](openai-compatible-interface.md)（Chat Completions / Responses API）**：  
  通过标准 `tools` + `tool_choice` 字段声明函数集合与调用策略（如 `"auto"`、`"required"` 或指定 `{"type": "function", "function": {"name": "xxx"}}`），模型返回 `tool_calls` 数组（含 `id`、`function.name`、`function.arguments`）；开发者解析后同步执行并构造 `tool_message` 回传。此方式兼容主流 SDK，适合快速迁移或通用对话应用。

- **自定义模型集成（DashScope 原生调用）**：  
  对支持函数调用的模型（如 `qwen3.7-plus`），可通过 DashScope 原生 `/api/v1/services/aigc/text-generation/generation` 接口，以 `tools` 参数注入工具定义，配合 `enable_search=false` 等约束使用。该路径更灵活，但需自行处理协议细节与错误重试。

> ⚠️ 注意：函数调用能力**不跨模型通用**——必须选用明确支持该能力的模型（如 Omni Realtime 系列、qwen-plus/max、qwen3.7-plus 等），旧版模型（如 `qwen-turbo` 部分版本）或专用模型（如 `qwen-coder-turbo`）可能不支持。

## 关键参数和配置

| 参数 | 类型 | 说明 | 必填 | 示例 |
|------|------|------|------|------|
| `tools` | `array` | 工具定义列表，每个元素为 `{ "type": "function", "function": { "name", "description", "parameters" } }` | 是 | `[{ "type": "function", "function": { "name": "calculator", "description": "计算数学表达式", "parameters": { "type": "object", "properties": { "expression": { "type": "string" } }, "required": ["expression"] } } }]` |
| `tool_choice` | `string` 或 `object` | 控制调用策略：<br>• `"auto"`（默认，模型自主决定）<br>• `"none"`（禁用）<br>• `{"type": "function", "function": {"name": "xxx"}}`（强制调用指定函数） | 否（默认 `auto`） | `"auto"` 或 `{"type":"function","function":{"name":"quark_search"}}` |
| `tool_id`（插件专用） | `string` | 插件市场中工具的唯一标识符，用于控制台绑定或 API 引用 | 是（插件场景） | `"quark_search"`、`"code_interpreter"` |
| `input parameters` | `object` | 实际传入工具的参数对象，字段名与 `tools[].function.parameters.properties` 严格一致；Object 类型子属性**不可为空** | 是（调用时） | `{"expression": "sqrt(144) + 2 * 3"}` |
| `biz_params`（插件专用） | `object` | 业务系统透传参数（非 LLM 识别），需在插件配置中设为“业务透传”模式 | 否 | `{"user_id": "u123", "session_id": "s456"}` |

- **Schema 规范**：`parameters` 必须符合 OpenAPI 3.0 的 JSON Schema 子集（支持 `string`/`number`/`boolean`/`object`/`array` 及 `required` 字段），嵌套 `object` 中所有属性均为必填。
- **安全要求**：自定义工具 URL 必须为 HTTPS，响应头需含 `Access-Control-Allow-Origin: *` 或明确允许百炼域名；鉴权参数（如 `api_key`）应置于 Header（`Authorization: Bearer xxx`）或 Query（需在插件配置中声明参数名）。
- **调用限制**：单次对话最多触发 10 次工具调用（含重复调用同一工具），总次数受应用配额约束。

## 面向开发者，简洁实用

- ✅ **快速验证**：优先选用 `qwen-plus` 或 `qwen3.7-plus` 模型 + [OpenAI 兼容接口](openai-compatible-interface.md)，用 `tools` + `tool_choice="auto"` 启动最小可行测试。
- ✅ **调试技巧**：开启 `stream=false` 获取完整响应，检查 `choices[0].message.tool_calls` 是否存在；若无调用，检查 `tools` Schema 是否匹配用户 query 语义，或尝试 `tool_choice="required"` 强制触发。
- ✅ **错误定位**：常见失败原因包括——`tools` 中 `name` 与实际工具 ID 不一致、`parameters` 字段缺失或类型错误、自定义工具返回非 JSON 或 HTTP 状态码非 200。
- ✅ **生产建议**：工具执行超时应设为 ≤10s；回传结果需精简（避免大文本），关键字段用 `output parameters` 显式声明，便于模型提取摘要。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)


