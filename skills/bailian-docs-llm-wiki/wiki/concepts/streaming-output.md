# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量方式分块、实时返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户体验，尤其适用于对话交互、实时语音合成、长文本生成等对响应速度敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中广泛支持于多种协议与模型类型，但具体行为和字段结构因接口协议而异：

- **[OpenAI 兼容接口](openai-compatible-interface.md)**（如 `/v1/chat/completions`）：启用 `stream=True` 后，服务按 token 粒度返回 `delta.content` 字段；客户端需累积拼接 `delta.content` 得到完整回复。工具调用（Function Calling）的 `delta.tool_calls` 也以流式方式逐段返回参数片段。
  
- **DashScope 原生接口**：通过 `stream=True` 开启流式，响应体中 `output.text` 字段为当前批次新增文本（非全量），配合 `incremental_output=True` 可确保每次仅返回新生成内容（避免重复传输历史内容）。

- **Realtime API（WebSocket/AOQ/WebRTC）**：底层默认采用流式事件驱动模型。文本输出通过 `content.text.delta` 事件实时推送；语音输出则以 PCM 音频帧形式分片下发（如 `audio.delta`），支持低延迟播放。VAD（语音活动检测）与 TTS 合成均依赖流式机制实现端到端实时性。

- **Application/Assistant API**：`stream=True` 触发逐 token 流式响应；若同时设置 `incremental_output=True`，则每个 chunk 仅含本次生成的新 token，便于前端做精准增量渲染（如打字机效果），无需维护上下文拼接逻辑。

> ⚠️ 注意：流式响应不改变模型生成逻辑，仅影响传输方式；所有流式接口仍受 `max_tokens`、速率限制及配额约束。

## 关键参数和配置

| 参数 | 类型 | 说明 | 生效范围 |
|------|------|------|----------|
| `stream` | `boolean` | 必须设为 `true` 才启用流式响应；设为 `false` 或省略时为同步阻塞模式 | 全部文本生成类接口（Qwen、Omni、Realtime、Assistant） |
| `incremental_output` | `boolean` | 仅在 `stream=True` 时生效；启用后每个响应 chunk 仅含本次新增内容（非累计），避免客户端重复解析 | DashScope 原生接口、Application/Assistant API |
| `modalities`（Realtime） | `array` | 指定输出模态（如 `["text", "audio"]`），决定流式事件类型（`text.delta` / `audio.delta`） | Omni Realtime、Realtime API |

- **HTTP Header 要求**：使用 WebSocket 或 AOQ 协议时，`stream` 由会话初始化参数控制（如 `session.update` 中的 `stream: true`），无需额外 Header；HTTP 接口需在请求体中显式传入。
- **SDK 支持**：DashScope Python SDK 的 `Generation.call()`、`AioGeneration.call()` 及 `RealtimeClient` 均原生支持流式；OpenAI 兼容 SDK（如 `openai>=1.0`）需使用 `stream=True` 并迭代 `response` 对象。

## 面向开发者：简洁实用建议

- ✅ **必做**：始终检查响应状态码（200）和 `done` 标志（如 OpenAI 的 `finish_reason`、DashScope 的 `is_last` 字段），确认流式结束。
- ✅ **推荐**：前端使用 `TextEncoder` + `ReadableStream` 或 `EventSource` 解析流式响应；服务端建议复用 HTTP 连接池（如 Python 的 `aiohttp.TCPConnector(limit_per_host=30)`）。
- ⚠️ **避坑**：
  - [OpenAI 兼容接口](openai-compatible-interface.md)返回 `delta.content` 为空字符串 `""` 表示该 chunk 无新文本（如仅触发 tool call），需跳过拼接；
  - DashScope 原生接口流式响应中 `output.text` 可能为空，应以 `output.choices[0].finish_reason` 判定终结；
  - `incremental_output=True` 不兼容部分旧版 SDK，请确保使用 DashScope SDK ≥ 4.28.0。
- 🚀 **进阶**：结合 `temperature`/`top_p` 控制生成稳定性，避免流式过程中出现频繁回退或重复；对语音场景，建议搭配 `turn_detection.silence_duration_ms` 优化 VAD 敏感度，减少流式中断。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)
- [more about models](../api/more-about-models.md)


