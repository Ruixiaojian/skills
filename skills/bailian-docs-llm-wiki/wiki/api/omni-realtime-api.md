# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时多模态交互接口，支持语音、文本、图像输入与文本、语音输出的端到端流式交互。它采用事件驱动模型，客户端通过发送结构化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态与数据流，服务端通过异步事件（如 `session.created`、`response.audio.delta`）实时反馈处理结果与生成内容。该 API 专为低延迟、高并发的语音助手、智能客服等场景设计。

## 支持的模型/功能

- **核心模型系列**：  
  - `qwen3.5-omni-realtime`（支持 `semantic_vad`、联网搜索、工具调用）  
  - `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`（支持 `idle_timeout_ms`、`smooth_output`）  
  - `qwen3-omni-flash-realtime`（默认音色 `Cherry`，支持 `smooth_output`）  
  - `qwen-omni-turbo-realtime`（默认音色 `Chelsie`，**不支持修改多数采样参数**）  

- **多模态能力**：  
  - 输入：PCM 音频（16 kHz）、JPG/JPEG 图像（≤1080p，Base64 编码 ≤256 KB）、实时视频帧（通过 `append_video`）  
  - 输出：文本 + PCM 音频（24 kHz），可单独禁用任一模态（`modalities: ["text"]`）  
  - 实时转录：内置 `qwen3-asr-flash-realtime` 模型，不可替换，支持 `conversation.item.input_audio_transcription.delta` 增量预览 [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)  

- **高级功能**：  
  - 语音活动检测（VAD）：`server_vad`（声学）或 `semantic_vad`（语义，仅 `qwen3.5-omni-realtime` 支持）  
  - 工具调用（Function Calling）：定义 `tools` 后模型自主触发，需客户端回传结果并调用 `response.create` [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)  
  - 联网搜索：`enable_search: true`（仅 `qwen3.5-omni-realtime` 系列），与 `tools` **互斥**  
  - 声音复刻：需先调用 `qwen-voice-enrollment` 创建音色，再在 `session.update` 中指定 `voice` 参数 [原文标题](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)  

> **注意**：文档 1 和文档 2 对 `voice` 默认值描述存在细微差异——文档 1 明确 `qwen3.5-omni-realtime` 默认为 `Tina`，而文档 2 的 `session.created` 示例中 `model` 字段为 `qwen3-omni-flash-realtime` 且 `voice` 为 `Cherry`。实际默认值严格按模型系列区分，以文档 1 和 SDK 文档（文档 3、4）为准。

## 关键参数

所有配置均通过 `session.update` 事件或 SDK 的 `update_session()` 方法设置：

