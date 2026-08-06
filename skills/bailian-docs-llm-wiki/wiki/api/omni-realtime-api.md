# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时[多模态](../concepts/multimodal.md)交互接口，支持语音输入、文本/音频输出、音视频融合、工具调用与联网搜索（部分模型），适用于智能客服、虚拟助手等低延迟对话场景。其核心为会话驱动的事件流协议，客户端通过发送标准化事件控制交互节奏，服务端以异步事件流返回响应。

## 支持的模型/功能

- **模型系列**：当前支持 `qwen3.5-omni-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime` 和 `qwen-omni-turbo-realtime` 等系列模型。各模型能力存在差异，例如 `semantic_vad` 仅 `qwen3.5-omni-realtime` 支持，`smooth_output` 仅 `qwen3-omni-flash-realtime` 系列生效 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **[多模态](../concepts/multimodal.md)输入**：支持 PCM 音频（16 kHz）和 JPG/JPEG 图像（≤1080p，Base64 编码，单图 ≤256 KB）[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **[多模态](../concepts/multimodal.md)输出**：支持 `["text"]` 或 `["text", "audio"]` 输出模态，音频格式固定为 24 kHz PCM [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **高级能力**：
  - 工具调用（`tools`）：仅 `qwen3.5-omni-realtime` 系列支持，需在 `session.update` 中声明函数定义。
  - 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 不兼容，不可同时启用。
  - 声音复刻音色：可将自定义音色（通过 `qwen-voice-enrollment` 创建）用于 `qwen3.5-omni-plus-realtime` 等指定模型，但复刻时 `target_model` 必须与后续 Omni 调用模型严格一致 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：文档中 `qwen3.5-omni-plus-realtime` 模型在 VAD 参数 `idle_timeout_ms` 的适用性描述存在不一致——[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 明确将其列为生效条件之一，而 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 也确认该字段会在对应模型下返回；但 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 和 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 的说明中仅提及 `qwen3.5-omni-flash-realtime`，未提 `plus`。实际使用时应以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 文档为准，即 `qwen3.5-omni-plus-realtime` 同样支持 `idle_timeout_ms`。

## 关键参数

所有可配置参数均通过 `session.update` 客户端事件或 SDK 的 `update_session` 方法设置，核心参数如下：

- **`modalities`**：输出模态数组，仅支持 `["text"]` 或 `["text","audio"]`（默认）。
- **`voice`**：音色名称，不同模型有默认值（如 `qwen3.5-omni-realtime`: `"Tina"`），亦可设为声音复刻生成的自定义 voice ID。
- **`instructions`**：系统提示词，用于设定角色与行为准则。
- **`turn_detection`**：VAD 配置对象，含 `type`（`server_vad` 或 `semantic_vad`）、`threshold`（[-1.0, 1.0]）、`silence_duration_ms`（[200, 6000] ms）及可选 `idle_timeout_ms`（[5000, 30000] ms）。
- **采样控制参数**（`temperature`、`top_p`、`top_k`、`repetition_penalty`、`presence_penalty`、`seed`、`max_tokens`）：各模型有默认值且部分参数（如 `qwen-omni-turbo` 系列）不支持修改，详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中的详细表格。
- **`smooth_output`**：仅 `qwen3-omni-flash-realtime` 系列支持，控制回复风格（`true` 口语化，`false` 书面化，`null` 自动选择）。
- **`enable_search` 与 `search_options`**：仅 `qwen3.5-omni-realtime` 系列支持，启用后模型可自主触发搜索，`search_options.enable_source` 控制是否返回来源。

## 使用方式

1. **建立连接**：使用 WebSocket 连接到地域专属域名（如北京：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），[Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 和 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 提供了封装好的 `connect()` 方法。
2. **初始化会话**：连接后，服务端立即返回 `session.created` 事件。随后应调用 `update_session` 发送 `session.update` 事件，以应用自定义配置（如 `instructions`、`voice` 等）。
3. **输入处理**：
   - **VAD 模式**（推荐，默认）：客户端持续 `append_audio`，服务端自动检测语音起止并触发 `input_audio_buffer.speech_started`/`speech_stopped`，无需手动 `commit`。
   - **Manual 模式**：客户端 `append_audio` 后，显式调用 `commit()` 提交音频缓冲区，再发送 `response.create` 触发响应。
4. **工具调用**：当服务端返回 `conversation.item.created` 类型为 `function_call` 的事件时，客户端执行本地工具，然后通过 `conversation.item.create` 回传结果，并在 Manual 模式下再次 `response.create`。
5. **响应消费**：服务端以流式事件返回响应，关键事件包括 `response.content_part.added`（文本增量）、`response.audio.delta`（音频增量）、`response.done`（响应结束）等。

## 限制和注意事项

- **音频格式硬性要求**：输入必须为 16 kHz PCM，输出固定为 24 kHz PCM，不支持其他采样率或编码格式。
- **模型能力隔离**：`tools` 与 `enable_search` 互斥，且均仅限 `qwen3.5-omni-realtime` 系列；`semantic_vad` 仅该系列支持；`smooth_output` 仅 `qwen3-omni-flash-realtime` 系列支持。
- **参数兼容性**：`temperature` 与 `top_p` 功能重叠，官方建议二者只设置其一。
- **`max_tokens` 行为**：该参数仅截断最终响应，不影响模型内部生成过程。
- **SDK 版本要求**：Java SDK ≥ v2.22.15，Python SDK ≥ v1.25.17，旧版本可能缺失新参数或事件支持 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
- **域名迁移**：强烈建议迁移到业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更优性能与稳定性，旧域名虽仍可用但非最优路径 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


