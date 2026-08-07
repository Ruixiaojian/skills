# 流式输出

流式输出（Streaming Output）是指模型在生成响应过程中，将结果以增量方式分块（chunk）实时返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户感知的响应速度与交互自然度，是构建实时对话、语音合成、长文本生成等低延迟场景的关键能力。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中贯穿多个调用层级和模态，具体应用如下：

- **模型直调（Model Experience）**：所有支持文本生成的 Qwen 系列模型（如 `qwen3.7-plus`、`qwen3.8-max`、`qwen3.7-flash`）均支持流式响应。适用于需实时渲染输出的终端（如聊天界面、IDE 插件），尤其在长上下文或复杂推理任务中可避免用户长时间等待。

- **应用调用（Application Call）**：  
  - DashScope 原生接口（`/api/v1/apps/{app_id}/completion`）**不直接暴露 `stream` 参数**，但底层默认启用流式传输（HTTP chunked encoding），SDK 会自动按 token 块解析并触发回调；  
  - [OpenAI 兼容接口](openai-compatible-interface.md)（`/api/v2/apps/agent/{app_id}/compatible-mode/v1/responses`）**显式支持 `stream: true`**，且工作流类应用需在控制台“结束节点”手动开启「流式输出」开关并重新发布，否则即使请求设为 `stream=true` 也不会生效。

- **语音处理（ASR/TTS）**：  
  - ASR 模型（如 `qwen-audio-3.0-asr-flash-streaming`）专为实时音频流设计，支持毫秒级语音片段持续输入与逐句/逐词转写输出；  
  - TTS 模型（如 `qwen-audio-3.0-tts-plus`）支持流式音频二进制分片返回（`audio/mpeg` 或 `audio/ogg`），便于前端边接收边播放，实现零缓冲语音播报。

- **全模态与智能体（Application Support）**：  
  - 当启用 `stream=true` 时，响应体为 Server-Sent Events（SSE）格式，每块含 `data:` 字段；  
  - 若需仅返回本次新增 token（而非累积历史），必须同时设置 `incremental_output=true`（该参数仅在 `stream=true` 时生效）；  
  - 插件调用（Function Calling）与联网搜索等中间步骤的输出**不参与流式返回**，流式仅作用于最终模型生成的 `text` 内容。

## 关键参数和配置

| 参数 | 类型 | 默认值 | 说明 | 生效范围 |
|------|------|--------|------|----------|
| `stream` | boolean | `false` | 启用流式传输模式。设为 `true` 后，响应头 `Content-Type` 变为 `text/event-stream`，数据按 SSE 格式分块推送。 | OpenAI 兼容 API（Responses 接口）、Assistant API |
| `incremental_output` | boolean | `false` | 仅当 `stream=true` 时有效。若为 `true`，每个 chunk 的 `delta.content` 仅包含本次新增 token（推荐用于前端增量渲染）；若为 `false`，则 `delta.content` 为从开头累计的完整文本（兼容旧逻辑）。 | Assistant API、OpenAI 兼容 Responses API |
| `stream_options.include_usage` | boolean | `false` | 控制是否在流式响应末尾的 `usage` 事件中返回 token 统计。需 DashScope SDK ≥1.25.0（Python）或对应新版 SDK 才支持。 | DashScope 原生接口（通过 SDK 透传） |

> ⚠️ 注意：  
> - DashScope 原生 RESTful 接口（如 `/api/v1/services/text-generation`）**不接受 `stream` 请求参数**，其流式行为由 SDK 自动处理（Python SDK 中 `stream=True` 即启用）；  
> - `stream=true` 与 `background=true`（异步模式）互斥，异步调用下 `stream` 参数被忽略；  
> - 流式响应中每个 chunk 的 `id` 和 `object` 字段保持一致，`choices[0].delta.content` 为增量内容，`choices[0].finish_reason` 出现在最后一个 chunk。

## 面向开发者，简洁实用

- ✅ **快速启用**：OpenAI 兼容调用只需在请求体加 `"stream": true`；DashScope SDK 调用时传 `stream=True`（Python）或 `.stream()` 方法（Java/JS）；  
- ✅ **前端渲染建议**：配合 `incremental_output=true` 使用，每次收到 `delta.content` 直接追加到 DOM，避免重复解析或闪烁；  
- ✅ **错误处理**：流式连接中断时，检查 HTTP 状态码（如 `499 Client Closed Request`）及 SSE `event: error`；重连应携带 `last-event-id`（若服务端支持）；  
- ❌ **不支持场景**：结构化 JSON 输出（`response_format={"type":"json_object"}`）与流式不可共存，会返回 `400 Bad Request`；Function Calling 的工具调用过程本身不流式化；  
- 📌 **调试技巧**：使用 `curl -N` 或 Postman 的 “Stream response” 开关观察原始 SSE 数据；Python SDK 中可用 `for chunk in response:` 迭代处理。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [application support](../guides/application-support.md)


