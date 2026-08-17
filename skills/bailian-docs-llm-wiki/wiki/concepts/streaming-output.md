# 流式输出

流式输出（Streaming）是指模型响应以增量、分块的方式实时返回给客户端，而非等待整个响应生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户感知的响应速度，并支持实时渲染、语音合成、逐字高亮等交互体验。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准文本生成（Chat/Completions/Responses 接口）**：通过设置 `stream=true` 启用流式，服务端按 token 或语义单元（如句子）分批返回 `content` 字段；适用于聊天界面逐字显示、代码补全实时提示等场景。[OpenAI 兼容接口](openai-compatible-interface.md)统一支持该模式，但需注意：**[OpenAI 兼容接口](openai-compatible-interface.md)不支持流式解析 `delta.tool_calls`**，工具调用结果始终在最终块中以 `content` 形式返回；如需完整结构化工具流式（如 `delta.tool_calls[0].function.arguments`），请使用 DashScope 原生或 Anthropic Messages 接口。

- **实时[多模态](multi-modal.md)交互（Omni Realtime API）**：基于 WebSocket 的事件驱动流式是默认行为。服务端通过 `response.text.delta`、`response.audio.delta`、`conversation.item.created` 等事件持续推送文本片段、音频 PCM 数据块、工具调用请求等，天然适配低延迟语音助手、实时会议转录与合成等场景。无需额外参数开启，流式即协议核心。

- **语音识别（ASR）与语音合成（TTS）**：`qwen-audio-3.0-asr-flash-streaming` 和 `qwen-audio-3.0-tts-flash` 等模型专为流式设计。ASR 支持实时音频 buffer 追加（`input_audio_buffer.append`）并即时返回部分识别结果；TTS 支持边生成边下发音频流，配合 `smooth_output` 参数可优化口语自然度。

- **批量处理（Batch Chat）**：虽为异步任务，但单次 Batch Chat 请求本身**不支持流式响应**——其响应体为完整 JSON 结果数组。流式能力仅存在于单次请求的 *内部*（即模型生成过程对服务端透明），对外表现为同步完成。

- **视觉与[多模态](multi-modal.md)模型（Qwen-VL、QVQ）**：QVQ 模型**仅支持流式输出**（强制 `stream=true`），不可关闭；其他视觉模型（如 Qwen-VL）则同时支持流式与非流式，适用于图文理解结果逐步呈现。

## 关键参数和配置

- **通用开关**：
  - `stream`: `boolean`，必填。设为 `true` 启用流式；设为 `false`（或省略）为非流式。所有 Chat/Completions/Responses 接口均支持。
  - `stream_options`: `object`，可选。目前仅支持 `{"include_usage": true}`，用于在流式结束时的 `data: [DONE]` 块中附加 `usage` 字段（含 `prompt_tokens`、`completion_tokens`）。

- **Realtime API 特有控制**（通过 `session.update` 事件配置）：
  - `modalities`: 必须显式指定 `["text"]` 或 `["text","audio"]`，决定服务端推送哪些类型的数据流；
  - `audio.output.format.type` / `sample_rate`: 控制音频流格式（`pcm`/`wav`）与采样率（`24000` 或 `48000`），直接影响客户端解码逻辑；
  - `smooth_output`: `boolean`，仅 `qwen3-omni-flash-realtime` 支持，启用后文本流更口语化，利于 TTS 自然度。

- **注意事项**：
  - 流式响应的 HTTP 状态码始终为 `200 OK`，即使发生错误（如鉴权失败、模型不可用），错误信息也通过流式数据块中的 `error` 字段返回；
  - 客户端必须正确处理 `data:` 前缀、空行分隔、`[DONE]` 结束标识，并兼容可能的乱序或重复块（尤其在网络不稳定时）；
  - 流式不改变计费逻辑：按实际生成的 completion tokens 计费，与是否流式无关。

## 面向开发者，简洁实用

- ✅ **首选流式**：只要前端需要实时反馈（如打字效果、语音播报），一律启用 `stream=true`；
- ✅ **工具调用选型**：若需逐字解析工具参数，请避开 [OpenAI 兼容接口](openai-compatible-interface.md)，改用 DashScope 原生或 Anthropic Messages；
- ✅ **Realtime 场景**：直接使用 Omni Realtime API，流式即默认，专注处理 `response.*.delta` 事件即可；
- ⚠️ **不要硬编码 `stream_options`**：当前仅 `include_usage` 有效，其他字段将被忽略；
- ⚠️ **务必校验流式结束**：监听 `data: [DONE]` 行，而非依赖连接关闭——后者不可靠且可能丢数据；
- 🛠️ **调试建议**：用 `curl -N` 或 Postman 的 SSE 模式测试流式响应，避免浏览器缓存干扰。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [model experience](../guides/model-experience.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


