# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时多模态交互接口，支持语音输入、文本/音频输出、VAD 自动检测、工具调用与联网搜索（部分模型）。它面向低延迟对话场景，需通过长连接维持会话状态，并通过结构化事件流（如 `session.update`、`input_audio_buffer.append`、`response.done`）驱动双向交互。

## 支持的模型与功能

- **核心模型系列**：
  - `qwen3.5-omni-realtime`：支持 `semantic_vad`、`enable_search`、完整工具调用（`tools`）、高自由度采样参数（`temperature`/`top_p`/`top_k`/`presence_penalty` 等可调）。
  - `qwen3-omni-flash-realtime`：默认音色 `Cherry`，支持 `smooth_output` 控制口语化程度，`server_vad` 模式下支持 `idle_timeout_ms`。
  - `qwen-omni-turbo-realtime`：默认音色 `Chelsie`，**多数生成参数不可修改**（如 `temperature`、`top_p`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`），仅支持基础配置 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
  
- **多模态能力**：
  - 输入：支持 PCM 音频（16 kHz）和 JPG/JPEG 图像（≤1080p，Base64 编码 ≤256KB）。
  - 输出：支持 `["text"]` 或 `["text","audio"]`，音频为 24 kHz PCM [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
  - 实时转录：内置 `qwen3-asr-flash-realtime` 模型，通过 `conversation.item.input_audio_transcription.delta` 提供增量识别结果 [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

- **高级功能**：
  - **VAD 模式**（`turn_detection.type = "server_vad"` 或 `"semantic_vad"`）：服务端自动检测语音起止并提交消息；`semantic_vad` 仅 `qwen3.5-omni-realtime` 支持。
  - **Manual 模式**（`turn_detection = null`）：客户端显式控制 `input_audio_buffer.commit` 和 `response.create`。
  - **工具调用**：模型自主触发[函数调用](../concepts/function-calling.md)，客户端回传结果后需发送 `response.create` 触发最终响应（Manual 模式下必须）[原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
  - **联网搜索**：仅 `qwen3.5-omni-realtime` 支持 `enable_search: true`，且与 `tools` 不兼容（不可同时启用）。

> **注意**：文档 1 与文档 2 对 `presence_penalty` 默认值描述存在矛盾——文档 1 称 `qwen3.5-omni-realtime` 默认为 `1.5`，而文档 2 在 `session.created` 示例中给出 `0.0`。以文档 1 为准，因其在参数说明章节明确列出各模型默认值；文档 2 的示例可能为旧快照或特定配置。

## 关键参数

所有可配置参数均通过 `session.update` 事件（或 SDK 的 `update_session` 方法）传递，嵌套于 `session` 对象内：

| 参数 | 类型 | 说明 | 限制与备注 |
|------|------|------|------------|
| `modalities` | `string[]` | 输出模态，`["text"]` 或 `["text","audio"]` | 默认 `["text","audio"]`；`["audio"]` 单独不合法 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `voice` | `string` | 音色名称 | 默认值按模型区分：`qwen3.5-omni-realtime`→`Tina`，`qwen3-omni-flash-realtime`→`Cherry`，`qwen-omni-turbo-realtime`→`Chelsie` |
| `input_audio_format` / `output_audio_format` | `string` | 音频格式 | 固定为 `"pcm"`；输入要求 16 kHz，输出为 24 kHz，**不可自定义采样率** |
| `instructions` | `string` | 系统角色提示词 | 用于设定模型行为边界，如客服、助理等角色 |
| `turn_detection` | `object` | VAD 配置 | `type`: `"server_vad"`（默认）或 `"semantic_vad"`（仅 `qwen3.5-omni-realtime`）；`threshold`: [-1.0, 1.0]；`silence_duration_ms`: [200, 6000]；`idle_timeout_ms`: [5000, 30000]（仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad`） |
| `enable_search` | `boolean` | 启用联网搜索 | 仅 `qwen3.5-omni-realtime` 有效；启用后 `tools` 必须为空 |
| `tools` | `object[]` | 工具定义列表 | 每个工具含 `function.name`、`function.description`、`function.parameters`（含 `properties` 和 `required`）；仅 `qwen3.5-omni-realtime` 有效 |
| `temperature` / `top_p` / `top_k` | `number` / `number` / `integer` | 采样控制 | 三者互斥建议只设其一；`qwen-omni-turbo` 系列**不支持修改** |
| `max_tokens` | `integer` | 最大输出 token 数 | 超限则截断；不影响生成过程；各模型最大值见官方模型列表 |
| `repetition_penalty` / `presence_penalty` | `number` | 重复惩罚 | `qwen-omni-turbo` 系列**不支持修改**；`presence_penalty` 范围 [-2.0, 2.0] |
| `seed` | `integer` | 随机种子 | 取值 [0, 2³¹−1]，默认 `-1`；`qwen-omni-turbo` 系列**不支持修改** |

## 使用方式

1. **建立 WebSocket 连接**：使用业务空间专属域名（推荐），如北京地域 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime` [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。
2. **初始化会话**：连接后服务端立即返回 `session.created` 事件，含默认配置。
3. **配置会话**：发送 `session.update` 事件（或调用 SDK `update_session`）设置 `modalities`、`voice`、`instructions` 等参数。
4. **输入数据**：
   - 音频：持续发送 `input_audio_buffer.append`（Base64 PCM 数据）；
   - 图像：发送 `input_image_buffer.append`（Base64 JPG/JPEG）；
   - 提交：VAD 模式下服务端自动 `commit`；Manual 模式下客户端主动发送 `input_audio_buffer.commit`。
5. **触发响应**：
   - VAD 模式：服务端检测到语音结束自动开始生成；
   - Manual 模式：客户端发送 `response.create` 显式触发。
6. **处理响应**：监听 `response.content_part.added`（文本流）、`response.audio.delta`（音频流）、`response.done`（完成）等事件。
7. **工具调用**：收到 `conversation.item.created`（`type="function_call"`）后，执行本地工具，再发送 `conversation.item.create` 回传结果，最后（Manual 模式下）发送 `response.create`。

## 限制和注意事项

- **模型能力隔离**：`qwen-omni-turbo-realtime` 系列**不支持修改** `temperature`、`top_p`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等参数，SDK 中设置将被忽略。
- **功能互斥**：`enable_search` 与 `tools` 不可同时启用，否则服务端返回 `invalid_request_error`。
- **VAD 模式依赖**：`semantic_vad` 仅 `qwen3.5-omni-realtime` 支持；`idle_timeout_ms` 仅在 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 下生效。
- **音频格式硬性约束**：输入必须为 16 kHz PCM，输出固定为 24 kHz PCM；图像仅支持 JPG/JPEG，单图 Base64 编码 ≤256KB。
- **连接稳定性**：推荐使用业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（如 `wss://dashscope.aliyuncs.com`）虽兼容但性能与稳定性较低 [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
- **错误处理**：服务端通过 `error` 事件返回结构化错误（含 `type`、`code`、`message`、`param`），需在客户端监听并解析，例如 `Invalid modalities` 错误会明确指出 `param: "session.modalities"`。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


