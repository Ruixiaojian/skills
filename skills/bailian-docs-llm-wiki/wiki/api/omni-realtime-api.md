# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时多模态交互接口，支持语音输入、文本/音频输出、实时转录、工具调用与联网搜索（部分模型），适用于智能客服、语音助手等低延迟场景。其核心为事件驱动架构，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话，服务端以对应事件（如 `session.created`、`input_audio_buffer.speech_started`）响应。

## 支持的模型/功能

- **模型系列**：当前支持 `qwen3.5-omni-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime` 和 `qwen-omni-turbo-realtime` 等系列。不同模型在音色默认值、VAD 类型支持、参数可调性上存在差异（详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- **[多模态输入](../concepts/multimodal-input.md)**：支持 PCM 音频（16 kHz）和 JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256 KB）；图像需在首次 `input_audio_buffer.append` 后发送 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **多模态输出**：支持 `["text"]` 或 `["text", "audio"]` 输出模态；音频输出固定为 24 kHz PCM [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **语音活动检测（VAD）**：提供 `server_vad`（所有模型）和 `semantic_vad`（仅 `qwen3.5-omni-realtime` 系列）两种模式，用于自动识别语音起止 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
- **高级能力**：
  - 工具调用（`tools`）：仅 `qwen3.5-omni-realtime` 系列支持，需配置 `function` 定义。
  - 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，与 `tools` 互斥。
  - 声音复刻：需先调用 `qwen-voice-enrollment` 模型创建音色，并确保 `target_model` 与后续 Omni 实时调用模型一致 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：文档中 `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 在 `idle_timeout_ms` 支持描述上存在不一致——[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 明确限定该参数“仅在使用 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` 模型且 VAD 类型为 `server_vad` 时生效”，而 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 仅提及“仅在 `server_vad` 模式下……时返回”，未明确限定模型范围。以客户端文档为准。

## 关键参数

所有可配置参数均通过 `session.update` 事件或 SDK 的 `update_session` 方法设置，核心参数如下：

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `modalities` | `array` | 输出模态，`["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` | `string` | 音色名 | `qwen3.5`: `"Tina"`；`qwen3-flash`: `"Cherry"`；`turbo`: `"Chelsie"` |
| `input_audio_format` / `output_audio_format` | `string` | 固定为 `"pcm"`；输入采样率 16 kHz，输出 24 kHz | 不可修改 |
| `instructions` | `string` | 系统角色指令 | 无默认值 |
| `turn_detection.type` | `string` | `server_vad`（默认）或 `semantic_vad`（仅 qwen3.5） | `server_vad` |
| `turn_detection.threshold` | `float` | VAD 灵敏度，范围 `[-1.0, 1.0]` | `0.5` |
| `turn_detection.silence_duration_ms` | `integer` | 静音触发阈值，范围 `[200, 6000]` ms | `800` |
| `turn_detection.idle_timeout_ms` | `integer` | 静默超时引导，范围 `[5000, 30000]` ms | 仅 qwen3.5-plus/flash + server_vad 有效 |
| `temperature` / `top_p` / `top_k` | `float`/`float`/`integer` | 生成多样性控制，**二者择一设置** | 各模型默认值不同，`qwen-omni-turbo` 系列不可修改 |
| `max_tokens` | `integer` | 最大输出 token 数，超限则截断 | 模型最大输出长度 |
| `repetition_penalty` / `presence_penalty` | `float`/`float` | 重复度控制 | `qwen-omni-turbo` 系列不可修改 |
| `seed` | `integer` | 确定性种子 | `-1`（随机），`qwen-omni-turbo` 系列不可修改 |
| `smooth_output` | `boolean` | 仅 `qwen3-omni-flash-realtime` 支持，控制口语化程度 | `true`（口语化） |

> **注意**：`tools` 和 `enable_search` 互斥，不可同时启用 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 使用方式

1. **建立连接**：使用 WebSocket 连接到地域专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），推荐迁移至业务空间专属域名以获得更高稳定性 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
2. **初始化会话**：连接后服务端立即返回 `session.created` 事件；随后可发送 `session.update` 调整配置。
3. **输入处理**：
   - **VAD 模式**（默认）：持续发送 `input_audio_buffer.append`，服务端自动检测 `speech_started`/`speech_stopped` 并提交缓冲区。
   - **Manual 模式**：发送 `input_audio_buffer.append` 后，显式发送 `input_audio_buffer.commit` 创建用户消息项 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
4. **触发响应**：
   - VAD 模式下，服务端在语音结束后自动触发 `response.create`。
   - Manual 模式下，需客户端主动发送 `response.create`。
5. **工具调用**：当服务端返回 `conversation.item.created`（type=`function_call`）时，客户端执行工具并回传 `conversation.item.create`（type=`function_call_output`），再发送 `response.create` 触发最终响应 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。
6. **流式消费**：监听 `response.audio.delta`（音频）、`response.text.delta`（文本）、`response.audio_transcript.delta`（ASR 中间结果）等事件实现低延迟渲染。

## 限制和注意事项

- **音频格式**：输入必须为 16 kHz PCM 单声道；输出固定为 24 kHz PCM，不支持自定义采样率 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **图像限制**：仅支持 JPG/JPEG；单图 Base64 编码后 ≤256 KB；建议分辨率 480p/720p；需在音频之后发送 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **参数兼容性**：`qwen-omni-turbo` 系列模型**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **错误处理**：服务端返回 `error` 事件（含 `type`、`code`、`message`、`param`），需根据 `param` 字段定位问题，例如 `session.modalities` 校验失败 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。
- **SDK 注意事项**：Python/Java SDK 中 `smooth_output`、`instructions`、`temperature` 等参数需通过 `parameters` 字典传入 `update_session`，而非顶层字段 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


