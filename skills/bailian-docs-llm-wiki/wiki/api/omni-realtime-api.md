# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的低延迟、多模态实时交互接口，支持语音输入/输出、文本、图像及[工具调用](../concepts/tool-use.md)等能力。它通过事件驱动模型实现双向流式通信，适用于智能客服、语音助手、实时会议等场景。所有交互均围绕会话（session）展开，客户端通过发送标准化事件控制流程，服务端通过响应事件推送状态与内容。

## 支持的模型/功能

Omni Realtime API 当前支持以下模型系列，各模型能力存在差异：

- `qwen3.5-omni-realtime`：全能力旗舰模型，支持 `semantic_vad`、联网搜索（`enable_search`）、[工具调用](../concepts/tool-use.md)（`tools`）及完整参数调节（[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- `qwen3-omni-flash-realtime`：高吞吐轻量模型，支持 `smooth_output` 控制回复风格，但**不支持** `enable_search` 和 `semantic_vad`（[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- `qwen-omni-turbo-realtime`：极致低延迟模型，仅支持基础语音交互，**所有生成参数（`temperature`、`top_p`、`max_tokens` 等）均不可修改**（[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。

> **注意**：文档 6 中提及的 `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 在声音复刻场景中作为 `target_model` 被支持，但其在实时 API 中的 VAD 行为与 `qwen3.5-omni-realtime` 不同——仅当 VAD 类型为 `server_vad` 时才支持 `idle_timeout_ms`，而 `semantic_vad` 对其无效。此细节在 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中有明确限定。

核心功能包括：
- **多模态输入**：实时音频（PCM 16kHz）、图像（JPG/JPEG，≤1080p，Base64 编码后 ≤256KB）。
- **多模态输出**：文本 + 音频（PCM 24kHz），或仅文本。
- **语音活动检测（VAD）**：`server_vad`（声学）和 `semantic_vad`（语义，仅 `qwen3.5-omni-realtime` 支持）两种模式。
- **[工具调用](../concepts/tool-use.md)（Function Calling）**：模型自主触发函数，客户端回传结果后生成最终响应。
- **联网搜索（Search）**：仅 `qwen3.5-omni-realtime` 支持，与 `tools` 互斥。
- **声音复刻集成**：复刻音色需与驱动模型（如 `qwen3.5-omni-plus-realtime`）严格匹配，否则合成失败（[原文标题](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）。

## 关键参数

所有参数均通过 `session.update` 事件或 SDK 的 `update_session` 方法配置。关键参数如下：

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `modalities` | `["text"]` 或 `["text","audio"]` | 输出模态，`["audio"]` 单独使用无效 | `["text","audio"]` |
| `voice` | `string` | 音色名称，不同模型默认值不同（`Tina`/`Cherry`/`Chelsie`） | 模型相关，默认见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `input_audio_format` / `output_audio_format` | `"pcm"` | 输入/输出音频格式，固定为 PCM；输入采样率 16kHz，输出 24kHz | 必须为 `"pcm"` |
| `turn_detection.type` | `"server_vad"` 或 `"semantic_vad"` | VAD 类型，后者仅 `qwen3.5-omni-realtime` 支持 | `"server_vad"` |
| `turn_detection.threshold` | `float [-1.0, 1.0]` | VAD 灵敏度，值越小越易误触发 | `0.5` |
| `turn_detection.silence_duration_ms` | `int [200, 6000]` | 语音结束后静音阈值，超时即响应 | `800` |
| `turn_detection.idle_timeout_ms` | `int [5000, 30000]` | **仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 有效**，静默后主动引导 | — |
| `instructions` | `string` | 系统角色指令，影响模型行为 | — |
| `enable_search` | `boolean` | **仅 `qwen3.5-omni-realtime` 生效**，启用联网搜索 | `false` |
| `tools` | `array` | **仅 `qwen3.5-omni-realtime` 生效**，定义可调用函数 | `[]` |
| `temperature` / `top_p` / `top_k` | `float` / `float` / `int` | 生成多样性控制，**`qwen-omni-turbo` 系列不可修改** | 模型相关，默认见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `max_tokens` | `int` | 响应截断长度，不影响生成过程 | 模型最大输出长度 |

> **注意**：`smooth_output` 仅对 `qwen3-omni-flash-realtime` 有效；`presence_penalty` 在 `qwen3.5-omni-realtime` 默认为 `1.5`，其他模型为 `0.0`，此差异在 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 中一致，但 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 文档未明确列出 `qwen3-omni-flash-realtime` 的 `presence_penalty` 默认值，以 SDK 文档为准。

## 使用方式

### 连接与初始化
1. **建立 WebSocket 连接**：使用业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），避免旧域名（[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)、[Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 均强调此迁移）。
2. **接收 `session.created`**：服务端返回初始会话配置，包含模型、默认音色等。
3. **调用 `update_session`**：立即发送 `session.update` 事件（或 SDK 对应方法）覆盖默认配置。

### 交互模式
- **VAD 模式（推荐）**：`turn_detection.type` 设为 `"server_vad"`（或 `"semantic_vad"`）。客户端持续 `append_audio`，服务端自动检测语音起止并提交缓冲区，无需手动 `commit` 或 `response.create`（[实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)）。
- **Manual 模式**：`turn_detection` 设为 `null`。客户端需显式 `append_audio` → `input_audio_buffer.commit` → `response.create` 触发响应（[实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)）。

### 工具调用流程
1. 模型返回 `response.function_call_arguments.done` 事件，含 `call_id` 和参数。
2. 客户端执行本地函数，获取结果。
3. 发送 `conversation.item.create` 事件，携带 `call_id` 和 `output`。
4. VAD 模式下服务端自动响应；Manual 模式下需再发 `response.create`（[实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)）。

## 限制和注意事项

- **音频/图像限制**：输入音频必须为 16kHz PCM；图像仅支持 JPG/JPEG，Base64 编码后 ≤256KB，建议分辨率 480p/720p（[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- **参数互斥性**：`enable_search` 与 `tools` 不可同时启用（[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- **模型能力边界**：`qwen-omni-turbo-realtime` 系列禁用所有生成参数调节，`qwen3-omni-flash-realtime` 不支持 `semantic_vad` 和 `enable_search`（[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- **域名迁移**：北京/新加坡地域必须使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等），旧域名虽兼容但性能与稳定性较低（[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)、[Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)、[声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md) 均强调此点）。
- **声音复刻一致性**：复刻时指定的 `target_model`（如 `qwen3.5-omni-plus-realtime`）必须与后续 Omni 实时调用的 `model` 参数完全一致，否则音色无法加载（[声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


