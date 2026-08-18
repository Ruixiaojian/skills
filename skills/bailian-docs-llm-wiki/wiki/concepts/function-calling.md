# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、并按需生成结构化工具调用请求的核心能力。它使大模型能够将自然语言请求自动转化为对预定义工具（如搜索、计算、图像生成等）的标准化调用，再由系统执行并返回结果，从而实现“思考—决策—行动”的闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中不是独立服务，而是**模型原生支持的能力**，其使用方式取决于调用路径和模型类型：

- **通过 Assistant API（推荐）**：在 `POST /compatible-mode/v1/chat/completions` 或 `/compatible-mode/v1/responses` 接口请求中，通过 `tools` 字段声明可用工具（含 `function.name`、`description`、`parameters`），模型将根据对话上下文自主判断是否调用、调用哪个工具，并以标准 `tool_calls` 格式返回结构化调用指令（含 `id`、`function.name`、`function.arguments`）。开发者需自行解析 `tool_calls`，执行对应工具逻辑，并将结果通过 `tool_choice="none"` + `messages` 追加工具响应后再次提交给模型完成推理闭环。

- **在智能体（Agent）应用中**：控制台创建智能体时启用「函数调用」开关后，系统自动为绑定的插件（如 `quark_search`、`calculator`）生成工具描述，并交由底层模型（如 `qwen3.7-plus`、`qwen3.8-max`）进行规划与调用。开发者无需手动构造 `tools`，但需确保所选模型明确支持该能力（见下文兼容性列表）。

- **在工作流（Workflow）中**：函数调用不作为自动决策环节；插件节点由人工编排触发，模型不参与调用决策。此时“函数调用”退化为普通 API 调用，不体现模型的自主规划能力。

> ✅ 支持函数调用的主流模型包括：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-omni-plus`、`qwen3-vl-plus`、`deepseek-v4-flash`、`glm-5.2`；  
> ❌ 不支持的模型包括：`qwen-turbo`（旧版）、`qwen-flash`（部分旧版本）、所有 Qwen-Audio 系列、`qwen-coder-turbo` 及非多模态文本模型（如 `qwen-long` 仅支持长上下文，不支持工具调用）。

## 关键参数和配置

- **`tools`（必需）**：数组，每个元素为一个工具定义对象，必须包含：
  - `function.name`：工具唯一标识（如 `"quark_search"`），需与插件市场或自定义插件发布的 ID 完全一致；
  - `function.description`：简洁的功能描述（≤512 字符），模型据此理解用途；
  - `function.parameters`：JSON Schema 格式，声明输入参数名、类型、是否必填、示例等（Object 类型子属性不可为空）。

- **`tool_choice`（可选）**：控制模型调用行为：
  - `"auto"`（默认）：模型自主决定是否及何时调用；
  - `"none"`：禁用函数调用，强制模型仅作文本回复；
  - `{"type": "function", "function": {"name": "xxx"}}`：强制指定调用某工具（调试/确定性流程常用）。

- **`response_format`（可选）**：设为 `{"type": "json_object"}` 可要求模型输出严格 JSON 结构（适用于需要强格式的函数调用结果解析）。

- **`enable_search`（注意区分）**：此参数用于启用模型内置联网搜索增强（非函数调用），返回的是融合搜索结果的自然语言回答，**不产生 `tool_calls`**。它与 `quark_search` 插件等显式函数调用互斥，不可同时启用。

- **鉴权与安全**：若调用自定义插件，其鉴权（如 Bearer Token）需在插件配置中预先设置，**不在主请求中透传**；业务级 Token 应通过 `biz_params` 字段传递（仅限智能体/工作流 API）。

## 面向开发者，简洁实用

- ✅ **最佳实践**：始终使用 `qwen3.7-plus` 或更高版本模型；优先采用 Assistant API（`/compatible-mode/v1/chat/completions`）而非旧版 `/api/v1/services/aigc/text-generation`，以获得完整函数调用支持。
- ✅ 工具参数 Schema 务必精简准确——冗余字段会降低模型理解精度；建议用 `examples` 字段提供 1–2 个典型调用示例。
- ⚠️ 模型返回的 `function.arguments` 是字符串（JSON 文本），**必须 `json.loads()` 解析后再传入工具**；未校验直接执行可能导致注入风险。
- ⚠️ 异步工具（如图像生成）需自行处理任务轮询或回调，函数调用本身只负责生成 `tool_calls`，不管理执行生命周期。
- 📌 所有函数调用均计入模型 token 消耗（含 `tools` 定义、`tool_calls` 输出及后续工具响应），请在配额评估中纳入计算。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [model experience](../guides/model-experience.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


