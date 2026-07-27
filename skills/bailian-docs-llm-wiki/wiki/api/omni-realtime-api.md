# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的全模态实时交互接口，支持语音、文本、图像多模态输入与文本+音频同步输出。其核心为低延迟流式响应，通过服务端 VAD（语音活动检测）或客户端手动控制实现自然对话节奏，适用于智能客服、语音助手等实时交互场景。

## 支持的模型/功能

API 当前支持以下 Qwen-Omni 系列实时模型，各模型能力与默认配置存在差异：

- `qwen3.5-omni-realtime`：支持 `semantic_vad`、联网搜索（`enable_search`）、工具调用（`tools`），默认 `voice="Tina"`，默认 `temperature=0.7`、`top_p=0.8`、`top_k=20`、`repetition_penalty=1.0`、`presence_penalty=1.5`  
- `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`：支持 `idle_timeout_ms`（需配合 `server_vad`），默认 `voice="Tina"` / `"Cherry"`，`smooth_output` 仅对 Flash 版生效  
- `qwen3-omni-flash-realtime`：支持 `smooth_output`，默认 `voice="Cherry"`，默认 `temperature=0.9`、`top_p=1.0`、`top_k=50`、`repetition_penalty=1.05`、`presence_penalty=0.0`  
- `qwen-omni-turbo-realtime`：**不支持修改** `temperature`/`top_p`/`top_k`/`max_tokens`/`repetition_penalty`/`presence_penalty`/`seed`，默认 `voice="Chelsie"`，默认 `temperature=1.0`、`top_p=0.01`、`top_k=20`、`repetition_penalty=1.05`、`presence_penalty=0.0`  

> **注意**：文档中 `qwen3.5-omni-realtime` 系列模型的 `presence_penalty` 默认值存在矛盾——[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 写为 `1.5`，而 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 示例中为 `1.5`，但 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 均写为 `1.5`；其余模型统一为 `0.0`。以 SDK 文档为准，即 `qwen3.5-omni-realtime` 系列为 `1.5`，其余为 `0.0`。

功能上支持：
- 多模态输入：PCM 音频（16 kHz）、JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256KB）
- 多模态输出：文本 + PCM 音频（24 kHz），可选仅文本
- 实时语音识别（ASR）：内置 `qwen3-asr-flash-realtime` 模型，不可替换
- 语音活动检测（VAD）：`server_vad`（声学）或 `semantic_vad`（语义，仅 `qwen3.5-omni-realtime` 支持）
- 工具调用（Function Calling）：仅 `qwen3.5-omni-realtime` 系列支持，与 `enable_search` 互斥
- 联网搜索：仅 `qwen3.5-omni-realtime` 系列支持，启用后自动判断是否搜索并返回来源（`search_options.enable_source`）
- 声音复刻：需先调用独立声音复刻 API 创建音色，再在 `session.update` 中通过 `voice` 参数传入，**驱动模型必须与复刻时指定的 `target_model` 严格一致**（详见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）

## 关键参数

所有会话级参数均通过 `session.update` 客户端事件或 SDK 的 `update_session()` 方法配置，服务端返回 `session.updated` 事件确认。关键参数如下：

| 参数 | 类型 | 说明 | 限制与默认值 |
|------|------|------|--------------|
| `modalities` | `["text"]` 或 `["text","audio"]` | 输出模态 | 默认 `["text","audio"]`；`["audio"]` 单独不支持 |
| `voice` | `string` | 合成音色 | 必须是预置音色名或声音复刻生成的 ID；不同模型默认值不同（见上节） |
| `input_audio_format` / `output_audio_format` | `"pcm"` | 音频编解码格式 | 固定为 PCM；输入要求 16 kHz，输出固定为 24 kHz |
| `instructions` | `string` | 系统提示词 | 设定角色与行为边界，影响模型响应风格 |
| `turn_detection.type` | `"server_vad"` 或 `"semantic_vad"` | VAD 类型 | `semantic_vad` 仅 `qwen3.5-omni-realtime` 支持；设为 `null` 则进入 Manual 模式 |
| `turn_detection.threshold` | `float [-1.0, 1.0]` | VAD 灵敏度 | 默认 `0.5`；嘈杂环境建议调高（如 `0.7`），安静环境调低（如 `0.3`） |
| `turn_detection.silence_duration_ms` | `int [200, 6000]` | 静音触发阈值 | 默认 `800` ms；值越小响应越快，越易误触发 |
| `turn_detection.idle_timeout_ms` | `int [5000, 30000]` | 静默超时（主动引导） | **仅 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 生效**；默认不启用 |
| `enable_search` | `boolean` | 启用联网搜索 | **仅 `qwen3.5-omni-realtime` 系列支持**；与 `tools` 互斥，不可同时为 `true` |
| `tools` | `array` | 工具定义列表 | **仅 `qwen3.5-omni-realtime` 系列支持**；每个工具需含 `type="function"`、`function.name`、`function.description` |
| `temperature` / `top_p` / `top_k` | `float` / `float` / `int` | 采样控制 | 三者建议只设其一；`qwen-omni-turbo` 系列**完全不可修改**（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)） |
| `max_tokens` | `int` | 最大输出 token 数 | 截断响应，不影响生成过程；`qwen-omni-turbo` 系列**不可修改** |
| `repetition_penalty` / `presence_penalty` | `float` | 重复惩罚 | `qwen-omni-turbo` 系列**不可修改**；`presence_penalty` 范围 `[-2.0, 2.0]` |
| `seed` | `int [0, 2^31-1]` | 随机种子 | 用于结果复现；`qwen-omni-turbo` 系列**不可修改** |

