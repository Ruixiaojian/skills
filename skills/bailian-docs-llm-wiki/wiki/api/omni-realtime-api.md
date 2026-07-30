# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时[多模态](../concepts/multi-modal.md)交互接口，支持语音、文本、图像输入与文本+音频同步输出。它采用事件驱动模型，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态和数据流，服务端通过异步事件（如 `input_audio_buffer.speech_stopped`、`response.audio.delta`）实时反馈处理结果。该 API 专为低延迟、高互动性场景设计，适用于智能客服、语音助手等实时对话应用。

## 支持的模型/功能

- **核心模型系列**：  
  - `qwen3.5-omni-realtime`（含 `plus` 和 `flash` 变体）：支持 `semantic_vad`、联网搜索（`enable_search`）、工具调用（`tools`）及完整参数调节；  
  - `qwen3-omni-flash-realtime`：支持 `smooth_output` 风格控制、`server_vad` 及全部采样参数；  
  - `qwen-omni-turbo-realtime`：轻量级模型，**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等参数，仅支持默认配置 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。  

- **[多模态](../concepts/multi-modal.md)能力**：  
  - 输入：支持 PCM 音频（16 kHz）、JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256 KB）；  
  - 输出：支持 `["text"]` 或 `["text","audio"]` 模态组合，音频固定为 24 kHz PCM [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)；  
  - 工具调用：仅 `qwen3.5-omni-realtime` 系列支持，需显式配置 `tools` 数组，且与 `enable_search` 互斥 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。  

- **高级功能**：  
  - 声音复刻：通过 `qwen-voice-enrollment` 模型创建专属音色，**必须与 Omni 实时模型 `target_model` 严格一致**（如 `qwen3.5-omni-plus-realtime`），否则合成失败 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)；  
  - 主动引导：`idle_timeout_ms` 仅在 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 模式下生效，用于静默超时后触发上下文引导。

> **注意**：文档 1 和文档 2 中关于 `qwen-omni-turbo-realtime` 默认 `voice` 的描述存在矛盾——文档 1 写为 `"Chelsie"`，文档 2 写为 `"Chelsie"`（一致），但文档 4 的 Java SDK 示例中误标为 `"Chelsie"`（实际应为 `"Chelsie"`）。经核对，三处均指向 `"Chelsie"`，无实质性矛盾；但文档 1 中 `modalities` 示例值为 `["text","audio"]`，而文档 3 的 `session.created` 示例中 `modalities` 顺序为 `["text","audio"]`，符合规范，无需修正。

## 关键参数

| 参数 | 类型 | 说明 | 适用模型 | 默认值 |
|------|------|------|----------|--------|
| `modalities` | `array` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | 全系列 | `["text","audio"]` |
| `voice` | `string` | 音色名称，需与声音复刻 `target_model` 匹配 | 全系列 | `qwen3.5`: `"Tina"`；`qwen3-flash`: `"Cherry"`；`turbo`: `"Chelsie"` |
| `input_audio_format` / `output_audio_format` | `string` | 固定为 `"pcm"`，输入采样率 16 kHz，输出 24 kHz | 全系列 | `"pcm"` |
| `turn_detection.type` | `string` | `server_vad`（默认）或 `semantic_vad`（仅 `qwen3.5-omni-realtime`） | `qwen3.5-omni-realtime` 支持 `semantic_vad` | `"server_vad"` |
| `turn_detection.threshold` | `float` | VAD 灵敏度 [-1.0, 1.0] | 全系列 | `0.5` |
| `turn_detection.silence_duration_ms` | `integer` | 静音触发阈值 [200, 6000] ms | 全系列 | `800` |
| `idle_timeout_ms` | `integer` | 静默超时引导 [5000, 30000] ms | `qwen3.5-omni-plus-realtime` / `flash-realtime` + `server_vad` | — |
| `enable_search` | `boolean` | 启用联网搜索（与 `tools` 互斥） | `qwen3.5-omni-realtime` | `false` |
| `tools` | `array` | 工具定义列表，含 `function.name`、`description`、`parameters` | `qwen3.5-omni-realtime` | `[]` |
| `temperature` / `top_p` / `top_k` | `float`/`float`/`integer` | 采样控制参数，**建议只设其一**；`qwen-omni-turbo` 不可修改 | `qwen3.5`/`qwen3-flash` 支持；`turbo` 不支持 | 见各模型默认值表 |
| `max_tokens` | `integer` | 最大输出 token 数（截断，不影响生成过程） | `qwen3.5`/`qwen3-flash` 支持；`turbo` 不支持 | 模型最大输出长度 |

## 使用方式

1. **建立连接**：使用 WebSocket URL（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），替换 `{WorkspaceId}` 为实际业务空间 ID [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。  
2. **初始化会话**：连接后服务端返回 `session.created` 事件，包含默认配置；随后可立即调用 `update_session`（SDK）或发送 `session.update` 事件（原生）更新参数。  
3. **输入数据**：  
   - **VAD 模式**（推荐）：设置 `turn_detection.type = "server_vad"`，持续发送 `input_audio_buffer.append`，服务端自动检测起止并提交；  
   - **Manual 模式**：设置 `turn_detection = null`，由客户端控制节奏：`append_audio` → `commit` → `response.create` [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。  
4. **处理响应**：监听 `response.audio.delta`（流式音频）、`response.audio_transcript.delta`（ASR 中间结果）、`response.done`（完成）等事件；工具调用需在收到 `response.function_call_arguments.done` 后，回传 `conversation.item.create` 并再次 `response.create`。  
5. **音色复刻**：先调用 `qwen-voice-enrollment` 创建音色，再在 `session.update` 或 SDK `update_session` 中传入该 `voice` 字符串，**确保 `target_model` 与 Omni 实时模型完全一致** [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

## 限制和注意事项

- **音频/图像限制**：输入音频必须为 16 kHz PCM；图像仅支持 JPG/JPEG，Base64 编码后 ≤256 KB，建议分辨率 480p–720p [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。  
- **参数兼容性**：`tools` 与 `enable_search` 不可同时启用；`qwen-omni-turbo` 系列所有采样参数（`temperature`、`top_p` 等）均不可修改，强行设置将被忽略 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。  
- **地域与域名**：北京/新加坡地域必须使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等），旧域名（`dashscope.aliyuncs.com`）虽兼容但性能较低 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。  
- **错误处理**：服务端返回 `error` 事件时，需检查 `error.param`（如 `session.modalities`）定位问题；`input_audio_buffer.commit` 在缓冲区为空时会报错 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。  
- **资源管理**：调用 `close()` 或发送 `input_audio_buffer.clear` 后需重置本地状态；`cancel_response` 仅取消当前响应，不影响后续请求。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)



