# omni realtime api

Qwen-Omni Realtime API 是阿里云百炼平台提供的低延迟、多模态实时交互接口，支持语音/音视频输入与文本/语音混合输出，适用于智能客服、虚拟助手等强交互场景。其核心能力基于 Qwen-Omni 系列实时模型（如 `qwen3.5-omni-realtime`），通过 WebSocket 协议实现端到端流式通信，并内置 VAD、ASR、TTS 及工具调用等全链路能力。

## 支持的模型与功能

- **主流模型**：`qwen3.5-omni-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`。各模型在能力上存在差异，例如 `qwen3.5-omni-realtime` 独家支持 `semantic_vad` 和 `enable_search`，而 `qwen-omni-turbo-realtime` 仅支持部分参数（如 `temperature`、`top_p` 等不可修改）[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
- **多模态输入**：支持纯音频、音视频（麦克风+摄像头）及本地音视频文件输入。图片需为 JPG/JPEG 格式，建议分辨率 480P–720P，单图 Base64 编码后 ≤256KB [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **多模态输出**：可配置 `output_modalities` 为 `["text"]` 或 `["text", "audio"]`，输出音频固定为 `PCM_24000HZ_MONO_16BIT` 格式。
- **高级能力**：
  - **VAD 模式**：自动检测语音起止（`server_vad` 或语义级 `semantic_vad`），支持语音打断；
  - **工具调用（Function Calling）**：仅 `qwen3.5-omni-realtime` 系列支持，需定义 `tools` 列表，与 `enable_search` 互斥；
  - **联网搜索**：仅 `qwen3.5-omni-realtime` 系列支持，启用 `enable_search` 后模型可自主触发搜索；
  - **声音复刻**：需先调用声音复刻 API 创建专属音色，且 `target_model` 必须与 Omni 实时调用模型严格一致 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：文档 1 与文档 6 中对 `qwen3.5-omni-realtime` 默认音色的描述不一致（文档 1 写 `"Tina"`，文档 6 写 `"Tina"` 但未标注系列全称），以 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 中明确标注的 `Qwen3.5-Omni-Realtime` 系列默认 `"Tina"` 为准。

## 关键参数

| 参数 | 类型 | 说明 | 适用模型 | 默认值 |
|------|------|------|----------|--------|
| `model` | string | 模型名称 | 全系列 | — |
| `voice` | string | 输出音色 | 全系列 | `qwen3.5`: `"Tina"`；`qwen3-flash`: `"Cherry"`；`turbo`: `"Chelsie"` |
| `turn_detection_type` | string | VAD 类型 | `qwen3.5-omni-realtime` 支持 `semantic_vad`，其余仅 `server_vad` | `"server_vad"` |
| `enable_search` | bool | 启用联网搜索 | 仅 `qwen3.5-omni-realtime` 系列 | `false` |
| `tools` | list[dict] | 工具定义列表 | 仅 `qwen3.5-omni-realtime` 系列 | `[]` |
| `smooth_output` | bool/null | 回复口语化程度 | 仅 `qwen3-omni-flash-realtime` | `null`（自动选择） |
| `temperature` / `top_p` / `top_k` | float/int | 生成多样性控制 | `qwen-omni-turbo` 系列**不支持修改** | 各模型有不同默认值，详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |

> **注意**：`qwen-omni-turbo-realtime` 系列模型对 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 均**不支持修改**，此限制在 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 中均被强调，属硬性约束。

## 使用方式

1. **连接初始化**：使用业务空间专属域名（推荐）建立 WebSocket 连接，格式为 `wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`，其中 `{WorkspaceId}` 需从百炼控制台获取 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
2. **会话配置**：
   - 调用 `update_session`（SDK）或发送 `session.update`（原始 WebSocket）设置 `output_modalities`、`voice`、`turn_detection` 等；
   - VAD 模式下 `enable_turn_detection=true`，Manual 模式下设为 `false` 并需手动 `commit` 和 `create_response` [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
3. **数据输入**：
   - 音频：`append_audio`（Base64 PCM 16kHz）；
   - 视频：`append_video`（Base64 JPG/JPEG，≤256KB）；
   - 提交：VAD 模式由服务端自动 `commit`，Manual 模式需客户端显式调用。
4. **响应处理**：
   - 服务端通过回调（如 `response.audio.delta`、`response.text.delta`）流式返回结果；
   - 工具调用时，客户端需监听 `response.function_call_arguments.done`，执行工具后通过 `conversation.item.create` 回传结果，再调用 `create_response` 触发最终响应。

## 限制和注意事项

- **地域与域名**：北京/新加坡地域已启用业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧域名 `wss://dashscope.aliyuncs.com`，**强烈建议迁移** [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
- **音频格式**：输入必须为 `PCM_16000HZ_MONO_16BIT`，输出固定为 `PCM_24000HZ_MONO_16BIT`，不支持自定义采样率。
- **并发与资源**：单次 `append_audio` 最大 15 MiB；图片建议 1 张/秒发送；VAD 模式下推荐使用耳机避免回声打断。
- **参数兼容性**：`tools` 与 `enable_search` 不可同时启用；`semantic_vad` 仅 `qwen3.5-omni-realtime` 支持；`idle_timeout_ms` 仅在 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 下生效。
- **错误处理**：服务端通过 `error` 事件返回结构化错误（含 `type`、`code`、`message`、`param`），需在回调中捕获并处理 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 来源文档

- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)


