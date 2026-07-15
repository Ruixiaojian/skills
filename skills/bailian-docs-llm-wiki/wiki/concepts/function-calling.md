# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行的能力。它使大模型能突破自身知识与能力边界，安全、可控地接入实时搜索、代码执行、图像生成、OCR解析、GUI操作等外部服务，实现“思考→规划→调用→整合”的闭环推理。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用并非单一接口，而是贯穿多类模型与交互范式的统一能力机制，具体体现为以下三种典型模式：

- **通用模型的自主工具调用**：`qwen3.7-plus`、`qwen3.6-flash`、`qwen3.5-omni-plus-realtime` 等主流模型在启用 `tools` 参数后，可基于用户输入自动决策是否调用、调用哪个工具、传入哪些参数，并返回标准化的 `tool_calls` 响应（含 `tool_id` 和 `arguments`）。该过程完全由模型内部推理完成，开发者只需提供工具定义（名称、描述、参数 schema），无需编写调度逻辑。

- **专用意图模型的显式决策**：`tongyi-intent-detect-v3` 是专为函数调用设计的轻量级模型，不生成自然语言回复，而是直接输出结构化意图标签（如 `"search"`、`"calculate"`）或完整工具调用指令（`INTENT_MODE` 模式）。适用于需强确定性、低延迟的路由/分发场景，常作为智能体前置网关。

- **垂直领域模型的内嵌工具链**：`gui-plus-2026-02-26` 通过 `computer_use` 工具实现 GUI 自动化；`qwen3.5-ocr` 在图文混合输入下自动触发结构化解析；`qwen-deep-research` 在研究流程中隐式调用检索与报告生成子模块。这些模型将函数调用深度集成至业务逻辑，对外表现为端到端能力，而非显式 `tool_calls` 字段。

> ⚠️ 注意：并非所有模型均支持函数调用。例如 `qwen-long`（10M上下文）明确不支持；`qwen3.7-max` 不支持结构化输出，因而无法返回合规的 `tool_calls`；`qwen-omni-turbo-realtime` 系列虽支持 `tools` 参数，但文档未确认其完整调用流程，建议优先选用 `qwen3.5-omni-realtime` 系列。

## 关键参数和配置

| 参数 | 类型 | 说明 | 必填 | 示例 |
|------|------|------|------|------|
| `tools` | `array` | 工具定义列表，每个元素包含 `tool_id`（字符串）、`description`（功能描述）、`parameters`（JSON Schema，定义必选/可选字段及类型） | 是（启用函数调用时） | `[{"tool_id": "calculator", "description": "执行数学计算", "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}]` |
| `tool_choice` | `string` 或 `object` | 控制调用策略：<br>`"auto"`（默认，模型自主决定）<br>`"none"`（禁用调用）<br>`{"type": "function", "function": {"name": "xxx"}}`（强制指定工具） | 否 | `"auto"` |
| `enable_search` | `boolean` | **仅 `qwen3.5-omni-realtime` 系列支持**，启用内置联网搜索（与 `tools` 互斥） | 否 | `true` |
| `result_format` | `string` | 必须设为 `"message"`（推荐），确保响应中包含 `tool_calls` 字段；设为 `"text"` 将丢失结构化调用信息 | 是（推荐） | `"message"` |

- **工具 ID 命名规范**：必须全局唯一、语义清晰（如 `quark_search`, `code_interpreter`），避免空格/特殊字符；官方插件 ID 可在控制台插件详情页复制。
- **参数 Schema 要求**：`parameters` 必须为合法 JSON Schema，`required` 数组需准确声明必填字段；`Object` 类型参数仅支持 `POST` 请求，`GET` 请求中禁止使用。
- **响应解析要点**：成功调用后，模型响应 `message` 中 `role` 为 `"assistant"`，`content` 为空或为中间思考，`tool_calls` 数组包含调用详情；后续需开发者自行执行工具并以 `tool_result` 角色提交结果，继续对话。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `qwen3.7-plus` + `calculator` 工具，发送 `"123 * 456 = ?"`，观察是否返回 `tool_calls`。
- ✅ **调试技巧**：若模型未触发调用，检查 `description` 是否足够清晰、`parameters.required` 是否遗漏关键字段、`messages` 中是否提供足够上下文。
- ✅ **生产建议**：  
  - 对高可靠性场景（如金融计算），优先使用 `tongyi-intent-detect-v3` 做意图路由，再交由专用工具执行；  
  - 实时语音对话中，`qwen3.5-omni-plus-realtime` 支持流式 `tool_calls` 事件，可边听边规划；  
  - 自定义插件务必完成在线调试并发布为“已发布”状态，否则调用失败且错误码不直观（常见 `130040`）。  
- ❌ **避坑提醒**：`tools` 与 `enable_search` 不能同时启用；`qwen-long` 等超长上下文模型不支持该能力；流式响应（`stream=true`）中 `tool_calls` 仅在最终 chunk 返回，勿在中间 chunk 解析。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [plug in](../guides/plug-in.md)
- [more models](../api/more-models.md)


