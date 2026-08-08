# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时多模态交互接口，支持语音、文本、图像输入与文本、语音输出的端到端流式交互。它采用事件驱动模型，客户端通过发送结构化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态和数据流，服务端通过异步事件（如 `session.created`、`response.audio.delta`）实时推送响应结果。该 API 专为低延迟、高保真语音交互场景设计，适用于智能客服、虚拟助手等实时对话系统。

## 支持的模型/功能

- **核心模型系列**：  
  - `qwen3.5-omni-realtime`（支持 `semantic_vad`、联网搜索、工具调用）  
  - `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime`（支持 `idle_timeout_ms`）  
  - `qwen3-omni-flash-realtime`（默认音色 `Cherry`，支持 `smooth_output`）  
  - `qwen-omni-turbo-realtime`（默认音色 `Chelsie`，参数不可修改）  

- **多模态能力**：  
  - 输入：PCM 音频（16 kHz）、JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256 KB）  
  - 输出：文本 + PCM 音频（24 kHz），支持 `["text"]` 或 `["text","audio"]` 模态组合  
  - 实时转录：内置 `qwen3-asr-flash-realtime` ASR 模型，不可替换 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)  

- **高级功能**：  
  - 语音活动检测（VAD）：`server_vad`（默认）或语义级 `semantic_vad`（仅 `qwen3.5-omni-realtime` 支持）  
  - 工具调用（Function Calling）：定义 `function` 类型工具，模型自主触发并返回 `call_id`，客户端回传结果后需显式调用 `response.create` [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)  
  - 联网搜索：仅 `qwen3.5-omni-realtime` 系列支持 `enable_search`，且与 `tools` 不兼容  
  - 声音复刻：通过独立 `qwen-voice-enrollment` 模型创建音色，复刻音色必须与 Omni 模型版本严格匹配（如 `qwen3.5-omni-plus-realtime`） [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)  

> **注意**：文档中 `qwen3.5-omni-plus-realtime` 在 VAD 参数描述中被多次提及（如 `idle_timeout_ms` 生效条件），但原始模型列表未明确列出该型号；实际使用请以控制台可用模型为准，避免硬编码不存在的模型名。

## 关键参数

所有参数均通过 `session.update` 事件或 SDK 的 `update_session()` 方法配置：

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `modalities` | `string[]` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` | `string` | 音色名，需与模型匹配（如 `Tina`/`Cherry`/`Chelsie`） | 按模型自动设定 |
| `input_audio_format` / `output_audio_format` | `string` | 固定为 `"pcm"`，采样率分别为 16 kHz / 24 kHz | 不可修改 |
| `turn_detection.type` | `string` | `"server_vad"`（声学）或 `"semantic_vad"`（语义） | `"server_vad"` |
| `turn_detection.threshold` | `float` | VAD 灵敏度 [-1.0, 1.0] | `0.5` |
| `turn_detection.silence_duration_ms` | `int` | 静音触发阈值 [200, 6000] ms | `800` |
| `idle_timeout_ms` | `int` | 静默超时引导响应 [5000, 30000] ms | 仅 `qwen3.5-omni-plus/flash-realtime` + `server_vad` 有效 |
| `instructions` | `string` | 系统角色提示词 | 无默认值 |
| `temperature` / `top_p` / `top_k` | `float`/`int` | 生成多样性控制（三选一即可） | 按模型预设，`qwen-omni-turbo` 系列不可修改 |
| `max_tokens` | `int` | 响应截断长度 | 模型最大输出长度 |
| `repetition_penalty` / `presence_penalty` | `float` | 重复惩罚系数 | 按模型预设，`qwen-omni-turbo` 系列不可修改 |
| `seed` | `int` | 生成确定性种子 [0, 2³¹−1] | `-1`（随机） |

> **注意**：`smooth_output` 仅对 `qwen3-omni-flash-realtime` 有效，且 `null` 表示模型自动选择风格；其他模型忽略此参数 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

## 使用方式

### 连接与初始化
1. 建立 WebSocket 连接，URL 格式：`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`（推荐业务空间专属域名）  
2. 服务端立即返回 `session.created` 事件，含默认配置  
3. 调用 `session.update`（或 SDK `update_session()`）覆盖默认参数  

### 两种交互模式
- **VAD 模式**（默认）：  
  - 客户端持续 `input_audio_buffer.append` 音频  
  - 服务端自动检测 `speech_started`/`speech_stopped` 并 `committed`，无需手动提交  
  - 响应由服务端自动触发（`response.create` 隐式执行）  

- **Manual 模式**（`turn_detection: null`）：  
  - 客户端 `input_audio_buffer.append` 后，必须显式 `input_audio_buffer.commit` 创建用户消息  
  - 必须显式发送 `response.create` 触发模型响应  
  - 适用于“按住说话”类 UI [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)  

### 工具调用流程
1. 模型返回 `conversation.item.created`（`type: "function_call"`）及 `call_id`  
2. 客户端执行本地工具，通过 `conversation.item.create` 回传 `output`  
3. **VAD 模式**：服务端自动继续生成；**Manual 模式**：客户端需再次 `response.create`  

### 音频/图像输入
- 音频：Base64 编码 PCM（16-bit, mono, 16 kHz），建议分块 ≤3200 字节  
- 图像：Base64 编码 JPG/JPEG（≤1080p），单图 ≤256 KB，建议 1 张/秒频率  

## 限制和注意事项

- **模型限制**：  
  - `qwen-omni-turbo-realtime` 系列不支持修改 `temperature`/`top_p`/`top_k`/`max_tokens`/`repetition_penalty`/`presence_penalty`/`seed`  
  - `tools` 与 `enable_search` 互斥，同时设置将导致 `invalid_request_error`  

- **音频约束**：  
  - 输入音频必须为 16 kHz PCM，输出为 24 kHz PCM，不支持自定义采样率  
  - `input_audio_buffer.append` 单次数据量无硬限制，但缓冲区总大小建议 ≤15 MiB  
  - 图像输入仅支持 JPG/JPEG，非标准格式（如 PNG）将失败  

- **连接与错误**：  
  - WebSocket 连接超时时间由服务端控制，客户端需实现重连逻辑  
  - 错误事件 `error` 包含 `code`（如 `invalid_value`）和 `param`（如 `session.modalities`），用于精准调试  

- **地域与域名**：  
  - 北京/新加坡地域必须使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等），旧域名 `dashscope.aliyuncs.com` 已逐步弃用  
  - 域名迁移是强制要求，否则可能遭遇性能下降或连接失败 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


