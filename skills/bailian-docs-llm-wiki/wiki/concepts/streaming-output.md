# 流式输出

流式输出（Streaming Output）是指模型在生成响应过程中，将结果以增量方式分块、实时返回给客户端，而非等待整个响应完成后再一次性返回。这种方式显著降低端到端延迟，提升用户体验，尤其适用于语音助手、实时对话、长文本生成等对响应速度敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中并非统一开关，而是按接入协议和模型能力分层支持，需结合具体接口显式启用：

- **Omni Realtime API（WebSocket）**：原生支持流式文本与音频输出。服务端通过 `text.delta` 和 `audio.delta` 事件持续推送增量内容（如逐字文本、连续 PCM 音频帧），无需额外参数；`modalities: ["text", "audio"]` 即默认启用双模态流式输出。
- **Qwen API（HTTP/OpenAI 兼容）**：需显式设置 `stream=True`（OpenAI 标准）或 `stream=true`（DashScope 原生）。支持文本 token 级别流式返回（`delta.content`），但**不支持 `delta.tool_calls` 结构**——工具调用结果始终在流结束时以完整 `tool_calls` 字段一次性返回。
- **Application Support（Assistant/Agent API）**：需**同时设置 `stream=True` 和 `incremental_output=True`** 才能启用真正的增量流式（即仅返回新增 token，非全量重传），否则 `stream=True` 仅返回标准 OpenAI-style delta 流（含重复历史）。
- **Vision API（Qwen-VL/QVQ）**：部分模型（如 QVQ）**仅支持流式输出**，必须设置 `stream=True`，否则请求将被拒绝。
- **Batch Chat / Files / Embedding 等异步或非交互接口**：**不支持流式输出**，仅提供最终结果。

> ⚠️ 注意：流式能力与模型强绑定。例如 `qwen-omni-turbo-realtime` 支持低延迟音频流，而 `qwen-turbo`（HTTP 文本模型）虽支持 `stream=True`，但无音频流能力；`qwen-vl` 在 OpenAI Vision 接口下支持流式，但在 DashScope 原生接口中不支持。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 备注 |
|------|------|------|----------|------|
| `stream` | `boolean` | 启用流式传输协议（HTTP chunked encoding / WebSocket event stream） | 是（流式场景） | 所有支持流式的接口均需设为 `true` |
| `incremental_output` | `boolean` | 启用增量式流式（仅返回本次新增内容） | 仅 Assistant/Agent API 需要 | 设为 `true` 可避免前端重复渲染；默认 `false` |
| `modalities` | `array<string>` | Omni Realtime 中指定输出模态，决定流式内容类型 | 是（Omni Realtime） | 必须包含 `"text"`；添加 `"audio"` 则启用音频流（24 kHz PCM） |
| `output_audio_format` | `string` | Omni Realtime 中固定为 `"pcm"`，不可更改 | — | 音频流格式已固化，无需配置采样率或编码 |

- **不推荐依赖的隐式行为**：  
  - 不要假设 `stream=True` 自动启用增量输出（仅 Assistant API 需配 `incremental_output`）；  
  - 不要尝试在不支持流式的接口（如 Completions、Embedding）中设置 `stream`，将导致 400 错误；  
  - `smooth_output`（Omni Realtime）影响音频流平滑度，但**不影响文本流行为**，属音频后处理参数，非流式开关。

## 面向开发者：简洁实用建议

- ✅ **首选 WebSocket 实时流**：对语音助手、实时客服等场景，直接使用 Omni Realtime API（`wss://.../realtime`），天然低延迟、双模态、事件驱动，无需手动解析 chunk。
- ✅ **HTTP 场景统一用 `stream=True`**：[OpenAI 兼容接口](openai-compatible-interface.md)（Chat Completions / Responses）和 DashScope 原生接口均支持，返回格式一致（`{"delta": {"content": "..."}}`）。
- ✅ **前端处理要点**：  
  - 监听 `data:` 行（HTTP）或 `message` 事件（WebSocket），拼接 `delta.content`；  
  - 检查 `finish_reason` 字段判断流是否结束（`"stop"` / `"length"` / `"tool_calls"`）；  
  - 对 Assistant API，务必检查 `incremental_output` 是否生效，避免重复渲染。
- ❌ **避免踩坑**：  
  - 不要在 `tools` 调用场景中期待 `delta.tool_calls` —— 工具参数始终在流末尾完整返回；  
  - 不要跨地域混用 `api_key` 和 `base_url`（如北京 key 调用新加坡 endpoint），会导致流式连接失败；  
  - `max_tokens` 仅控制截断长度，**不影响流式生成过程**，流仍会持续直到自然结束或超时。

流式输出是百炼平台实现“实时 AI”的基础设施能力。正确配置参数、匹配接口协议、理解各模型限制，即可高效构建响应迅捷、体验流畅的 AI 应用。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [model experience](../guides/model-experience.md)
- [application support](../guides/application-support.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


