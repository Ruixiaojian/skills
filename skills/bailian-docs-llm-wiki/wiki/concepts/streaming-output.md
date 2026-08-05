# 流式输出

流式输出（Streaming Output）是指模型响应以增量方式、分块（chunk）实时返回给客户端，而非等待整个生成过程完成后再一次性返回全部结果。这种方式显著降低端到端延迟，提升用户体验，尤其适用于对话交互、实时语音合成、长文本生成等对响应速度敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **文本生成类 API（Qwen 系列）**：  
  所有协议（OpenAI 兼容 Chat Completions / Anthropic Messages / DashScope 原生）均支持 `stream=true`。启用后，服务端持续推送增量文本（如 OpenAI 协议返回 `delta.content`，DashScope 返回 `output.text` 增量），开发者可逐块渲染、实时朗读或流式写入日志。

- **实时多模态 API（Omni Realtime / Realtime API）**：  
  流式是默认且核心能力。WebSocket 或 AOQ 连接建立后，服务端通过结构化事件（如 `response.text.delta`、`response.audio.delta`）持续推送文本片段和 PCM 音频帧，支持低延迟语音合成与实时打断。`smooth_output` 参数可进一步优化音频流连续性。

- **视觉与嵌入类 API**：  
  `qwen-vl-plus` 和 `qvq` 等视觉模型在 [OpenAI 兼容接口](openai-compatible-interface.md)中**仅支持流式输出**（不可关闭）；Embedding 和重排序类接口则**不支持流式**，始终为同步响应。

- **批量与异步任务**：  
  Batch 文件处理、Tripo 3D 异步生成等**不支持流式输出**，需轮询任务状态获取最终结果。

> ⚠️ 注意：不同协议的流式 chunk 结构不兼容——OpenAI 接口用 `delta`，DashScope 用 `output.text`，Omni Realtime 用 `response.text.delta` 事件。解析逻辑不可混用。

## 关键参数和配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stream` | boolean | `false` | 全局开关，设为 `true` 启用流式响应。所有文本生成类接口均支持。 |
| `stream_options.include_usage` | boolean | `false` | 仅 [OpenAI 兼容接口](openai-compatible-interface.md)支持；设为 `true` 可在流式结束的 final chunk 中返回 `usage` 字段（含 `prompt_tokens`/`completion_tokens`）。 |
| `smooth_output` | boolean / null | `null` | Omni Realtime 特有参数，仅 `qwen3.5-omni-flash-realtime` 等模型生效，用于平滑音频流输出节奏，减少卡顿。 |

- **认证与传输要求**：  
  - 流式请求必须使用 `Authorization: Bearer <API_KEY>`（HTTP）或 `X-DashScope-Authentication-Token`（DashScope 原生）；  
  - WebSocket/AOQ/QUIC 等实时协议天然适配流式，HTTP 流式需保持连接（`Transfer-Encoding: chunked`），客户端须正确处理分块响应。

## 面向开发者，简洁实用

- ✅ **推荐开启场景**：聊天界面实时打字效果、语音助手 TTS 播放、长文档摘要渐进展示、代码补全预览。  
- ❌ **避免开启场景**：需要完整响应做校验/缓存的批处理、[Token](token.md) 统计强依赖的计费逻辑（应改用 `stream_options.include_usage`）。  
- 🛠️ **调试技巧**：  
  - 使用 `curl -N` 或 SDK 的 `stream=True` 选项发起请求；  
  - 监听 `data:` 行（HTTP SSE）或 `message` 事件（WebSocket），忽略空行和注释；  
  - 对 `final chunk`（含 `"finish_reason": "stop"` 或 `"done"`）做收尾处理（如关闭 loading 动画、触发回调）。  
- 📏 **性能提示**：流式不降低单 token 生成延迟，但大幅改善首字节时间（TTFB）和用户感知延迟；高并发下注意连接池管理与超时设置（建议 ≥60 秒）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model experience](../guides/model-experience.md)


