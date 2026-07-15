# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的全模态实时交互接口，支持文本、音频、图像多模态输入与文本+音频双模态输出，适用于语音助手、智能客服等低延迟对话场景。其核心能力包括实时语音识别（ASR）、大模型流式推理、TTS 音频合成、工具调用（Function Calling）及可选的联网搜索，所有交互均通过事件驱动模型完成。

## 支持的模型/功能

- **模型系列**：当前支持 `qwen3.5-omni-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime` 和 `qwen-omni-turbo-realtime`。各模型在 VAD 类型、参数可调性、音色默认值等方面存在差异，详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **多模态输入**：支持 PCM 音频（16 kHz）和 JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256 KB），图像需在首次音频追加后发送。
- **多模态输出**：支持 `["text"]` 或 `["text", "audio"]` 输出模态；音频输出固定为 24 kHz PCM，不可自定义采样率。
- **语音活动检测（VAD）**：提供 `server_vad`（声学检测）和 `semantic_vad`（语义检测，仅 `qwen3.5-omni-realtime` 支持）两种模式，支持静默超时（`idle_timeout_ms`）主动引导对话。
- **高级功能**：
  - 工具调用（`tools`）：模型自主触发函数并返回参数，客户端执行后需回传结果并调用 `response.create`。
  - 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，与 `tools` 不兼容。
  > **注意**：文档 5 中提到的声音复刻功能（`qwen-voice-enrollment`）属于独立服务，需先创建音色再在 `session.update` 中通过 `voice` 参数引用，其模型绑定要求（如 `target_model` 必须与 Omni 模型一致）在 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md) 中有明确约束。

## 关键参数

所有会话级配置均通过 `session.update` 事件或 SDK 的 `update_session` 方法设置，关键参数如下：

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `modalities` | `array` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` | `string` | TTS 音色名 | `qwen3.5`: `"Tina"`；`qwen3-flash`: `"Cherry"`；`qwen-turbo`: `"Chelsie"` |
| `input_audio_format` / `output_audio_format` | `string` | 固定为 `"pcm"`；输入需 16 kHz，输出为 24 kHz | — |
| `instructions` | `string` | 系统提示词，定义角色与行为边界 | — |
| `turn_detection.type` | `string` | `server_vad`（默认）或 `semantic_vad`（仅 `qwen3.5-omni-realtime`） | `server_vad` |
| `turn_detection.threshold` | `float` | VAD 灵敏度 [-1.0, 1.0] | `0.5` |
| `turn_detection.silence_duration_ms` | `int` | 静音触发阈值 [200, 6000] ms | `800` |
| `enable_search` | `boolean` | 启用联网搜索（仅 `qwen3.5-omni-realtime`） | `false` |
| `tools` | `array` | 工具定义列表，`type` 固定为 `"function"` | `[]` |
| `temperature` / `top_p` / `top_k` | `float`/`float`/`int` | 采样控制参数；`qwen-omni-turbo` 系列不支持修改 | 见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 表格 |
| `max_tokens` | `int` | 响应最大 token 数（截断，不影响生成过程） | 模型最大输出长度 |
| `repetition_penalty` / `presence_penalty` | `float` | 重复惩罚参数；`qwen-omni-turbo` 系列不支持修改 | 见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 表格 |

> **注意**：`smooth_output` 参数仅对 `qwen3-omni-flash-realtime` 生效，且文档 1 与文档 3、4 在默认值描述上存在不一致——文档 1 称 `true` 为默认值，而文档 3、4 明确标注 `null`（自动选择）为默认值。实际行为以 SDK 实现为准，建议显式设置。

## 使用方式

1. **建立连接**：使用 WSS 协议连接业务空间专属域名（推荐），格式为 `wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`，其中 `{WorkspaceId}` 为控制台获取的业务空间 ID。
2. **初始化会话**：连接后服务端立即返回 `session.created` 事件，含默认配置。随后调用 `session.update`（或 SDK `update_session`）覆盖默认参数。
3. **输入处理**：
   - **VAD 模式**（`enable_turn_detection=true`）：持续 `input_audio_buffer.append` 音频，服务端自动检测起止并提交；可选 `input_image_buffer.append` 图像。
   - **Manual 模式**（`enable_turn_detection=false`）：手动 `append` 后必须 `input_audio_buffer.commit` 提交。
4. **触发响应**：
   - VAD 模式下，语音停止后服务端自动触发 `response.create`。
   - Manual 模式或工具调用后，需显式发送 `response.create`。
5. **处理响应**：监听 `response.content_part.added`（文本增量）、`response.audio.delta`（音频增量）、`response.done`（完成）等事件。
6. **工具调用流程**：收到 `conversation.item.created`（`type="function_call"`）→ 执行本地函数 → 发送 `conversation.item.create`（`type="function_call_output"`）→ 发送 `response.create`。

SDK 封装了上述流程，Python 使用 `OmniRealtimeConversation` 类，Java 使用 `OmniRealtimeConversation` 类，二者均提供 `append_audio`、`commit`、`create_response` 等方法，详细用法见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。

## 限制和注意事项

- **音频限制**：输入音频必须为 16 kHz PCM；单次 `append_audio` 数据量无硬限制，但缓冲区总大小建议 ≤15 MiB（文档 3、4 明确提及）。
- **图像限制**：仅 JPG/JPEG；Base64 编码后 ≤256 KB；建议分辨率 480p/720p；发送频率 ≤1 张/秒。
- **参数兼容性**：
  - `tools` 与 `enable_search` 互斥，不可同时启用。
  - `qwen-omni-turbo-realtime` 系列模型**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`（文档 1、3、4 均强调）。
- **VAD 行为**：`semantic_vad` 仅 `qwen3.5-omni-realtime` 支持；`idle_timeout_ms` 仅在 `server_vad` + `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` 下生效。
- **错误处理**：服务端返回 `error` 事件（如 `invalid_request_error`），需检查 `param` 字段定位问题，例如 `modalities` 值必须为 `["text"]` 或 `["text","audio"]`（文档 2 示例明确指出错误消息）。
- **域名迁移**：旧域名（如 `dashscope.aliyuncs.com`）仍可用，但百炼官方强烈推荐迁移到业务空间专属域名以获得更高性能与稳定性（文档 3、4、5 均强调）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


