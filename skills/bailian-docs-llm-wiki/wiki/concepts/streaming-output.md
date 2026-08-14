# 流式输出

流式输出（Streaming Output）是指模型响应以增量方式分块（chunk）持续返回，而非等待完整结果一次性返回。它适用于实时对话、语音合成、长文本生成等对延迟敏感的场景，可显著降低首字延迟（Time to First [Token](token.md), TTFT）并提升用户体验。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中存在两类独立实现机制，需根据接入方式选择对应配置：

- **Realtime API（AOQ/WebSocket/WebRTC）**：  
  所有支持音频/文本输出的实时模型（如 `qwen3.5-omni-plus-realtime`、`Fun-ASR-Realtime`、`CosyVoice` 等）**默认启用流式输出**，无需显式开关。响应通过协议原生通道（如 WebSocket message、AOQ data track 或 WebRTC DataChannel）以事件形式持续推送，例如：
  - `text.delta` 事件：返回新增文本片段；
  - `audio.delta` 事件：返回 PCM 音频帧（按 `audio.output.format.sample_rate` 切片）；
  - `session.updated` 后即开始流式输出，开发者需注册对应事件监听器实时消费。

- **Application / Assistant API（非实时 HTTP 接口）**：  
  需**显式启用**流式能力，通过请求参数控制：
  - `stream=True`：启用流式响应（HTTP chunked transfer encoding）；
  - `incremental_output=True`：启用增量式语义分块（如按句子/标点切分），避免单字或乱序输出；  
  二者需同时设置才生效。响应体为 `text/event-stream` 格式，每行以 `data:` 开头，前端需用 `EventSource` 或手动解析 chunk。

> ⚠️ 注意：Realtime API 与 Application API 的流式机制互不兼容——Realtime 不接受 `stream` 参数，Application 不支持 `audio.delta` 等实时事件。

## 关键参数和配置

| 场景 | 参数名 | 类型 | 说明 | 必填 |
|------|--------|------|------|------|
| **Application API** | `stream` | `bool` | 启用 HTTP 流式传输 | 是（若需流式） |
| | `incremental_output` | `bool` | 启用语义级增量分块（推荐开启） | 是（若需可控分块） |
| **Realtime API（WebSocket/AOQ）** | `modalities` | `string[]` | 指定输出模态，如 `["text", "audio"]` | 是 |
| | `audio.output.format.type` | `string` | 输出编码格式：`"pcm"`（推荐）、`"wav"` | 否（默认 `"pcm"`） |
| | `audio.output.format.sample_rate` | `int` | 输出采样率：`8000`/`16000`/`24000`（默认）/`48000` | 否 |
| | `turn_detection.type` | `string` | VAD 类型（影响音频流断句时机）：`"server_vad"`（默认）或 `"semantic_vad"`（仅 Omni 3.5+） | 否 |

- Realtime API 中，`audio.delta` 和 `text.delta` 事件天然按模型生成节奏推送，无需额外参数控制“是否流式”，但可通过 `turn_detection` 调整音频流的语义断点。
- Application API 中，`incremental_output=True` 可确保文本按自然语言单位（如句号、换行）分块，避免 `stream=True` 单独使用时出现碎片化输出（如单字、半词）。

## 面向开发者的实践建议

- ✅ **优先选用 Realtime API 实现真流式**：语音助手、实时翻译等场景必须用 AOQ/WebSocket，其端到端延迟更低、音频/文本同步性更好。
- ✅ **Application 流式仅用于轻量文本交互**：如客服机器人网页端，配合 `incremental_output=True` + 前端 `EventSource` 即可快速实现打字机效果。
- ❌ **勿混用参数**：在 Realtime 请求中传 `stream=True` 将被忽略；在 Application 请求中设 `modalities` 会报错。
- 🛠️ **调试技巧**：  
  - Realtime：监听 `text.delta` 和 `audio.delta` 事件日志，确认 chunk size 是否符合预期（如 PCM 每帧 20ms）；  
  - Application：用 `curl -N` 测试响应流，验证 `data:` 行是否连续、无空行。

## 关联主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application support](../guides/application-support.md)


