# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的低延迟多模态实时交互接口，支持语音输入、文本/音频输出、工具调用与联网搜索（部分模型），适用于智能客服、虚拟助手等需要自然对话体验的场景。其核心为会话驱动的事件流模型，客户端通过发送结构化事件控制交互节奏，服务端以异步事件流返回响应。

## 支持的模型/功能

当前支持以下实时系列模型，各模型能力存在差异：

- `qwen3.5-omni-realtime`：支持 `semantic_vad`、`enable_search`、`tools`、`presence_penalty=1.5`（默认）；[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中明确列出其为 `enable_search` 和 `semantic_vad` 的唯一支持者。
- `qwen3-omni-flash-realtime`：支持 `smooth_output`、`idle_timeout_ms`（需配合 `server_vad`）、`repetition_penalty=1.05`（默认）；[原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 指出其默认音色为 `"Cherry"`，且 `smooth_output` 仅对该系列生效。
- `qwen-omni-turbo-realtime`：**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等生成参数；[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md) 多次强调该系列模型的参数不可变性。

> **注意**：文档 6（声音复刻）中声明驱动音色的全模态模型仅限 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` 等，**未包含 `qwen-omni-turbo-realtime`**。这意味着 turbo 系列不支持声音复刻，与文档 1 和 2 中 turbo 模型的音色配置（如 `"Chelsie"`）存在隐含矛盾——turbo 可设音色但无法复刻，此为能力边界限制，非配置错误。

核心功能包括：
- **双模态 I/O**：支持 `["text"]` 或 `["text","audio"]` 输出；输入音频强制 `pcm`（16kHz），输出音频强制 `pcm`（24kHz）。
- **VAD 模式**：`server_vad`（默认）或 `semantic_vad`（仅 qwen3.5-omni-realtime）；Manual 模式需显式 `input_audio_buffer.commit` + `response.create`。
- **工具调用**：通过 `tools` 数组定义函数，模型触发后客户端回传 `conversation.item.create`；与 `enable_search` 互斥。
- **联网搜索**：仅 `qwen3.5-omni-realtime` 支持，启用后模型可自主决策是否搜索并返回来源（`search_options.enable_source`）。

## 关键参数

所有参数均通过 `session.update` 事件或 SDK 的 `update_session` 方法配置。关键参数按作用域分类：

| 参数 | 作用域 | 说明 | 默认值/约束 |
|--------|---------|------|-------------|
| `modalities` | 全局 | 输出模态 | `["text","audio"]`；`["text"]` 合法，`["audio"]` 非法（[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md) 明确要求组合） |
| `voice` | 全局 | 音色ID | 按模型区分：`qwen3.5-*`: `"Tina"`；`qwen3-omni-flash-*`: `"Cherry"`；`qwen-omni-turbo-*`: `"Chelsie"` |
| `turn_detection.type` | VAD | VAD 类型 | `server_vad`（默认）；`semantic_vad` 仅 `qwen3.5-omni-realtime` 支持 |
| `turn_detection.threshold` | VAD | 灵敏度 | `[-1.0, 1.0]`，默认 `0.5` |
| `turn_detection.silence_duration_ms` | VAD | 静音触发阈值 | `[200, 6000]` ms，默认 `800` |
| `idle_timeout_ms` | VAD 扩展 | 静默超时引导 | `[5000, 30000]` ms，**仅 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 有效** |
| `enable_search` | 功能开关 | 启用联网搜索 | `false`；仅 `qwen3.5-omni-realtime` 生效，且与 `tools` 不兼容 |
| `tools` | 功能开关 | 工具定义列表 | 空数组；每个工具需含 `type="function"`、`function.name`、`function.description` |
| `temperature` / `top_p` / `top_k` | 生成控制 | 多样性控制 | **`qwen-omni-turbo` 系列完全不可修改**；建议二者择一设置 |
| `max_tokens` | 生成控制 | 最大输出长度 | 截断响应，不影响生成过程；`qwen-omni-turbo` 不可修改 |
| `smooth_output` | 生成风格 | 口语化/书面化 | `true`（口语）、`false`（书面）、`null`（自动）；**仅 `qwen3-omni-flash-realtime` 支持** |

## 使用方式

1. **建立连接**：使用业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），避免旧域名 `dashscope.aliyuncs.com`。
2. **初始化会话**：连接后立即调用 `update_session`（SDK）或发送 `session.update` 事件，配置 `modalities`、`voice`、`turn_detection` 等。
3. **输入处理**：
   - *VAD 模式*（`enable_turn_detection=true`）：持续 `append_audio`，服务端自动检测 `speech_started`/`speech_stopped` 并提交。
   - *Manual 模式*（`enable_turn_detection=false`）：`append_audio` → `commit` → `response.create`。
   - 图像输入：`append_video`（JPG/JPEG，≤256KB Base64），与音频缓冲区一同由 `commit` 提交。
4. **响应生成**：
   - VAD 模式下服务端自动触发 `response.created` → `response.content_part.added` → `response.done`。
   - Manual 模式或工具调用后需显式 `response.create`。
5. **工具调用流程**：`response.function_call_arguments.done` → 客户端执行工具 → `conversation.item.create` → （VAD 模式自动 / Manual 模式需再次 `response.create`）→ 最终响应。

## 限制和注意事项

- **音频格式硬性限制**：输入必须为 16kHz PCM，输出固定为 24kHz PCM；`input_audio_format`/`output_audio_format` 仅允许 `"pcm"`，设其他值将报错。
- **参数不可变性**：`qwen-omni-turbo-realtime` 系列所有生成参数（`temperature`, `top_p`, `max_tokens` 等）均不可修改，尝试设置将被忽略或报错。
- **功能互斥**：`enable_search` 与 `tools` 不可同时启用，否则 `session.update` 将返回 `invalid_request_error`。
- **音色一致性**：声音复刻创建的音色（文档 6）**必须与 Omni 调用时的 `model` 参数严格一致**，否则合成失败；`qwen-omni-turbo-realtime` 不在复刻支持列表中。
- **VAD 模式依赖**：`idle_timeout_ms` 仅在 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` 且 `turn_detection.type="server_vad"` 时生效，其他组合下该字段无效。
- **图像限制**：单图 Base64 ≤ 256KB，建议原始大小 ≤ 190KB；分辨率推荐 480p/720p，最高 1080p；需先发送 `append_audio` 才能发送 `append_video`。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


