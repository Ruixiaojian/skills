# omni realtime api

Qwen-Omni Realtime API 是阿里云百炼平台提供的低延迟、[多模态](../concepts/multi-modal.md)实时交互接口，支持语音/音视频输入与文本/音频输出的流式双向通信。它基于 WebSocket 协议，内置 VAD（语音活动检测）、ASR（语音识别）、LLM 推理与 TTS（语音合成）全链路能力，适用于智能客服、虚拟助手、实时会议等场景。开发者可通过 Python 或 Java SDK 快速集成，无需自行编排模型调用流程。

## 支持的模型与功能

当前支持以下 Qwen-Omni 实时系列模型，各模型能力存在差异，需按需选型：

- **`qwen3.5-omni-realtime`**：基础旗舰版，支持 `semantic_vad`、联网搜索（`enable_search`）和工具调用（`tools`），是唯一同时支持三者的模型。
- **`qwen3.5-omni-plus-realtime` 与 `qwen3.5-omni-flash-realtime`**：增强与轻量变体，支持 `idle_timeout_ms` 等高级 VAD 参数，但**不支持 `semantic_vad`**；仅 `plus` 版支持声音复刻驱动（见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）。
- **`qwen3-omni-flash-realtime`**：侧重响应速度，支持 `smooth_output` 口语化控制，但**不支持联网搜索与工具调用**。
- **`qwen-omni-turbo-realtime`**：极致轻量版，参数（如 `temperature`、`top_p`、`max_tokens` 等）**完全不可修改**，仅支持基础对话。

> **注意**：文档 1 和文档 6 均称 `qwen3.5-omni-realtime` 支持 `semantic_vad`，而文档 2 明确指出该能力“仅 `qwen3.5-omni-realtime` 系列模型支持”，但文档 4 的 `session.created` 示例中 `turn_detection.type` 字段注释却写为“取值为 `server_vad` 或 `semantic_vad`（仅 `qwen3.5-omni-realtime` 支持）”，存在表述冗余。以文档 1 和文档 2 的明确限定为准：`semantic_vad` 为 `qwen3.5-omni-realtime` 独占特性。

所有模型均支持：
- [多模态](../concepts/multi-modal.md)输入：纯音频、音视频（`append_audio` + `append_video`）
- [多模态](../concepts/multi-modal.md)输出：文本（`TEXT`）与音频（`AUDIO`）组合
- 实时语音转录（ASR）：固定使用 `qwen3-asr-flash-realtime` 模型，不可替换
- 声音复刻音色接入：需确保复刻时指定的 `target_model` 与实时对话模型严格一致（详见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）

## 关键参数

参数分为连接级（构造时设置）与会话级（`update_session` 时设置），部分参数模型间行为不同：

| 参数 | 类型 | 说明 | 模型兼容性 |
|------|------|------|------------|
| `model` | `str`/`String` | 模型名称，如 `"qwen3.5-omni-realtime"` | 所有模型 |
| `url` | `str`/`String` | WebSocket 地址，**必须使用业务空间专属域名**：<br>`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`（北京）<br>`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`（新加坡） | 所有模型，[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 与 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 均强调此迁移要求 |
| `output_modalities` | `list[MultiModality]`/`List<OmniRealtimeModality>` | 输出模态，`[TEXT]` 或 `[TEXT, AUDIO]`（默认） | 所有模型 |
| `voice` | `str`/`String` | 音色名，如 `"Tina"`；自定义音色需通过声音复刻获取 | 所有模型 |
| `turn_detection_type` | `str`/`String` | VAD 类型：`"server_vad"`（默认）或 `"semantic_vad"`（仅 `qwen3.5-omni-realtime`） | 见上文注意项 |
| `enable_search` | `bool`/`Boolean` | 启用联网搜索，**与 `tools` 互斥** | 仅 `qwen3.5-omni-realtime` |
| `tools` | `list[dict]`/`List<Map<String, Object>>` | 工具定义列表，**与 `enable_search` 互斥** | 仅 `qwen3.5-omni-realtime` |
| `smooth_output` | `bool`/`Boolean` | 口语化开关，`true`/`false`/`null`，**仅 `qwen3-omni-flash-realtime` 支持** | 仅 `qwen3-omni-flash-realtime` |
| `temperature` / `top_p` / `top_k` / `max_tokens` 等采样参数 | 各自类型 | 控制生成多样性与长度，详见各文档默认值表 | `qwen-omni-turbo-realtime` 系列**全部不可修改** |

> **注意**：`repetition_penalty` 默认值在文档 1 中写为“其他模型：1.05”，而文档 2 写为“`qwen3-omni-flash-realtime` 系列：1.05；`qwen-omni-turbo-realtime` 系列：1.05”，文档 4 的 `session.created` 示例中亦为 `1.05`。文档 6 未提及其他模型默认值，仅重复 `qwen3.5-omni-realtime` 为 `1.0`。此处以文档 2 的完整列表为准。

## 使用方式

API 交互基于 WebSocket，核心流程分两种模式：

### 1. VAD 模式（推荐，默认）
服务端自动检测语音起止并触发响应，客户端只需持续 `append_audio`（及可选 `append_video`）：
```python
conv = OmniRealtimeConversation(model="qwen3.5-omni-realtime", callback=cb, url=url)
conv.connect()
conv.update_session(enable_turn_detection=True)  # 启用 server_vad
# 循环：mic.read() → conv.append_audio(base64)
# 无需手动 commit 或 create_response
```
- 事件流：`input_audio_buffer.speech_started` → `input_audio_buffer.speech_stopped` → `input_audio_buffer.committed` → `response.*`
- 工具调用时，服务端发送 `response.function_call_arguments.done` 后，客户端执行工具并调用 `conversation.item.create`，服务端**自动**生成最终响应（见 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)）。

### 2. Manual 模式
客户端完全控制节奏，需显式提交与触发：
```java
conversation.updateSession(OmniRealtimeConfig.builder()
    .enableTurnDetection(false) // 关闭 VAD
    .build());
// ... appendAudio ...
conversation.commit(); // 提交音频缓冲区
conversation.createResponse(null, Arrays.asList(AUDIO, TEXT)); // 触发响应
```
- 适用场景：聊天软件“按住说话”、离线音频文件处理。
- 工具调用时，客户端在收到 `response.function_call_arguments.done` 后，需**手动再次调用 `createResponse`** 触发最终响应（见 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)）。

## 限制和注意事项

- **域名迁移强制要求**：华北2（北京）与新加坡地域必须使用 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 或 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，旧域名 `dashscope.aliyuncs.com` 将逐步下线（[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 与 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 均明确提示）。
- **音视频格式约束**：
  - 输入音频：`PCM_16000HZ_MONO_16BIT`（Python）或 `PCM_16000HZ_MONO_16BIT`（Java），Base64 编码。
  - 输入视频：JPG/JPEG 格式，分辨率建议 480P–720P（≤1080P），单图 Base64 后 ≤256KB。
  - 输出音频：固定 `PCM_24000HZ_MONO_16BIT`，不可自定义。
- **并发与资源**：单个 WebSocket 连接对应一个会话；`append_audio` 单次数据块无明确上限，但 `commit` 前总缓冲区建议 ≤15 MiB（[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 提示）。
- **互斥配置**：`enable_search` 与 `tools` 不可同时启用，否则返回 `invalid_request_error`（[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 明确说明）。
- **错误处理**：所有服务端错误均以 `error` 事件返回，含 `type`、`code`、`message` 和 `param`（见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）。

## 来源文档

- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)


