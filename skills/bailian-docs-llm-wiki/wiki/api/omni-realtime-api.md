# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的低延迟[多模态](../concepts/multi-modal.md)实时交互接口，支持语音输入、文本/音频输出、VAD 自动断句、[工具调用](../concepts/tool-use.md)与联网搜索（部分模型）。它面向对话式 AI 应用场景，如智能客服、虚拟助手和实时音视频交互系统。

## 支持的模型与功能

- **核心模型系列**：
  - `qwen3.5-omni-realtime`：支持 `semantic_vad`、`enable_search`、完整[工具调用](../concepts/tool-use.md)（`tools`）及高精度[多模态](../concepts/multi-modal.md)理解。
  - `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`：支持 `idle_timeout_ms` 静默超时主动引导，但不支持 `semantic_vad`；`flash` 版本独有 `smooth_output` 参数控制口语化程度。
  - `qwen3-omni-flash-realtime`：默认音色为 `Cherry`，支持 `server_vad` 和完整生成参数调节（除 `qwen-omni-turbo` 系列外）。
  - `qwen-omni-turbo-realtime`：默认音色为 `Chelsie`，**所有生成参数（`temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`）均不可修改**，仅支持基础配置 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

- **关键功能**：
  - 双模态输出：支持 `["text"]` 或 `["text", "audio"]`（默认），音频格式固定为 `pcm`（输入 16 kHz，输出 24 kHz）。
  - VAD 模式（`server_vad` 或 `semantic_vad`）与 Manual 模式并存，前者自动检测语音起止，后者需显式调用 `input_audio_buffer.commit` 和 `response.create` [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
  - [工具调用](../concepts/tool-use.md)（`tools`）与联网搜索（`enable_search`）**互斥**，不可同时启用；二者均仅对 `qwen3.5-omni-realtime` 系列生效。
  - 声音复刻支持：需通过独立 `qwen-voice-enrollment` 模型创建音色，并在 Omni Realtime 调用中指定 `target_model` 一致的 `voice` 参数 [原文标题](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：文档 1 中 `qwen-omni-turbo-realtime` 的 `temperature` 默认值标为 `1.0`，而文档 2 和 3 在 Python/Java SDK 参数说明中均明确指出该系列模型“**不支持修改**”所有采样参数。实际使用中应以 SDK 文档为准——即 `qwen-omni-turbo-realtime` 的生成参数为只读，传入将被忽略。

## 关键参数

所有会话级参数均通过 `session.update` 事件或 SDK 的 `update_session()` 方法设置，以下为通用核心字段：

| 参数 | 类型 | 说明 | 适用模型 | 默认值 |
|------|------|------|----------|--------|
| `modalities` | `string[]` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | 全系列 | `["text","audio"]` |
| `voice` | `string` | 音色名称 | 全系列 | `Tina`（3.5）、`Cherry`（3-Flash）、`Chelsie`（Turbo） |
| `input_audio_format` / `output_audio_format` | `string` | 固定为 `"pcm"`，采样率分别为 16 kHz / 24 kHz | 全系列 | `"pcm"` |
| `instructions` | `string` | 系统角色提示词 | 全系列 | — |
| `turn_detection.type` | `string` | `server_vad`（默认）或 `semantic_vad`（仅 3.5 支持） | 3.5 支持 `semantic_vad`，其余仅 `server_vad` | `"server_vad"` |
| `turn_detection.threshold` | `float` | VAD 灵敏度 [-1.0, 1.0] | 全系列 | `0.5` |
| `turn_detection.silence_duration_ms` | `int` | 静音触发响应阈值 [200, 6000] ms | 全系列 | `800` |
| `turn_detection_param.idle_timeout_ms` | `int` | 静默后主动引导时间 [5000, 30000] ms | 仅 `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime` + `server_vad` | — |
| `enable_search` | `boolean` | 启用联网搜索 | 仅 `qwen3.5-omni-realtime` | `false` |
| `search_options.enable_source` | `boolean` | 返回搜索来源 | 同上 | `false` |
| `tools` | `object[]` | 工具定义列表 | 仅 `qwen3.5-omni-realtime` | `[]` |
| `temperature` / `top_p` / `top_k` | `float` / `float` / `int` | 采样控制（二选一推荐） | `qwen3.5-omni-realtime`、`qwen3-omni-flash-realtime`；`turbo` 系列不可改 | 见各模型文档 |
| `max_tokens` | `int` | 最大输出 token 数（截断） | `qwen3.5-omni-realtime`、`qwen3-omni-flash-realtime`；`turbo` 不可改 | 模型最大输出长度 |
| `repetition_penalty` / `presence_penalty` | `float` | 重复惩罚 | `qwen3.5-omni-realtime`、`qwen3-omni-flash-realtime`；`turbo` 不可改 | 各模型不同 |

> **注意**：`smooth_output` 为 `qwen3-omni-flash-realtime` 独有布尔参数，控制回复风格（`true`=口语化，`false`=书面化，`null`=自动选择），文档 1 与文档 2/3 描述一致，无矛盾。

## 使用方式

1. **建立连接**：  
   使用 WebSocket 连接到地域专属 endpoint（推荐）：  
   - 北京：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`  
   - 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`  
   （`{WorkspaceId}` 从百炼控制台获取；旧域名 `dashscope.aliyuncs.com` 仍可用但非推荐）

2. **初始化会话**：  
   连接后服务端立即返回 `session.created` 事件，含默认配置。随后可发送 `session.update` 事件（或调用 SDK `update_session()`）覆盖默认值。

3. **输入处理**：  
   - **VAD 模式**（`enable_turn_detection=true`）：持续 `append_audio()`，服务端自动检测并提交，无需 `commit()`。  
   - **Manual 模式**（`enable_turn_detection=false`）：`append_audio()` → `commit()` → `create_response()` 触发响应。

4. **工具调用流程**：  
   - 模型返回 `response.function_call_arguments.done` → 客户端执行工具 → `conversation.item.create` 提交结果 → （VAD 模式下自动触发响应；Manual 模式需再次 `create_response()`）。

5. **响应消费**：  
   监听 `response.audio.delta`（流式音频）、`response.audio_transcript.delta`（实时 ASR）、`response.content_part.added`（文本）等事件，最终以 `response.done` 结束。

## 限制和注意事项

- **音频限制**：输入音频必须为 16 kHz PCM；单次 `append_audio()` 数据无硬上限，但缓冲区总大小建议 ≤15 MiB（SDK 文档提及）；图片输入仅支持 JPG/JPEG，Base64 编码后 ≤256 KB，分辨率建议 480p–720p。
- **并发与配额**：WebSocket 连接数、每秒事件吞吐量、音频流持续时长受百炼平台配额限制，具体请查阅控制台用量监控。
- **错误处理**：服务端返回 `error` 事件（如 `invalid_request_error`），需检查 `param` 字段定位问题（例如 `session.modalities` 值非法）。
- **音色一致性**：声音复刻创建的 `voice` 必须与 Omni 调用的 `model` 严格匹配（如 `qwen3.5-omni-plus-realtime` 创建的音色，只能用于同名模型），否则合成失败。
- **VAD 模式依赖**：`input_audio_buffer.speech_started` / `speech_stopped` 事件仅在 `turn_detection.type` 非 `null` 时触发；`idle_timeout_ms` 仅在 `server_vad` + 特定 3.5 子型号下生效。
- **SDK 版本要求**：Python SDK ≥1.25.17，Java SDK ≥2.22.15，否则可能缺失 `turn_detection_param` 或 `smooth_output` 等新参数支持。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