| 参数 | 类型 | 说明 | 限制 |
|------|------|------|------|
| `modalities` | `["text"]` 或 `["text","audio"]` | 输出模态组合 | 不支持 `["audio"]` 单独输出 |
| `voice` | `string` | 音色名 | 必须是[音色列表](https://help.aliyun.com/zh/model-studio/realtime#f9c68d860a3rs)中的有效值；声音复刻生成的音色亦可传入 |
| `input_audio_format` / `output_audio_format` | `"pcm"` | 音频编解码格式 | 固定为 PCM；输入采样率 16 kHz，输出 24 kHz，**不可自定义** |
| `instructions` | `string` | 系统角色指令 | 影响模型行为，建议明确限定职责与边界 |
| `turn_detection.type` | `"server_vad"` 或 `"semantic_vad"` | VAD 类型 | `semantic_vad` 仅 `qwen3.5-omni-realtime` 支持；设为 `null` 则启用 Manual 模式 |
| `turn_detection.threshold` | `float [-1.0, 1.0]` | VAD 灵敏度 | 默认 `0.5`；嘈杂环境建议调高（如 `0.7`） |
| `turn_detection.silence_duration_ms` | `int [200, 6000]` | 静音触发阈值 | 默认 `800` ms；值越小响应越快但误触发风险越高 |
| `idle_timeout_ms` | `int [5000, 30000]` | 静默超时（主动引导） | **仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 有效** |
| `enable_search` | `boolean` | 启用联网搜索 | 仅 `qwen3.5-omni-realtime` 系列有效；与 `tools` 冲突，不可共存 |
| `tools` | `array` | 工具函数定义 | 每个工具含 `name`、`description`、`parameters`（含 `properties` 和 `required`）；`parameters.type` 固定为 `"object"` |

**采样参数（模型级）**：  
- `temperature` / `top_p`：二选一控制多样性（`qwen-omni-turbo` 系列**不可修改**）  
- `top_k`：候选集大小（`qwen-omni-turbo` 系列**不可修改**）  
- `max_tokens`：响应截断长度（不影响生成过程）  
- `repetition_penalty` / `presence_penalty` / `seed`：重复控制与确定性（`qwen-omni-turbo` 系列**不可修改**）  

## 使用方式

1. **建立连接**：  
   - WebSocket URL 格式：`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`（推荐业务空间专属域名，替代旧 `dashscope.aliyuncs.com`）  
   - 连接后立即收到 `session.created` 事件，含默认配置 [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)  

2. **配置会话**：  
   - 发送 `session.update` 事件（或调用 SDK `update_session()`），传入所需参数。成功后服务端返回 `session.updated`。  

3. **输入数据**：  
   - **音频**：持续发送 `input_audio_buffer.append`（Base64 PCM），VAD 模式下由服务端自动提交；Manual 模式下需显式发送 `input_audio_buffer.commit`。  
   - **图像**：发送 `input_image_buffer.append`（Base64 JPG/JPEG），**必须在首次 `input_audio_buffer.append` 之后**，且与音频缓冲区一同提交。  

4. **触发响应**：  
   - **VAD 模式**：语音结束自动触发，无需客户端操作。  
   - **Manual 模式**：发送 `input_audio_buffer.commit` 后，再发送 `response.create`。  
   - **工具调用后**：客户端执行工具并发送 `conversation.item.create`，再发 `response.create`（Manual 模式）或等待服务端自动触发（VAD 模式）。  

5. **处理输出**：  
   - 文本流：`response.text.delta` → `response.text.done`  
   - 音频流：`response.audio.delta` → `response.audio.done`  
   - 转录流：`conversation.item.input_audio_transcription.delta`（拼接 `text` + `stash` 获取实时预览）→ `conversation.item.input_audio_transcription.completed`（最终结果）  

## 限制和注意事项

- **协议与兼容性**：  
  - 必须使用 WebSocket，HTTP REST 不支持。  
  - `qwen-omni-turbo-realtime` 系列**禁止修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`（文档 1、3、4 均明确标注）。  

- **资源约束**：  
  - 单张图片 Base64 编码后 ≤ 256 KB；音频缓冲区最大 15 MiB（Manual 模式）；声音复刻音频 ≤ 60 秒且 < 10 MB。  
  - `idle_timeout_ms` 仅对特定模型+VAD 组合生效，其他组合设置将被忽略。  

- **关键互斥规则**：  
  - `tools` 与 `enable_search` **不可同时启用**，否则 `session.update` 将返回 `invalid_request_error`。  
  - `smooth_output` **仅对 `qwen3-omni-flash-realtime` 有效**，其他模型设置将被忽略（文档 1、3、4 一致）。  

- **错误处理**：  
  - 所有错误均以 `error` 事件返回，含 `type`、`code`、`message`、`param` 字段，例如 `invalid_value` 错误会明确指出违规参数（如 `session.modalities`） [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)。  
  - `input_audio_buffer.commit` 在缓冲区为空时返回错误；`response.cancel` 在无进行中响应时返回错误。  

- **最佳实践**：  
  - VAD 模式推荐使用耳机避免回声打断；Manual 模式适用于“按住说话”类 UI。  
  - 声音复刻音色必须与 Omni 模型版本严格匹配（如 `qwen3.5-omni-plus-realtime` 复刻的音色只能用于同系列模型）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


