# 函数调用

函数调用（Function Calling）是百炼平台支持的一种关键能力，允许大模型在推理过程中动态识别用户意图，并按预定义 Schema 生成结构化工具调用请求（而非直接生成自然语言回复），从而实现与外部系统（如数据库、API、计算器、搜索服务等）的安全、可控交互。该能力是构建智能体（Agent）、自动化工作流和多步骤任务系统的基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非独立服务，而是**内嵌于特定模型的推理能力中**，需配合支持该能力的模型及正确配置方可启用：

- **意图理解与工具调度**：`tongyi-intent-detect-v3` 是专为函数调用设计的轻量级模型，适用于快速识别用户指令中的工具调用意图（如“查北京天气”“订明天会议室”），并直接输出符合 OpenAI 工具 Schema 的 `tool_calls` 数组，常用于前端意图解析或 Agent 的第一层路由。
  
- **通用大模型增强交互**：`qwen3.7-plus`、`qwen3.7-max-2026-06-08`、`qwen3.5-omni-plus` 等主力文本/全模态模型原生支持函数调用。开发者通过 `tools` 参数传入工具定义后，模型可在单次响应中返回 `tool_calls`（含 `function.name` 和 `function.arguments`），后续由业务逻辑解析并执行真实调用，再将结果以 `tool_message` 形式回填继续对话。

- **端到端语音智能体**：`qwen-audio-3.0-realtime-plus`（S2S 模型）在语音对话流中支持 `enable_function_calling: true`，可实时触发工具调用（如查询日程、控制IoT设备），实现“听—思—调—说”闭环。

> ⚠️ 注意：函数调用能力**不依赖异步任务机制**，所有支持模型均通过同步接口（如 `/api/v1/services/aigc/text-generation/generation` 或 OpenAI 兼容 `/v1/chat/completions`）完成；但若工具执行本身耗时较长（如视频生成），建议由上层业务自行封装为异步流程。

## 关键参数和配置

- **`tools`（必需）**：OpenAI 兼容格式的工具列表，每个工具需包含 `type: "function"`、`function.name`、`function.description` 及 `function.parameters`（JSON Schema）。百炼严格校验 Schema 合法性，非法定义将导致 400 错误。

- **`tool_choice`（可选）**：控制调用策略：
  - `"auto"`（默认）：模型自主决定是否调用及调用哪个工具；
  - `"none"`：禁用函数调用，强制返回自然语言；
  - `{"type": "function", "function": {"name": "xxx"}}`：强制指定调用某工具（适用于确定性流程）。

- **`enable_function_calling`（部分模型专用）**：`qwen-audio-3.0-realtime-plus` 等 S2S 模型需显式设置此布尔参数为 `true` 才启用函数调用能力（`tools` 仍需同时提供）。

- **`response_format`（推荐）**：当需确保模型优先返回工具调用而非自由回答时，可配合设置 `{"type": "json_object"}`，提升结构化输出稳定性。

- **输入消息约束**：`system` message 中避免模糊指令（如“你是一个助手”），建议明确提示：“你必须严格按工具定义执行操作，仅在无法满足用户需求时才返回自然语言解释。”

## 面向开发者，简洁实用

- ✅ **立即验证**：使用 `qwen3.7-plus` + 最小工具集（如一个 `get_weather` 函数），通过 DashScope Python SDK 或 OpenAI SDK 发起一次调用，观察响应中是否含 `choices[0].message.tool_calls` 字段。
- ✅ **错误排查重点**：若未触发调用，检查——工具 `parameters` 是否为合法 JSON Schema（非 Python dict）、`tools` 是否传入顶层 `messages` 外的参数位置、模型是否确属支持列表（见文档 2 表格，注意快照版本后缀）。
- ✅ **生产建议**：对 `tool_arguments` 做 JSON 解析容错（模型可能输出语法错误的 JSON），并在工具执行失败后构造 `tool_message` 返回错误信息，交由模型重试或降级处理。
- ❌ **不支持场景**：函数调用不可跨模型链式触发（如 A 模型调用工具后，结果不能自动喂给 B 模型继续调用）；也不支持在异步任务（如图像生成）的创建请求中启用。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [more models](../api/more-models.md)
- [model experience](../guides/model-experience.md)


