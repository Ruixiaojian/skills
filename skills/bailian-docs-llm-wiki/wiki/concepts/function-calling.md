# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具协同机制，允许大模型在推理过程中主动识别用户意图、生成标准化的工具调用请求（而非自由文本），并由平台或开发者后端执行对应函数后将结果注入上下文，从而实现联网搜索、代码执行、数据库查询、外部 API 调用等确定性操作。该能力是构建可靠智能体（Agent）的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体编排（Responses 接口）**：在 `qwen3.7-plus`、`qwen3.5-omni-plus` 等支持模型上，通过 `tools` 参数声明可用工具，启用 `enable_search=true` 或 `enable_code_interpreter=true` 后，模型可自动触发内置工具（如联网搜索、Python 代码解释器），无需开发者手动解析 `tool_calls` —— 平台完成调用、结果注入与最终响应合成，返回的是“已执行完毕”的自然语言答案。

- **可控工具链集成（DashScope 原生 / Anthropic 兼容接口）**：在 DashScope 原生接口或 Anthropic 兼容 `messages` 接口中，模型会以标准 JSON 格式输出 `tool_calls`（含 `function.name` 和 `function.arguments`），开发者需自行解析、调用对应函数，并将结果以 `tool_message` 形式重新提交给模型进行下一步推理。适用于需要自定义工具逻辑、审计调用过程或集成私有服务的场景。

- **多模态任务协同**：`qwen3.5-omni-plus` 等全模态模型支持在图文/音视频理解过程中触发工具，例如对截图中的表格调用 OCR 工具提取结构化数据，或对语音转写结果调用知识库检索工具补充背景信息。

- **异步工作流衔接**：函数调用可作为异步任务（如文生图、TTS 合成）的触发入口。模型返回 `tool_call` 后，开发者调用异步创建接口获取 `task_id`，再通过轮询或 EventBridge 事件通知等待结果，最终将生成内容作为 `tool_message` 回传继续对话。

> ⚠️ 注意：OpenAI 兼容的 `chat/completions` 接口**不支持函数调用**；仅 `responses`（自动模式）和 `messages`（Anthropic 兼容，显式模式）两类接口提供完整支持。

## 关键参数和配置

- `tools`: 必填数组，定义可用工具的 OpenAI 风格 Schema（`type="function"`），包含 `name`、`description`、`parameters`（JSON Schema）。百炼兼容 OpenAI v1 规范，但要求 `parameters` 必须为合法 JSON Schema 对象（不可为 `null` 或省略）。

- `tool_choice`: 可选，控制调用策略：
  - `"auto"`（默认）：模型自主决定是否及调用哪个工具；
  - `"none"`：禁止调用任何工具；
  - `{"type": "function", "function": {"name": "xxx"}}`：强制指定调用某工具（适用于确定性流程）。

- `enable_search` / `enable_code_interpreter`: DashScope 原生接口专用布尔开关，用于快速启用内置工具（等价于在 `tools` 中预注册对应函数）。开启后，模型无需显式声明 `tool_calls` 即可触发，结果自动注入。

- `response_format`: 当需确保模型输出严格符合结构时，可配合 `tools` 使用 `{"type": "json_object"}`，强制模型以 JSON 格式返回（包括 `tool_calls` 字段），便于程序化解析。

- 请求头 `X-DashScope-OssResourceResolve: enable`: 若工具参数中包含 `oss://` 临时 URL（如上传的图片、PDF），必须携带此 Header，否则工具执行时无法解析资源。

## 面向开发者，简洁实用

- ✅ **首选 `responses` 接口**：快速验证工具链效果，免去手动解析与重提交逻辑；适合原型开发与轻量智能体。
- ✅ **生产环境用 `messages` + 自研工具网关**：完全掌控工具调用权限、超时、重试与错误处理；推荐封装统一 `tool_executor` 模块。
- ✅ **工具 Schema 要精简**：`parameters` 中只保留必要字段，避免过度嵌套；复杂参数建议用 `string` 类型 + 自然语言描述，由后端解析。
- ❌ 避免在 `chat/completions` 中传 `tools`：该接口忽略该字段，且不会返回 `tool_calls`。
- ❌ 不要硬编码 API Key 调用工具服务：工具后端应使用临时凭证或服务间鉴权（如 RAM Role），尤其当工具涉及敏感操作时。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


