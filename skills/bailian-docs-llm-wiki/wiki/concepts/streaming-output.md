# 流式输出

流式输出（Streaming）是指模型响应以增量方式、分块返回给客户端的机制，而非等待整个生成结果完成后再一次性返回。它通过服务器发送事件（SSE）、JSON Lines 或 WebSocket 消息等形式，将 token 或语义单元逐步推送，显著降低首字延迟（Time to First [Token](token.md), TTFT），提升用户感知的响应实时性与交互流畅度。

## 在百炼平台的不同场景中，这个概念如何使用

- **[OpenAI 兼容接口](openai-compatible-api.md)（Chat Completions / Responses / Vision 等）**：通过 `stream=true` 参数启用，服务端返回标准 SSE 格式（`data: {...}`），每条消息包含一个 `delta.content` 片段及可选 `finish_reason`；支持 `stream_options={"include_usage": true}` 在流末尾附加 token 统计。
  
- **DashScope 原生接口（如文本生成）**：同样使用 `stream=true`，但响应格式为 JSON Lines（每行一个 JSON 对象），便于服务端解析与日志追踪；额外支持 `incremental_output=true`（部分模型）实现更细粒度的 token 级增量输出。

- **Managed Agents API**：不直接暴露 `stream` 参数，而是通过 `GET /sessions/{session_id}/events/stream` 提供 SSE 事件流，返回 `message`（含增量文本）、`tool_use`、`function_call` 等结构化事件，天然支持智能体多步推理与工具调用过程的实时反馈。

- **Omni Realtime API 与 Realtime API**：基于 WebSocket 协议，采用事件驱动模型，服务端主动推送 `message.delta`（文本片段）、`audio.chunk`（PCM 音频帧）等事件；无需显式设置 `stream`，流式行为是协议默认能力，且支持音视频与文本同步流式输出。

- **Batch 接口（Batch File / Batch Chat）**：**不支持流式输出**，所有请求均以异步或同步阻塞方式返回完整结果，适用于离线处理场景。

## 关键参数和配置

| 参数 | 类型 | 说明 | 支持接口 |
|------|------|------|----------|
| `stream` | boolean | 启用流式响应的核心开关 | [OpenAI 兼容接口](openai-compatible-api.md)、DashScope 原生接口 |
| `stream_options` | object | 控制流式行为细节，当前仅支持 `{"include_usage": true}`（在流末尾附加 `usage` 字段） | [OpenAI 兼容接口](openai-compatible-api.md)（v1.0+） |
| `incremental_output` | boolean | DashScope 原生接口特有，启用后返回更紧凑的增量 token 输出（如单 token 而非完整 delta） | DashScope 原生文本生成接口 |
| SSE `Content-Type` | header | 必须为 `text/event-stream` | OpenAI 兼容 & Managed Agents 流式端点 |
| WebSocket event type | — | 如 `message.delta`、`audio.chunk`、`session.status` 等，由协议定义 | Omni Realtime / Realtime API |

> ⚠️ 注意：  
> - `stream=true` 时，`max_tokens` 仍生效，但截断发生在流式生成过程中，不会导致提前终止流；  
> - 流式响应下，`finish_reason` 可能为 `"stop"`、`"length"`、`"tool_calls"` 或 `"content_filter"`，需在客户端正确处理；  
> - 所有流式接口均要求客户端保持连接并及时读取，超时或中断将导致会话终止（Managed Agents 除外，其 Session 状态独立于流连接）。

## 面向开发者，简洁实用

- ✅ **快速启用**：只需在请求体中添加 `"stream": true`，配合对应 SDK 的 `stream=True`（Python）或 `.stream()`（JS）方法即可；
- ✅ **解析建议**：  
  - OpenAI 兼容流：按行分割 SSE 数据，忽略空行和 `event:` 行，`JSON.parse(data)` 解析 `data:` 后内容；  
  - DashScope JSON Lines：逐行 `JSON.parse()`，检查 `output.text` 是否存在增量内容；  
  - WebSocket 流：监听 `message` 事件，根据 `event` 字段类型（如 `message.delta`）提取 `delta.content` 或 `audio.data`；
- ✅ **错误处理**：流式请求失败时，HTTP 状态码（如 429/503）仍会在首响应头返回；流中出现 `error` 事件需主动捕获并重试；
- ✅ **性能提示**：启用流式后，TTFT 通常 < 500ms（取决于模型与网络），但总延迟（TTLT）不变；建议搭配 `temperature=0.3` ~ `0.7` 平衡确定性与流畅性；
- ❌ **避坑提醒**：  
  - 不要对流式响应做 `response.json()` 全量解析（会失败）；  
  - `repetition_penalty` 等高级采样参数在 OpenAI 兼容接口中会被忽略，请优先使用 DashScope 原生接口；  
  - Managed Agents 的流式事件不可用于重放或状态回溯，仅作实时展示用途。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


