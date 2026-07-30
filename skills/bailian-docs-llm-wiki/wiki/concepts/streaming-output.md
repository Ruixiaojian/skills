# 流式输出

流式输出（Streaming Output）是指模型响应以增量方式、分块（chunk）持续返回给客户端的通信模式，而非等待整个响应生成完毕后一次性返回。它显著降低端到端延迟，提升用户感知的响应实时性，是构建高交互性 AI 应用（如对话助手、实时语音合成、代码补全等）的关键能力。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中并非统一开关，而是按协议、模型类型和调用模式差异化支持：

- **同步 API 调用（Application Call / Qwen Model API）**：  
  通过请求参数 `stream=true` 启用。适用于 `application-call`（新版/旧版智能体、工作流）、`qwen-*` 文本生成模型等同步接口。服务端将按 token 或语义单元（如句子、工具调用片段）分批返回 `data: {...}` 格式的 SSE（Server-Sent Events）响应。前端需使用 `EventSource` 或 SDK 的流式解析器（如 DashScope Python SDK 的 `StreamIterator`）逐块消费。

- **Realtime API（Omni / Audio 系列）**：  
  流式为**默认且强制行为**，不依赖 `stream` 参数。WebSocket 连接建立后，服务端通过标准化事件（如 `response.text.delta`、`response.audio.delta`、`response.tool_calls.delta`）实时推送增量内容，天然适配语音、文本、音频[多模态](multi-modal.md)混合输出场景。

- **异步调用（`background=true`）**：  
  **明确不支持流式输出**。异步模式下，API 立即返回任务 ID，结果需通过轮询 `retrieve` 接口获取完整响应。若在异步请求中设置 `stream=true`，该参数将被忽略。

- **OpenAI 兼容 Responses API**：  
  支持流式，但存在兼容性差异：部分流式 chunk 中 `delta.tool_calls` 字段可能缺失参数细节，建议在非流式模式下验证工具调用逻辑后再启用流式。

## 关键参数和配置

| 参数名 | 类型 | 作用 | 适用场景 | 注意事项 |
|--------|------|------|----------|----------|
| `stream` | `boolean` | 启用基础流式响应 | Application Call、Qwen 模型 API（DashScope / OpenAI 兼容） | 默认 `false`；仅同步调用有效；异步调用中设为 `true` 无效 |
| `incremental_output` | `boolean` | 启用**增量式流式输出**（即每次只返回新生成的 token，而非重发全部已生成内容） | Application Call、Qwen 模型 API（DashScope 原生接口） | 必须与 `stream=true` 同时设置；可显著减少网络传输量和前端处理开销 |
| `modalities`（Realtime） | `array` | 控制输出模态组合（如 `["text", "audio"]`） | Omni Realtime、Audio Realtime API | 决定流式事件类型（`response.text.delta` / `response.audio.delta`），影响前端解析逻辑 |

> 💡 **最佳实践**：  
> - 对话类应用：始终启用 `stream=true` + `incremental_output=true`（DashScope 接口）；  
> - 实时语音助手：直接使用 Omni Realtime API，无需手动配置 `stream`，专注处理 `response.*.delta` 事件；  
> - 调试流式行为：使用控制台「API 调试」页或 `curl -N` 命令观察原始 SSE 流。

## 面向开发者的重要提示

- **前端必须正确解析 SSE**：确保使用支持 `text/event-stream` 的客户端（如 `EventSource`、`fetch + ReadableStream` 或 SDK 封装的流式迭代器），避免因未处理 `data:` 前缀或忽略 `event:` 类型导致解析失败。
- **流式 ≠ 实时语音级低延迟**：文本流式通常为 100–500ms 级别；如需 <200ms 端到端语音交互，请务必选用 `Omni Realtime` 或 `Audio Realtime` 系列模型及 WebSocket/AOQ 协议。
- **错误处理需适配流式**：流式响应中，错误可能出现在任意 chunk（如 `event: error`），不可仅依赖 HTTP 状态码；应监听所有事件并检查 `error` 字段。
- **计费与 [Token](token.md) 统计**：流式输出按实际生成的 token 总数计费，与是否启用流式无关；各 chunk 中的 `usage` 字段（如存在）仅反映该块 token 数，完整用量请以最终 `done` 事件或非流式响应为准。

## 关联主题页

- [application call](../api/application-call.md)
- [application support](../guides/application-support.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


