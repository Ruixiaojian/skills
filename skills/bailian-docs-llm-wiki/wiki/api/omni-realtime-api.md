# omni realtime api

Qwen-Omni-Realtime API 是一个基于 WebSocket 的实时多模态交互接口，支持语音输入、文本/音频输出、工具调用与联网搜索（部分模型），适用于智能对话、语音助手等低延迟场景。其核心是服务端事件驱动模型，客户端通过发送标准事件（如 `session.update`、`input_audio_buffer.append`）控制会话流程，并接收服务端推送的结构化事件流（如 `session.created`、`conversation.item.input_audio_transcription.delta`）。

## 支持的模型/功能

- **主流模型系列**：`qwen3.5-omni-realtime`（含 `plus`/`flash` 变体）、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`。各模型能力存在差异，需按需选型。
- **多模态输入**：支持 PCM 音频（16 kHz）和 JPG/JPEG 图像（≤1080p，Base64 编码）。图像需在首次音频追加后发送，且与音频缓冲区共用 `commit` 操作 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **多模态输出**：支持 `["text"]` 或 `["text", "audio"]` 输出模态组合；音频输出固定为 24 kHz PCM [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)。
- **语音活动检测（VAD）**：提供 `server_vad`（声学检测）和 `semantic_vad`（语义检测）两种模式，后者仅 `qwen3.5-omni-realtime` 系列支持 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **高级功能**：
  - 工具调用（Function Calling）：通过 `tools` 参数定义函数，模型自主触发并返回参数，客户端执行后回传结果。
  - 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 互斥，不可同时启用。
  - 声音复刻：需先调用独立声音复刻 API 创建音色，再在 `voice` 参数中指定该音色 ID 使用（详见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）。

> **注意**：文档 2 和文档 3 中关于 `qwen-omni-turbo-realtime` 系列模型的 `temperature`、`top_p`、`top_k` 等参数均明确标注“**不支持修改**”，但文档 1 的 `session.updated` 示例中却包含了这些字段。实际使用时应以客户端事件文档为准，`qwen-omni-turbo-realtime` 的采样参数为只读。

## 关键参数

所有可配置参数均通过 `session.update` 客户端事件或 SDK 的 `update_session` 方法设置，服务端响应 `session.updated` 事件确认生效。

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `modalities` | `array` | 输出模态，`["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` | `string` | 音色名称 | `qwen3.5`: `"Tina"`；`qwen3-omni-flash`: `"Cherry"`；`qwen-omni-turbo`: `"Chelsie"` |
| `instructions` | `string` | 系统角色指令 | — |
| `turn_detection.type` | `string` | VAD 类型 | `"server_vad"` |
| `turn_detection.threshold` | `float` | VAD 灵敏度 | `[-1.0, 1.0]`，默认 `0.5` |
| `turn_detection.silence_duration_ms` | `int` | 静音触发阈值 | `[200, 6000]` ms，默认 `800` |
| `turn_detection.idle_timeout_ms` | `int` | 静默超时（仅 `qwen3.5-omni-plus/flash` + `server_vad`） | `[5000, 30000]` ms |
| `enable_search` | `boolean` | 启用联网搜索（仅 `qwen3.5-omni-realtime`） | `false` |
| `tools` | `array` | 工具定义列表（仅 `qwen3.5-omni-realtime`） | — |
| `temperature` / `top_p` | `float` | 控制生成多样性（二选一） | 各模型默认值不同，`qwen-omni-turbo` 不可修改 |
| `max_tokens` | `int` | 最大输出 token 数（截断，不影响生成过程） | 模型最大长度 |

> **注意**：`smooth_output` 参数仅对 `qwen3-omni-flash-realtime` 系列有效，用于切换口语化/书面化回复风格；其他模型忽略此参数。

## 使用方式

1. **建立连接**：使用 WebSocket URL（推荐业务空间专属域名，如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`）建立长连接。
2. **初始化会话**：连接后，服务端立即推送 `session.created` 事件，包含默认配置。
3. **配置会话（可选）**：发送 `session.update` 事件调整参数（如 `voice`、`tools`、`turn_detection` 等）。
4. **输入数据**：
   - **音频**：持续发送 `input_audio_buffer.append`（Base64 PCM 数据）。
   - **图像**：发送 `input_image_buffer.append`（Base64 JPG/JPEG）。
5. **触发响应**：
   - **VAD 模式**（默认）：服务端自动检测语音起止，无需客户端主动提交；检测到 `speech_stopped` 后自动 `commit` 并生成响应。
   - **Manual 模式**：客户端发送 `input_audio_buffer.commit` 提交音频，再发送 `response.create` 显式触发响应 [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
6. **处理响应**：监听服务端事件流，如 `conversation.item.created`（新消息项）、`response.audio.delta`（流式音频）、`conversation.item.input_audio_transcription.delta`（实时转录预览）等。

## 限制和注意事项

- **音频格式**：输入必须为 16 kHz PCM，输出固定为 24 kHz PCM；不支持自定义采样率或编码格式。
- **图像限制**：单图 Base64 编码后 ≤ 256 KB，建议原始大小 ≤ 190 KB；格式仅限 JPG/JPEG；分辨率建议 480p/720p，上限 1080p。
- **并发与配额**：受百炼平台配额限制，具体请查阅控制台。
- **工具与搜索互斥**：`tools` 和 `enable_search` 不可同时启用，否则服务端返回 `invalid_request_error`。
- **SDK 兼容性**：Python SDK 要求 ≥ v1.25.17，Java SDK 要求 ≥ v2.22.15。
- **错误处理**：所有错误均以 `error` 事件形式返回，包含 `type`、`code`、`message` 和 `param` 字段，便于精准定位问题 [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 来源文档

- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


