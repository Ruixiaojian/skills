# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的低延迟、多模态实时交互接口，支持语音输入/输出、文本生成、图像理解及工具调用等能力。它采用事件驱动模型，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态与数据流，服务端通过异步事件（如 `session.created`、`response.audio.delta`）实时推送响应。该 API 专为语音助手、智能客服、实时音视频交互等场景设计。

## 支持的模型/功能

- **核心模型系列**：  
  - `qwen3.5-omni-realtime`（含 `plus` 和 `flash` 变体）：支持 `semantic_vad`、联网搜索（`enable_search`）、完整工具调用（`tools`）及高保真音频生成；  
  - `qwen3-omni-flash-realtime`：主打低延迟，支持 `smooth_output` 风格控制，VAD 类型仅限 `server_vad`；  
  - `qwen-omni-turbo-realtime`：轻量级模型，仅支持基础 VAD 和固定参数（[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中明确标注其不支持修改 `temperature`/`top_p` 等多数采样参数）。

- **多模态能力**：  
  - 输入：16 kHz PCM 音频（必选）、JPG/JPEG 图像（可选，需先追加音频）；  
  - 输出：24 kHz PCM 音频 + 文本（默认），或纯文本（`["text"]`）；  
  - 实时转录：内置 `qwen3-asr-flash-realtime` 模型，通过 `conversation.item.input_audio_transcription.delta` 提供流式识别结果（[原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)）。

- **高级功能**：  
  - 语音活动检测（VAD）：`server_vad`（全模型支持）和 `semantic_vad`（仅 `qwen3.5-omni-realtime` 支持）；  
  - 声音复刻：需先调用独立声音复刻 API 创建音色，再在 `session.update` 中通过 `voice` 参数传入（[原文标题](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）；  
  - 工具调用与联网搜索：二者互斥，不可同时启用（[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md) 明确警告）。

> **注意**：文档 2（`server-events.md`）中 `session.created` 示例显示 `input_audio_transcription.model` 固定为 `qwen3-asr-flash-realtime`，而文档 1（`client-events.md`）未提及此字段可配置——这与文档 3（Python SDK）中 `input_audio_transcription_model` 参数描述存在隐含矛盾。实际开发中应以服务端返回的 `session.created` 为准，客户端无法覆盖该值。

## 关键参数

所有会话级参数均通过 `session.update` 事件或 SDK 的 `update_session()` 方法设置，结构化为 `session` 对象子字段：

- **基础配置**：  
  - `modalities`: `["text"]` 或 `["text","audio"]`（默认），决定输出模态；  
  - `voice`: 音色名称（如 `"Chelsie"`），不同模型有默认值（[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)）；  
  - `instructions`: 系统角色提示词，直接影响模型行为。

- **音频处理**：  
  - `input_audio_format` / `output_audio_format`: 均固定为 `"pcm"`，对应 16 kHz 输入 / 24 kHz 输出；  
  - `turn_detection`: VAD 配置对象，含 `type`（`"server_vad"`/`"semantic_vad"`）、`threshold`（-1.0~1.0）、`silence_duration_ms`（200~6000）；  
  - `idle_timeout_ms`: 仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` 在 `server_vad` 下生效，定义静默后主动引导的毫秒数（5000~30000）。

- **生成控制**（部分模型受限）：  
  - `temperature` / `top_p` / `top_k`: 控制多样性，建议只设其一；`qwen-omni-turbo` 系列完全不可修改；  
  - `max_tokens`: 截断响应长度，不影响生成过程；  
  - `repetition_penalty` / `presence_penalty`: 调整重复倾向；  
  - `seed`: 复现结果的随机种子（`qwen-omni-turbo` 不支持）。

- **扩展能力**：  
  - `enable_search`: 仅 `qwen3.5-omni-realtime` 支持，启用后模型可自主触发搜索；  
  - `tools`: 工具函数定义列表，每个含 `name`、`description`、`parameters`（遵循 OpenAPI Schema）；  
  - `smooth_output`: 仅 `qwen3-omni-flash-realtime` 支持，控制口语化（`true`）或书面化（`false`）风格。

## 使用方式

1. **建立连接**：  
   使用 WSS 协议连接业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），避免旧版 `dashscope.aliyuncs.com` 域名（[原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 强调迁移必要性）。

2. **初始化会话**：  
   连接后立即收到 `session.created` 事件，包含默认配置；随后调用 `session.update` 同步自定义参数（如 `voice`、`instructions`）。

3. **数据输入**：  
   - **VAD 模式**（推荐）：持续发送 `input_audio_buffer.append`，服务端自动检测起止并提交（无需 `commit`）；  
   - **Manual 模式**：发送 `input_audio_buffer.append` 后，显式调用 `input_audio_buffer.commit` 创建用户消息项。

4. **触发响应**：  
   - VAD 模式下，服务端检测到语音结束即自动触发 `response.create`；  
   - Manual 模式下，客户端需在 `commit` 后主动发送 `response.create`。

5. **处理工具调用**：  
   当收到 `conversation.item.created`（`type: "function_call"`）时，执行本地工具，再通过 `conversation.item.create` 回传结果，最后发送 `response.create` 获取最终响应（[原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md) 详细说明两种模式流程差异）。

6. **流式消费输出**：  
   监听 `response.audio.delta`（Base64 音频片段）、`response.text.delta`（文本片段）、`response.audio_transcript.delta`（ASR 中间结果）等事件，按需渲染。

## 限制和注意事项

- **音频/图像限制**：  
  - 输入音频必须为 16 kHz PCM；图像仅支持 JPG/JPEG，单张 Base64 编码后 ≤256 KB，建议分辨率 480p/720p；  
  - 图像缓冲区需在至少一次 `input_audio_buffer.append` 后才可使用（[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。

- **模型能力边界**：  
  - `qwen-omni-turbo-realtime` 系列不支持修改 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等全部生成参数（文档 1、3、4 多次强调）；  
  - `tools` 与 `enable_search` 严格互斥，同时设置将导致 `error` 事件（[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。

- **连接与稳定性**：  
  - 推荐使用业务空间专属域名（北京/新加坡），旧域名虽兼容但性能与稳定性较低（[原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)）；  
  - 手动模式下，`input_audio_buffer.commit` 若在空缓冲区调用将返回错误；VAD 模式下客户端不应发送 `commit`（文档 1 明确说明）。

- **调试建议**：  
  - 优先监听 `error` 事件排查参数错误（如 `invalid_value` for `session.modalities`）；  
  - 使用 `conversation.item.input_audio_transcription.delta` 的 `text` + `stash` 拼接实现 ASR 实时预览（[原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md) 提供完整示例）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)


