# 流式输出

流式输出（Streaming Output）是指模型响应内容以增量、分块的方式持续返回，而非等待全部生成完成后再一次性返回。这种机制显著降低首 [Token](token.md) 延迟（Time to First [Token](token.md), TTFT），提升用户感知的实时性与交互自然度，是语音对话、实时翻译、智能客服等低延迟场景的核心能力支撑。

## 在百炼平台的不同场景中，这个概念如何使用

- **Realtime API（实时多模态交互）**：  
  所有协议（AOQ/WebRTC/WebSocket）均默认启用流式输出。文本以 `text.delta` 事件逐字/逐词推送；音频以 PCM 分片（chunk）形式持续下发（如 `audio.delta`），采样率固定为 24kHz，客户端需按序拼接并实时播放。VAD 检测（如 `semantic_vad`）与流式生成深度协同，实现“边说边想、边想边说”。

- **Omni Realtime API（WebSocket 多模态实时接口）**：  
  采用事件驱动流式模型：服务端通过 `text.delta`、`audio.delta`、`tool_call` 等事件持续推送中间结果。`smooth_output: true`（仅 `qwen3-omni-flash-realtime` 支持）可进一步优化文本流节奏，减少停顿感；`max_tokens` 仅控制最终截断，不影响流式过程。

- **Managed Agents（托管智能体）**：  
  通过 Server-Sent Events（SSE）提供流式事件订阅（`/sessions/{id}/events/stream`）。开发者可实时监听 `message.delta`（文本增量）、`tool_call`（工具触发）、`tool_output`（工具执行结果）等事件，实现渐进式响应渲染与异步任务状态同步。

- **Qwen 原生 API（DashScope 文本生成）**：  
  通过 `stream: true` 参数启用流式响应。服务端返回 `text` 字段的增量片段（如 `"content": "今天"` → `"content": "天气"`），客户端需按 SSE 或 chunked transfer 编码解析。`incremental_output: true`（DashScope 原生接口特有）可进一步优化首 [Token](token.md) 调度，降低 TTFT。

- **Application Monitoring（应用观测）**：  
  流式输出行为直接影响可观测指标：`LLM` 节点的「延时」统计包含完整流式生命周期（从首 Token 到末 Token）；「Token 总量」累计所有流式分块的输入与输出 token 数，用于精准计费与性能分析。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 | 是否必需 |
|------|----------|------|------|-----------|
| `stream` | Qwen 原生 / OpenAI 兼容 API | boolean | 启用流式响应（返回 `text.delta` 分块） | 否（默认 `false`） |
| `incremental_output` | DashScope 原生 API | boolean | 启用增量调度优化，显著降低首 Token 延迟 | 否（默认 `false`） |
| `modalities: ["text","audio"]` | Realtime / Omni Realtime API | array | 指定启用文本+音频双流输出（单 `["audio"]` 不生效） | 是（若需音频） |
| `smooth_output` | Omni Realtime（`qwen3-omni-flash-realtime`） | boolean | 平滑文本流节奏，避免短句卡顿 | 否 |
| SSE `event` 类型 | Managed Agents | string | `message.delta`、`tool_call`、`tool_output` 等事件标识流式内容类型 | — |

> ⚠️ 注意：  
> - Realtime API 中，音频流必须配合 `output_audio_format: "pcm"` 和 `sampleRate: 24000` 使用；  
> - 所有流式接口均要求客户端具备分块解析与状态维护能力（如累积 `delta`、处理 `done` 事件）；  
> - `qwen-omni-turbo-realtime` 等极低延迟模型禁用 `temperature`/`top_p` 等参数，但流式行为不受影响。

## 面向开发者，简洁实用

- ✅ **必做**：启用流式时，始终监听 `done` 或 `session.ended` 事件作为流终止信号，避免遗漏结尾；  
- ✅ **推荐**：对文本流做简单缓冲（如 50ms 合并），避免 UI 频繁重绘；对音频流严格按时间戳/采样数对齐播放；  
- ✅ **调试**：在 Application Monitoring 中筛选 `LLM` Span，查看 `TTFT`、`ITL`（Inter-Token Latency）和 `TTL`（Time to Last Token）三指标定位流式瓶颈；  
- ❌ **避免**：在 WebSocket 或 SSE 连接中手动 `JSON.parse()` 整个响应体——应使用标准流式解析器（如 `fetch().body.getReader()` 或 `EventSource`）；  
- 📦 **SDK 提示**：Python `dashscope` SDK 自动处理 `stream=True` 的分块合并；Node.js SDK 需显式调用 `.on('data', ...)`；Realtime AOQ SDK 提供 `onAudioDelta` 回调直接接收 PCM buffer。

## 关联主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [managed agents](../guides/managed-agents.md)
- [application monitoring](../guides/application-monitoring.md)
- [qwen api reference](../api/qwen-api-reference.md)


