# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的低延迟多模态实时交互接口，支持语音输入、文本/音频输出、VAD 自动断句、工具调用与联网搜索（部分模型）。它面向语音助手、智能客服等实时对话场景，核心为事件驱动的双向流式通信。

## 支持的模型/功能

- **主流模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`。其中 `qwen3.5-omni-realtime` 系列（如 `qwen3.5-omni-plus-realtime`）是唯一支持 `semantic_vad` 和 `enable_search` 的模型 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **多模态输出**：支持 `["text"]` 或 `["text", "audio"]`，不支持纯音频输出；`audio` 输出需配合 `voice` 参数指定音色（默认值因模型而异：`Tina`/`Cherry`/`Chelsie`）。
- **语音活动检测（VAD）**：提供 `server_vad`（声学检测）和 `semantic_vad`（语义检测，仅 `qwen3.5-omni-realtime` 系列支持）两种模式 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。
- **扩展能力**：
  - 工具调用（`tools`）：模型可自主触发[函数调用](../concepts/function-calling.md)，适用于天气查询、时间获取等场景；
  - 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 互斥；
  - 声音复刻：需先调用 `qwen-voice-enrollment` 创建音色，再在 `session.update` 中通过 `voice` 字段传入 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：文档 2 中 `session.created` 事件示例显示 `input_audio_format` 和 `output_audio_format` 固定为 `"pcm"` 且采样率不可配置，但文档 1 明确说明 `audio.input.format.sample_rate` 和 `audio.output.format.sample_rate` 支持 `8000/16000/24000/48000`，且文档 3、4 的 SDK 均提供 `AudioFormatConfig` 接口。实际以 SDK 和文档 1 的嵌套字段为准，`input_audio_format`/`output_audio_format` 为历史兼容字段，**新增接入必须使用 `audio.input.format` 和 `audio.output.format`**。

## 关键参数

所有参数均通过 `session.update` 事件或 SDK 的 `update_session` 方法配置，分为以下几类：

| 类别 | 参数名 | 说明 | 取值范围/示例 | 模型限制 |
|--------|---------|------|----------------|-----------|
| **基础配置** | `model` | 模型名称 | `"qwen3.5-omni-flash-realtime"` | 必填，连接后不可变更 |
| | `modalities` | 输出模态 | `["text", "audio"]` | 仅支持该组合或 `["text"]` |
| | `voice` | 音色ID | `"Tina"` | 默认值依模型而定 |
| **音频格式** | `audio.input.format.type` | 输入编码格式 | `"pcm"` 或 `"wav"` | 所有支持音频的模型 |
| | `audio.input.format.sample_rate` | 输入采样率 | `8000`, `16000`(默认), `24000`, `48000` | 同上 |
| | `audio.output.format.type` | 输出编码格式 | `"pcm"` 或 `"wav"` | 同上 |
| | `audio.output.format.sample_rate` | 输出采样率 | `8000`, `16000`, `24000`(默认), `48000` | 同上 |
| **VAD** | `turn_detection.type` | VAD类型 | `"server_vad"`(默认) 或 `"semantic_vad"` | `semantic_vad` 仅 `qwen3.5-omni-realtime` 系列支持 |
| | `turn_detection.threshold` | 灵敏度阈值 | `[-1.0, 1.0]`，默认 `0.5` | — |
| | `turn_detection.silence_duration_ms` | 静音触发时长 | `[200, 6000]`，默认 `800` | — |
| | `idle_timeout_ms` | 静默超时（主动引导） | `[5000, 30000]` | 仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 有效 |
| **生成控制** | `temperature` / `top_p` | 多样性控制 | `temperature∈[0,2)`；`top_p∈(0,1.0]` | **二者选一设置**；`qwen-omni-turbo` 系列不可修改 |
| | `max_tokens` | 最大输出[Token](../concepts/token.md)数 | ≥0，截断而非终止生成 | `qwen-omni-turbo` 不可修改 |
| | `repetition_penalty` | 重复惩罚 | >0，默认 `1.0`/`1.05` | `qwen-omni-turbo` 不可修改 |
| | `presence_penalty` | 全局重复惩罚 | `[-2.0, 2.0]`，默认 `1.5`/`0.0` | `qwen-omni-turbo` 不可修改 |
| **高级功能** | `enable_search` | 启用联网搜索 | `true`/`false` | 仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 互斥 |
| | `tools` | 工具定义列表 | 数组，每个含 `function.name`/`description`/`parameters` | 同上 |

## 使用方式

1. **建立连接**：使用 WSS 协议连接业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 均封装了 `connect()` 方法。
2. **初始化会话**：连接后服务端返回 `session.created` 事件，随后应立即调用 `update_session` 发送 `session.update` 事件配置参数（如 `modalities`, `voice`, `turn_detection`）。
3. **输入数据**：
   - **VAD 模式**（推荐）：持续 `append_audio()`，服务端自动检测 `speech_started`/`speech_stopped` 并提交缓冲区，无需手动 `commit()`。
   - **Manual 模式**：`append_audio()` 后显式调用 `commit()` 创建用户消息项，再调用 `create_response()` 触发响应。
4. **处理响应**：监听 `response.audio.delta`（流式音频）、`response.text.delta`（流式文本）、`conversation.item.input_audio_transcription.delta`（ASR 实时结果）等事件。
5. **工具调用**：当收到 `conversation.item.created` 且 `item.type === "function_call"` 时，执行本地函数，再通过 `conversation.item.create` 回传结果，最后调用 `create_response()` 获取最终回复。

## 限制和注意事项

- **音频限制**：输入音频需为单声道 PCM/WAV，采样率建议 `16kHz`；图片输入仅支持 JPG/JPEG，Base64 编码后 ≤256KB，分辨率建议 480p–720p。
- **并发与超时**：单个 WebSocket 连接对应一个会话；`idle_timeout_ms` 仅在 `server_vad` 模式下生效，且计时从模型音频播放完毕开始。
- **互斥约束**：`tools` 和 `enable_search` 不可同时启用；`qwen-omni-turbo` 系列模型的 `temperature`/`top_p`/`max_tokens` 等参数**完全不可修改**，SDK 文档中相关说明为通用模板，实际调用将被忽略。
- **错误处理**：服务端通过 `error` 事件返回结构化错误（含 `type`, `code`, `message`, `param`），例如 `invalid_value` 错误会明确指出非法参数路径（如 `"session.modalities"`）。
- **SDK 差异**：Python SDK 的 `smooth_output` 参数仅对 `qwen3-omni-flash-realtime` 生效，Java SDK 需通过 `parameters` Map 设置；所有 SDK 均要求 `enable_turn_detection` 与 VAD 模式严格匹配（`true` 对应 VAD，`false` 对应 Manual）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


