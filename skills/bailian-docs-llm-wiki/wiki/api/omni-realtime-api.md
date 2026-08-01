# omni realtime api

Qwen-Omni-Realtime API 是一个基于 WebSocket 的实时多模态交互接口，支持语音输入/输出、文本生成、图像理解及工具调用等能力。它采用事件驱动模型，客户端通过发送结构化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态与数据流，服务端则通过异步事件（如 `session.created`、`response.audio.delta`）实时推送响应与中间结果。该 API 专为低延迟、高保真语音对话场景设计，适用于智能客服、虚拟助手等应用。

## 支持的模型/功能

Omni Realtime API 当前支持以下核心模型系列，各模型能力与默认配置存在差异：

- **`qwen3.5-omni-realtime`**：旗舰级实时模型，支持 `semantic_vad`、联网搜索（`enable_search`）、工具调用（`tools`），默认 `temperature=0.7`、`top_p=0.8`、`top_k=20`。
- **`qwen3-omni-flash-realtime`**：高性能轻量模型，支持 `smooth_output` 参数调节口语化程度，VAD 类型仅限 `server_vad`，默认 `voice="Cherry"`、`temperature=0.9`、`top_p=1.0`。
- **`qwen-omni-turbo-realtime`**：超低延迟模型，**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等采样参数，仅支持 `modalities=["text","audio"]` 和 `server_vad`，默认 `voice="Chelsie"`、`temperature=1.0`、`top_p=0.01` [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

> **注意**：文档 2 中 `session.created` 示例显示 `model: "qwen3-omni-flash-realtime"`，但文档 1 中 `voice` 默认值描述为 `"Cherry"`，而文档 3 和 4 均明确列出 `"Cherry"` 对应 `Qwen3-Omni-Flash-Realtime`，三者一致；但文档 1 中 `qwen3.5-omni-realtime` 默认 `voice="Tina"`，文档 3 和 4 亦确认此点，无矛盾。需注意 `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 在 `idle_timeout_ms` 支持上完全一致，但文档 1 与文档 2 均限定其生效条件为 `server_vad` 模式，此为关键约束 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

功能方面，API 支持：
- **多模态 I/O**：输入支持 PCM 音频（16 kHz）与 JPG/JPEG 图像（≤1080p，Base64 编码）；输出支持文本与 PCM 音频（24 kHz）。
- **语音活动检测（VAD）**：提供 `server_vad`（声学）与 `semantic_vad`（语义，仅 `qwen3.5-omni-realtime` 支持）两种模式。
- **工具调用（Function Calling）**：模型可自主触发预定义函数，客户端需回传结果并显式调用 `response.create` 触发后续响应 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **声音复刻集成**：复刻音色（via `qwen-voice-enrollment`）后，可在 `session.update` 中直接指定 `voice` 参数使用，但必须确保 `target_model` 与 Omni 实时模型严格一致。

## 关键参数

所有可配置参数均通过 `session.update` 客户端事件或 SDK 的 `update_session` 方法设置。核心参数如下：

| 参数 | 类型 | 说明 | 适用模型 | 默认值 |
|------|------|------|----------|--------|
| `modalities` | `["text"]` 或 `["text","audio"]` | 输出模态组合，`["audio"]` 单独不支持 | 全系列 | `["text","audio"]` |
| `voice` | `string` | 音色 ID，需从[音色列表](https://help.aliyun.com/zh/model-studio/realtime#f9c68d860a3rs)选取 | 全系列 | `Tina`/`Cherry`/`Chelsie`（按模型） |
| `input_audio_format` / `output_audio_format` | `"pcm"` | 固定值，输入要求 16 kHz PCM，输出为 24 kHz PCM | 全系列 | `"pcm"` |
| `smooth_output` | `boolean` or `null` | 仅 `qwen3-omni-flash-realtime` 支持：`true`（口语化）、`false`（书面化）、`null`（自动） | `qwen3-omni-flash-realtime` | `true` |
| `instructions` | `string` | 系统角色提示词，影响模型行为 | 全系列 | `""` |
| `turn_detection.type` | `"server_vad"` or `"semantic_vad"` | VAD 类型，后者仅 `qwen3.5-omni-realtime` 支持 | `qwen3.5-omni-realtime`（`semantic_vad`）<br>全系列（`server_vad`） | `"server_vad"` |
| `turn_detection.threshold` | `float [-1.0, 1.0]` | VAD 灵敏度，值越低越易误触发 | 全系列 | `0.5` |
| `turn_detection.silence_duration_ms` | `int [200, 6000]` | 语音结束静音阈值（ms） | 全系列 | `800` |
| `turn_detection.idle_timeout_ms` | `int [5000, 30000]` | 静默超时主动响应，仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 生效 | 特定模型 | — |
| `enable_search` | `boolean` | 启用联网搜索，与 `tools` 互斥 | `qwen3.5-omni-realtime` | `false` |
| `search_options.enable_source` | `boolean` | 是否返回搜索来源 | `qwen3.5-omni-realtime` | `false` |
| `tools` | `array` | 工具定义列表，含 `name`、`description`、`parameters` | `qwen3.5-omni-realtime` | `[]` |
| `temperature` / `top_p` / `top_k` | `float` / `float` / `int` | 采样控制参数，**`qwen-omni-turbo` 系列不可修改** | `qwen3.5`/`qwen3-flash` | 按模型不同（见上文） |

> **注意**：`tools` 与 `enable_search` 不兼容，同时设置将导致 `error` 事件 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 使用方式

### 连接与初始化
1. **建立 WebSocket 连接**：使用业务空间专属域名（推荐），格式为 `wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`（北京/新加坡）。
2. **接收 `session.created`**：连接后服务端立即返回初始会话配置，包含 `model`、`voice`、`modalities` 等。
3. **调用 `session.update`**：根据需求更新配置（如设置 `instructions`、`tools`、`turn_detection`），服务端校验后返回 `session.updated` 或 `error`。

### 数据流控制（两种模式）
- **VAD 模式（默认）**：  
  客户端持续 `append_audio` → 服务端自动检测 `speech_started`/`speech_stopped` → 自动 `committed` → 自动触发响应。  
  工具调用时，客户端收到 `response.function_call_arguments.done` 后，执行本地函数，再发 `conversation.item.create` + `response.create`。

- **Manual 模式**：  
  客户端 `append_audio` → 显式 `input_audio_buffer.commit` 创建用户消息 → 显式 `response.create` 触发响应。  
  此模式适用于“按住说话”类 UI，需手动控制节奏 [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。

### SDK 快速接入
- **Python**：使用 `dashscope.audio.qwen_omni.OmniRealtimeConversation`，通过 `update_session()` 设置参数，`append_audio()`/`commit()`/`create_response()` 控制流。
- **Java**：使用 `com.alibaba.dashscope.audio.omni.OmniRealtimeConversation`，参数通过 `OmniRealtimeConfig.builder()` 构建，方法名与 Python SDK 一一对应。

## 限制和注意事项

- **音频/图像限制**：输入音频必须为 16 kHz PCM；图像仅支持 JPG/JPEG，单张 Base64 编码 ≤ 256 KB，建议分辨率 480p/720p。
- **并发与配额**：受百炼平台配额限制，具体请查阅控制台；WebSocket 连接超时时间为 30 分钟。
- **`qwen-omni-turbo` 系列限制**：所有采样参数（`temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`）均**不可修改**，且不支持 `semantic_vad` 与 `enable_search`。
- **工具调用约束**：`tools` 仅 `qwen3.5-omni-realtime` 支持；工具调用期间模型不生成音频，仅输出 `function_call` 项；客户端必须严格按 `call_id` 回传结果。
- **域名迁移**：强烈建议迁移到业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性，旧域名（`dashscope.aliyuncs.com`）虽仍可用但非最优 [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


