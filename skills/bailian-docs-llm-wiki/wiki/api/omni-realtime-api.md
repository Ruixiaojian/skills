# omni realtime api

Qwen-Omni-Realtime API 是一个低延迟、多模态的实时对话接口，支持语音输入/输出、文本交互、工具调用与联网搜索（部分模型），基于 WebSocket 协议提供流式事件响应。其核心设计围绕服务端事件驱动模型，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态与数据流。

## 支持的模型与功能

- **支持模型**：`qwen3.5-omni-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`。各模型能力存在差异，需注意兼容性限制。
- **多模态输入**：支持 PCM 音频（16 kHz）和 JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256 KB）。图像需在首次音频追加后发送 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **多模态输出**：支持 `["text"]` 或 `["text", "audio"]` 输出模态；音频输出固定为 24 kHz PCM，不可自定义采样率 [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)。
- **语音活动检测（VAD）**：提供 `server_vad`（默认）与 `semantic_vad`（仅 `qwen3.5-omni-realtime` 系列支持）两种模式，用于自动识别语音起止 [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
- **高级功能**：
  - 工具调用（Function Calling）：支持定义 `function` 类型工具，模型自主触发并返回参数；客户端回传结果后触发后续响应。
  - 联网搜索（`enable_search`）：**仅 `qwen3.5-omni-realtime` 系列模型支持**，且与 `tools` 不兼容，不可同时启用 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
  - 实时语音转录：内置 `qwen3-asr-flash-realtime` 模型，不可替换，支持增量（`delta`）与完成（`completed`）事件。

> **注意**：文档 1 中 `session.created` 示例显示 `model: "qwen3-omni-flash-realtime"`，而文档 2 的 `voice` 默认值说明中称该模型默认音色为 `"Cherry"`；但文档 4 的 Python SDK 文档明确列出 `Qwen3-Omni-Flash-Realtime` 对应 `"Cherry"`，与文档 1 一致。文档 5 Java SDK 中却将 `Qwen3-Omni-Flash-Realtime` 默认音色写作“Cherry”，但拼写为“Cherry”，属笔误，以文档 1 和 4 为准。

## 关键参数

| 参数 | 类型 | 说明 | 默认值 / 取值范围 | 生效模型 |
|------|------|------|-------------------|----------|
| `modalities` | `array` | 输出模态，`["text"]` 或 `["text","audio"]` | `["text","audio"]` | 全系列 |
| `voice` | `string` | 合成音色 | `qwen3.5`: `"Tina"`; `qwen3-omni-flash`: `"Cherry"`; `qwen-omni-turbo`: `"Chelsie"` | 全系列 |
| `turn_detection.type` | `string` | VAD 类型 | `"server_vad"` | `qwen3.5-omni-realtime` 支持 `semantic_vad` |
| `turn_detection.threshold` | `float` | VAD 灵敏度 | `[-1.0, 1.0]`, 默认 `0.5` | 全系列 |
| `turn_detection.silence_duration_ms` | `int` | 语音结束静音阈值 | `[200, 6000]`, 默认 `800` | 全系列 |
| `turn_detection.idle_timeout_ms` | `int` | 静默超时（主动引导） | `[5000, 30000]`, **仅 `qwen3.5-omni-plus/flash-realtime` + `server_vad`** | 限定模型 |
| `enable_search` | `boolean` | 启用联网搜索 | `false` | **仅 `qwen3.5-omni-realtime` 系列** |
| `tools` | `array` | 工具定义列表 | — | **仅 `qwen3.5-omni-realtime` 系列** |
| `temperature` / `top_p` | `float` | 生成多样性控制（二选一） | `qwen3.5`: `0.7`/`0.8`; `qwen3-flash`: `0.9`/`1.0`; `qwen-turbo`: `1.0`/`0.01` | `qwen-turbo` 不可修改 |
| `max_tokens` | `int` | 最大输出 token 数 | 模型最大长度 | `qwen-turbo` 不可修改 |
| `repetition_penalty` | `float` | 重复惩罚 | `qwen3.5`: `1.0`; 其他: `1.05` | `qwen-turbo` 不可修改 |
| `presence_penalty` | `float` | 存在惩罚 | `qwen3.5`: `1.5`; 其他: `0.0` | `qwen-turbo` 不可修改 |
| `seed` | `int` | 随机种子 | `-1`（随机） | `qwen-turbo` 不可修改 |

> **注意**：`smooth_output` 参数仅对 `qwen3-omni-flash-realtime` 系列生效，控制回复风格（口语化/书面化），但文档 1 的 `session.updated` 示例未包含该字段，而文档 2 和 4 明确将其列为客户端可配置项，表明其属于 `session.update` 请求体的一部分，而非服务端返回的 `session` 对象字段。

## 使用方式

1. **建立连接**：使用 WebSocket 连接到地域专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），[原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
2. **初始化会话**：连接后，服务端立即返回 `session.created` 事件，含初始配置；客户端可立即发送 `session.update` 事件调整参数。
3. **输入处理**：
   - **VAD 模式**（默认）：持续发送 `input_audio_buffer.append`；服务端自动检测 `speech_started`/`speech_stopped` 并提交缓冲区，无需客户端调用 `commit`。
   - **Manual 模式**：发送 `input_audio_buffer.append` 后，**必须**显式发送 `input_audio_buffer.commit` 创建用户消息项；再发送 `response.create` 触发响应 [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
4. **工具调用**：当服务端返回 `conversation.item.created` 且 `type: "function_call"` 时，客户端执行工具，然后发送 `conversation.item.create`（`type: "function_call_output"`）回传结果，最后发送 `response.create` 生成最终响应。
5. **响应消费**：监听 `response.*` 事件（如 `response.audio.delta`, `response.text.delta`, `response.done`）获取[流式输出](../concepts/streaming-output.md)。

## 限制和注意事项

- **音频格式硬性要求**：输入必须为 16 kHz PCM，输出固定为 24 kHz PCM；不支持 MP3、WAV 等其他格式 [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)。
- **并发与资源**：单次连接仅支持一个会话；音频缓冲区最大 15 MiB；图像建议 1 张/秒，单图 Base64 ≤256 KB。
- **功能互斥**：`tools` 与 `enable_search` 不可同时启用，否则服务端返回错误。
- **模型能力边界**：`qwen-omni-turbo-realtime` 系列**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等参数，这些字段在请求中设置将被忽略。
- **错误处理**：所有错误均以 `error` 事件返回，含 `type`、`code`、`message` 和 `param`，需在客户端统一捕获处理 [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)。
- **SDK 差异**：Python SDK 的 `update_session` 方法直接接受参数，而 Java SDK 要求通过 `OmniRealtimeConfig.builder().parameters(Map.of(...))` 设置 `temperature` 等高级参数，使用时需注意 API 形式差异。

## 来源文档

- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)


