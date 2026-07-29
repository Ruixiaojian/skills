# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中分块（chunk）返回结果，而非等待全部内容完成后再一次性返回。它显著降低端到端延迟，提升用户交互体验，并支持前端实现打字机效果、实时转录、语音合成驱动等增量式渲染场景。

## 在百炼平台的不同场景中如何使用

流式输出在以下核心能力中被统一支持，但协议、事件格式与适用范围存在差异：

- **知识问答（`/api/v2/apps/knowledge/chat`）**：通过 Server-Sent Events（SSE）协议返回 `text/event-stream` 响应，按阶段输出 `planning` → `tool_calling` → `generation` 三类事件，每个事件携带结构化字段（如 `event: generation`, `data: {"text": "..."}`），需客户端正确解析 `data:` 前缀与换行分隔。

- **智能体/工作流调用（Responses API）**：在同步调用接口（如 `/responses`）中设置 `stream=true`，返回符合 OpenAI 兼容格式的 SSE 流，每 chunk 包含 `delta.content`（增量文本）、`finish_reason` 等字段；**异步调用（`background=true`）不支持流式输出**。

- **Realtime API（AOQ/WebRTC/WebSocket）**：基于长连接的双向事件流，非传统 HTTP SSE。服务端通过 `response.delta`（文本增量）、`response.audio.delta`（音频 PCM 片段）、`conversation.item.input_audio_transcription.delta`（ASR 实时识别）等事件主动推送，客户端需监听并拼接。

- **Omni Realtime API（WebSocket）**：采用自定义 WebSocket 事件协议，关键事件包括 `response.delta`（文本流）、`response.audio.delta`（音频流）、`response.done`（结束标识）。支持 `incremental_output=true` 进一步确保每次只返回新生成 token，避免重复内容。

- **通用应用调用（DashScope API）**：`/api/v1/apps/{APP_ID}/completion` 接口本身**不原生支持流式输出**；如需流式能力，必须使用 Responses API 兼容路径（即 `compatible-mode/v1/responses`）并显式启用 `stream=true`。

> ✅ 统一原则：所有流式能力均要求客户端具备事件解析、缓冲管理与错误重连能力；不支持流式的调用（如[异步任务](asynchronous-task.md)、DashScope 原生 completion）将返回完整 JSON 响应体。

## 关键参数和配置

| 参数 | 类型 | 作用 | 是否必需 | 说明 |
|------|------|------|----------|------|
| `stream` | `boolean` | 启用流式响应模式 | 否（默认 `false`） | 所有支持流式的接口均需显式设为 `true`；设为 `false` 或不传则返回完整响应 |
| `incremental_output` | `boolean` | 启用真正增量式输出（仅 `stream=true` 时生效） | 否（默认 `false`） | 若为 `true`，每个 chunk 的 `delta.content` 仅含本次新生成内容（非累计）；若为 `false`，部分场景可能重复返回已发送内容，前端需自行去重 |
| `modalities` | `string[]` | 指定输出模态（Realtime/Omni 场景） | 是（当含 `"audio"` 时） | 必须包含 `"text"`；若需语音合成，需同时指定 `"audio"` 并配置 `voice` |
| `turn_detection.type` | `string` | VAD 检测模式（Realtime/Omni） | 否（默认 `"server_vad"`） | 影响流式触发时机：`"semantic_vad"` 可实现语义级断句流式，`"server_vad"` 依赖音频静音检测 |

> ⚠️ 注意事项：
> - `stream=true` 时，HTTP 响应头必须包含 `Content-Type: text/event-stream`（SSE）或维持 WebSocket/AOQ 长连接；
> - 流式响应无 `Content-Length`，客户端不可依赖该 header 判断结束；
> - 超时时间需延长（建议 ≥60s），避免因网络波动中断连接；
> - 错误发生时，服务端会发送 `error` 事件（SSE）或 `error` WebSocket message，需捕获处理。

## 面向开发者：简洁实用建议

- **前端渲染**：对 `stream=true` + `incremental_output=true` 的响应，直接追加 `delta.content` 到 DOM 即可，无需缓存或去重；若未启用 `incremental_output`，请维护本地 buffer 并比对上一 chunk 内容。
- **错误处理**：监听 `event: error`（SSE）或 `error` message（WebSocket），检查 `data.code` 和 `data.message`，常见错误如 `429 Too Many Requests`（需指数退避）、`503 Service Unavailable`（重试）。
- **调试技巧**：使用 `curl -N` 或浏览器 DevTools Network → EventStream 查看原始 SSE 数据；WebSocket 场景可用 `wscat` 工具连接测试。
- **性能优化**：Realtime/Omni 场景下，优先选用 `semantic_vad` + `incremental_output=true` 组合，可最小化首包延迟（TTFT）与生成延迟（TPOT）。
- **兼容性提醒**：旧版 DashScope 原生 API（如 `/completion`）不支持流式，请务必切换至 Responses API 兼容路径。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [application call](../api/application-call.md)
- [application support](../guides/application-support.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


