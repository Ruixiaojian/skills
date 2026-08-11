# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的低延迟[多模态](../concepts/multi-modal.md)实时交互接口，支持语音输入、文本/音频输出、VAD 自动断句、工具调用与联网搜索（部分模型），适用于智能客服、虚拟助手等实时对话场景。其核心是事件驱动的双向通信模型，客户端通过发送标准化事件控制会话状态，服务端通过事件流返回响应内容、转录结果与状态通知。

## 支持的模型/功能

- **模型系列**：当前支持 `qwen3.5-omni-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime` 和 `qwen-omni-turbo-realtime`。各模型能力存在差异，详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中的参数兼容性说明。
- **[多模态](../concepts/multi-modal.md)输入**：支持 PCM 音频（16 kHz）和 JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256 KB）；图像需在首次 `input_audio_buffer.append` 后发送，且通过 `input_audio_buffer.commit` 统一提交。
- **[多模态](../concepts/multi-modal.md)输出**：支持 `["text"]` 或 `["text", "audio"]`（默认），音频为 24 kHz PCM 流；`qwen3-omni-flash-realtime` 系列额外支持 `smooth_output` 参数控制口语化/书面化风格。
- **语音活动检测（VAD）**：提供 `server_vad`（声学特征）和 `semantic_vad`（语义有效性，仅 `qwen3.5-omni-realtime` 系列支持）两种模式；Manual 模式下需客户端显式调用 `input_audio_buffer.commit` 和 `response.create`。
- **高级能力**：
  - 工具调用（`tools`）：仅 `qwen3.5-omni-realtime` 系列支持，模型返回结构化[函数调用](../concepts/function-calling.md)参数，客户端执行后需通过 `conversation.item.create` 回传结果。
  - 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，与 `tools` 互斥，不可同时启用。
  - 声音复刻：需先调用独立的 `qwen-voice-enrollment` 接口创建音色，再在 `session.update` 中通过 `voice` 字段指定使用；**音色绑定的 `target_model` 必须与 Omni 实时会话使用的模型完全一致**，否则合成失败 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：文档 1 与文档 5 对 `modalities` 的合法值描述存在不一致——文档 1 明确列出 `["text","audio"]` 为默认值且 `["audio"]` 单独存在未被提及；而文档 5 的 `error` 示例中指出 `["audio"]` 是非法组合，仅支持 `["text"]` 和 `["audio", "text"]`。以文档 5 的 `error` 示例为准，`["audio"]` 不被允许。

## 关键参数

所有会话级配置均通过 `session.update` 事件或 SDK 的 `update_session` 方法设置，参数按模型能力分组：

- **基础模态与音色**：
  - `modalities`: `["text"]` 或 `["text","audio"]`（必选，无 `["audio"]` 单独选项）。
  - `voice`: 音色名称，不同模型默认值不同（如 `qwen3.5-omni-realtime` 默认 `"Tina"`），自定义音色需通过声音复刻获取 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。
  - `input_audio_format` / `output_audio_format`: 固定为 `"pcm"`，对应 SDK 中的 `PCM_16000HZ_MONO_16BIT` / `PCM_24000HZ_MONO_16BIT`。

- **VAD 控制**（`turn_detection`）：
  - `type`: `"server_vad"`（默认）或 `"semantic_vad"`（仅 `qwen3.5-omni-realtime`）。
  - `threshold`: `[-1.0, 1.0]`，默认 `0.5`；值越低越灵敏。
  - `silence_duration_ms`: `[200, 6000]`，默认 `800`。
  - `idle_timeout_ms`: `[5000, 30000]`，**仅在 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 时生效**。

- **生成控制**（部分参数 `qwen-omni-turbo` 系列不支持修改）：
  - `temperature`: `[0, 2)`，默认值因模型而异（如 `qwen3.5-omni-realtime` 为 `0.7`）；与 `top_p` 二选一。
  - `top_p`: `(0, 1.0]`，默认值因模型而异（如 `qwen3.5-omni-realtime` 为 `0.8`）。
  - `top_k`: `≥0`，默认值因模型而异（如 `qwen3.5-omni-realtime` 为 `20`）；设为 `null` 或 `>100` 则禁用。
  - `max_tokens`: 截断输出长度，不影响生成过程；默认为模型最大输出长度。
  - `repetition_penalty`: `>0`，默认 `1.0`（`qwen3.5-omni-realtime`）或 `1.05`（其他）。
  - `presence_penalty`: `[-2.0, 2.0]`，默认 `1.5`（`qwen3.5-omni-realtime`）或 `0.0`（其他）。
  - `seed`: `0` 到 `2^31-1`，用于结果可复现，默认 `-1`。

- **高级功能开关**：
  - `enable_search`: `bool`，仅 `qwen3.5-omni-realtime` 系列有效，与 `tools` 互斥。
  - `search_options.enable_source`: `bool`，控制是否返回搜索来源。
  - `tools`: `function` 数组，定义可调用工具的 schema；仅 `qwen3.5-omni-realtime` 系列有效。

## 使用方式

1. **建立连接**：使用 WebSocket URL（推荐业务空间专属域名，如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`）连接，SDK 中调用 `connect()`。
2. **初始化会话**：连接后服务端返回 `session.created` 事件，包含默认配置；建议立即调用 `update_session()` 应用自定义参数（如 `voice`, `instructions`, `turn_detection`）。
3. **输入处理**：
   - **VAD 模式**（`enable_turn_detection=true`）：持续调用 `append_audio()` 发送音频片段，服务端自动检测起止并提交；无需手动 `commit()`。
   - **Manual 模式**（`enable_turn_detection=false`）：调用 `append_audio()` 后，必须调用 `commit()` 创建用户消息项；图像同理，通过 `append_video()` 添加。
4. **触发响应**：
   - VAD 模式下，服务端检测到语音结束自动触发响应。
   - Manual 模式下，`commit()` 后需显式调用 `create_response()`。
5. **工具调用处理**：收到 `response.function_call_arguments.done` 事件后，执行本地工具，再调用 `create_item()` 回传结果，并（在 Manual 模式下）再次调用 `create_response()`。
6. **接收输出**：监听 `response.audio.delta`（音频流）、`response.audio_transcript.delta`（ASR 中间结果）、`response.content_part.added`（文本流）等事件；最终以 `response.done` 结束。

## 限制和注意事项

- **音频/图像限制**：输入音频必须为 16 kHz PCM；图像仅支持 JPG/JPEG，Base64 编码后 ≤256 KB，建议分辨率 480p/720p；图像需与音频配合使用，不可单独提交。
- **并发与超时**：单个 WebSocket 连接为单会话；`idle_timeout_ms` 仅对特定模型+VAD 组合生效；`max_tokens` 仅截断输出，不中断生成。
- **参数兼容性**：`qwen-omni-turbo` 系列模型**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`；`smooth_output` 仅 `qwen3-omni-flash-realtime` 系列支持；`semantic_vad` 仅 `qwen3.5-omni-realtime` 系列支持。
- **互斥约束**：`tools` 与 `enable_search` 不可同时启用；`["audio"]` 作为 `modalities` 值非法，必须包含 `"text"`。
- **域名迁移**：强烈建议迁移到业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


