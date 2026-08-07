# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时[多模态](../concepts/multi-modal.md)交互接口，支持语音、文本、图像输入与文本、语音输出的端到端流式交互。它采用事件驱动模型，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态和数据流，服务端通过异步事件（如 `session.created`、`response.audio.delta`）实时推送响应片段。该 API 专为低延迟、高并发的语音助手、智能客服等场景设计。

## 支持的模型/功能

Omni Realtime API 当前支持以下系列模型，各模型能力与默认配置存在差异：

- **`qwen3.5-omni-realtime` 系列**：支持 `semantic_vad`（语义级语音活动检测）、联网搜索（`enable_search`）、工具调用（`tools`），默认 `voice: "Tina"`，默认 `temperature: 0.7`、`top_p: 0.8`、`top_k: 20`、`repetition_penalty: 1.0`、`presence_penalty: 1.5`。
- **`qwen3-omni-flash-realtime` 系列**：支持 `server_vad`、`smooth_output`（口语化/书面化风格切换），默认 `voice: "Cherry"`，默认 `temperature: 0.9`、`top_p: 1.0`、`top_k: 50`、`repetition_penalty: 1.05`、`presence_penalty: 0.0`。
- **`qwen-omni-turbo-realtime` 系列**：仅支持 `server_vad`，**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等采样参数，[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)明确指出其为“只读”；默认 `voice: "Chelsie"`，默认 `temperature: 1.0`、`top_p: 0.01`、`top_k: 20`、`repetition_penalty: 1.05`、`presence_penalty: 0.0`。

> **注意**：文档 2（[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）中 `session.created` 示例显示 `model: "qwen3-omni-flash-realtime"`，但未列出 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` —— 这两类模型在 `idle_timeout_ms` 等高级 VAD 参数上具有专属支持，实际可用性需以 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中的 `idle_timeout_ms` 说明为准。

核心功能包括：
- 实时语音输入与 ASR 转录（固定使用 `qwen3-asr-flash-realtime` 模型）
- [多模态](../concepts/multi-modal.md)输出（文本 + PCM 音频，24 kHz）
- 图像输入（JPG/JPEG，≤1080p，Base64 编码 ≤256KB）
- 工具调用（Function Calling）与联网搜索（二者互斥）
- 声音复刻音色集成（需先调用独立声音复刻 API 创建 `voice` ID，再在 `session.update` 中传入）

## 关键参数

所有可配置参数均通过 `session.update` 客户端事件或 SDK 的 `update_session()` 方法设置。关键参数按功能分组如下：

### 会话与模态
- `modalities`: `["text"]` 或 `["text", "audio"]`（默认），不支持 `["audio"]` 单独输出。
- `voice`: 音色 ID，支持官方音色或声音复刻生成的定制音色（参见 [原文标题](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）。
- `input_audio_format` / `output_audio_format`: 固定为 `"pcm"`，对应 `PCM_16000HZ_MONO_16BIT` 输入与 `PCM_24000HZ_MONO_16BIT` 输出。

### 语音活动检测（VAD）
- `turn_detection.type`: `"server_vad"`（默认）或 `"semantic_vad"`（仅 `qwen3.5-omni-realtime` 支持）。
- `turn_detection.threshold`: `[-1.0, 1.0]`，默认 `0.5`；值越低越灵敏。
- `turn_detection.silence_duration_ms`: `[200, 6000]`，默认 `800`。
- `turn_detection.idle_timeout_ms`: `[5000, 30000]`，**仅对 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` 且 `type="server_vad"` 生效**。

### 生成控制（模型级）
- `temperature` / `top_p`: 控制多样性，**二者建议只设其一**；`qwen-omni-turbo` 系列不可修改。
- `top_k`: `[0, 100]`，设为 `null` 或 `>100` 则禁用。
- `max_tokens`: 截断响应长度，不影响生成过程。
- `repetition_penalty`: `>0`，默认 `1.0`（`qwen3.5`）或 `1.05`（其他）。
- `presence_penalty`: `[-2.0, 2.0]`，默认 `1.5`（`qwen3.5`）或 `0.0`（其他）。
- `seed`: `0` 到 `2^31-1`，用于结果复现。

### 高级能力
- `instructions`: 系统角色提示词。
- `enable_search`: `true/false`，仅 `qwen3.5-omni-realtime` 支持；启用后 `tools` 必须为空。
- `search_options.enable_source`: `true/false`，控制是否返回搜索来源。
- `tools`: 函数定义数组，每个含 `name`、`description`、`parameters`（含 `properties` 和 `required`）。
- `smooth_output`: `true`（口语化）/`false`（书面化）/`null`（自动），**仅 `qwen3-omni-flash-realtime` 支持**。

## 使用方式

API 通过 WebSocket 连接交互，典型流程分为三阶段：

1. **建立连接与初始化**  
   客户端连接至地域专属 WSS 地址（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），服务端立即返回 `session.created` 事件。随后应调用 `session.update` 设置初始配置（推荐在 `connect()` 后立即执行）。

2. **输入数据流**  
   - **VAD 模式**（`turn_detection.type = "server_vad"`）：客户端持续发送 `input_audio_buffer.append`，服务端自动检测起止并触发 `speech_started`/`speech_stopped`/`committed`；图像通过 `input_image_buffer.append` 发送，与音频缓冲区一同由服务端提交。  
   - **Manual 模式**（`turn_detection = null`）：客户端控制节奏，需显式发送 `input_audio_buffer.commit` 提交音频（及关联图像），再发送 `response.create` 触发响应。

3. **响应处理与工具调用**  
   - 服务端流式返回 `response.audio.delta`（音频片段）、`response.text.delta`（文本片段）、`response.audio_transcript.delta`（ASR 中间结果）等事件。  
   - 若模型决定调用工具，服务端发送 `response.function_call_arguments.done`（含 `call_id`），客户端执行本地函数后，通过 `conversation.item.create` 回传结果，并在 Manual 模式下需再次发送 `response.create`；VAD 模式下服务端自动续生成。

SDK 封装了上述逻辑：Python SDK 的 `OmniRealtimeConversation` 类提供 `append_audio()`、`commit()`、`create_response()` 等方法；Java SDK 的 `OmniRealtimeConversation` 提供对应 `appendAudio()`、`commit()`、`createResponse()` 方法，参数配置统一通过 `OmniRealtimeConfig` 的 `parameters()` 方法注入。

## 限制和注意事项

- **协议限制**：必须使用 WebSocket（WSS），不支持 HTTP REST 调用；连接需携带有效 API Key。
- **音频限制**：输入音频为 16 kHz PCM，输出为 24 kHz PCM；单次 `append` 数据无明确上限，但总缓冲区建议 ≤15 MiB（[原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)）。
- **图像限制**：仅 JPG/JPEG，分辨率建议 480p–720p，Base64 编码后 ≤256KB，发送频率建议 ≤1 张/秒。
- **互斥约束**：`enable_search` 与 `tools` 不可同时启用；`qwen-omni-turbo` 系列模型所有生成参数均为只读。
- **地域与域名**：强烈建议使用业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽兼容但性能与稳定性较低（[原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)）。
- **错误处理**：服务端通过 `error` 事件返回结构化错误（含 `type`、`code`、`message`、`param`），客户端需监听并解析 `param` 字段定位问题（如 `session.modalities` 格式错误）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)


