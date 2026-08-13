# 流式输出

流式输出（Streaming）是指模型在生成响应过程中，将结果以增量方式分块（chunk）实时返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户感知的响应实时性，是构建交互式 AI 应用（如聊天助手、语音对话、代码补全）的关键能力。

## 在百炼平台的不同场景中如何使用

- **文本生成（Qwen 系列）**：通过 DashScope 原生接口或 [OpenAI 兼容接口](openai-compatibility.md)（`/chat/completions`）启用 `stream=true`，服务端按 token 或语义单元逐块返回 `delta.content`；工具调用阶段可能返回 `delta.tool_calls`，需兼容空 content 场景。
- **专用模型（法睿、意图识别、OCR、MT 等）**：所有专用模型均支持流式输出，调用时设置 `stream=True`（Python SDK）或 `"stream": true`（HTTP），适用于法律文书渐进生成、翻译片段实时呈现、OCR 结构化字段逐步解析等场景。
- **实时[多模态](multimodal.md)（Omni Realtime / Realtime API）**：基于 WebSocket 的实时接口天然采用事件流模式，文本、音频、工具调用结果均以独立事件（如 `text.delta`、`audio.delta`、`function_call.delta`）实时推送，支持毫秒级响应与低延迟语音交互。
- **[OpenAI 兼容接口](openai-compatibility.md)（Chat、Responses、Vision）**：完全遵循 OpenAI 流式协议（SSE），返回 `data: {...}` 格式事件流；`Responses API` 在启用联网搜索时，流式输出会包含中间检索步骤与最终答案，便于前端展示思考过程。
- **批量与框架集成（LangChain / Batch）**：LangChain 的 `streaming=True` 选项可透传至百炼底层；Batch 接口暂不支持流式，但单次请求内多个子任务仍可通过 `stream_options={"include_usage": true}` 在流末尾附加 token 统计。

## 关键参数和配置

- **`stream`**（必选布尔值）：启用流式输出的核心开关。默认为 `false`；设为 `true` 后，响应体变为事件流（HTTP SSE）或异步迭代器（SDK）。
- **`stream_options`**（可选对象，仅 [OpenAI 兼容接口](openai-compatibility.md)）：
  - `{"include_usage": true}`：在流结束前发送一条含 `usage` 字段的 final chunk，包含 `prompt_tokens`、`completion_tokens` 和 `total_tokens`。
- **SDK 使用要点**：
  - Python DashScope：`Generation.call(..., stream=True)` 返回 `Generator`，需循环 `for chunk in response:` 处理；
  - Python OpenAI SDK：`client.chat.completions.create(..., stream=True)` 返回 `Stream` 对象，同样迭代处理；
  - Node.js / curl：需正确处理 `Content-Type: text/event-stream` 及 `data:` 前缀，按行解析并去除空行与注释（`event:`、`id:` 等字段可忽略）。
- **注意事项**：
  - 流式响应中 `delta.content` 可能为空（尤其在工具调用或思考阶段），务必检查 `delta.tool_calls` 或 `delta.function_call` 字段；
  - OpenAI 兼容接口的 `choices[0].delta` 字段结构与标准 OpenAI 一致，但部分字段（如 `finish_reason`）仅出现在 final chunk；
  - 实时 API（WebSocket）无 `stream` 参数，其流式行为由协议本身保证，开发者直接监听 `text.delta`、`audio.delta` 等事件即可。

面向开发者：优先使用 SDK 封装的流式迭代器（如 Python 的 `for chunk in response:`），避免手动解析 SSE；生产环境务必添加超时、重试与错误降级逻辑；前端渲染时建议对 `delta.content` 做防抖合并，避免频繁 DOM 更新。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [more models](../api/more-models.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


