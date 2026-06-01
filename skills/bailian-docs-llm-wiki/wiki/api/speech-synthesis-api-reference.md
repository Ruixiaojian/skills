# speech synthesis api reference

百炼平台提供多种语音合成（TTS）API，涵盖 Qwen-TTS、CosyVoice、Sambert 和 MiniMax 等模型系列，支持实时与非实时两种合成模式。本文汇总各模型的接口规格、关键参数和调用方式，帮助开发者快速选型和集成。

## 支持的模型

### Qwen-TTS 系列

| 模型 | 模式 | 协议 | 说明 |
|------|------|------|------|
| `qwen3-tts-flash` | 非实时 | HTTP | 基础语音合成 |
| `qwen3-tts-instruct-flash` | 非实时 | HTTP | 支持指令控制（instructions）|
| `qwen3-tts-flash-realtime` | 实时 | WebSocket | 实时流式合成 |
| `qwen3-tts-instruct-flash-realtime` | 实时 | WebSocket | 实时 + 指令控制 |

详见 [非实时语音合成（Qwen-TTS）API参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-api.md) 和 [Qwen-TTS-Realtime WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/interactive-process-of-qwen-tts-realtime-synthesis.md)。

### CosyVoice 系列

| 模型 | 协议 | 备注 |
|------|------|------|
| `cosyvoice-v3.5-plus` | WebSocket / HTTP | 最新版本 |
| `cosyvoice-v3.5-flash` | WebSocket / HTTP | 低延迟版 |
| `cosyvoice-v3-plus` | WebSocket / HTTP | — |
| `cosyvoice-v3-flash` | WebSocket / HTTP | — |
| `cosyvoice-v2` | WebSocket / HTTP | — |

CosyVoice 同时支持实时（WebSocket 双向流式）和非实时（HTTP）两种调用方式。非实时 HTTP 方式仅在中国内地（北京地域）可用。

### Sambert 系列

Sambert 模型（如 `sambert-zhichu-v1`）仅支持在北京地域使用，且不支持流式文本输入——所有待合成文本必须在 `run-task` 事件中一次性发送。

### MiniMax 系列

| 模型 | 单价（每万字符）|
|------|----------------|
| `MiniMax/speech-2.8-hd` | 3.5 元 |
| `MiniMax/speech-02-hd` | 3.5 元 |
| `MiniMax/speech-2.8-turbo` | 2 元 |
| `MiniMax/speech-02-turbo` | 2 元 |

## 服务端点

### HTTP 端点

| 部署范围 | URL |
|---------|-----|
| 中国内地（北京）| `https://dashscope.aliyuncs.com/api/v1` |
| 国际（新加坡）| `https://dashscope-intl.aliyuncs.com/api/v1` |

### WebSocket 端点

| 模型系列 | 中国内地 | 国际 |
|---------|---------|------|
| CosyVoice / Sambert | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` | `wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference` |
| Qwen-TTS Realtime | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=<model>` | `wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime?model=<model>` |

> **注意**：Sambert 仅支持北京地域的 WebSocket 端点，不支持国际地域。不同地域的 API Key 不同，请确保使用对应地域的 Key。

## 关键参数

### 通用音频参数

以下参数在大多数模型中通用，但取值范围和默认值因模型而异：

| 参数 | 类型 | 说明 | CosyVoice 默认值 | Qwen-TTS Realtime 默认值 | Sambert 默认值 |
|------|------|------|-----------------|------------------------|--------------|
| `voice` | string | 音色标识（必选）| — | Cherry | — |
| `format` | string | 音频格式 | mp3 | pcm | wav |
| `sample_rate` | integer | 采样率 (Hz) | 22050 | 24000 | 16000 |
| `volume` | integer | 音量 [0, 100] | 50 | 50 | 50 |
| `rate` / `speech_rate` | float | 语速 [0.5, 2.0] | 1.0 | 1.0 | 1.0 |
| `pitch` / `pitch_rate` | float | 音调 [0.5, 2.0] | 1.0 | — | 1.0 |

> **注意**：CosyVoice 的 `cosyvoice-v1` 模型不支持 `opus` 格式和 `seed` 参数。Qwen-TTS Realtime 的早期模型（`qwen-tts-realtime`）仅支持 `pcm` 格式和 24000 采样率。

### 音色相关

所有模型都支持系统预置音色。此外还可通过以下方式获取专属音色：

- **声音复刻**：上传音频样本创建音色，详见 [声音复刻HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-http-api.md)
- **声音设计**：通过文本描述生成音色（支持 CosyVoice 和 Qwen 两种声音设计模型）

每个模型仅支持一组特定的音色，不能跨模型混用。创建音色时的 `target_model` 必须与后续语音合成时使用的模型一致。

### Qwen-TTS Realtime 交互模式

Qwen-TTS Realtime 支持两种交互模式：

- **`server_commit`**（默认）：服务端自动判断文本分段与合成时机，平衡延迟与质量
- **`commit`**：客户端手动控制合成触发，延迟最低，需自行管理句子完整性

## 调用方式

### SDK 支持矩阵

