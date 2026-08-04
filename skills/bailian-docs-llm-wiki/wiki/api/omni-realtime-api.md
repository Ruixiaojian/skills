# omni realtime api

Qwen-Omni-Realtime API 是一个基于 WebSocket 的实时多模态交互接口，支持语音输入、文本/音频输出、VAD 自动检测、工具调用与联网搜索（部分模型），适用于构建低延迟、高沉浸感的语音助手应用。其核心能力围绕会话生命周期管理、流式音视频处理和模型参数精细化控制展开。

## 支持的模型/功能

当前支持三类实时模型系列，功能与默认配置存在差异：

- **`qwen3.5-omni-realtime` 系列**：支持 `semantic_vad`、`enable_search`、`tools`、`presence_penalty=1.5`；默认 `temperature=0.7`, `top_p=0.8`, `top_k=20`。
- **`qwen3-omni-flash-realtime` 系列**：支持 `smooth_output`、`idle_timeout_ms`（需配合 `server_vad`）；默认 `voice="Cherry"`，`temperature=0.9`, `top_p=1.0`, `top_k=50`。
- **`qwen-omni-turbo-realtime` 系列**：仅支持 `["text","audio"]` 输出模态；**所有生成参数（`temperature`/`top_p`/`top_k`/`max_tokens`/`repetition_penalty`/`presence_penalty`/`seed`）均不支持修改**，默认 `voice="Chelsie"`，`temperature=1.0`, `top_p=0.01` [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

> **注意**：文档 2 中 `session.created` 示例显示 `model: "qwen3-omni-flash-realtime"`，但文档 1 和 3 均明确列出 `qwen3.5-omni-realtime` 为 `semantic_vad` 唯一支持模型；而文档 6 在声音复刻部分将 `qwen3.5-omni-plus-realtime` 列为可选驱动模型，该型号未在客户端/服务端事件文档中被显式描述其能力。实际使用时请以 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中对各参数的“仅在…时生效”约束为准。

除模型外，API 提供以下关键功能：
- **双模式语音交互**：`server_vad`（自动检测语音起止）与 `Manual`（客户端显式提交）两种模式，详见 [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
- **多模态输入**：支持 `input_audio_buffer.append`（PCM 16kHz）与 `input_image_buffer.append`（JPG/JPEG，≤256KB Base64 编码）。
- **工具调用（Function Calling）**：模型可自主触发[函数调用](../concepts/function-calling.md)，客户端通过 `conversation.item.create` 回传结果。
- **联网搜索（Search）**：仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 互斥。

## 关键参数

所有参数均通过 `session.update` 客户端事件或 SDK 的 `update_session` 方法配置。核心参数如下：

| 参数 | 类型 | 说明 | 模型限制 |
|------|------|------|----------|
| `modalities` | `["text"]` 或 `["text","audio"]` | 输出模态组合，`["audio"]` 单独不合法 | 全系列支持 |
| `voice` | `string` | 音色名称，如 `"Tina"`/`"Cherry"`/`"Chelsie"`；声音复刻生成的 `voice` ID 亦可传入 | 全系列支持 |
| `input_audio_format` / `output_audio_format` | `"pcm"` | 输入要求 16kHz PCM；输出固定为 24kHz PCM | 全系列强制 |
| `turn_detection.type` | `"server_vad"`（默认）或 `"semantic_vad"` | VAD 类型；后者仅 `qwen3.5-omni-realtime` 支持 | [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `turn_detection.threshold` | `float [-1.0, 1.0]` | VAD 灵敏度，值越低越易误触发 | 全系列支持 |
| `turn_detection.silence_duration_ms` | `int [200, 6000]` | 静音超时阈值，默认 800ms | 全系列支持 |
| `idle_timeout_ms` | `int [5000, 30000]` | 静默后主动引导响应，仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 生效 | 文档 1 & 3 一致 |
| `enable_search` | `boolean` | 启用联网搜索，与 `tools` 不兼容 | 仅 `qwen3.5-omni-realtime` |
| `tools` | `array` | 工具定义列表，含 `name`/`description`/`parameters` | 仅 `qwen3.5-omni-realtime` |
| `temperature` / `top_p` / `top_k` | `float`/`float`/`int` | 控制生成多样性，**建议只设其一**；`qwen-omni-turbo` 系列不可修改 | [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `max_tokens` | `int` | 响应截断长度，不影响生成过程 | `qwen-omni-turbo` 不可修改 |
| `smooth_output` | `boolean`/`null` | 仅 `qwen3-omni-flash-realtime` 支持，控制口语化程度 | 文档 1 & 3 一致 |

## 使用方式

1. **建立连接**：使用 WebSocket 连接到地域专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），[原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 强烈建议迁移至此以获得更高稳定性。
2. **初始化会话**：连接后服务端立即返回 `session.created` 事件，包含默认配置。
3. **配置会话**：发送 `session.update` 事件（或调用 SDK `update_session`）设置 `modalities`、`voice`、`turn_detection` 等参数。
4. **输入数据**：
   - VAD 模式：持续 `input_audio_buffer.append` 音频，服务端自动检测并提交。
   - Manual 模式：`append` 后必须 `input_audio_buffer.commit`，再发 `response.create` 触发响应。
   - 图像输入：`input_image_buffer.append` 后，由 `input_audio_buffer.commit` 一并提交。
5. **处理响应**：监听 `response.audio.delta`（流式音频）、`response.text.delta`（流式文本）、`response.done`（完成）等事件。
6. **工具调用**：收到 `response.function_call_arguments.done` 后，执行本地函数，再通过 `conversation.item.create` 回传结果，并（在 Manual 模式下）再次 `response.create`。

## 限制和注意事项

- **音频格式硬性要求**：输入必须为 16kHz PCM（单声道），输出固定为 24kHz PCM；图像仅支持 JPG/JPEG，Base64 编码后 ≤256KB。
- **参数互斥性**：`enable_search` 与 `tools` 不可同时启用；`qwen-omni-turbo` 系列所有生成参数锁定，无法覆盖。
- **VAD 模式依赖**：`input_audio_buffer.speech_started`/`speech_stopped` 事件仅在 `turn_detection.type` 非 `null` 时触发；`idle_timeout_ms` 仅在 `server_vad` + 特定模型下有效。
- **SDK 差异**：Python/Java SDK 将部分参数（如 `temperature`）封装在 `parameters` 字典中传递，而非顶层字段，需按 SDK 文档 [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 调用。
- **声音复刻集成**：复刻音色需与 Omni 模型严格匹配（如 `target_model="qwen3.5-omni-plus-realtime"`），否则合成失败；复刻本身是独立 API，不属于 Omni Realtime WebSocket 流程。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


