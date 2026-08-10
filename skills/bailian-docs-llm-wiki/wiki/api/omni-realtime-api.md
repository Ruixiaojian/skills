# omni realtime api

Qwen-Omni-Realtime API 是一个基于 WebSocket 的实时[多模态](../concepts/multi-modal.md)交互接口，支持语音输入、文本/音频输出、实时转录、工具调用与 VAD 自动检测。它面向低延迟对话场景，要求客户端维持长连接并按事件协议双向通信。

## 支持的模型与功能

- **核心模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`。不同模型在功能支持上存在差异：
  - `semantic_vad` 仅 `qwen3.5-omni-realtime` 系列支持（注意：文档中多次出现 `qwen3.5-omni-realtime` 作为统称，但实际模型名含 `-plus-` 或 `-flash-` 后缀，需以 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 中 `session.created` 返回的 `model` 字段为准）；
  - 联网搜索（`enable_search`）和工具调用（`tools`）**仅 `qwen3.5-omni-realtime` 系列支持**，且二者互斥，不可同时启用；
  - `smooth_output` 参数仅对 `qwen3-omni-flash-realtime` 系列生效；
  - `qwen-omni-turbo-realtime` 系列**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty` 和 `seed`（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。

- **[多模态](../concepts/multi-modal.md)能力**：
  - 输入：PCM 音频（16 kHz）、JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256 KB）；
  - 输出：文本 + PCM 音频（24 kHz），或仅文本；
  - 实时语音转录：内置 `qwen3-asr-flash-realtime` 模型，不可替换；
  - 声音复刻：需通过独立 API 创建音色，复刻音色仅可在对应 `target_model` 的 Omni-Realtime 调用中使用（详见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）。

> **注意**：文档 1 中 `session.updated` 示例返回了 `max_response_output_token: "inf"`，但该字段未在任何客户端事件或 SDK 参数文档中定义，亦未在其他事件结构中出现，属于冗余或过时字段，应忽略。

## 关键参数

所有可配置参数均通过 `session.update` 客户端事件或 SDK 的 `update_session()` 方法设置，主要分为以下几类：

- **基础配置**：
  - `modalities`: 必选数组，取值为 `["text"]` 或 `["text","audio"]`（默认）；
  - `voice`: 音色名，不同模型默认值不同（`Tina`/`Cherry`/`Chelsie`），复刻音色需显式传入；
  - `instructions`: 系统角色提示词，用于设定模型行为；
  - `input_audio_format` / `output_audio_format`: 固定为 `"pcm"`，对应采样率分别为 16 kHz 和 24 kHz。

- **VAD 控制**（语音活动检测）：
  - `turn_detection.type`: `"server_vad"`（默认）或 `"semantic_vad"`（仅 qwen3.5 系列）；
  - `turn_detection.threshold`: [-1.0, 1.0]，阈值越低越灵敏；
  - `turn_detection.silence_duration_ms`: [200, 6000]，默认 800 ms；
  - `turn_detection.idle_timeout_ms`: [5000, 30000]，**仅在 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 下生效**。

- **生成控制**（各模型默认值见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）：
  - `temperature`: [0, 2)，与 `top_p` 二选一；
  - `top_p`: (0, 1.0]，与 `temperature` 二选一；
  - `top_k`: ≥0，设为 `null` 或 >100 时禁用；
  - `max_tokens`: 截断响应长度，不影响生成过程；
  - `repetition_penalty`: >0，1.0 表示无惩罚；
  - `presence_penalty`: [-2.0, 2.0]；
  - `seed`: 0~2³¹−1，默认 -1。

- **高级功能**（条件启用）：
  - `enable_search`: `true` 时启用联网搜索（仅 qwen3.5 系列）；
  - `search_options.enable_source`: 是否返回搜索来源；
  - `tools`: 工具函数定义列表（仅 qwen3.5 系列），结构需严格遵循 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 规范。

## 使用方式

1. **建立连接**：使用 WebSocket 连接到业务空间专属域名（推荐 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime` 或新加坡地域对应地址），[Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 和 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 提供封装好的 `connect()` 方法。

2. **初始化会话**：连接后立即发送 `session.update` 事件（或调用 `update_session()`）配置参数。服务端返回 `session.created`（首次）或 `session.updated` 事件确认配置。

3. **输入数据**：
   - **音频**：持续发送 `input_audio_buffer.append`（Base64 PCM 数据）；
   - **图像**：发送 `input_image_buffer.append`（Base64 JPG/JPEG），需先有音频输入；
   - **手动提交**：在 Manual 模式下，发送 `input_audio_buffer.commit` 创建用户消息项；VAD 模式下由服务端自动提交。

4. **触发响应**：
   - VAD 模式：服务端检测到语音结束自动触发响应；
   - Manual 模式：客户端发送 `response.create` 显式触发。

5. **处理工具调用**：当收到 `conversation.item.created` 且 `type` 为 `"function_call"` 时，执行本地工具，再通过 `conversation.item.create`（`type: "function_call_output"`）回传结果，最后发送 `response.create` 获取最终响应。

6. **接收输出**：监听 `response.audio.delta`（流式音频）、`response.text.delta`（流式文本）、`response.audio_transcript.delta`（ASR 中间结果）等事件。

## 限制和注意事项

- **音频格式硬性要求**：输入必须为 16 kHz PCM 单声道，输出固定为 24 kHz PCM，不支持自定义采样率或编码格式。
- **VAD 模式依赖环境**：`server_vad` 在嘈杂环境中易误触发，建议调高 `threshold`；`semantic_vad` 可过滤背景音但仅限 qwen3.5 系列。
- **功能互斥**：`tools` 与 `enable_search` 不可同时启用，否则服务端返回 `invalid_request_error`。
- **SDK 版本要求**：Java SDK ≥ v2.22.15，Python SDK ≥ v1.25.17，旧版本可能缺失关键参数支持。
- **域名迁移**：旧域名（`dashscope.aliyuncs.com`）仍可用，但官方强烈推荐迁移到业务空间专属域名以获得更高稳定性与性能（见 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 和 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 文档）。
- **错误处理**：所有错误均以 `error` 事件形式返回，包含 `type`、`code`、`message` 和 `param`，需在客户端做健壮解析（参见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）。

## 来源文档

- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


