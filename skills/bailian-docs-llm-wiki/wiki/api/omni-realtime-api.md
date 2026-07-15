# omni realtime api

Qwen-Omni-Realtime API 是一个基于 WebSocket 的实时多模态交互接口，支持语音输入、文本/音频输出、VAD 自动检测、工具调用与联网搜索（部分模型），适用于智能客服、虚拟助手等低延迟对话场景。其核心是双向事件流通信：客户端发送 `session.update`、`input_audio_buffer.append` 等事件，服务端返回 `session.created`、`response.audio.delta` 等事件。

## 支持的模型与功能

- **支持模型**：`qwen3.5-omni-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`。各模型能力存在差异，详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中的参数兼容性说明。
- **核心模态**：默认支持 `["text", "audio"]` 输出；可设为 `["text"]` 仅输出文本。输入仅支持 `pcm` 格式音频（16 kHz 采样率）。
- **语音活动检测（VAD）**：支持 `server_vad`（声学检测）和 `semantic_vad`（语义检测，**仅 `qwen3.5-omni-realtime` 支持**）[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **高级功能**：
  - 工具调用（`tools`）：所有支持模型均可配置，但仅 `qwen3.5-omni-realtime` 系列在文档中明确标注支持完整流程；
  - 联网搜索（`enable_search`）：**仅 `qwen3.5-omni-realtime` 系列支持**，且与 `tools` 不兼容 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)；
  - 声音复刻：需先调用独立声音复刻 API 创建音色，再在 `session.update` 中通过 `voice` 参数传入，**驱动模型必须与复刻时指定的 `target_model` 严格一致** [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：文档 2（服务端事件）中 `session.created` 示例显示 `model: "qwen3-omni-flash-realtime"`，而文档 1（客户端事件）中 `voice` 默认值表格将 `qwen3-omni-flash-realtime` 对应音色列为 `"Cherry"`，但文档 3（Python SDK）和文档 4（Java SDK）均将该模型写作 `"qwen3-omni-flash-realtime"`（无连字符），而文档 6（声音复刻）中 `target_model` 列表使用 `"qwen3.5-omni-flash-realtime"`。实际调用时请以控制台模型列表或最新 SDK 枚举为准，避免因命名不一致导致 `invalid_request_error`。

## 关键参数

所有参数均通过 `session.update` 客户端事件或 SDK 的 `update_session()` 方法设置：

| 参数 | 类型 | 说明 | 兼容性 |
|------|------|------|--------|
| `modalities` | `["text"]` 或 `["text","audio"]` | 输出模态组合 | 全系列支持 |
| `voice` | `string` | 音色 ID，如 `"Chelsie"`、`"Tina"`；复刻音色需传入生成的 voice ID | 全系列支持 |
| `input_audio_format` / `output_audio_format` | `"pcm"` | 输入/输出音频格式，固定值 | 全系列支持 |
| `instructions` | `string` | 系统角色提示词 | 全系列支持 |
| `turn_detection.type` | `"server_vad"` 或 `"semantic_vad"` | VAD 类型 | `semantic_vad` 仅 `qwen3.5-omni-realtime` 支持 |
| `turn_detection.silence_duration_ms` | `integer [200, 6000]` | 静音触发响应阈值（毫秒） | 全系列支持 |
| `turn_detection.idle_timeout_ms` | `integer [5000, 30000]` | 静默超时主动引导时间 | **仅 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 时生效** |
| `enable_search` | `boolean` | 启用联网搜索 | **仅 `qwen3.5-omni-realtime` 系列支持** |
| `tools` | `array` | 工具定义列表 | 全系列支持，但 `qwen3.5-omni-realtime` 文档最完整 |
| `temperature` / `top_p` / `top_k` | `float` / `float` / `integer` | 采样控制参数 | `qwen-omni-turbo` 系列**不支持修改** |
| `max_tokens` | `integer` | 最大输出 token 数 | `qwen-omni-turbo` 系列**不支持修改** |
| `smooth_output` | `boolean` or `null` | **仅 `qwen3-omni-flash-realtime` 系列支持**，控制口语化/书面化风格 | |

> **注意**：`repetition_penalty` 和 `presence_penalty` 在文档 1 和文档 2 中默认值存在差异（如 `qwen3.5-omni-realtime` 的 `presence_penalty`，文档 1 写 `1.5`，文档 2 未明确，默认值以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 为准。

## 使用方式

1. **建立连接**：使用 WebSocket 连接到地域专属域名（推荐 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime` 或 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`），`{WorkspaceId}` 从控制台获取。
2. **初始化会话**：连接后，服务端立即返回 `session.created` 事件。随后调用 `session.update` 设置初始配置（如 `modalities`, `voice`, `instructions`）。
3. **输入数据**：
   - **VAD 模式（推荐）**：持续发送 `input_audio_buffer.append`，服务端自动检测起止并提交；无需手动发 `commit` 或 `response.create` [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
   - **Manual 模式**：发送 `input_audio_buffer.append` → `input_audio_buffer.commit` → `response.create` 触发响应。
4. **处理响应**：监听 `response.audio.delta`（流式音频）、`response.text.delta`（流式文本）、`response.done`（完成）等事件。
5. **工具调用**：当收到 `response.function_call_arguments.done` 事件时，执行本地工具，再通过 `conversation.item.create` 回传结果，最后发 `response.create`（Manual 模式）或等待服务端自动响应（VAD 模式）。

## 限制和注意事项

- **音频限制**：输入音频必须为 16 kHz PCM；输出音频固定为 24 kHz PCM；单次 `append_audio` 数据量无明确上限，但 SDK 示例建议 ≤15 MiB。
- **图片限制**：仅 JPG/JPEG；Base64 编码后 ≤256 KB；建议分辨率 480p/720p；发送频率 ≤1 张/秒。
- **并发与超时**：单个 WebSocket 连接对应一个会话；`idle_timeout_ms` 仅在特定模型+VAD 组合下生效；`max_tokens` 截断响应但不影响生成过程。
- **兼容性约束**：
  - `tools` 与 `enable_search` **不可同时启用**；
  - `qwen-omni-turbo` 系列模型**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`；
  - `semantic_vad` 仅 `qwen3.5-omni-realtime` 支持，其他模型设为该值将报错；
  - 声音复刻音色必须与 Omni 调用模型严格匹配（如复刻时 `target_model="qwen3.5-omni-plus-realtime"`，则 Omni 调用时 `model` 和 `voice` 必须对应同一模型）[声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。
- **错误处理**：服务端返回 `error` 事件（含 `type`、`code`、`message`、`param`），需根据 `param` 字段定位问题参数。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


