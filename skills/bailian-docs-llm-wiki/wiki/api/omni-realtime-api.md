# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时多模态交互接口，支持语音、文本、图像输入与文本、语音输出的端到端流式交互。它采用事件驱动模型，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态和数据流，服务端通过异步事件（如 `session.created`、`response.audio.delta`）实时推送响应结果。该 API 专为低延迟、高保真语音交互场景设计，适用于智能客服、虚拟助手、音视频会议等应用。

## 支持的模型/功能

- **核心模型系列**：
  - `qwen3.5-omni-realtime`：支持 `semantic_vad`、联网搜索（`enable_search`）及完整工具调用。
  - `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`：支持 `idle_timeout_ms` 静默超时主动引导，`smooth_output` 参数生效。
  - `qwen3-omni-flash-realtime`：默认音色为 `Cherry`，VAD 类型仅支持 `server_vad`。
  - `qwen-omni-turbo-realtime`：默认音色为 `Chelsie`，**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty` 和 `seed` 等生成参数 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

- **多模态能力**：
  - 输入：PCM 音频（16 kHz）、JPG/JPEG 图像（≤1080p，Base64 编码 ≤256 KB）、文本指令。
  - 输出：文本 + PCM 音频（24 kHz），支持 `["text"]` 或 `["text","audio"]` 模态组合。
  - 实时转录：内置 `qwen3-asr-flash-realtime` ASR 模型，不可替换 [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

- **高级功能**：
  - 语音活动检测（VAD）：`server_vad`（声学）或 `semantic_vad`（语义，仅 `qwen3.5-omni-realtime` 支持）。
  - 工具调用（Function Calling）：模型可自主触发预定义函数，需配合 `conversation.item.create` 回传结果。
  - 联网搜索：仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 不兼容 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
  - 声音复刻：通过独立 `qwen-voice-enrollment` 模型创建定制音色，**必须与 Omni 模型版本严格匹配**（如 `qwen3.5-omni-plus-realtime` 创建的音色只能用于同名模型）。

> **注意**：文档 6 中明确要求声音复刻时 `target_model` 必须与后续 Omni 调用的 `model` 完全一致，但文档 1 和文档 2 的 `session.created` 示例中 `model` 字段值为 `qwen3-omni-flash-realtime`，而文档 6 列出的可选 `target_model` 包含 `qwen3.5-omni-plus-realtime` 等带 `.5` 版本号的名称。实际使用中务必以文档 6 的 `target_model` 枚举为准，避免因版本号不匹配导致合成失败。

## 关键参数

所有可配置参数均通过 `session.update` 客户端事件或 SDK 的 `update_session()` 方法设置，统一归入 `session` 对象：

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `modalities` | `array` | 输出模态，`["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` | `string` | 音色名称 | `Tina`（Qwen3.5）、`Cherry`（Qwen3-Flash）、`Chelsie`（Turbo） |
| `input_audio_format` / `output_audio_format` | `string` | 固定为 `"pcm"`；输入需 16 kHz，输出为 24 kHz | — |
| `instructions` | `string` | 系统角色指令 | — |
| `turn_detection.type` | `string` | `server_vad`（默认）或 `semantic_vad`（仅 Qwen3.5） | `server_vad` |
| `turn_detection.threshold` | `float` | VAD 灵敏度 [-1.0, 1.0] | `0.5` |
| `turn_detection.silence_duration_ms` | `integer` | 静音触发阈值 [200, 6000] ms | `800` |
| `turn_detection.idle_timeout_ms` | `integer` | 静默超时引导 [5000, 30000] ms，**仅 Qwen3.5-Plus/Flash + `server_vad` 生效** | — |
| `enable_search` | `boolean` | 启用联网搜索（仅 Qwen3.5） | `false` |
| `search_options.enable_source` | `boolean` | 返回搜索来源 | `false` |
| `tools` | `array` | 工具定义列表（仅 Qwen3.5） | `[]` |
| `temperature` / `top_p` / `top_k` | `float`/`float`/`integer` | 采样控制，**Turbo 系列不支持修改** | 见各模型默认值 |
| `max_tokens` | `integer` | 最大输出 token 数，超长则截断 | 模型最大长度 |
| `repetition_penalty` / `presence_penalty` | `float` | 重复惩罚，**Turbo 系列不支持修改** | 见各模型默认值 |
| `seed` | `integer` | 生成确定性种子 [0, 2³¹−1] | `-1` |

> **注意**：`smooth_output` 仅对 `qwen3-omni-flash-realtime` 系列生效，且必须通过 `parameters` 字典传入（如 Java/Python SDK 的 `update_session`），不能直接置于 `session` 顶层字段中。

## 使用方式

1. **建立连接**：使用 WSS 协议连接业务空间专属域名（推荐），格式为 `wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`。[原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 明确指出旧域名（`dashscope.aliyuncs.com`）已迁移，新域名提供更高性能与稳定性。

2. **初始化会话**：连接后服务端立即返回 `session.created` 事件。建议在收到该事件后立即调用 `session.update` 设置自定义配置（如 `voice`、`instructions`、`tools`）。

3. **输入处理**：
   - **VAD 模式**（`turn_detection.type` 非 null）：客户端持续 `append_audio`，服务端自动检测起止并提交（无需 `input_audio_buffer.commit`）。
   - **Manual 模式**（`turn_detection` 设为 `null`）：客户端 `append_audio` 后显式 `input_audio_buffer.commit` 提交音频，再发 `response.create` 触发响应。

4. **工具调用流程**：
   - 服务端返回 `conversation.item.created`（type=`function_call`）→ 客户端执行本地函数 → 发送 `conversation.item.create`（type=`function_call_output`）→ 服务端自动生成最终响应（VAD 模式）或等待客户端 `response.create`（Manual 模式）。

5. **输出消费**：监听 `response.audio.delta`（流式音频 Base64）、`response.text.delta`（流式文本）、`response.audio_transcript.done`（ASR 结果）等事件。

## 限制和注意事项

- **音频/图像限制**：
  - 输入音频：PCM 格式，16 kHz 采样率，单次 `append` 数据量无硬限，但缓冲区总大小建议 ≤15 MiB。
  - 输入图像：JPG/JPEG，分辨率 ≤1080p，Base64 编码后 ≤256 KB，建议 1 张/秒频率发送。
  - 声音复刻音频：10–20 秒，WAV/MP3/M4A，≥24 kHz 采样率，单声道，无背景音 [原文标题](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

- **功能互斥**：
  - `enable_search` 与 `tools` 不可同时启用，否则参数校验失败。
  - `qwen-omni-turbo-realtime` 系列模型**完全禁止修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`，尝试设置将被忽略。

- **错误处理**：
  - 服务端返回 `error` 事件（如 `invalid_value` 错误码），需检查 `param` 字段定位问题参数（如 `session.modalities`）。
  - `input_audio_buffer.commit` 在缓冲区为空时触发错误，需确保先 `append_audio`。

- **SDK 差异**：
  - Java/Python SDK 中，`smooth_output`、`temperature` 等参数必须通过 `parameters` Map 传入 `update_session`，而非直接作为方法参数（见文档 3 和文档 5 的代码示例）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


