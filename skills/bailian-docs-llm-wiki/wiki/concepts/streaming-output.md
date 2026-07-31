# 流式输出

流式输出（Streaming Output）是指模型或应用在生成响应过程中，将结果以增量、分块的方式持续返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户感知的实时性与交互流畅度，是构建对话式、语音交互、长文本生成等场景的关键能力。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非全局默认能力，其支持范围和启用方式因调用路径与服务类型而异，需按以下场景分别配置：

- **Application Call（智能体/工作流调用）**  
  仅支持**同步调用**（即 `background=false`），且需同时满足：  
  - 请求参数中显式设置 `"stream": true`；  
  - 工作流应用必须在**结束节点（End Node）开启“流式输出”开关**并重新发布；  
  - 新版智能体（Agent 2.0）默认支持流式，无需额外配置开关；  
  - 异步调用（`background=true`）**不支持流式输出**，返回的是任务 ID，结果需轮询或通过事件总线获取。

- **Realtime API（实时[多模态](multi-modal.md)交互）**  
  所有 Realtime 协议（AOQ/WebRTC/WebSocket）均**原生支持流式输出**，且为默认行为：  
  - 文本以 `text.delta` 事件逐 token 推送；  
  - 音频以 PCM 帧（24 kHz）流式下发，配合 VAD 自动切分语句；  
  - 不需要额外启用参数，但需客户端正确监听 `onDataMsg` 或 WebSocket `message` 事件并处理增量数据。

- **Omni Realtime API（Qwen-Omni 系列）**  
  同样为默认流式，但提供精细化控制：  
  - `smooth_output: true`（仅 `qwen3.5-omni-flash-realtime`）可平滑语音输出节奏，减少停顿感；  
  - `semantic_vad` 模式下，文本流与音频流严格对齐语义单元（如完整句子），提升自然度；  
  - 所有流式事件均通过 `session.update` 配置后实时生效，无需重启连接。

- **标准模型调用（如 qwen3.7-plus）**  
  [OpenAI 兼容接口](openai-compatible-api.md)与 DashScope SDK 均支持流式：  
  - OpenAI SDK 中传入 `stream=True`；  
  - DashScope SDK 中设置 `stream=True` 并使用 `for chunk in response:` 迭代处理；  
  - 注意：部分轻量模型（如 `qwen-omni-turbo-realtime`）虽支持流式文本，但**不支持修改采样参数**，流式行为不可定制。

> ⚠️ 关键限制：流式输出**不兼容异步任务、文件上传临时 URL 场景及部分第三方模型**（详见各模型文档）。若请求中同时指定 `stream=true` 和 `background=true`，平台将忽略 `stream` 并降级为异步模式。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 默认值 | 是否必需 |
|------|------|------|------|--------|----------|
| `stream` | Application Call / 标准模型请求体 | boolean | 启用流式响应（仅同步调用有效） | `false` | 否 |
| `modalities` | Realtime / Omni Realtime `session.update` | string[] | 指定输出模态，决定流式内容类型 | `["text","audio"]` | 是（Realtime） |
| `smooth_output` | Omni Realtime `session.update` | boolean | 控制语音流是否平滑衔接（仅 flash 版本） | `false` | 否 |
| `turn_detection.type` | Omni Realtime `session.update` | string | 影响流式文本/音频的切分粒度（`server_vad` vs `semantic_vad`） | `"server_vad"` | 否 |

- **HTTP Header 要求**：流式响应必须使用 `Content-Type: text/event-stream`（SSE）或 WebSocket 二进制帧，客户端需适配对应解析逻辑；
- **SDK 提示**：OpenAI 兼容 SDK 使用 `ChatCompletionChunk` 对象；DashScope SDK 返回 `GenerationResponse` 的 `output.text` 字段为增量字符串，需累积拼接；
- **错误处理**：流式中断时（如网络断开），客户端应监听 `error` 事件并重连，平台不保证中间状态恢复。

## 面向开发者，简洁实用

- ✅ **快速启用**：只需在同步请求中加 `"stream": true`，并确保服务端（工作流/智能体）已配置支持；
- ✅ **实时调试**：使用 `curl -N` 或浏览器 DevTools 的 Network → EventStream 查看原始 SSE 流；
- ✅ **性能优化**：流式可降低首字节延迟（TTFB），但总耗时不变；建议搭配 `max_tokens` 限长防阻塞；
- ❌ **避坑提醒**：  
  - 不要在异步任务中尝试 `stream=true` —— 请求会被静默忽略；  
  - 工作流未开启结束节点流式开关 → 返回 `400 Bad Request`；  
  - Realtime 连接未收到 `session.updated` 就发送音频 → 服务端丢弃数据；  
- 🛠️ **推荐实践**：前端用 `ReadableStream` + `TextDecoderStream` 解析 SSE；服务端用 `aiohttp` 或 `fastapi.StreamingResponse` 透传流式数据。

## 关联主题页

- [application call](../api/application-call.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [more about models](../api/more-about-models.md)
- [get started with models](../guides/get-started-with-models.md)


