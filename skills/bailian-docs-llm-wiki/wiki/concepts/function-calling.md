# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具请求并协同外部能力完成任务的核心机制。它不是简单的 API 封装，而是模型在理解对话上下文后，自主决策是否需要调用工具、选择哪个工具、构造合法参数，并将执行结果无缝融入后续推理链路的端到端能力。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼中并非单一接口功能，而是贯穿多个技术路径的横切能力，具体体现为以下三类实践模式：

- **模型原生函数调用（推荐）**：通过 DashScope 原生接口（如 `/api/v1/services/aigc/text-generation/generation`）传入 `tools` 数组（含 `tool_id`、`description` 和可选 `parameters` schema），由 `qwen-max`、`qwen-plus`、`qwen-turbo` 等支持模型直接输出 `function_call` 结构。模型返回 `output.choices[0].message.tool_calls`，包含 `id`、`tool_name` 和 `tool_input`，开发者需解析后同步/异步调用对应工具，再将结果以 `tool_response` 形式回传继续对话。

- **意图识别辅助调用**：使用专用意图模型（如 `tongyi-intent-detect-v3`）在 `INTENT_MODE` 下对用户输入做轻量级解析，返回标准化意图标签（如 `"search_news"`）和结构化参数（如 `{"keyword": "AI政策", "time_range": "7d"}`）。该方式延迟低、确定性强，适用于路由分发、规则引擎前置等场景，不依赖大模型生成，但需自行绑定工具逻辑。

- **智能体/工作流编排调用**：在可视化应用中，插件（Plugin）作为已注册的工具单元被显式添加至智能体或拖入工作流节点。此时函数调用由平台运行时自动触发——模型输出 `tool_use` 指令后，平台根据 `tool_id` 查找已授权插件，注入参数并执行，结果自动注入上下文。此模式屏蔽底层协议细节，适合非代码型开发者快速集成。

> ⚠️ 注意：[OpenAI 兼容接口](openai-compatible-interface.md)（`/v1/chat/completions`）**不原生支持函数调用**；其 `functions` / `function_call` 参数被忽略。若需兼容 OpenAI 客户端，必须自行封装：将工具描述注入 `system` 提示词，解析模型 `content` 中的 JSON-like 调用指令，再手动调度。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 必填 |
|------|------|------|------|------|
| `tools` | 请求体 `input` 或 `messages` 同级 | array | 工具定义列表，每个元素含 `tool_id`（字符串，如 `"quark_search"`）、`description`（自然语言描述）、`parameters`（JSON Schema，用于约束输入格式） | 是（启用函数调用时） |
| `tool_choice` | 请求体 `parameters` 内 | string 或 object | 控制调用策略：`"auto"`（默认，模型自主决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | 否 |
| `enable_search` / `enable_code_interpreter` | 请求体 `parameters` 内 | boolean | DashScope 原生接口快捷开关（仅限内置工具），等价于预置对应 `tools` | 否（推荐用 `tools` 显式声明） |
| `tool_response` | 后续请求 `messages` 中 | object | 上一轮工具执行结果，格式为 `{"role": "tool", "content": "...", "tool_id": "...", "tool_call_id": "..."}`，必须与前次 `tool_calls[0].id` 匹配 | 是（多轮调用时） |

- **工具 ID 规范**：必须与插件市场注册的 `tool_id` 完全一致（区分大小写），如 `calculator`、`text_to_image`；自定义插件需确保 `tool_id` 在业务空间内唯一且已授权。
- **参数校验**：模型生成的 `tool_input` 会依据 `parameters` schema 进行基础校验（如类型、必填字段），但**不执行业务逻辑验证**（如搜索关键词长度、图片尺寸合法性），需在工具侧二次校验。
- **流式响应注意**：函数调用结果在流式响应中可能分块到达（如 `delta.tool_calls`），需按 `index` 和 `id` 组装完整 `tool_call` 对象，不可仅依赖首块。

## 面向开发者，简洁实用

- ✅ **首选 DashScope 原生接口**：功能最全、错误反馈明确（如 `invalid_tool_id`）、支持长上下文与私有模型。
- ✅ **始终显式声明 `tools`**：避免依赖隐式开关（如 `enable_search`），确保行为可预测、可审计。
- ✅ **验证 `tool_call_id` 回传**：多轮调用中，`tool_response` 的 `tool_call_id` 必须严格匹配模型返回的 `id`，否则平台拒绝处理。
- ❌ **勿在 [OpenAI 兼容接口](openai-compatible-interface.md)中传 `functions`**：该字段被静默忽略，会导致调用逻辑失效。
- ❌ **勿跳过 `tool_response` 格式校验**：`content` 字段必须为字符串（即使返回 JSON），且 `role` 必须为 `"tool"`。
- 🚀 **生产建议**：对高并发场景，使用连接池（Java 设置 `connectionPoolSize`，Python 复用 `requests.Session`）；对耗时工具（如 `quark_search`），结合[异步任务](asynchronous-task.md) + EventBridge 回调，避免阻塞主线程。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [more models](../api/more-models.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)