## 使用方式

### 连接与初始化
1. 使用业务空间专属域名建立 WebSocket 连接（推荐）：  
   - 北京：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`  
   - 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`  
   （`{WorkspaceId}` 在百炼控制台获取；旧域名 `dashscope.aliyuncs.com` 仍可用但性能较低）

2. 连接后，服务端立即返回 `session.created` 事件，含默认配置。

3. 调用 `session.update`（或 SDK `update_session()`）覆盖默认参数。**强烈建议连接后立即调用**，避免使用过期默认值。

### 两种交互模式
- **VAD 模式**（默认）：`turn_detection.type="server_vad"`  
  - 客户端持续 `input_audio_buffer.append` 音频流  
  - 服务端自动检测 `speech_started`/`speech_stopped`，并 `committed` → `conversation.item.created`  
  - 响应由服务端自动触发（无需 `response.create`）  
  - 工具调用后，客户端回传 `conversation.item.create`，服务端自动续生成（见 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)）

- **Manual 模式**：`turn_detection=null`  
  - 客户端 `input_audio_buffer.append` 后，**必须显式发送** `input_audio_buffer.commit` 创建用户消息  
  - 客户端**必须显式发送** `response.create` 触发模型响应  
  - 工具调用后，客户端回传 `conversation.item.create`，**再发送 `response.create`** 续生成（见 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)）

### 核心事件流（VAD 模式示例）
```json
// 客户端
{"type":"session.update", "session":{...}} 
{"type":"input_audio_buffer.append", "audio":"UklGR..."}
{"type":"input_audio_buffer.append", "audio":"UklGR..."}

// 服务端（自动）
{"type":"input_audio_buffer.speech_started", ...}
{"type":"input_audio_buffer.speech_stopped", ...}
{"type":"input_audio_buffer.committed", ...}
{"type":"conversation.item.created", "item":{"type":"message", ...}}
{"type":"response.created", ...}
{"type":"response.content_part.added", ...}
{"type":"response.audio.delta", ...}
{"type":"response.done", ...}
```

## 限制和注意事项

- **音频限制**：输入音频必须为 16 kHz PCM；单次 `append` 数据无硬限，但缓冲区总大小建议 ≤15 MiB；图像单张 Base64 编码后 ≤256KB，格式仅 JPG/JPEG。
- **并发与超时**：单个 WebSocket 连接对应一个会话；服务端无明确空闲超时，但 `idle_timeout_ms` 仅在特定模型+VAD 下触发主动响应。
- **互斥配置**：`enable_search=true` 与 `tools` 非空 **不可共存**，否则 `session.update` 返回 `invalid_request_error`。
- **模型兼容性**：声音复刻创建的音色，其 `target_model` 必须与 Omni 实时调用的 `model` 参数**完全一致**，否则合成失败（见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）。
- **SDK 差异**：Python/Java SDK 中，`smooth_output`、`temperature` 等高级参数需通过 `parameters` 字典传入（如 `parameters={"smooth_output": True}`），而非顶层字段（见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)）。
- **错误处理**：所有客户端事件错误均以 `error` 事件返回，含 `error.code`（如 `invalid_value`）和 `error.param`（定位问题字段），需监听并处理（见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)


