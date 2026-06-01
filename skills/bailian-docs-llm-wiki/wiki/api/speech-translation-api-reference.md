# speech translation api reference

百炼平台提供两类语音/音视频翻译 API：基于 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)的离线翻译（qwen3-livetranslate-flash）和基于 WebSocket 的实时翻译（qwen3.5-livetranslate-flash-realtime）。前者适用于已有音频或视频文件的翻译场景，后者适用于实时语音流式翻译场景，支持声音复刻和热词定制。

## 支持的模型

| 模型名称 | 接口类型 | 说明 |
|---------|---------|------|
| `qwen3-livetranslate-flash` | OpenAI 兼容（HTTP） | 离线音视频翻译，支持音频/视频文件输入 |
| `qwen3-livetranslate-flash-2025-12-01` | OpenAI 兼容（HTTP） | 同上，日期快照版本 |
| `qwen3.5-livetranslate-flash-realtime` | WebSocket | 实时语音翻译（推荐），支持声音复刻 |
| `qwen3-livetranslate-flash-realtime` | WebSocket | 旧版实时翻译模型 |

## 离线翻译接口（OpenAI 兼容）

详见 [音视频翻译-通义千问 API 参考](../../raw/model-api-reference/speech-translation-api-reference/qwen3-livetranslate-flash-api.md)。

### 调用地址

| 地域 | base_url |
|------|----------|
| 北京 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |

> **注意**：不支持通过 DashScope 接口调用离线翻译模型，仅可通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用。

### 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型名称 |
| `messages` | array | 是 | 仅支持传入一个 User Message，包含 `input_audio` 或 `video_url` |
| `stream` | boolean | 是 | 必须设为 `true`，仅支持[流式输出](../concepts/streaming.md) |
| `modalities` | array | 否 | `["text","audio"]` 输出文本+音频；`["text"]` 仅输出文本 |
| `audio` | object | 否 | 设置输出音色（`voice`）和格式（仅支持 `wav`） |
| `translation_options` | object | 是 | 翻译配置，含 `source_lang`（可选）和 `target_lang`（必选） |

`translation_options` 为非 OpenAI 标准参数，Python SDK 调用时需放入 `extra_body` 中：

```python
extra_body={"translation_options": {"source_lang": "zh", "target_lang": "en"}}
```

### 输入格式

- **音频输入**：`type` 设为 `input_audio`，通过 `data` 传入音频 URL 或 Base64，`format` 指定格式（如 `mp3`、`wav`）
- **视频输入**：`type` 设为 `video_url`，通过 `url` 传入视频文件 URL 或 Base64

### 响应结构

流式返回三类 chunk：
1. **文本 chunk**：`choices[0].delta.content` 包含增量翻译文本
2. **音频 chunk**：`choices[0].delta.audio.data` 包含 Base64 音频数据
3. **Token 消耗 chunk**：`usage` 字段包含 [prompt](../guides/prompt.md)_tokens、completion_tokens 等统计

## 实时翻译接口（WebSocket）

实时翻译通过 WebSocket 连接实现双向通信。详细的事件定义参见 [客户端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-client-events.md) 和 [服务端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-server-events.md)。

### 连接地址