| 模型系列 | Python SDK | Java SDK | Android SDK | iOS SDK | HTTP API | WebSocket |
|---------|-----------|---------|------------|---------|---------|-----------|
| Qwen-TTS（非实时）| ✅ | ✅ | — | — | ✅ | — |
| Qwen-TTS Realtime | ✅ | ✅ | — | — | — | ✅ |
| CosyVoice（实时）| ✅ | ✅ | ✅ | ✅ | — | ✅ |
| CosyVoice（非实时）| ✅ | ✅ | — | — | ✅ | — |
| Sambert | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| MiniMax | ✅ | ✅ | — | — | ✅ | — |

### CosyVoice WebSocket 交互流程

1. 建立 WebSocket 连接
2. 发送 `run-task` 事件（设置模型、音色等参数）
3. 收到 `task-started` 后，通过 `continue-task` 发送文本片段
4. 通过 binary 通道接收音频流，同时接收 `result-generated` 事件
5. 文本发送完毕后发送 `finish-task`
6. 收到 `task-finished` 后关闭或复用连接

同一次任务中 `run-task`、`continue-task`、`finish-task` 必须使用相同的 `task_id`。建议复用 WebSocket 连接处理多个任务。

### Qwen-TTS Realtime WebSocket 交互流程

1. 连接后收到 `session.created`
2. 发送 `session.update` 配置音色、格式等
3. 通过 `input_text_buffer.append` 添加文本
4. 通过 `input_text_buffer.commit`（commit 模式）或自动触发（server_commit 模式）合成
5. 接收 `response.audio.delta`（base64 编码音频）
6. 发送 `session.finish` 结束会话

### SDK 最低版本要求

| SDK | 最低版本 |
|-----|---------|
| DashScope Python | ≥ 1.25.11（Realtime）/ ≥ 1.25.17（非实时 CosyVoice）|
| DashScope Java | ≥ 2.22.7（Realtime）/ ≥ 2.22.15（非实时 CosyVoice）|

## 特性说明

### SSML 支持

CosyVoice 和 Sambert 支持 SSML 标记语言。使用时需将 `enable_ssml` 设为 `true`，且仅允许发送一次 `continue-task` 指令（CosyVoice WebSocket 模式下）。

### 字级别时间戳

通过 `word_timestamp_enabled` 参数开启。CosyVoice 仅部分音色支持（需参照音色列表中的标注），Sambert 所有模型均支持。Sambert 还额外支持 `phoneme_timestamp_enabled`（音素级别时间戳）。

### 指令控制（Instruct）

- Qwen-TTS：使用 `qwen3-tts-instruct-flash` 或 `qwen3-tts-instruct-flash-realtime` 模型，通过 `instructions` 参数传入自然语言描述
- CosyVoice：部分音色支持通过 `instruction` 参数设置情感、场景等

## 限制和注意事项

- 单次文本长度限制：SDK 调用一般不超过 **20000 字符**，累计不超过 **20 万字符**（CosyVoice 流式）；MiniMax 文本长度限制 **10000 字符**
- Sambert **不支持流式文本输入**（`streaming` 为 `out` 而非 `duplex`），不支持 `continue-task` 和 `finish-task` 指令
- CosyVoice 非实时 HTTP API **仅限中国内地（北京地域）** 使用
- 声音复刻/设计的 `target_model` 必须与语音合成时的 `model` 一致，否则合成将失败
- WebSocket 鉴权在握手阶段验证，API Key 无效或缺失将返回 HTTP 401/403 错误
- Qwen-TTS 非实时 API 中，Python SDK 的 `SpeechSynthesizer` 接口已统一为 `MultiModalConversation`，使用方法和参数保持一致

## 来源文档

- [非实时语音合成（Qwen-TTS）API参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-api.md)
- [声音设计API参考](../../raw/model-api-reference/speech-synthesis-api-reference/voice-design-api-references.md)
- [CosyVoice WebSocket API参考](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-websocket-api.md)
- [CosyVoice服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-server-events.md)
- [CosyVoice客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-client-events.md)
- [实时语音合成CosyVoice Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-java-sdk.md)
- [实时语音合成CosyVoice Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-python-sdk.md)
- [语音合成CosyVoice Android SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-android-sdk.md)
- [语音合成CosyVoice iOS SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-ios-sdk.md)
- [Sambert客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-client-events.md)
- [Sambert WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-websocket-api.md)
- [CosyVoice音色列表](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-voice-list.md)
- [Sambert服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-server-events.md)
- [语音合成Sambert Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-java-sdk.md)
- [语音合成Sambert Android SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-android-sdk.md)
- [语音合成Sambert Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-python-sdk.md)
- [Qwen-TTS-Realtime WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/interactive-process-of-qwen-tts-realtime-synthesis.md)
- [语音合成Sambert iOS SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-ios-sdk.md)
- [客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-client-events.md)
- [服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-server-events.md)
- [Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-python-sdk.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-http-api.md)
- [Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-java-sdk.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-java-sdk.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-python-sdk.md)
- [MiniMax同步语音合成API参考](../../raw/model-api-reference/speech-synthesis-api-reference/minimax-speech-synthesis/minimax-synchronous-speech-synthesis-api.md)
- [声音复刻Java SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-java-sdk.md)
- [声音复刻HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-http-api.md)
- [声音复刻Python SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-python-sdk.md)

