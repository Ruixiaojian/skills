# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的低延迟、多模态实时交互接口，支持语音输入/输出、文本生成、图像理解及工具调用等能力。它采用事件驱动模型，客户端通过发送结构化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态与数据流，服务端通过异步事件（如 `input_audio_buffer.speech_started`、`response.audio.delta`）实时反馈处理进展。该 API 专为语音助手、智能客服、实时音视频交互等场景设计。

## 支持的模型/功能

当前支持以下实时系列模型，各模型能力与默认参数存在差异：

- `qwen3.5-omni-plus-realtime`：支持 `semantic_vad`、联网搜索（`enable_search`）、自定义音频 I/O 格式（`audio.input.format` / `audio.output.format`）及静默超时（`idle_timeout_ms`）。
- `qwen3.5-omni-flash-realtime`：支持 `server_vad`、`smooth_output` 口语化控制、自定义音频 I/O 格式及静默超时；默认音色为 `Cherry`。
- `qwen-omni-turbo-realtime`：仅支持基础 `server_vad`，**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty` 和 `seed` 等采样参数；默认音色为 `Chelsie`。

核心功能包括：
- **多模态输入**：实时音频流（PCM/WAV）、图像（JPG/JPEG，≤1080p，Base64 编码后 ≤256KB）、文本指令（`instructions`）。
- **多模态输出**：文本（`text`）、音频（PCM/WAV，采样率 8k/16k/24k/48k Hz），可独立或组合启用（`modalities: ["text"]` 或 `["text","audio"]`）。
- **语音活动检测（VAD）**：提供 `server_vad`（声学特征）和 `semantic_vad`（语义有效性）两种模式，后者仅 `qwen3.5-omni-plus-realtime` 支持。
- **工具调用（Function Calling）**：模型可自主触发预定义函数，客户端需回传结果并显式调用 `response.create` 触发最终响应。
- **联网搜索（Search）**：仅 `qwen3.5-omni-plus-realtime` 支持，通过 `enable_search: true` 启用，与 `tools` 不兼容。
- **声音复刻集成**：支持将复刻音色（`voice`）作为 `session.update` 的参数传入，用于定制化语音输出 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：文档 1 中称 `qwen3.5-omni-plus-realtime` 支持 `enable_search`，但文档 2 和文档 4 明确指出该功能“**仅在使用 Qwen3.5-Omni-Realtime 系列模型时生效**”，而 `qwen3.5-omni-plus-realtime` 属于该系列，此处无矛盾；但文档 1 示例中 `model` 字段值为 `qwen3.5-omni-flash-realtime`，却配置了 `enable_search: true`，这与“仅 Qwen3.5-Omni-Realtime 系列支持”的约束直接冲突。因此，该示例配置为**错误示例**，实际使用时需确保 `enable_search` 仅与 `qwen3.5-omni-plus-realtime` 搭配。

## 关键参数

所有会话级配置均通过 `session.update` 事件（或 SDK 的 `update_session` 方法）设置，主要参数如下：

| 参数 | 类型 | 说明 | 适用模型 | 默认值 |
|------|------|------|----------|--------|
| `modalities` | `array` | 输出模态，`["text"]` 或 `["text","audio"]` | 全部 | `["text","audio"]` |
| `voice` | `string` | 音色名称 | 全部 | `Tina` (qwen3.5), `Cherry` (flash), `Chelsie` (turbo) |
| `audio.input.format.type` / `.sample_rate` | `string` / `integer` | 输入音频格式（`pcm`/`wav`）与采样率（8k/16k/24k/48k Hz） | `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime` | `pcm`, `16000` |
| `audio.output.format.type` / `.sample_rate` | `string` / `integer` | 输出音频格式（`pcm`/`wav`）与采样率（8k/16k/24k/48k Hz） | `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime` | `pcm`, `24000` |
| `turn_detection.type` | `string` | VAD 类型：`server_vad` 或 `semantic_vad` | `qwen3.5-omni-plus-realtime`（全支持），`qwen3.5-omni-flash-realtime`（仅 `server_vad`） | `server_vad` |
| `turn_detection.threshold` | `float` | VAD 灵敏度（-1.0 ~ 1.0） | 全部 | `0.5` |
| `turn_detection.silence_duration_ms` | `integer` | 静音触发响应时长（200 ~ 6000 ms） | 全部 | `800` |
| `turn_detection.idle_timeout_ms` | `integer` | 静默超时主动引导（5000 ~ 30000 ms） | `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`（`server_vad` 模式下） | — |
| `enable_search` | `boolean` | 启用联网搜索 | `qwen3.5-omni-plus-realtime` | `false` |
| `tools` | `array` | 工具定义列表 | `qwen3.5-omni-plus-realtime` | `[]` |
| `temperature` / `top_p` / `top_k` | `float` / `float` / `integer` | 采样控制参数（三选一即可） | `qwen3.5-omni-plus-realtime`（全支持），`qwen3.5-omni-flash-realtime`（全支持），`qwen-omni-turbo-realtime`（**不支持修改**） | 见各模型说明 |
| `max_tokens` | `integer` | 响应最大 [Token](../concepts/token.md) 数（截断，不影响生成过程） | `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime` | 模型最大输出长度 |
| `repetition_penalty` / `presence_penalty` | `float` | 重复惩罚参数 | `qwen3.5-omni-plus-realtime`（全支持），`qwen3.5-omni-flash-realtime`（全支持），`qwen-omni-turbo-realtime`（**不支持修改**） | 见各模型说明 |
| `seed` | `integer` | 随机种子（提升确定性） | `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime` | `-1` |

> **注意**：文档 3 的 `session.created` 事件示例中，`input_audio_format` 和 `output_audio_format` 字段值均为 `"pcm"`，且明确说明“当前仅支持设为`pcm`”、“当前不支持自定义输出采样率”。这与文档 1 和文档 2 中详述的 `audio.input.format` / `audio.output.format` 嵌套结构及对 `wav` 格式和多种采样率的支持存在明显矛盾。经交叉验证，文档 1 和文档 2 为最新、最完整的参数说明，文档 3 的描述已**过时**，应以嵌套结构 `audio.*.format` 为准 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 使用方式

1. **建立连接**：使用 WebSocket 客户端连接至地域专属域名（推荐），例如北京地域：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime` [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
2. **初始化会话**：连接后，服务端立即返回 `session.created` 事件。随后，客户端应尽快发送 `session.update` 事件（或调用 SDK 的 `update_session`）配置 `modalities`、`voice`、`turn_detection` 等核心参数。
3. **输入数据**：
   - **音频**：持续发送 `input_audio_buffer.append`（Base64 编码 PCM/WAV 数据）。在 `server_vad` 模式下，服务端自动检测语音起止并提交；在 `Manual` 模式下，客户端需在说完后发送 `input_audio_buffer.commit`。
   - **图像**：发送 `input_image_buffer.append`（Base64 编码 JPG/JPEG），需在首次音频追加后发送；图像与音频缓冲区由同一 `commit` 事件提交。
4. **触发响应**：
   - `server_vad` 模式：服务端检测到语音结束即自动触发响应，无需客户端干预。
   - `Manual` 模式：客户端在 `commit` 后，必须发送 `response.create` 事件显式请求响应。
5. **处理工具调用**：若服务端返回 `conversation.item.created` 且 `item.type == "function_call"`，客户端执行对应函数，并通过 `conversation.item.create` 回传结果，再发送 `response.create` 获取最终响应。
6. **流式消费输出**：监听 `response.text.delta`、`response.audio.delta`、`response.audio_transcript.delta` 等事件，实时获取文本、音频和转录结果。

## 限制和注意事项

- **VAD 模式 vs Manual 模式**：`server_vad` 是默认模式，适用于连续语音流；`Manual` 模式（`turn_detection: null`）适用于按键说话等离散输入场景，此时 `input_audio_buffer.commit` 和 `response.create` 为必需步骤 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
- **参数互斥性**：`tools` 和 `enable_search` 不可同时启用，否则服务端将返回错误。
- **音频格式兼容性**：输入音频要求为单声道、16-bit PCM 或 WAV；输出音频支持 PCM/WAV，但部分旧版客户端事件（如 `input_audio_format`）仅回显 `pcm`，应优先使用新式 `audio.*.format` 结构。
- **性能与稳定性**：强烈建议使用业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），其性能和稳定性优于通用域名 `wss://dashscope.aliyuncs.com` [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
- **SDK 版本要求**：Python SDK ≥ 1.26.5，Java SDK ≥ v2.22.15，以确保支持全部功能。
- **图像限制**：单张图片 Base64 编码后 ≤256KB，建议原始大小 ≤190KB；分辨率建议 480p/720p，最高 1080p；发送频率建议 ≤1 张/秒。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


