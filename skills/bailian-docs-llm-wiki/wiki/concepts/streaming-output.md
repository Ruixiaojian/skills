# 流式输出

流式输出（Streaming Output）是指模型响应不等待全部生成完成，而是以增量方式逐段（通常为 token 或语义单元）实时返回结果的通信机制。它显著降低端到端延迟，提升用户体验，并支持前端实时渲染、语音合成流式播报、长文本渐进式处理等关键场景。

## 在百炼平台的不同场景中如何使用

- **标准文本生成（Qwen API）**：在 DashScope 原生接口或 OpenAI/Anthropic 兼容接口中，设置 `stream=true` 即可启用。[OpenAI 兼容接口](openai-compatible-interface.md)返回 `delta.content` 字段；DashScope 原生接口返回 `output.text` 字段（每次为新增内容片段），需按 SSE（Server-Sent Events）协议解析。
  
- **智能体（Agent）与 Responses API**：`stream=true` 同样生效，但需注意：工具调用（tool call）阶段可能先返回 `{"delta": {"role": "assistant", "content": ""}}` 或 `{"delta": {"tool_calls": [...]}}`，最终响应中 `finish_reason` 为 `"stop"` 或 `"tool_calls"`，开发者需按事件类型分别处理文本流与工具指令流。

- **Realtime API（Omni / Audio 系列）**：原生基于 WebSocket 或 AOQ 的实时协议，默认即为流式交互。文本输出通过 `conversation.item.input` / `conversation.item.output` 事件持续推送；音频输出则以 PCM 数据块形式分帧下发（如 `output_audio` 事件），支持低延迟 TTS 播放与 VAD 驱动的自然对话节奏。

- **应用层（Application Support）**：在百炼控制台创建的 AI 应用或通过 Assistant API 调用时，`stream=True` 可开启流式响应；若进一步设置 `incremental_output=True`，服务端将确保每个 chunk 仅包含本次新增 token（而非历史内容重传），大幅减少网络带宽与前端拼接开销。

- **批量与[文件处理](file-processing.md)（Batch / Files）**：目前 Batch Chat（同步式）和 Files 接口**不支持流式输出**，均为全量响应。如需流式处理大量文档，建议拆分为多个小请求并行调用，或使用 Realtime API + 自定义流式编排逻辑。

## 关键参数和配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stream` | boolean | `false` | 全局开关，启用后返回流式响应（SSE 或 WebSocket event stream）。所有主流接口均支持。 |
| `incremental_output` | boolean | `false` | **仅在 `stream=true` 时有效**。启用后，每个响应 chunk 仅含本次生成的新 token，避免重复传输历史内容，推荐前端渲染、日志记录等场景开启。 |
| `stream_options.include_usage` | object | — | [OpenAI 兼容接口](openai-compatible-interface.md)特有。设为 `{"include_usage": true}` 时，流式结束前的最后一个 event 将携带完整 `usage` 统计（`prompt_tokens`, `completion_tokens`, `total_tokens`）。 |

> ⚠️ 注意：  
> - DashScope 原生接口不支持 `stream_options`，token 统计需通过 `output.usage` 字段在最终响应中获取（非流式）或启用 `enable_search` 等高级能力时在中间 event 中附带；  
> - Realtime API 无 `stream` 参数，其流式行为由协议本身保证，相关控制通过 `modalities`、`turn_detection` 等会话级配置实现；  
> - `incremental_output` 当前仅在 Application Support 场景及部分新版 DashScope SDK 中稳定支持，旧版 SDK 或直连 REST 接口需自行去重处理。

## 面向开发者：简洁实用提示

- ✅ **必做**：始终监听 `data: [event]`（SSE）或 `event` 字段（WebSocket），按 `finish_reason` 判断流是否结束（常见值：`"stop"`、`"length"`、`"tool_calls"`、`"error"`）；  
- ✅ **推荐**：前端使用 `TextDecoderStream` 或 `ReadableStream` 解析 SSE，避免手动分割导致的字符截断；  
- ✅ **调试技巧**：用 `curl -N` 或 Postman 的 “Stream response” 开关快速验证流式行为；  
- ❌ **避免**：在未检查 `delta.content` 是否为 `null` 或空字符串时直接拼接（[OpenAI 兼容接口](openai-compatible-interface.md)中，工具调用阶段 `content` 可为空）；  
- 🚀 **进阶**：结合 `incremental_output=True` 与前端 Markdown 渲染器（如 `marked.js`），实现「边打字边加粗」的富文本实时预览效果。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)


