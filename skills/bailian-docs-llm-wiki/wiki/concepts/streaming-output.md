# 流式输出

流式输出（Streaming Output）是指模型在生成过程中，将结果以增量、分块的方式实时返回给客户端，而非等待全部内容生成完毕后一次性返回。这种机制显著降低端到端延迟，提升交互实时性，是语音助手、实时翻译、长文本生成等低延迟场景的核心能力。

## 在百炼平台的不同场景中如何使用

- **Realtime API（WebSocket/WebRTC/AOQ）**：  
  所有实时交互类模型（如 `qwen3.5-omni-realtime`、`qwen-audio-3.0-realtime-plus`）默认启用流式输出。服务端通过事件流（如 `response.text.delta`、`response.audio.delta`、`conversation.item.input_audio_transcription.delta`）持续推送文本片段或音频帧，客户端可即时渲染或播放，实现“边说边听、边生成边响应”。

- **Qwen 系列文本生成 API（OpenAI/Anthropic/DashScope 兼容接口）**：  
  通过设置 `stream: true` 参数启用流式响应。DashScope 原生接口返回 JSON Lines 格式（每行一个 JSON 对象），[OpenAI 兼容接口](openai-compatible-interface.md)返回 Server-Sent Events（SSE）格式（`data: {...}`）。适用于对话续写、代码补全、长文档摘要等需快速反馈的场景。

- **ASR/TTS 模型（如 `qwen-audio-3.0-asr-flash-streaming`、`cosyvoice-v3.5-plus`）**：  
  流式输出体现为实时语音识别结果（逐字/逐词转录）或合成音频流（PCM 分片），配合 VAD（语音活动检测）实现“说话即识别、生成即播放”的无缝体验。

- **多模态理解与生成（如 `qwen3.7-plus` 图文理解、`wan2.7-i2v` 视频生成）**：  
  当前主要支持非流式输出；但部分长视频生成任务可通过 `enable_thinking` + 结构化分步输出模拟类流式行为（如分阶段返回关键帧描述），严格意义上的流式视频帧输出暂未开放。

## 关键参数和配置

- **通用开关**：  
  - `stream: true`（所有 HTTP 类 API 必填）  
  - WebSocket Realtime API 中无需显式设置，流式为协议默认行为  

- **Realtime API 特有控制**：  
  - `smooth_output`: 仅 `qwen3-omni-flash-realtime` 支持，设为 `true` 可优化口语化文本流的连贯性（减少停顿词、增强语句衔接）  
  - `turn_detection.type`: 使用 `semantic_vad` 可提升流式响应与用户语音中断的协同精度，避免过早截断或延迟响应  

- **文本生成 API 参数影响流式体验**：  
  - `temperature` / `top_p`: 值越低，token 生成越确定，流式输出更稳定；过高可能导致首 token 延迟增加  
  - `max_tokens`: 不影响流式触发，但限制总长度；建议结合业务预期合理设置，避免无意义截断  
  - `enable_thinking`: 开启后流式输出包含推理步骤（`"type": "thinking"` 事件），便于前端展示思考过程  

- **注意事项**：  
  - `qwen-omni-turbo-realtime` 等轻量模型不支持调节 `temperature`/`top_p`，流式行为由模型固有策略决定  
  - WebSocket Realtime API 的 `modalities` 若设为 `["text"]`，则仅流式返回文本；设为 `["text","audio"]` 时，文本与音频 delta 事件并行推送，需分别处理  
  - [OpenAI 兼容接口](openai-compatible-interface.md)的流式响应中，`delta.content` 为空字符串表示 token 生成结束；DashScope 接口则通过 `"finish_reason": "stop"` 字段标识终止  

面向开发者：优先选用 WebSocket Realtime API 实现端到端流式交互；HTTP 类流式调用请务必处理好 SSE 或 JSON Lines 解析逻辑，并做好连接保活与错误重试。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [model experience](../guides/model-experience.md)
- [qwen api reference](../api/qwen-api-reference.md)


