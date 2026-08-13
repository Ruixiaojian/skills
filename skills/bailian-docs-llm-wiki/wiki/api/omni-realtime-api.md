# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时[多模态](../concepts/multimodal.md)对话接口，支持语音输入/输出、文本交互、图像理解及工具调用等能力。它通过事件驱动模型实现低延迟流式响应，适用于智能客服、语音助手、实时会议纪要等场景。所有交互均围绕会话（session）生命周期展开，客户端通过发送标准化事件控制流程，服务端通过事件流返回状态、内容与元数据。

## 支持的模型/功能

- **核心模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-omni-turbo-realtime`（注意：文档中多次出现 `qwen3-omni-*` 与 `qwen3.5-omni-*` 混用，实际以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中示例为准，推荐使用 `qwen3.5-omni-*` 前缀命名）。
- **[多模态](../concepts/multimodal.md)输入**：实时音频（PCM/WAV）、图像（JPG/JPEG，≤1080p，Base64 编码后 ≤256KB）、文本（通过 `instructions` 或 ASR 转录）。
- **[多模态](../concepts/multimodal.md)输出**：文本、音频（PCM/WAV，采样率 8k/16k/24k/48k Hz 可配）、结构化工具调用参数。
- **高级能力**：
  - 语音活动检测（VAD）：`server_vad`（声学）与 `semantic_vad`（语义，仅 `qwen3.5-omni-realtime` 系列支持）；
  - 工具调用（Function Calling）：模型自主触发外部函数，需配置 `tools` 列表；
  - 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，与 `tools` 互斥；
  - 声音复刻集成：复刻音色需与驱动模型（如 `qwen3.5-omni-plus-realtime`）严格匹配，详见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：文档 3（[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）声明 `output_audio_format` 当前“仅支持设为 `pcm`”，而文档 1（[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）明确支持 `wav` 输出格式并给出示例。以客户端事件文档为准，`wav` 格式可用，服务端事件中 `audio.output.format.type` 字段会如实回显该配置。

## 关键参数

所有参数均通过 `session.update` 事件或 SDK 的 `update_session` 方法设置，部分参数按模型系列有默认值或限制：

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `modalities` | `["text"]` \| `["text","audio"]` | 输出模态组合 | `["text","audio"]` |
| `voice` | `string` | 音色名称 | `Tina`（Qwen3.5）、`Cherry`（Flash）、`Chelsie`（Turbo） |
| `audio.input.format` / `audio.output.format` | `{type: "pcm"\|"wav", sample_rate: int}` | 输入/输出音频格式与采样率 | 输入：`pcm`+16000Hz；输出：`wav`+24000Hz（文档 1 示例） |
| `instructions` | `string` | 系统角色提示词 | 无默认值 |
| `turn_detection.type` | `"server_vad"` \| `"semantic_vad"` | VAD 类型 | `"server_vad"` |
| `turn_detection.threshold` | `float [-1.0, 1.0]` | VAD 灵敏度 | `0.5` |
| `turn_detection.silence_duration_ms` | `int [200, 6000]` | 静音触发阈值 | `800` |
| `idle_timeout_ms` | `int [5000, 30000]` | 静默超时（仅 Flash/Plus + `server_vad`） | 无默认值，需显式设置 |
| `tools` | `array` | 工具定义列表 | 空数组 |
| `enable_search` | `boolean` | 启用联网搜索（仅 Qwen3.5 系列） | `false` |
| `temperature` / `top_p` / `top_k` | `float` / `float` / `int` | 采样控制参数 | 各模型有不同默认值（见文档 1），`qwen-omni-turbo` 系列不支持修改 |
| `max_tokens` | `int` | 最大输出 token 数 | 模型最大长度，`qwen-omni-turbo` 不支持修改 |
| `repetition_penalty` / `presence_penalty` | `float` | 重复惩罚参数 | 各模型有不同默认值，`qwen-omni-turbo` 不支持修改 |
| `seed` | `int` | 随机种子 | `-1`，`qwen-omni-turbo` 不支持修改 |

> **注意**：`input_audio_format` 和 `output_audio_format` 是历史兼容字段，新增接入**必须**使用嵌套的 `audio.input.format` 和 `audio.output.format`（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。

## 使用方式

1. **建立连接**：使用 WebSocket URL（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`）连接，URL 中 `{WorkspaceId}` 需替换为实际业务空间 ID（[来源文档](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 推荐迁移至专属域名）。
2. **初始化会话**：连接后服务端立即返回 `session.created` 事件，含默认配置。
3. **配置会话**：调用 `session.update`（或 SDK `update_session`）设置 `modalities`、`voice`、`audio`、`tools` 等参数。建议在连接后立即执行。
4. **输入数据**：
   - **VAD 模式**（`turn_detection.type` 非 null）：持续 `input_audio_buffer.append` 音频，服务端自动检测起止并提交；可选 `input_image_buffer.append` 图像。
   - **Manual 模式**（`turn_detection` 设为 `null`）：`input_audio_buffer.append` → `input_audio_buffer.commit` → `response.create` 触发响应。
5. **处理响应**：监听 `response.audio.delta`（流式音频）、`response.text.delta`（流式文本）、`response.done`（完成）等事件。
6. **工具调用**：当收到 `response.function_call_arguments.done`，执行本地函数后，用 `conversation.item.create` 回传结果，再发 `response.create` 获取最终响应。

## 限制和注意事项

- **音频限制**：输入音频采样率支持 `8000/16000/24000/48000` Hz；输出音频采样率同理；单张图片 Base64 编码后 ≤256KB；建议图像分辨率 ≤1080p。
- **并发与超时**：`idle_timeout_ms` 仅在 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 下生效；`qwen-omni-turbo` 系列绝大多数参数（`temperature`, `top_p`, `max_tokens`, `repetition_penalty`, `presence_penalty`, `seed`）**不支持修改**。
- **互斥功能**：`tools` 与 `enable_search` 不可同时启用，否则服务端报错。
- **模式选择**：VAD 模式适合持续语音流（如智能音箱），Manual 模式适合按键说话（如聊天 App）。SDK 中 `enable_turn_detection` 参数需与 `session.turn_detection` 保持一致（见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)）。
- **错误处理**：服务端返回 `error` 事件（含 `type`, `code`, `message`, `param`），客户端需据此重试或降级（如 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 所示）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


