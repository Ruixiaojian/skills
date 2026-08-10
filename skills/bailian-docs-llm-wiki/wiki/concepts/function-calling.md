# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行的关键能力。它使大模型能突破纯文本生成边界，与数据库、API、插件等真实世界服务安全协同，是构建智能体（Agent）、RAG增强应用和自动化工作流的核心机制。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用文本模型（如 `qwen3.8-max`、`qwen3.7-plus`）**：通过在请求中传入 `tools` 数组定义可用函数，模型自动判断是否需调用、调用哪个函数及填充参数；响应中返回 `tool_calls` 字段（非流式）或 `delta.tool_calls`（流式），供开发者解析并执行。
- **意图理解专用模型（`tongyi-intent-detect-v3`）**：在 `INTENT_MODE` 下，模型直接输出标准化的意图标签 + 函数调用参数（如 `{"intent": "book_flight", "parameters": {"from": "北京", "to": "上海"}}`），无需 `tools` 定义，适用于规则明确的业务路由。
- **[OpenAI 兼容接口](openai-compatible-interface.md)（`/v1/chat/completions` 和 `/v1/responses`）**：支持标准 OpenAI `function` 工具 schema，但 `/responses` 模式下由服务端自动编排调用（不返回 `tool_calls`，而是直接执行并注入结果），适合开箱即用的联网搜索、代码解释等内置能力。
- **GUI 自动化模型（`gui-plus-2026-02-26`）**：将 GUI 操作抽象为函数（如 `left_click(x=120, y=85)`），模型严格按 `<tools>` 声明生成调用，输出必须符合 `<tool_call>` 格式约束，确保动作可被下游执行器精确解析。
- **应用层集成（RAG/智能体）**：作为插件调度协议，连接自定义 API 函数或官方插件（如计算器、二维码生成）。平台不透传自定义 Header，仅允许携带 `Authorization`，调用逻辑需由开发者自行实现。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `tools` | 必填数组，声明可用函数的名称、描述、参数 Schema（JSON Schema 格式） | DashScope 原生接口与 [OpenAI 兼容接口](openai-compatible-interface.md)均支持，但 Anthropic 接口要求 `tool_use` 结构，Qwen 自研 `retrieval` 类型暂不兼容 |
| `tool_choice` | 控制调用策略：<br>• `"auto"`（默认）：模型自主决定<br>• `"none"`：禁止调用<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制指定函数 | DashScope 原生接口支持最全；[OpenAI 兼容接口](openai-compatible-interface.md)仅支持 `"auto"` 或 `"none"` |
| `stream` / `incremental_output` | 启用流式响应时，`tool_calls` 以增量方式分片返回（如 `delta.tool_calls[0].function.arguments` 逐步拼接） | 需客户端按 `index` 和 `id` 正确聚合片段；`incremental_output=True` 可避免重复传输已返回内容 |
| `messages` 中的 `role: "system"` | 系统提示需包含清晰的工具使用指令（如“你是一个天气助手，请调用 `get_weather` 获取实时数据”） | 对于 `gui-plus`、`intent-detect-v3` 等专用模型，系统提示有固定格式要求（如 `Response in INTENT_MODE.` 或 `<tools>...</tools>`） |

## 面向开发者，简洁实用

- ✅ **必做**：始终验证 `tool_calls` 是否存在且 `function.name` 在 `tools` 列表中；参数需 JSON Schema 校验后再执行，防止注入风险。
- ✅ **推荐**：使用 DashScope 原生接口（而非 OpenAI 兼容）以获得完整 `tool_choice` 控制、`response_format` 强约束及[多模态](multi-modal.md)工具支持。
- ⚠️ **避坑**：  
  - `qwen-long` 不支持函数调用；`qwen3-vl-plus` 等旧版视觉模型已弃用内置工具能力；  
  - Anthropic 兼容接口不支持 Qwen 自研工具类型（如 `retrieval`）；  
  - 自定义函数调用时，`Authorization` 是唯一允许透传的 Header，其他字段需封装进请求体。
- 🚀 **提效**：结合 `previous_response_id`（`responses` 接口）或会话管理 API，复用历史工具执行上下文，减少冗余推理。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [more models](../api/more-models.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application support](../guides/application-support.md)


