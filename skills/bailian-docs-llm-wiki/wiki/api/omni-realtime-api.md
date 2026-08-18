# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的低延迟、多模态实时交互接口，支持语音输入/输出、文本生成、图像理解及工具调用等能力。它采用事件驱动模型，客户端通过发送结构化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态与数据流，服务端通过异步事件（如 `input_audio_buffer.speech_started`、`response.audio.delta`）实时反馈处理进展。该 API 专为语音助手、智能客服、实时音视频交互等场景设计。

## 支持的模型/功能

- **核心模型系列**：
  - `qwen3.5-omni-plus-realtime`：高保真、强语义理解，支持 `semantic_vad` 和联网搜索。
  - `qwen3.5-omni-flash-realtime`：低延迟、高吞吐，支持 `smooth_output` 口语化控制。
  - `qwen-omni-turbo-realtime`：极致轻量，仅支持基础文本/音频输出，**多数参数不可修改**（见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。

- **多模态能力**：
  - 输入：PCM/WAV 音频（8k–48k Hz）、JPG/JPEG 图像（≤1080p，Base64 编码后 ≤256KB）。
  - 输出：文本 + 音频（PCM/WAV，8k–48k Hz），支持 `modalities: ["text"]` 或 `["text","audio"]`。
  - 图像理解：需在 `input_image_buffer.append` 后配合 `input_audio_buffer.commit` 提交，由模型自主融合分析。

- **高级功能**：
  - 语音活动检测（VAD）：`server_vad`（声学）或 `semantic_vad`（语义，仅 `qwen3.5-omni-plus-realtime` 支持）。
  - 工具调用（Function Calling）：定义 `tools` 后，模型可自主触发并返回 `function_call` 项，客户端执行后需回传结果。
  - 联网搜索：`enable_search: true`（仅 `qwen3.5-omni-plus-realtime` 支持），与 `tools` **互斥**。
  - 声音复刻：需先调用 `qwen-voice-enrollment` 创建音色，再于 `session.update` 中通过 `voice` 字段指定使用（详见[声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）。

> **注意**：文档中 `qwen3-omni-flash-realtime` 与 `qwen3.5-omni-flash-realtime` 模型名存在不一致（如[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)中混用），实际应以控制台和最新 SDK 文档为准，推荐使用带 `.5` 的完整命名（如 `qwen3.5-omni-flash-realtime`）。

## 关键参数

所有参数均通过 `session.update` 事件或 SDK 的 `update_session()` 方法配置。以下为常用且易混淆的参数：

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `modalities` | `string[]` | 输出模态组合 | `["text","audio"]`；仅 `["text"]` 或 `["text","audio"]` 合法，`["audio"]` 不支持 |
| `voice` | `string` | 音色ID | `Tina`（qwen3.5 系列）、`Cherry`（qwen3-flash）、`Chelsie`（turbo）；亦可填声音复刻生成的自定义 voice ID |
| `audio.input.format` / `audio.output.format` | `object` | **推荐新接入方式**：嵌套定义 `type`（`pcm`/`wav`）和 `sample_rate`（Hz） | 输入默认 `16000`，输出默认 `24000`；历史字段 `input_audio_format`/`output_audio_format` 仍兼容但不推荐 |
| `turn_detection.type` | `string` | VAD 类型 | `server_vad`（默认）；`semantic_vad` 仅 `qwen3.5-omni-plus-realtime` 支持 |
| `turn_detection.threshold` | `float` | VAD 灵敏度 | `[-1.0, 1.0]`，默认 `0.5`；嘈杂环境建议调高（如 `0.7`） |
| `turn_detection.silence_duration_ms` | `int` | 静音触发响应时长 | `[200, 6000]` ms， 默认 `800` |
| `idle_timeout_ms` | `int` | 静默超时主动引导（仅 server_vad + qwen3.5-flash/plus） | `[5000, 30000]` ms，需通过 `turn_detection_param` 传入 |
| `enable_search` | `boolean` | 启用联网搜索 | `false`（仅 qwen3.5-plus-realtime 支持）；与 `tools` 冲突，不可共存 |
| `tools` | `object[]` | 工具定义列表 | 仅 qwen3.5-plus-realtime 支持；每个 tool 必须含 `type: "function"` 和 `function.name` |
| `temperature` / `top_p` / `top_k` | `float`/`int` | 采样控制参数 | **三者勿同时设置**；`qwen-omni-turbo` 系列完全不可修改（见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)） |

## 使用方式

1. **建立连接**：  
   使用业务空间专属域名（强烈推荐）：  
   - 北京：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`  
   - 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`  
   （`{WorkspaceId}` 在百炼控制台获取；旧域名 `dashscope.aliyuncs.com` 仍可用但性能较低）

2. **初始化会话**：  
   连接后立即发送 `session.update` 事件（或调用 SDK `update_session()`），配置 `model`、`modalities`、`voice`、`instructions` 等。服务端返回 `session.updated` 确认。

3. **音频交互模式**：  
   - **VAD 模式（默认）**：设 `turn_detection.type: "server_vad"`。客户端持续 `append_audio`，服务端自动检测 `speech_started`/`speech_stopped` 并提交缓冲区，无需手动 `commit`。适用于实时麦克风流。  
   - **Manual 模式**：设 `turn_detection: null`。客户端需显式 `append_audio` → `input_audio_buffer.commit` → `response.create`。适用于“按住说话”类 UI。

4. **工具调用流程**：  
   - 模型返回 `conversation.item.created`（`type: "function_call"`）→ 客户端执行本地函数 → 发送 `conversation.item.create`（`type: "function_call_output"`）→ 发送 `response.create` 触发最终响应。

5. **图像输入**：  
   先 `append_audio`（至少一次），再 `append_video`（JPG/Base64），最后 `commit`。服务端将音频转录文本与图像一并送入模型。

## 限制和注意事项

- **音频格式限制**：  
  输入音频必须为单声道、16-bit PCM 或 WAV；采样率支持 `8000`/`16000`/`24000`/`48000` Hz。输出音频采样率 `24000` Hz 最稳定，`48000` Hz 可能导致部分客户端播放异常。

- **并发与配额**：  
  单个 WebSocket 连接仅支持一个会话；高频 `append_audio`（如 >100ms/帧）可能导致缓冲区积压。具体 QPS/并发限制请查阅百炼控制台配额页。

- **参数兼容性冲突**：  
  > **注意**：`enable_search` 与 `tools` 绝对互斥，同时启用将导致 `session.update` 返回 `invalid_request_error`（见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。务必根据业务需求二选一。

- **SDK 特定行为**：  
  - Python SDK 的 `smooth_output` 仅对 `qwen3.5-omni-flash-realtime` 生效，设为 `False` 时可能因书面化内容（如公式、代码）导致 TTS 效果下降。  
  - Java SDK 中 `instructions`、`temperature` 等参数**必须**通过 `OmniRealtimeConfig.parameters(Map)` 设置，直接调用 setter 无效（见[Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)）。

- **错误处理**：  
  服务端统一返回 `error` 事件（`type: "error"`），含 `code`（如 `invalid_value`）和 `param`（如 `session.modalities`），需在回调中捕获并解析 `error.message`。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


