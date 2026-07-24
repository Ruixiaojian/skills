# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具协同能力，允许大模型在推理过程中主动识别用户意图、生成符合 JSON Schema 的工具调用请求，并将结果交由外部系统执行，从而实现联网搜索、代码执行、数据库查询、第三方服务集成等扩展能力。该能力不依赖硬编码指令，而是由模型基于对话上下文自主决策是否调用、调用哪个工具及传入何种参数。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中不是独立服务，而是嵌入于多种模型与协议中的核心交互机制，主要应用于以下三类场景：

- **文本生成模型增强推理**：`qwen3.7-plus`、`qwen3.7-max`、`qwen3.5-omni-plus` 等旗舰文本/多模态模型原生支持函数调用。开发者通过声明 `tools` 列表（JSON Schema 描述），模型可在响应中输出 `tool_calls` 字段，包含工具名与参数；后续需由业务逻辑解析并执行对应函数，再将结果以 `tool_result` 形式回传给模型完成多轮协同。
  
- **多协议接口兼容性适配**：
  - **DashScope 原生接口**：直接支持 `tools` + `tool_choice` 参数，返回标准 `output.tool_calls` 结构；
  - **Anthropic 兼容 Messages 接口**：使用 `tool_use` 类型的 `content` block，支持显式思维链控制；
  - **OpenAI 兼容 Chat Completions 接口**：虽非原生标准字段，但百炼在 `response.choices[0].message.tool_calls` 中提供兼容格式（非旧式 `function_call`），需 SDK v2.0+ 或手动解析。

- **多模态协同工作流**：视觉模型（如 `qwen3.6-flash`）、全模态模型（如 `qwen3.5-omni-plus`）可在理解图像/音视频内容后触发函数调用，例如：识别发票后调用财务系统 API 校验金额，或分析监控视频后触发告警服务。此时输入 `messages` 可含多模态 content（如 base64 图片 + 文本指令），模型自动融合信息并决策调用。

> ⚠️ 注意：并非所有模型均支持函数调用。仅明确标注支持 Function Calling 的模型（见 [model experience](../../raw/model-user-guide/model-experience.md)）才具备该能力；OCR、ASR、Embedding 等纯感知类模型不支持。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 示例 |
|------|------|------|----------|------|
| `tools` | array | 工具定义列表，每个元素为符合 OpenAPI 3.0 规范的 JSON Schema 对象 | 否（无工具则不触发调用） | `[{"type": "function", "function": {"name": "get_weather", "description": "获取指定城市天气", "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}}}]` |
| `tool_choice` | string / object | 控制调用策略：<br>`"auto"`（默认，模型自主决定）<br>`"none"`（禁用调用）<br>`{"type": "function", "name": "xxx"}`（强制调用指定工具） | 否 | `"auto"` 或 `{"type": "function", "name": "search_web"}` |
| `enable_search` | boolean | （仅 DashScope 原生接口）快捷启用内置联网搜索工具（等价于预置 `tools` 中的 search 工具） | 否 | `true` |
| `enable_code_interpreter` | boolean | （仅 DashScope 原生接口）快捷启用内置代码解释器工具 | 否 | `true` |

- **工具 Schema 要求**：必须包含 `name`、`description` 和 `parameters`（类型为 `object`），且 `parameters` 中每个字段需明确定义 `type`（如 `"string"`、`"number"`、`"boolean"`），不支持 `anyOf`/`oneOf` 等复杂联合类型。
- **调用结果回传**：当模型返回 `tool_calls` 后，需构造新请求，将 `messages` 追加一条 `role: "tool"` 的消息，`content` 为 JSON 字符串格式的执行结果（非原始对象），并保持 `tool_call_id` 一致。

## 面向开发者，简洁实用

- ✅ **快速起步**：优先使用 DashScope 原生接口 + `tools` 参数，配合 Python SDK 的 `Generation.call()`，最简示例见 [qwen api reference](../../raw/model-api-reference/qwen-api-reference.md)；
- ✅ **调试技巧**：设置 `tool_choice="none"` 可强制模型不调用工具，用于验证 [prompt](../guides/prompt.md) 设计；设为 `{"type": "function", "name": "xxx"}` 可固定测试单个工具路径；
- ✅ **生产建议**：避免在 `tools` 中暴露敏感操作（如数据库写入），应在业务层做权限校验与参数白名单过滤；工具执行超时建议设为 5–10 秒，失败后返回结构化错误供模型重试；
- ❌ **常见陷阱**：  
  - [OpenAI 兼容接口](openai-compatible-api.md)中误读 `function_call` 字段（百炼实际返回 `tool_calls`）；  
  - `tool_call_id` 在回传时未严格匹配，导致模型无法关联结果；  
  - `tools` 中 `parameters` 缺少 `required` 字段声明，导致模型可能传入空值。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)


