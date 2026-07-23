# omni realtime api

Qwen-Omni-Realtime API 是一个基于 WebSocket 的实时多模态交互接口，支持语音、文本、图像输入与文本+音频同步输出。它采用事件驱动架构，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态和数据流，服务端通过异步事件（如 `input_audio_buffer.speech_stopped`、`response.audio.delta`）实时反馈处理结果。该 API 专为低延迟、高保真语音交互场景设计，适用于智能客服、虚拟助手等实时对话应用。

## 支持的模型/功能

- **核心模型系列**：
  - `qwen3.5-omni-realtime`：支持 `semantic_vad`、联网搜索（`enable_search`）及完整工具调用（`tools`）。
  - `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`：支持 `idle_timeout_ms` 静默超时主动引导，但**不支持 `semantic_vad`**（仅 `server_vad`）。
  - `qwen3-omni-flash-realtime`：支持 `smooth_output` 控制口语化/书面化风格。
  - `qwen-omni-turbo-realtime`：轻量级模型，**所有生成参数（`temperature`、`top_p`、`max_tokens` 等）均不可修改**，仅支持基础语音交互 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

- **多模态能力**：
  - 输入：实时 PCM 音频（16 kHz）、JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256 KB）、文本（通过 `instructions` 或 ASR 转录）。
  - 输出：文本 + PCM 音频（24 kHz），可选仅文本模式（`modalities: ["text"]`）。
  - 工具调用：仅 `qwen3.5-omni-realtime` 系列支持，需配置 `tools` 数组，模型触发后返回 `function_call` 项，客户端回传结果后需显式调用 `response.create` [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
  - 联网搜索：仅 `qwen3.5-omni-realtime` 系列支持 `enable_search`，且与 `tools` **互斥**，不可同时启用 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

> **注意**：文档 6 中提到的 `qwen3.5-omni-plus` 和 `qwen3.5-omni-flash` 是**非实时（batch）模型**，不能用于本 API；本 API 仅接受 `-realtime` 后缀的模型名（如 `qwen3.5-omni-plus-realtime`），否则连接将失败。

## 关键参数

所有参数均通过 `session.update` 事件或 SDK 的 `update_session` 方法配置，分为以下几类：

- **基础配置**：
  - `modalities`: `["text"]` 或 `["text","audio"]`（默认），不支持 `["audio"]` 单独输出。
  - `voice`: 音色名，不同模型默认值不同（如 `qwen3.5-omni-realtime` 默认 `Tina`），亦可使用声音复刻生成的自定义音色 [原文标题](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。
  - `input_audio_format` / `output_audio_format`: 固定为 `"pcm"`，对应 16 kHz 输入 / 24 kHz 输出。

- **VAD 控制**（语音活动检测）：
  - `turn_detection.type`: `"server_vad"`（默认）或 `"semantic_vad"`（仅 `qwen3.5-omni-realtime` 支持）。
  - `turn_detection.threshold`: [-1.0, 1.0]，值越低越灵敏（易误触），默认 `0.5`。
  - `turn_detection.silence_duration_ms`: [200, 6000] ms，静音超时触发响应，默认 `800`。
  - `turn_detection.idle_timeout_ms`: [5000, 30000] ms，**仅 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` 在 `server_vad` 模式下生效**，用于静默后主动引导。

- **生成控制**（部分参数在 `qwen-omni-turbo-realtime` 上不可修改）：
  - `temperature` / `top_p`: 控制多样性，建议**二选一**设置。默认值因模型而异（如 `qwen3.5-omni-realtime`: `0.7` / `0.8`）。
  - `top_k`: 候选 Token 数，≥0，设为 `null` 或 >100 时禁用。
  - `max_tokens`: 最大输出长度，超长则截断，不影响生成过程。
  - `repetition_penalty` / `presence_penalty`: 控制重复度，默认值模型间有差异（如 `qwen3.5-omni-realtime`: `1.0` / `1.5`）。
  - `seed`: 用于结果复现，取值范围 `[0, 2^31-1]`，默认 `-1`。

## 使用方式

1. **建立连接**：使用 WebSocket URL（推荐业务空间专属域名，如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`）连接，首条服务端事件为 `session.created`。

2. **配置会话**：连接后立即发送 `session.update` 事件（或调用 SDK `update_session`），设置 `modalities`、`voice`、`turn_detection` 等。服务端校验后返回 `session.updated`。

3. **输入数据**：
   - **VAD 模式**（`turn_detection.type` 非 null）：持续发送 `input_audio_buffer.append`，服务端自动检测起止并提交，客户端无需调用 `input_audio_buffer.commit`。
   - **Manual 模式**（`turn_detection` 设为 `null`）：发送 `input_audio_buffer.append` 后，必须显式发送 `input_audio_buffer.commit` 创建用户消息项。

4. **触发响应**：
   - VAD 模式：服务端检测到语音结束自动触发 `response.create`。
   - Manual 模式：客户端在提交音频后，需主动发送 `response.create` 事件。

5. **处理工具调用**：当服务端返回 `conversation.item.created` 类型为 `function_call` 时，客户端执行工具，再通过 `conversation.item.create` 回传结果，并发送 `response.create` 触发最终响应。

## 限制和注意事项

- **音频/图像限制**：输入音频必须为 16 kHz PCM；图像仅支持 JPG/JPEG，Base64 编码后 ≤256 KB，建议分辨率 480p–720p。
- **并发与配额**：单个 WebSocket 连接仅支持一个会话；具体 QPS 和 Token 配额需参考百炼控制台配额管理。
- **SDK 版本要求**：Python SDK ≥1.25.17，Java SDK ≥2.22.15，旧版本可能缺失 `idle_timeout_ms` 等新参数支持。
- **地域与域名**：北京/新加坡地域**必须使用业务空间专属域名**（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等），旧域名（`dashscope.aliyuncs.com`）已逐步弃用，性能与稳定性较差。
- **错误处理**：服务端返回 `error` 事件时，`error.param` 字段明确指示出错参数（如 `"session.modalities"`），应据此修正请求。

> **注意**：文档 2 和文档 4 中 `enable_turn_detection` 参数在 Python/Java SDK 中是布尔开关，其底层映射到 `session.turn_detection.type`；若设为 `False`，实际等效于 `turn_detection: null`（即 Manual 模式），而非 `type: "server_vad"` 且 `threshold: 0`。此逻辑一致性需开发者注意。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


