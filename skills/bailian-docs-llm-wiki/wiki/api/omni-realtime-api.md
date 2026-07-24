# omni realtime api

Qwen-Omni-Realtime API 是一个基于 WebSocket 的实时[多模态](../concepts/multi-modal.md)交互接口，支持语音输入、文本/音频输出、实时转录、工具调用与 VAD 自动检测。它面向低延迟语音对话场景，要求客户端维持长连接并按事件驱动模型处理双向流式数据。

## 支持的模型/功能

- **核心模型系列**：
  - `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`：支持 `semantic_vad`、联网搜索（`enable_search`）、自定义 `idle_timeout_ms`；
  - `qwen3-omni-flash-realtime`：默认音色为 `"Cherry"`，支持 `smooth_output` 参数控制口语化程度；
  - `qwen-omni-turbo-realtime`：默认音色为 `"Chelsie"`，**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty` 和 `seed` 等生成参数 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)；
  - 所有模型均强制使用 `qwen3-asr-flash-realtime` 进行输入音频转录，不可替换 [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

- **关键功能**：
  - 双模态输出：支持 `["text"]` 或 `["text", "audio"]` 组合；
  - 实时语音活动检测（VAD）：`server_vad`（全系列支持）与 `semantic_vad`（仅 `qwen3.5-omni-realtime` 系列支持）；
  - 工具调用（Function Calling）：需通过 `tools` 数组声明，模型自主触发，客户端回传结果后需显式调用 `response.create` 触发后续响应（Manual 模式下）或由服务端自动触发（VAD 模式下）；
  - 声音复刻集成：复刻音色必须与 `target_model` 匹配，且仅限 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` 等指定模型 [原文标题](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)；
  - 联网搜索：仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 互斥，不可同时启用。

> **注意**：文档 2（客户端事件）与文档 1（服务端事件）对 `session.created` 中 `modalities` 默认值描述一致（`["text","audio"]`），但文档 3（Java SDK）示例代码中 `OmniRealtimeConfig.builder()` 的 `modalities` 设置顺序为 `[AUDIO, TEXT]`，实际行为以服务端为准；所有文档均明确 `input_audio_format` 和 `output_audio_format` 仅支持 `pcm`（对应 `PCM_16000HZ_MONO_16BIT` / `PCM_24000HZ_MONO_16BIT`），无例外。

## 关键参数

| 参数 | 类型 | 说明 | 默认值 | 适用模型 | 备注 |
|------|------|------|--------|----------|------|
| `voice` | `string` | 输出音色 | `Tina`（qwen3.5）、`Cherry`（qwen3-flash）、`Chelsie`（turbo） | 全系列 | 音色列表见官方文档；声音复刻生成的 `voice` ID 可直接传入 |
| `modalities` | `array` | 输出模态 | `["text","audio"]` | 全系列 | 仅支持 `["text"]` 或 `["text","audio"]` |
| `instructions` | `string` | 系统角色提示 | — | 全系列 | 通过 `parameters` 字段传入（Java/Python SDK）或 `session.update` 直接设置 |
| `turn_detection.type` | `string` | VAD 类型 | `"server_vad"` | 全系列（`semantic_vad` 仅 qwen3.5） | `null` 表示 Manual 模式 |
| `turn_detection.threshold` | `float` | VAD 灵敏度 | `0.5` | 全系列 | 范围 `[-1.0, 1.0]`；值越小越敏感 |
| `turn_detection.silence_duration_ms` | `int` | 静音触发阈值 | `800` | 全系列 | 范围 `[200, 6000]` |
| `turn_detection.idle_timeout_ms` | `int` | 静默超时（主动引导） | — | 仅 `qwen3.5-omni-plus-realtime` / `flash-realtime` + `server_vad` | 范围 `[5000, 30000]`，需通过 `turnDetectionParam`（Java）或 `turn_detection_param`（Python）传入 |
| `enable_search` | `boolean` | 启用联网搜索 | `false` | 仅 qwen3.5 系列 | 与 `tools` 不兼容 |
| `tools` | `array` | 工具定义列表 | `[]` | 仅 qwen3.5 系列 | 每个工具 `function.parameters` 中 `properties` 的 `description` 字段用于模型参数提取 |
| `temperature` / `top_p` | `float` | 生成多样性控制 | 见下文 | qwen3.5: `0.7`/`0.8`；qwen3-flash: `0.9`/`1.0`；turbo: `1.0`/`0.01` | **建议只设其一**；turbo 系列不可修改 |
| `max_tokens` | `int` | 最大输出 token 数 | 模型上限 | 全系列（turbo 不可修改） | 截断响应，不影响生成过程 |
| `repetition_penalty` | `float` | 重复惩罚 | qwen3.5: `1.0`；其余: `1.05` | 全系列（turbo 不可修改） | >1.0 降低重复 |
| `presence_penalty` | `float` | 全局重复惩罚 | qwen3.5: `1.5`；其余: `0.0` | 全系列（turbo 不可修改） | 范围 `[-2.0, 2.0]` |

## 使用方式

1. **建立连接**：  
   使用 WebSocket 连接到地域专属域名（推荐）：  
   - 北京：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`  
   - 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`  
   （`{WorkspaceId}` 为业务空间 ID，[原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)）

2. **初始化会话**：  
   连接后立即发送 `session.update` 事件配置参数（如 `modalities`, `voice`, `turn_detection` 等），服务端返回 `session.created` 或 `session.updated` 事件确认。

3. **音频输入**：  
   - **VAD 模式**（`turn_detection.type = "server_vad"`）：持续发送 `input_audio_buffer.append`，服务端自动检测起止并提交；  
   - **Manual 模式**（`turn_detection = null`）：发送 `input_audio_buffer.append` 后，显式发送 `input_audio_buffer.commit` 创建用户消息项。

4. **触发响应**：  
   - VAD 模式下，服务端在语音停止后自动触发响应；  
   - Manual 模式下，需发送 `response.create` 事件；  
   - 工具调用后，客户端回传结果 via `conversation.item.create`，再发送 `response.create`（Manual）或等待服务端自动触发（VAD）。

5. **处理输出**：  
   监听服务端事件：  
   - `conversation.item.input_audio_transcription.delta` → 拼接 `text` + `stash` 获取实时 ASR 预览；  
   - `conversation.item.input_audio_transcription.completed` → 获取最终转录文本；  
   - `response.audio.delta` / `response.text.delta` → 流式消费模型输出；  
   - `response.done` → 响应结束。

## 限制和注意事项

- **音频格式硬性约束**：输入必须为 16 kHz PCM（单声道、16-bit），输出固定为 24 kHz PCM；不支持自定义采样率或编码格式。
- **工具与搜索互斥**：`tools` 和 `enable_search` 不可同时启用，否则服务端返回 `invalid_request_error` [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **turbo 系列参数锁定**：`qwen-omni-turbo-realtime` 的所有生成参数（`temperature`, `top_p`, `max_tokens` 等）均不可修改，SDK 文档已明确标注 [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
- **图像输入限制**：仅 JPG/JPEG 格式，Base64 编码后 ≤256KB，建议分辨率 480p–720p，发送频率 ≤1 张/秒；需先发送音频事件再发送图像。
- **错误处理**：所有错误均以 `error` 事件返回，含 `type`、`code`、`message` 和 `param` 字段，例如 `Invalid modalities: ['audio']` 表明模态组合非法 [原文标题](../../raw/model-api-reference/omni-realtime-api/server-events.md)。
- **连接稳定性**：推荐使用业务空间专属域名（`maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽兼容但性能与稳定性较低。

## 来源文档

- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)


