# 流式输出

流式输出（Streaming Output）是指模型响应以增量方式、分块（chunk）持续返回给客户端，而非等待整个响应生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户体验，并支持实时渲染、语音合成、前端逐字显示等交互场景。

## 在百炼平台的不同场景中如何使用

流式输出是百炼平台多项核心能力的默认或可选传输模式，具体应用如下：

- **知识问答（`/api/v2/apps/knowledge/chat`）**：默认启用流式输出（`stream=true`），通过 Server-Sent Events（SSE）协议返回三阶段事件（`plan` → `tool_call` → `answer`），便于前端分阶段展示思考过程与最终答案，并支持引用溯源。
  
- **Qwen 文本生成 API（OpenAI 兼容 / DashScope 原生）**：  
  - DashScope 原生接口默认流式（`stream=true`）；  
  - [OpenAI 兼容接口](openai-compatible-api.md)默认非流式（`stream=false`），需显式设置 `stream=true` 才启用；  
  - 启用后，响应为 SSE 格式，每块包含 `delta.content` 字段，需按 `data:` 行解析并累积拼接。

- **Omni Realtime API（WebSocket）**：本质即为全链路流式交互——音频输入流、文本/音频输出流均实时双向传输。无需额外配置 `stream` 参数，但需正确处理 `text_delta` 和 `audio_delta` 类型的 WebSocket 消息帧。

- **Realtime API（WebRTC/AOQ）**：底层协议天然支持低延迟流式，文本输出以 `text_delta` 事件推送，语音输出以 PCM 音频流分片下发，开发者需在客户端实现缓冲与播放同步逻辑。

> ⚠️ 注意：流式响应要求客户端主动声明接收格式（如 HTTP 请求头 `Accept: text/event-stream` 或 WebSocket 消息监听机制），否则可能因解析失败导致连接中断或数据丢失。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 默认值 | 适用接口 |
|--------|------|------|--------|----------|
| `stream` | boolean | 控制是否启用流式响应 | DashScope 原生：`true`；OpenAI 兼容：`false`；Knowledge Chat：`true` | `/api/v2/apps/knowledge/chat`, `/v1/chat/completions`, `/api/v1/services/aigc/text-generation/generation` |
| `Accept: text/event-stream` | HTTP Header | 必须设置，用于告知服务端返回 SSE 格式 | — | 所有基于 HTTP 的流式接口（非 WebSocket） |
| `output_modalities` | array | 指定输出模态（如 `["text", "audio"]`），决定流式内容类型 | `["text"]` | Omni Realtime / Realtime API（WebSocket/WebRTC） |
| `smooth_output` | boolean | （仅 `qwen3-omni-flash-realtime`）控制文本输出是否口语化、适合语音流式播报 | `null`（自动选择） | Omni Realtime API |

> ✅ 最佳实践：  
> - 开发者应始终检查响应状态码（如 `200 OK`）后再开始解析流；  
> - 对 SSE 响应，需忽略空行、跳过注释行（以 `:` 开头）、按 `data:` 提取 JSON；  
> - 对 WebSocket 流，建议使用 SDK 封装的消息处理器（如 `onTextDelta`, `onAudioDelta`），避免手动解析二进制帧；  
> - 流式调用不改变计费逻辑：仍按实际输出 token 数量计费，与是否流式无关。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


