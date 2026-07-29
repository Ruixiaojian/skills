# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化模型交互能力，允许开发者在请求中声明可被模型识别并调用的工具函数（如搜索、计算、数据库查询等），由模型自主决定是否调用、调用哪个函数及传入何种参数，最终返回标准 JSON 格式的函数调用请求（而非自由文本）。该机制是构建可靠 AI Agent 的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用能力已在多个模型和业务场景中深度集成，使用方式因模型类型与接口协议略有差异，但逻辑一致：

- **通用大模型（如 `qwen3.7-plus`、`qwen3.5-omni-plus`）**：原生支持 OpenAI 兼容的 `functions` / `tools` 参数。开发者通过 `tools` 字段传入函数定义（含 `name`、`description`、`parameters`），模型在响应中返回 `tool_calls` 数组；平台自动解析并返回结构化结果，无需额外后处理。
  
- **意图理解专用模型（`tongyi-intent-detect-v3`）**：专为函数调用优化，毫秒级响应，支持高并发意图识别与函数名/参数生成。需在 `system` 消息中明确声明 `Response in INTENT_MODE.`，并可选提供预定义意图字典（即函数列表），模型将严格按字典输出标准化意图标识与参数。

- **全模态与实时语音模型（如 `qwen-audio-3.0-realtime-plus`、`qwen3.5-omni-plus-realtime`）**：在流式语音对话中支持低延迟函数调用触发，适用于智能助手、语音控制等场景。需启用 `enable_function_calling=true`（部分模型为默认开启），函数调用事件将作为独立消息帧（`tool_call` 类型）实时推送。

- **不支持函数调用的模型**：如 `qwen-long`、`qwen3-rerank`、`text-embedding-v4` 等向量/重排序/超长文本模型，明确不支持该能力，请求中若携带 `tools` 将被忽略或报错。

> ✅ 提示：函数调用是**模型能力属性**，非接口层功能。即使使用 OpenAI 兼容路径（`/v1/chat/completions`），也必须选用明确标注支持 Function Calling 的模型（见 [model experience](guides/model-experience.md) 中各模型的能力矩阵），否则 `tools` 字段无效。

## 关键参数和配置

| 参数 | 说明 | 示例/要求 | 注意事项 |
|------|------|-----------|----------|
| `tools` | 必选（启用函数调用时）。数组，每个元素为一个工具定义对象，含 `type="function"`、`function.name`、`function.description`、`function.parameters`（JSON Schema） | `[{ "type": "function", "function": { "name": "search_web", "description": "Search the web for up-to-date information", "parameters": { "type": "object", "properties": { "query": { "type": "string" } } } } }]` | `parameters` 必须为合法 JSON Schema，不支持 `anyOf`/`oneOf`；建议字段数 ≤ 8，避免模型解析失败 |
| `tool_choice` | 可选。控制模型调用行为：`"auto"`（默认，由模型决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | `"auto"` 或 `{ "type": "function", "function": { "name": "get_weather" } }` | 强制指定时，若模型无法生成有效参数，可能返回空 `arguments` 或报错 |
| `response_format: { "type": "json_object" }` | 推荐搭配使用。确保模型以 JSON 格式输出（包括 `tool_calls` 字段），提升解析稳定性 | `{ "type": "json_object" }` | 部分模型（如 `qwen3.7-flash`）对 JSON 输出支持更鲁棒，推荐优先选用 |
| `enable_function_calling`（部分模型） | 部分实时/语音模型需显式启用（如 `qwen-audio-3.0-realtime-plus`） | `true` | 查阅对应模型文档确认是否需要此参数 |

- **SDK 使用要点**：
  - Python SDK：`dashscope.Generation.call(..., tools=..., tool_choice=...)`
  - Java SDK：`GenerationParam.builder().tools(...).toolChoice(...).build()`
  - WebSocket 流式调用：函数调用事件以独立 `tool_call` 消息类型推送，需监听 `event == "tool_call"` 并解析 `content` 字段

- **安全与调试**：
  - 函数名与参数应使用小写字母+下划线命名（如 `get_user_profile`），避免特殊字符；
  - 生产环境建议对 `tool_calls` 响应做白名单校验（验证 `name` 是否在预设函数集中）；
  - 若模型返回无效 JSON 或空 `arguments`，可添加 `system` 消息强化指令，例如：`"Always output valid JSON for tool calls. Never omit required parameters."`

## 面向开发者，简洁实用

- ✅ **快速起步**：选 `qwen3.7-plus` 或 `tongyi-intent-detect-v3` → 构造 `tools` 数组 → 发起请求 → 解析 `response.choices[0].message.tool_calls`。
- ⚠️ **避坑提示**：不要在不支持的模型（如 `qwen-long`）上尝试函数调用；子空间调用需确保该空间已授权所用模型；[异步任务](asynchronous-task.md)（如视频生成）不支持函数调用，仅同步/流式接口可用。
- 🚀 **进阶建议**：结合 `response_format: json_object` + `temperature=0` 提升结构化输出稳定性；对高敏感函数（如支付、删除），务必在服务端二次校验参数合法性与用户权限。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [model experience](../guides/model-experience.md)
- [more models](../api/more-models.md)


