# omni realtime api

Qwen-Omni-Realtime API 是一个基于 WebSocket 的实时[多模态](../concepts/multimodal.md)交互接口，支持语音输入、文本/音频输出、VAD 自动检测、工具调用与联网搜索（部分模型），适用于智能客服、虚拟助手等低延迟对话场景。其核心是双向流式通信：客户端通过事件驱动方式发送音频、图像和控制指令，服务端以结构化事件流实时返回转录、响应内容、音频流及状态通知。

## 支持的模型/功能

- **模型系列**：当前支持 `qwen3.5-omni-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime` 和 `qwen-omni-turbo-realtime` 等系列。各模型在音色默认值、VAD 类型支持、参数可调性上存在差异（详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- **[多模态](../concepts/multimodal.md)输入**：支持 PCM 音频（16 kHz）和 JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256 KB），图像需在首次 `input_audio_buffer.append` 后发送。
- **[多模态](../concepts/multimodal.md)输出**：支持 `["text"]` 或 `["text", "audio"]` 输出模态；音频输出固定为 24 kHz PCM。
- **语音活动检测（VAD）**：提供 `server_vad`（所有模型）和 `semantic_vad`（仅 `qwen3.5-omni-realtime` 系列支持）两种模式，用于自动识别语音起止。
- **高级能力**：
  - 工具调用（`tools`）：仅 `qwen3.5-omni-realtime` 系列支持，需定义 `function` 结构并处理 `conversation.item.create` 回传。
  - 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，与 `tools` 互斥。
  - 声音复刻集成：通过 `qwen-voice-enrollment` 创建音色后，在 `session.update` 中指定 `voice` 参数即可使用（参见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）。
  > **注意**：文档 1 与文档 2 对 `semantic_vad` 的支持范围描述一致，但文档 3 和文档 4 的 SDK 示例中未体现该能力，实际使用前请以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中的模型兼容性说明为准。

## 关键参数

所有可配置参数均通过 `session.update` 客户端事件或 SDK 的 `update_session` 方法设置，服务端在 `session.updated` 事件中返回最终生效值。

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `modalities` | `array` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` | `string` | 音色名称，需与所选模型默认音色列表匹配 | `qwen3.5`: `"Tina"`；`qwen3-flash`: `"Cherry"`；`turbo`: `"Chelsie"` |
| `input_audio_format` / `output_audio_format` | `string` | 固定为 `"pcm"`；输入要求 16 kHz，输出为 24 kHz | 不可修改 |
| `instructions` | `string` | 系统角色提示词，影响模型行为 | — |
| `turn_detection.type` | `string` | VAD 类型：`"server_vad"`（默认）或 `"semantic_vad"`（仅 `qwen3.5-omni-realtime`） | `"server_vad"` |
| `turn_detection.threshold` | `float` | VAD 灵敏度，范围 `[-1.0, 1.0]` | `0.5` |
| `turn_detection.silence_duration_ms` | `integer` | 静音触发阈值，范围 `[200, 6000]` ms | `800` |
| `turn_detection.idle_timeout_ms` | `integer` | 静默超时引导响应，仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 生效，范围 `[5000, 30000]` | — |
| `smooth_output` | `boolean/null` | 仅 `qwen3-omni-flash-realtime` 支持：`true`（口语化）、`false`（书面化）、`null`（自动） | `true` |
| `temperature` / `top_p` / `top_k` | `float`/`float`/`integer` | 生成多样性控制参数；**二者择一设置**；`qwen-omni-turbo` 系列不可修改 | 见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 表格 |
| `max_tokens` | `integer` | 最大输出 token 数，超长则截断 | 模型最大输出长度 |
| `repetition_penalty` / `presence_penalty` | `float` | 重复惩罚参数；`qwen-omni-turbo` 系列不可修改 | 见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 表格 |
| `seed` | `integer` | 确定性种子，范围 `[0, 2^31-1]`，`-1` 表示随机 | `-1` |
| `enable_search` | `boolean` | 仅 `qwen3.5-omni-realtime` 支持；启用后模型可自主搜索 | `false` |
| `search_options.enable_source` | `boolean` | 是否返回搜索来源 | `false` |
| `tools` | `array` | 工具定义列表；与 `enable_search` 互斥；仅 `qwen3.5-omni-realtime` 支持 | `[]` |

> **注意**：文档 1 明确指出 `tools` 和 `enable_search` 不兼容，但文档 2 的 `session.updated` 示例中同时设置了二者，属于矛盾信息。实际使用时应严格遵循 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 的互斥约束。

## 使用方式

1. **建立连接**：使用 WebSocket 连接到地域专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 提供封装好的 `connect()` 方法。
2. **初始化会话**：连接后服务端立即返回 `session.created` 事件；随后调用 `update_session()` 发送 `session.update` 事件配置参数。
3. **输入数据**：
   - **音频**：持续调用 `append_audio()`（SDK）或发送 `input_audio_buffer.append` 事件；VAD 模式下由服务端自动提交，Manual 模式下需显式调用 `commit()` 或发送 `input_audio_buffer.commit`。
   - **图像**：调用 `append_video()`（SDK）或发送 `input_image_buffer.append`；须在音频缓冲区非空后发送，且与音频一同提交。
4. **触发响应**：
   - VAD 模式：服务端检测到 `speech_stopped` 后自动触发响应，无需客户端干预。
   - Manual 模式：客户端在 `commit()` 后需显式调用 `create_response()` 或发送 `response.create` 事件。
5. **处理工具调用**：当收到 `conversation.item.created` 类型为 `function_call` 的事件时，执行本地工具，再通过 `create_item()` 或 `conversation.item.create` 回传结果，最后（Manual 模式下）再次调用 `create_response()`。
6. **接收输出**：监听 `response.content_part.added`（文本）、`response.audio.delta`（音频流）、`response.audio_transcript.done`（ASR 结果）等事件。

## 限制和注意事项

- **域名迁移**：强烈建议使用业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低（参见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 文档）。
- **音频格式**：输入必须为 16 kHz PCM，输出固定为 24 kHz PCM；不支持自定义采样率或编码格式。
- **图像限制**：单图 Base64 编码后 ≤256 KB，建议原始大小 ≤190 KB；格式限 JPG/JPEG；分辨率建议 480p/720p，最高 1080p；发送频率建议 ≤1 张/秒。
- **参数兼容性**：`qwen-omni-turbo` 系列模型**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty` 和 `seed`，尝试设置将被忽略。
- **VAD 模式依赖**：`input_audio_buffer.speech_started`/`stopped` 事件仅在 `turn_detection.type` 非 `null` 时触发；Manual 模式下这些事件不会出现。
- **错误处理**：服务端通过 `error` 事件返回结构化错误（如 `invalid_request_error`），需检查 `error.param` 字段定位问题参数（参见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


