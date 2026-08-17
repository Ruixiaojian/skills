# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时[多模态](../concepts/multi-modal.md)交互接口，支持语音输入、文本/音频输出、音视频理解及工具调用等能力。它采用事件驱动模型，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态，服务端通过异步事件流（如 `response.audio.delta`、`conversation.item.created`）实时反馈处理结果。该 API 专为低延迟、高保真语音交互场景设计，适用于智能客服、虚拟助手、实时会议等应用。

## 支持的模型/功能

- **核心模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen-omni-turbo-realtime`；其中 `qwen3.5-omni-realtime` 系列（含 `plus` 和 `flash`）支持语义 VAD、联网搜索和完整工具调用；`turbo` 系列仅支持基础语音交互，且多数参数不可修改 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **[多模态](../concepts/multi-modal.md)输入**：支持实时音频（PCM/WAV，采样率 8k–48k Hz）、图像（JPG/JPEG，≤1080p，Base64 编码后 ≤256KB）；图像需在首次音频追加后发送 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **[多模态](../concepts/multi-modal.md)输出**：支持 `["text"]` 或 `["text", "audio"]` 输出模态；音频输出格式支持 `pcm`/`wav`，采样率支持 8k–48k Hz（默认 24k Hz）。
- **高级功能**：
  - **语音活动检测（VAD）**：`server_vad`（声学）或 `semantic_vad`（语义，仅 `qwen3.5-omni-realtime` 系列支持）；
  - **工具调用（Function Calling）**：模型可自主触发预定义函数，客户端回传结果后继续生成响应；
  - **联网搜索（Enable Search）**：仅 `qwen3.5-omni-realtime` 系列支持，与 `tools` 互斥；
  - **声音复刻（Voice Cloning）**：需先调用独立的 `qwen-voice-enrollment` 模型创建音色，再在 `session.update` 中指定 `voice` 参数使用 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：文档 3（服务端事件）中明确指出 `output_audio_format` 当前“仅支持设为 `pcm`”，且“不支持自定义输出采样率”；但文档 1（客户端事件）和文档 2（Python SDK）均允许配置 `audio.output.format.sample_rate` 为 `24000`（默认）或 `48000`。此为平台实际能力与文档描述不一致，**以文档 1 和文档 2 的配置项为准，服务端已支持 24k/48k 输出采样率**。

## 关键参数

所有参数均通过 `session.update` 事件（或 SDK 的 `update_session` 方法）配置，作用于整个会话生命周期：

- **基础配置**：
  - `modalities`: 输出模态数组，仅限 `["text"]` 或 `["text","audio"]`；
  - `voice`: 音色名称，不同模型有默认值（`Tina`/`Cherry`/`Chelsie`），亦可填入声音复刻生成的自定义 `voice` ID；
  - `instructions`: 系统角色指令，用于设定模型行为边界。

- **音频配置**（适用模型：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`）：
  - `audio.input.format.type` / `sample_rate`: 输入格式（`pcm`/`wav`）与采样率（`8000`/`16000`/`24000`/`48000`）；
  - `audio.output.format.type` / `sample_rate`: 输出格式与采样率（同上）；
  - `smooth_output`: 仅 `qwen3-omni-flash-realtime` 支持，控制口语化（`true`）或书面化（`false`）风格。

- **VAD 配置**：
  - `turn_detection.type`: `server_vad`（默认）或 `semantic_vad`（仅 `qwen3.5-omni-realtime`）；
  - `turn_detection.threshold`: [-1.0, 1.0]，值越小越灵敏；
  - `turn_detection.silence_duration_ms`: [200, 6000] ms，静音超时触发响应；
  - `idle_timeout_ms`: [5000, 30000] ms，仅 `server_vad` + `qwen3.5-omni-plus/flash-realtime` 生效，用于静默引导。

- **生成控制参数**（`qwen-omni-turbo` 系列均不支持修改）：
  - `temperature` / `top_p`: 控制多样性，**二者选一设置即可**；
  - `top_k`: 候选集大小（0–100），设为 `null` 或 >100 则禁用；
  - `max_tokens`: 响应最大 token 数（截断，不影响生成过程）；
  - `repetition_penalty`: >0，抑制重复（默认 `1.0` 或 `1.05`）；
  - `presence_penalty`: [-2.0, 2.0]，控制全局重复度（`qwen3.5-omni-realtime` 默认 `1.5`，其余 `0.0`）；
  - `seed`: 整数，用于结果复现。

- **扩展功能**：
  - `enable_search`: `boolean`，仅 `qwen3.5-omni-realtime` 系列有效；
  - `search_options.enable_source`: `boolean`，是否返回搜索来源；
  - `tools`: 工具定义数组，每个工具含 `name`、`description`、`parameters`（符合 OpenAI Function Calling Schema）。

## 使用方式

1. **建立连接**：使用 WebSocket 连接到地域专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 均封装了 `connect()` 方法。
2. **初始化会话**：连接后立即发送 `session.update` 事件（或调用 `update_session()`），配置 `modalities`、`voice`、`audio`、`turn_detection` 等核心参数。
3. **输入数据**：
   - **VAD 模式**（推荐）：持续发送 `input_audio_buffer.append`，服务端自动检测语音起止并提交（无需 `commit`）；
   - **Manual 模式**：发送 `input_audio_buffer.append` 后，显式发送 `input_audio_buffer.commit` 创建用户消息项。
   - 图像输入：通过 `input_image_buffer.append` 发送，与音频缓冲区一同由 `commit` 提交。
4. **触发响应**：
   - VAD 模式下，服务端检测到语音结束即自动触发 `response.create`；
   - Manual 模式下，客户端需在 `commit` 后主动发送 `response.create`。
5. **处理工具调用**：若服务端返回 `response.function_call_arguments.done`，客户端执行本地函数后，通过 `conversation.item.create` 回传结果，再发 `response.create` 继续生成。
6. **流式消费响应**：监听 `response.audio.delta`（音频流）、`response.content_part.added`（文本流）、`response.audio_transcript.delta`（ASR 实时转录）等事件。

## 限制和注意事项

- **模型兼容性**：`qwen-omni-turbo-realtime` 系列不支持修改 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等参数，相关字段在请求中会被忽略 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **音频约束**：输入音频建议 16k Hz PCM（单声道、16bit），但 `qwen3.5-omni-realtime` 系列支持 `wav` 封装；输出音频默认 24k Hz PCM，但实际支持 `wav` 及 48k Hz（见前述注意）。
- **图像约束**：单图 Base64 编码后 ≤256KB，建议原始图 ≤190KB；分辨率建议 480p/720p，上限 1080p；需在首次音频追加后发送。
- **VAD 行为差异**：`semantic_vad` 可过滤回应语、背景音，但仅 `qwen3.5-omni-realtime` 系列支持；`server_vad` 模式下 `idle_timeout_ms` 仅对 `qwen3.5-omni-plus/flash-realtime` 生效。
- **功能互斥**：`tools` 与 `enable_search` 不可同时启用，否则会返回错误。
- **域名迁移**：北京/新加坡地域必须使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