| 地域 | WebSocket URL |
|------|--------------|
| 中国内地 | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` |
| 国际 | `wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime` |

### 会话配置（session.update）

连接建立后，客户端需首先发送 `session.update` 事件配置会话参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `modalities` | array | `["text","audio"]` | 输出模态 |
| `voice` | string | Qwen3.5: `Tina`; Qwen3: `Cherry` | 输出音色 |
| `sample_rate` | integer | 16000 | 输入采样率（8000 或 16000） |
| `input_audio_format` | string | `pcm` | 输入音频格式（`pcm` 或 `opus`） |
| `output_audio_format` | string | `pcm` | 输出音频格式（当前仅支持 `pcm`） |
| `input_audio_transcription.model` | string | - | 设为 `qwen3-asr-flash-realtime` 可同时返回源语言识别结果 |
| `input_audio_transcription.language` | string | `en` | 源语种 |
| `translation.language` | string | `en` | 目标语种 |
| `translation.corpus.phrases` | object | - | 热词映射表 |
| `enable_voice_clone` | boolean | `false` | 是否启用声音复刻 |

> **注意**：服务端事件 `session.created` 示例中显示 `voice` 为 `Cherry`，但文档说明 Qwen3.5-LiveTranslate-Flash-Realtime 的默认音色为 `Tina`。请以参数说明为准。

### 声音复刻

启用声音复刻时，需将 `enable_voice_clone` 设为 `true`，并通过 `voice_clone_options.frequency` 控制复刻策略：

- `once`：会话开始时基于输入音频复刻一次（单人场景），`voice` 设为 `default`
- `always`：每次输出前实时复刻（多人场景），`voice` 设为 `default`
- `never`：使用预先复刻的音色 ID，`voice` 设为该 ID

### 客户端事件

| 事件 | 说明 |
|------|------|
| `session.update` | 更新会话配置 |
| `input_audio_buffer.append` | 追加 Base64 编码的音频数据 |
| `input_image_buffer.append` | 追加 Base64 编码的图像数据（JPG/JPEG） |
| `session.finish` | 通知服务端结束会话 |

### 服务端事件

| 事件 | 说明 |
|------|------|
| `session.created` | 连接建立后返回默认配置 |
| `session.updated` | 配置更新成功 |
| `session.finished` | 会话结束，客户端可断开连接 |
| `response.created` | 新的翻译响应开始 |
| `response.done` | 响应完成，含 Token 消耗信息 |
| `response.text.text` | 增量文本输出（仅文本模态） |
| `response.text.done` | 文本输出完成 |
| `response.audio.delta` | 增量音频输出 |
| `response.audio.done` | 音频输出完成 |
| `response.audio_transcript.text` | 音频模态下的增量翻译文本 |
| `response.audio_transcript.done` | 音频模态下的完整翻译文本 |
| `conversation.item.input_audio_transcription.text` | 输入音频的增量识别结果 |
| `conversation.item.input_audio_transcription.completed` | 输入音频识别完成 |
| `error` | 错误信息 |

### 文本流式机制

实时翻译文本输出使用 `text` + `stash` 机制：
- `text`：已确认的翻译文本
- `stash`：待确认的临时文本（可能被后续事件修正）
- 收到 `done` 事件后，`text`/`transcript` 字段即为最终完整结果

## SDK 使用

### Python SDK（DashScope）

详见 [实时音视频翻译（Qwen-LiveTranslate）Python SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-python-sdk.md)。

- 要求 DashScope SDK 版本 ≥ 1.25.6
- 核心类：`OmniRealtimeConversation`、`OmniRealtimeCallback`、`TranslationParams`
- 关键方法：`connect()`、`update_session()`、`append_audio()`、`end_session()`、`close()`

### Java SDK（DashScope）

详见 [实时音视频翻译（Qwen-LiveTranslate）Java SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-java-sdk.md)。

- 要求 DashScope SDK 版本 ≥ 2.22.5
- 核心类：`OmniRealtimeConversation`、`OmniRealtimeCallback`、`OmniRealtimeParam`、`OmniRealtimeConfig`
- Java SDK 额外提供 `getFirstTextDelay()` 和 `getFirstAudioDelay()` 方法获取延迟信息

### OpenAI SDK（离线翻译）

离线翻译可通过 OpenAI Python/Node.js SDK 或 curl 直接调用，使用标准 chat completions 接口。

## 限制和注意事项

- 离线翻译仅支持**[流式输出](../concepts/streaming.md)**（`stream` 必须为 `true`）
- 离线翻译输出音频格式仅支持 `wav`
- 实时翻译图像输入限制：JPG/JPEG 格式，建议 480p/720p，最高 1080p，单张 ≤ 500KB，频率 ≤ 2 帧/秒，且需先发送过音频数据
- `temperature`、`top_p`、`top_k`、`presence_penalty`、`repetition_penalty` 等采样参数不建议修改，以保证翻译准确性
- 非 OpenAI 标准参数（如 `translation_options`、`top_k`、`repetition_penalty`）在 Python SDK 中需通过 `extra_body` 传递
- 北京地域和新加坡地域使用不同的 API Key

## 来源文档

- [音视频翻译-通义千问 API 参考](../../raw/model-api-reference/speech-translation-api-reference/qwen3-livetranslate-flash-api.md)
- [客户端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-client-events.md)
- [服务端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-server-events.md)
- [实时音视频翻译（Qwen-LiveTranslate）Python SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-python-sdk.md)
- [实时音视频翻译（Qwen-LiveTranslate）Java SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-java-sdk.md)

