# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时[多模态](../concepts/multi-modal.md)交互接口，支持语音、文本、图像输入与文本、语音输出的端到端流式交互。它采用事件驱动模型，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态和数据流，服务端通过异步事件（如 `session.created`、`response.audio.delta`）实时推送响应。该 API 专为低延迟、高保真语音交互场景设计，适用于智能客服、虚拟助手等实时对话系统。

## 支持的模型/功能

当前支持以下 Qwen-Omni 系列实时模型，各模型能力与默认配置存在差异：

- `qwen3.5-omni-realtime`：支持 `semantic_vad`、联网搜索（`enable_search`）、工具调用（`tools`），默认 `temperature=0.7`、`top_p=0.8`、`top_k=20`、`presence_penalty=1.5`。
- `qwen3-omni-flash-realtime`：支持 `smooth_output` 参数控制口语化/书面化风格，不支持 `enable_search` 或 `semantic_vad`，默认 `voice="Cherry"`、`temperature=0.9`、`top_p=1.0`、`top_k=50`。
- `qwen-omni-turbo-realtime`：仅支持基础 VAD 和音频/文本输出，**所有生成参数（`temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`）均不可修改**，默认 `voice="Chelsie"`、`temperature=1.0`、`top_p=0.01` [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

> **注意**：文档 4（Java SDK）中称 `qwen3.5-omni-realtime` 默认 `presence_penalty=1.5`，而文档 1（客户端事件）中明确列出其默认值为 `1.5`，但文档 3（服务端事件）示例中 `session.created` 返回的 `presence_penalty` 为 `0.0`。以 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中的明确声明为准，即 `qwen3.5-omni-realtime` 系列默认 `presence_penalty=1.5`。

核心功能包括：
- **[多模态](../concepts/multi-modal.md)输入**：支持 PCM 音频（16 kHz）和 JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256KB）。
- **[多模态](../concepts/multi-modal.md)输出**：可配置 `["text"]` 或 `["text","audio"]`，输出音频为 24 kHz PCM [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **语音活动检测（VAD）**：提供 `server_vad`（声学特征）和 `semantic_vad`（语义有效性）两种模式，后者仅 `qwen3.5-omni-realtime` 支持。
- **主动引导**：`idle_timeout_ms` 可在静默超时后触发模型主动响应，仅对 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` 模型生效 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **扩展能力**：`qwen3.5-omni-realtime` 独有支持联网搜索（`enable_search`）和工具调用（`tools`），二者互斥。

## 关键参数

所有可配置参数均通过 `session.update` 事件或 SDK 的 `update_session` 方法设置，主要分为以下几类：

| 参数 | 类型 | 说明 | 适用模型 | 默认值 |
|------|------|------|----------|--------|
| `modalities` | `["text"]` 或 `["text","audio"]` | 输出模态组合 | 全系列 | `["text","audio"]` |
| `voice` | `string` | 音色名称 | 全系列 | `Tina`/`Cherry`/`Chelsie`（按模型） |
| `instructions` | `string` | 系统角色提示词 | 全系列 | 无 |
| `turn_detection.type` | `"server_vad"` 或 `"semantic_vad"` | VAD 类型 | `qwen3.5-omni-realtime`（后者）；全系列（前者） | `"server_vad"` |
| `turn_detection.threshold` | `float [-1.0, 1.0]` | VAD 灵敏度 | 全系列 | `0.5` |
| `turn_detection.silence_duration_ms` | `int [200, 6000]` | 静音触发阈值 | 全系列 | `800` |
| `turn_detection.idle_timeout_ms` | `int [5000, 30000]` | 静默超时主动响应 | `qwen3.5-omni-plus-realtime`/`flash-realtime` | 无 |
| `enable_search` | `boolean` | 启用联网搜索 | `qwen3.5-omni-realtime` | `false` |
| `search_options.enable_source` | `boolean` | 返回搜索来源 | `qwen3.5-omni-realtime`（需 `enable_search=true`） | `false` |
| `tools` | `array` | 工具定义列表 | `qwen3.5-omni-realtime` | `[]` |
| `temperature` | `float [0, 2)` | 采样温度 | `qwen3.5`/`flash` | `0.7`/`0.9` |
| `top_p` | `float (0, 1.0]` | 核采样阈值 | `qwen3.5`/`flash` | `0.8`/`1.0` |
| `top_k` | `int ≥0` | 候选集大小 | `qwen3.5`/`flash` | `20`/`50` |
| `max_tokens` | `int` | 最大输出 token 数 | `qwen3.5`/`flash` | 模型最大长度 |
| `repetition_penalty` | `float >0` | 重复惩罚 | `qwen3.5`/`flash` | `1.0`/`1.05` |
| `presence_penalty` | `float [-2.0, 2.0]` | 存在惩罚 | `qwen3.5`/`flash` | `1.5`/`0.0` |
| `seed` | `int [0, 2^31-1]` | 随机种子 | `qwen3.5`/`flash` | `-1` |

> **注意**：`qwen-omni-turbo-realtime` 系列模型的所有生成参数均不可修改，任何尝试设置都将被忽略 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 使用方式

API 通过 WebSocket 连接工作，典型流程如下：

1. **建立连接**：使用地域专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`）连接，连接成功后服务端立即返回 `session.created` 事件。
2. **配置会话**：调用 `session.update` 事件（或 SDK 的 `update_session`）设置 `modalities`、`voice`、`instructions` 等参数。推荐在连接后立即执行。
3. **输入数据**：
   - **音频**：持续发送 `input_audio_buffer.append`（Base64 PCM 数据），在 VAD 模式下由服务端自动提交；在 Manual 模式下需显式发送 `input_audio_buffer.commit` [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
   - **图像**：发送 `input_image_buffer.append`（Base64 JPG/JPEG），需在音频缓冲区已初始化后发送，且与音频一同通过 `input_audio_buffer.commit` 提交。
4. **触发响应**：
   - VAD 模式：服务端检测到 `speech_stopped` 后自动开始生成，无需客户端干预。
   - Manual 模式：客户端在提交音频后，必须发送 `response.create` 事件。
5. **处理响应**：监听 `response.audio.delta`（流式音频）、`response.text.delta`（流式文本）、`response.done`（完成）等事件。
6. **工具调用**：当服务端返回 `conversation.item.created` 且 `type="function_call"` 时，客户端执行工具并回传结果 via `conversation.item.create`，再发送 `response.create` 触发最终响应。

SDK 封装了上述流程，Python 和 Java SDK 均提供 `OmniRealtimeConversation` 类，其 `connect()`、`append_audio()`、`commit()`、`create_response()` 等方法直接映射底层事件。

## 限制和注意事项

- **音频格式**：输入必须为 16 kHz PCM（`input_audio_format="pcm"`），输出固定为 24 kHz PCM（`output_audio_format="pcm"`），不支持自定义采样率 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **图像限制**：仅支持 JPG/JPEG，建议分辨率 480p/720p，单图 Base64 编码后 ≤256KB，建议原始大小 ≤190KB，发送频率 ≤1 张/秒。
- **参数互斥**：`enable_search` 与 `tools` 不可同时启用，否则会返回 `invalid_request_error`。
- **模型兼容性**：声音复刻创建的音色（`voice`）必须与 Omni 实时 API 调用时指定的 `model` 完全一致，否则合成失败 [原文标题](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。
- **域名迁移**：强烈建议使用业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但新域名提供更高性能与稳定性。
- **错误处理**：所有错误均以 `error` 事件返回，包含 `type`、`code`、`message` 和 `param` 字段，需在回调中统一捕获。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


