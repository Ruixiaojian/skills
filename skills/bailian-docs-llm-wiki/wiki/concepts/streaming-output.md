# 流式输出

流式输出（Streaming Output）是指模型响应不等待全部生成完成，而是以增量方式分块、实时地将 token 或事件片段逐批返回给客户端的通信模式。它显著降低端到端延迟，提升用户感知流畅度，并支持前端实时渲染、语音合成流式驱动、工具调用过程观测等关键交互场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准大模型 API（Qwen 系列）**：通过 [OpenAI 兼容接口](openai-compatible-api.md)（`/v1/chat/completions`）或 DashScope 原生接口启用 `stream=true`，服务端按 token 逐帧返回 `content` 片段；适用于对话应用、代码补全等需低延迟反馈的场景。注意：[OpenAI 兼容接口](openai-compatible-api.md)的流式响应**不包含完整 usage 和 finish_reason 字段**，如需精确统计或控制终止逻辑，推荐使用 DashScope 接口。

- **Managed Agents（托管智能体）**：采用 Server-Sent Events（SSE）协议实现结构化流式事件推送，包括 `message`（模型文本输出）、`tool_call`（工具调用请求）、`tool_output`（工具执行结果）、`session_status`（会话状态变更）等类型事件。开发者可据此构建带中间反馈的长周期任务界面（如[文件处理](file-processing.md)进度、代码执行日志）。

- **Realtime API（实时多模态）**：基于 WebSocket 或 AOQ 协议，以事件流形式推送细粒度多模态输出，例如：
  - `response.text.delta`：文本 token 增量；
  - `response.audio.delta`：PCM 音频帧流；
  - `input_audio_buffer.speech_started` / `speech_ended`：语音活动检测事件。
  此类流式设计专为语音助手、实时翻译等毫秒级交互优化，支持 VAD 触发、静音超时、平滑音频输出等高级控制。

- **Application Support（AI 应用编排）**：在百炼控制台构建的应用中，可通过开启 `stream=True` 启用基础流式；进一步设置 `incremental_output=True` 可确保每次响应仅含**新增内容**（而非重发历史），避免前端重复渲染或音频合成重复拼接，是构建高质量语音/文字混合输出应用的推荐配置。

## 关键参数和配置

| 参数 | 类型 | 说明 | 所属场景 | 默认值 |
|------|------|------|----------|--------|
| `stream` | boolean | 启用流式响应模式 | 所有 API（Qwen、Agents、Application） | `false` |
| `incremental_output` | boolean | 在 `stream=true` 下启用增量式输出（仅返回新 token，非全量重传） | Application Support、部分 DashScope 接口 | `false` |
| SSE `Accept: text/event-stream` | HTTP Header | 必须在请求头中声明，用于 Managed Agents 和部分 DashScope 流式接口 | Managed Agents、DashScope 原生流式 | — |
| WebSocket event types | string | 如 `response.text.delta`, `response.audio.delta`，需按文档订阅对应事件 | Realtime API（WebSocket/AOQ） | — |
| `x-dashscope-rtc-transport` | HTTP Header | 指定 Realtime 协议类型（`websocket`/`webrtc`/`moq`），影响流式传输能力与延迟特性 | Realtime API | — |

> ⚠️ 注意：  
> - `stream=true` 是流式输出的**必要开关**，但不同协议对响应格式、事件语义和元数据支持差异显著；  
> - [OpenAI 兼容接口](openai-compatible-api.md)的流式响应体为 `data: {...}` 格式，每行一个 JSON 对象，需按标准 SSE 解析（即使未显式声明 `text/event-stream`）；  
> - DashScope 原生接口流式响应为纯 JSON Lines（NDJSON），每行一个完整 JSON 对象，无 `data:` 前缀；  
> - Realtime API 的 WebSocket 流必须先发送 `session.update` 事件完成初始化，再接收输出事件，否则可能丢帧或连接中断。

## 面向开发者，简洁实用

- ✅ **首选实践**：前端应用务必设置 `stream=true` + `incremental_output=true`（若支持），并监听 `delta` 类事件，避免缓存/拼接逻辑错误。  
- ✅ **调试建议**：使用 `curl -N` 或 Postman 的 SSE 模式测试流式接口；Realtime API 建议优先选用 WebSocket 协议快速验证，生产环境再按终端选 AOQ/WebRTC。  
- ✅ **错误防御**：流式连接需设置超时（如 SSE `timeout=120s`，WebSocket `ping/pong` 心跳），并实现断线重连与会话恢复逻辑（尤其 Managed Agents 场景）。  
- ❌ **避免陷阱**：不要在 OpenAI 兼容流式中依赖 `usage.total_tokens` 或 `finish_reason` 判断完成——它们只在最后一帧出现且字段名不一致；应监听 `choices[0].delta.content === null` 或 `finish_reason` 字段存在性作为终止信号。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents](../guides/managed-agents.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)


