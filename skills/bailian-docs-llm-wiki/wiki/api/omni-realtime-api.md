# omni realtime api

Qwen-Omni-Realtime API 是百炼平台提供的实时多模态交互接口，基于 WebSocket 协议实现低延迟的音频、视频、文本双向流式通信。该 API 支持语音活动检测（VAD）、语音打断、工具调用（Function Calling）、联网搜索及声音复刻等能力，适用于实时语音对话、音视频交互等场景。

## 支持的模型

| 模型系列 | 默认音色 | 特有功能 | 备注 |
|---------|---------|---------|------|
| `qwen3.5-omni-realtime` 系列 | Tina | 联网搜索、工具调用、`semantic_vad` | 功能最全 |
| `qwen3-omni-flash-realtime` 系列 | Cherry | `smooth_output` 控制回复风格 | — |
| `qwen-omni-turbo-realtime` 系列 | Chelsie | — | 多数采样参数**不支持修改** |

> **注意**：`qwen-omni-turbo` 系列模型不支持修改 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等参数。

声音复刻功能当前仅支持 `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 模型，详见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

## 交互模式

API 提供两种交互模式，详细流程参见 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。

### VAD 模式（默认）

将 `turn_detection` 设为 `"server_vad"` 或 `"semantic_vad"` 启用。服务端自动检测语音起止并触发模型响应，支持语音打断。适用于持续发送音频的实时对话场景。

- 服务端自动提交音频缓冲区，客户端无需手动 commit
- 检测到用户说话时自动打断正在进行的模型回复
- `semantic_vad` 模式可过滤回应语和背景音（仅 `qwen3.5-omni-realtime` 支持）

### Manual 模式

将 `turn_detection` 设为 `null` 启用。客户端需手动发送 `input_audio_buffer.commit` 提交音频，再发送 `response.create` 触发响应。适用于"按下即说"等需要精确控制发送节奏的场景。

## 客户端与服务端事件

API 通过 WebSocket 进行双向事件通信。完整的事件定义参见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 和 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

### 主要客户端事件

| 事件 | 用途 |
|------|------|
| `session.update` | 更新会话配置（模态、音色、VAD、工具等） |
| `input_audio_buffer.append` | 追加 Base64 编码的音频数据 |
| `input_image_buffer.append` | 追加 Base64 编码的图像数据 |
| `input_audio_buffer.commit` | 提交音频缓冲区（Manual 模式必需） |
| `input_audio_buffer.clear` | 清除音频缓冲区 |
| `response.create` | 触发模型生成响应 |
| `response.cancel` | 取消正在进行的响应 |
| `conversation.item.create` | 回传工具函数执行结果 |

### 主要服务端事件

| 事件 | 用途 |
|------|------|
| `session.created` / `session.updated` | 会话创建/配置更新确认 |
| `input_audio_buffer.speech_started` / `speech_stopped` | VAD 检测到语音开始/结束 |
| `response.audio.delta` / `response.text.delta` | 增量音频/文本输出 |
| `response.audio_transcript.delta` / `done` | 模型输出转录文本 |
| `conversation.item.input_audio_transcription.delta` / `completed` | 用户输入音频的实时/最终转录 |
| `response.function_call_arguments.delta` / `done` | 工具调用参数（增量/完成） |
| `response.done` | 响应完成 |
| `error` | 错误信息 |

## 关键参数

### 会话配置（session.update）

通过 `session.update` 事件或 SDK 的 `update_session` 方法设置：

- **modalities**：输出模态，`["text"]` 或 `["text", "audio"]`（默认）
- **voice**：音色，各模型默认值不同
- **instructions**：系统消息，设定模型角色
- **input_audio_format**：仅支持 `pcm`（16 kHz）
- **output_audio_format**：仅支持 `pcm`（24 kHz），不支持自定义输出采样率
- **smooth_output**：回复风格控制（仅 `qwen3-omni-flash-realtime` 生效）

### VAD 配置

| 参数 | 说明 | 范围 | 默认值 |
|------|------|------|--------|
| `type` | `server_vad` 或 `semantic_vad` | — | `server_vad` |
| `threshold` | 灵敏度，值越低越灵敏 | [-1.0, 1.0] | 0.5 |
| `silence_duration_ms` | 静音触发响应的最短时间（毫秒） | [200, 6000] | 800 |

### 采样参数

各模型的默认值有所不同，具体默认值可参考客户端事件文档。`temperature` 和 `top_p` 建议只设置其中一个。

### 工具调用与联网搜索

- **tools**：工具定义列表，仅 `qwen3.5-omni-realtime` 支持
- **enable_search**：联网搜索，仅 `qwen3.5-omni-realtime` 支持

> **注意**：`tools` 和 `enable_search` **不可同时开启**。

## SDK 使用

### Python SDK

SDK 版本需 ≥ 1.25.17。通过 `OmniRealtimeConversation` 类进行交互：

```python
from dashscope.audio.qwen_omni import MultiModality, OmniRealtimeCallback, OmniRealtimeConversation

conv = OmniRealtimeConversation(model="qwen3.5-omni-realtime", callback=callback)
conv.connect()
conv.update_session(
    output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
    voice="Tina"
)
# 持续发送音频
conv.append_audio(base64_audio)
# Manual 模式需手动提交和创建响应
# conv.commit()
# conv.create_response()
```

详见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

### Java SDK

SDK 版本需 ≥ 2.22.15。通过 `OmniRealtimeConversation` 和 `OmniRealtimeParam` / `OmniRealtimeConfig` 进行配置。部分参数（如 `instructions`、`temperature`、`tools` 等）需通过 `OmniRealtimeConfig` 的 `parameters` 方法设置。

## 图像/视频输入限制

- 格式：JPG / JPEG
- 分辨率：建议 480p 或 720p，最高 1080p
- 单张图片 Base64 编码后 ≤ 256 KB（建议原始 ≤ 190 KB）
- 推荐发送频率：1 张/秒
- 发送图像前须至少发送过一次音频数据
- 图像缓冲区随 `input_audio_buffer.commit` 一起提交

## 音频输入与对齐

- 输入音频以时间轴为基准，图片按发送时间插入音频流中
- 推荐音频发送频率：100ms 一包
- 推荐使用耳机播放，避免回声触发语音打断

## 声音复刻

通过 `qwen-voice-enrollment` 模型创建自定义音色，仅需 10~20 秒音频。创建音色时指定的 `target_model` 必须与后续实时对话使用的模型一致。支持中文、英文等 30 余种语言及多种中文方言。

## 工具调用流程

1. 服务端识别到需要调用工具后，发送 `response.function_call_arguments.done` 事件
2. 客户端本地执行工具函数
3. 客户端通过 `conversation.item.create` 回传执行结果（`type` 为 `function_call_output`）
4. VAD 模式下服务端自动生成最终响应；Manual 模式下需额外发送 `response.create`

> **注意**：命中工具调用时，模型不生成音频，仅返回工具调用参数。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)

