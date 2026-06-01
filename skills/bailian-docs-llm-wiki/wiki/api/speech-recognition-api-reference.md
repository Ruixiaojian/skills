# Speech Recognition API Reference

百炼平台提供多种语音识别模型和 API，覆盖实时语音识别与录音文件识别两大场景。本文汇总了各模型系列（Qwen-ASR、Fun-ASR、Paraformer）的接入方式、关键参数、支持的 SDK 及使用限制，帮助开发者快速选型和集成。

## 支持的模型与功能概览

平台语音识别服务分为**实时语音识别**和**录音文件识别**两大类，涵盖三个模型系列：

### Qwen-ASR（千问语音识别）

| 场景 | 模型 | 接入方式 |
|------|------|----------|
| 录音文件识别 | qwen3-asr-flash | OpenAI 兼容、DashScope 同步调用 |
| 录音文件识别 | qwen3-asr-flash-filetrans | 仅 DashScope 异步调用 |
| 实时语音识别 | qwen3-asr-flash-realtime | WebSocket（Realtime API）、Python/Java SDK |

Qwen-ASR 支持的语种最为丰富，实时识别支持中文、英文、日语、韩语、德语、法语、俄语、葡萄牙语、阿拉伯语等 20+ 语种。详见 [录音文件识别（Qwen-ASR）API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-api-reference.md) 和 [Qwen-ASR实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-interaction-process.md)。

### Fun-ASR

| 场景 | 模型 | 采样率 | 接入方式 |
|------|------|--------|----------|
| 实时语音识别 | fun-asr-realtime | 16kHz | WebSocket、Python/Java/Android/iOS SDK |
| 实时语音识别 | fun-asr-flash-8k-realtime | 8kHz | WebSocket、Python/Java/Android/iOS SDK |
| 录音文件识别 | fun-asr / fun-asr-mtl-2025-08-25 | 任意 | DashScope 异步调用、Python/Java/Android/iOS SDK |

- **支持语种**：fun-asr-realtime 支持中文（含多种方言）、英文、日语；fun-asr-mtl-2025-08-25 额外支持粤语、泰语、越南语、印尼语
- **支持音频格式**（实时）：pcm、wav、mp3、opus、speex、aac、amr

### Paraformer

| 场景 | 模型（推荐） | 采样率 | 接入方式 |
|------|-------------|--------|----------|
| 实时语音识别 | paraformer-realtime-v2 | 任意 | WebSocket、Python/Java/Android/iOS SDK |
| 实时语音识别 | paraformer-realtime-8k-v2 | 8kHz | WebSocket、Python/Java/Android/iOS SDK |
| 录音文件识别 | paraformer-v2 | 任意 | RESTful API、Python/Java/Android/iOS SDK |

- **paraformer-realtime-v2** 支持中文（含多种方言）、英文、日语、韩语、德语、法语、俄语
- **paraformer-realtime-8k-v2** 支持情感识别（需关闭语义断句）
- Paraformer 对音频格式有额外约束：opus/speex 必须使用 Ogg 封装，wav 必须为 PCM 编码，amr 仅支持 AMR-NB

### 定制热词

所有模型系列均支持通过 `vocabulary_id` 参数使用定制热词，可通过 [定制热词HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md) 或 Python/Java SDK 管理热词列表（创建、查询、更新、删除）。

> **注意**：新加坡地域的子业务空间暂不支持热词功能。

## 服务端点与鉴权

### HTTP / [OpenAI 兼容接口](../concepts/openai-compatible-api.md)

| 地域 | 端点 |
|------|------|
| 中国内地（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容）<br>`https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription`（录音文件异步） |
| 国际（新加坡） | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`<br>`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/transcription` |

### WebSocket 接口

| 模型系列 | 中国内地 | 国际 |
|----------|----------|------|
| Fun-ASR / Paraformer | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` | `wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference` |
| Qwen-ASR Realtime | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=<model_name>` | `wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime?model=<model_name>` |

### 鉴权方式

所有接口统一使用 `Authorization: Bearer <your_api_key>` 进行鉴权。WebSocket 接口在握手阶段验证，API Key 无效时返回 HTTP 401/403。

建议将 API Key 配置到环境变量，避免硬编码。对于移动端或第三方应用场景，建议使用临时鉴权 Token（有效期 60 秒）。

## 关键参数说明

### 实时语音识别通用参数

| 参数 | 说明 | 适用模型 |
|------|------|----------|
| `format` | 音频格式（pcm/wav/mp3/opus/speex/aac/amr） | Fun-ASR、Paraformer |
| `sample_rate` | 采样率（8000 或 16000 Hz） | Fun-ASR、Paraformer |
| `language_hints` | 指定待识别语种 | Fun-ASR、paraformer-realtime-v2、Qwen-ASR |
| `vocabulary_id` | 热词列表 ID | Fun-ASR、Paraformer、Qwen-ASR |
| `semantic_punctuation_enabled` | 语义断句开关（默认 false） | Fun-ASR、Paraformer |
| `max_sentence_silence` | VAD 断句静音阈值（ms），默认 1300，范围 [200, 6000] | Fun-ASR、Paraformer（语义断句关闭时生效） |
| `disfluency_removal_enabled` | 过滤语气词 | 仅 Paraformer |

### Qwen-ASR Realtime 特有参数

Qwen-ASR Realtime 使用独立的事件驱动协议，关键配置通过 `session.update` 事件设置：

- `input_audio_format`：支持 pcm、opus（默认 pcm）
- `sample_rate`：支持 16000、8000（默认 16000）
- `turn_detection`：VAD 配置，设为 null 则切换为 Manual 模式
- `turn_detection.threshold`：VAD 检测阈值，推荐 0.0（默认 0.2），范围 [-1, 1]
- `turn_detection.silence_duration_ms`：断句静默阈值，推荐 400（默认 800），范围 [200, 6000]

### 录音文件识别通用参数

| 参数 | 说明 |
|------|------|
| `file_urls` | 待识别文件 URL 列表（单次最多 100 个） |
| `channel_id` | 音轨索引 |
| `diarization_enabled` | 是否启用说话人分离 |
| `speaker_count` | 说话人数量参考 |
| `language_hints` | 待识别语种 |

## 使用方式

### 实时语音识别交互流程

**Fun-ASR 和 Paraformer** 使用 WebSocket 双工流式协议，交互流程为：

1. 建立 WebSocket 连接
2. 发送 `run-task` 指令启动任务
3. 收到 `task-started` 后开始发送二进制音频流（须为单声道）
4. 持续接收 `result-generated` 事件获取识别结果
5. 发送 `finish-task` 通知结束
6. 收到 `task-finished` 后关闭连接

**Qwen-ASR Realtime** 支持两种交互模式：
- **VAD 模式**（默认）：服务端自动检测语音端点，适用于会议、对话场景
- **Manual 模式**：客户端控制断句，适用于语音消息等明确边界的场景

### 录音文件识别调用模式

录音文件识别采用异步"提交-轮询"模式：

1. 调用提交任务接口，获取 `task_id`
2. 使用 `task_id` 轮询查询任务状态（PENDING → RUNNING → SUCCEEDED/FAILED）
3. 任务完成后获取识别结果

> **注意**：每个任务完成后，识别结果和 URL 下载链接有效期为 **24 小时**，超时后无法查询或下载。

### SDK 支持情况

| SDK | Fun-ASR 实时 | Fun-ASR 录音 | Paraformer 实时 | Paraformer 录音 | Qwen-ASR 实时 | Qwen-ASR 录音 |
|-----|:-----------:|:-----------:|:--------------:|:--------------:|:------------:|:------------:|
| Python | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Java | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Android | ✅ | ✅ | ✅ | ✅ | — | — |
| iOS | ✅ | ✅ | ✅ | ✅ | — | — |
| WebSocket | ✅ | — | ✅ | — | ✅ | — |
| RESTful | — | ✅ | — | ✅ | — | ✅ |

## 限制和注意事项

### 音频输入限制

- **录音文件识别不支持本地文件直传**，输入必须为可通过公网访问的 HTTP/HTTPS URL。使用 SDK 时不支持 `oss://` 前缀的临时 URL
- 录音文件大小不超过 **2GB**，时长不超过 **12 小时**；启用说话人分离时建议不超过 2 小时
- 实时识别音频须为**单声道**
- 视频文件虽可兼容，但建议预处理提取音轨以提高效率，可使用 ffmpeg：`ffmpeg -i input-video -ac 1 -ar 16000 -acodec libopus output.opus`

### 采样率约束

不同模型对采样率要求不同：
- 8k 模型（fun-asr-flash-8k-realtime、paraformer-realtime-8k-v2 等）仅支持 8000 Hz
- paraformer-realtime-v2 支持任意采样率
- 其他模型一般仅支持 16000 Hz
- Qwen-ASR Realtime 设置为 8000 Hz 时会升采样到 16000 Hz，可能引入微小延迟

> **注意**：Fun-ASR/Paraformer 的 WebSocket 端点（`/api-ws/v1/inference`）与 Qwen-ASR Realtime 的端点（`/api-ws/v1/realtime`）不同，请勿混用。

### 计费与免费额度

- Fun-ASR 实时：中国内地 0.00033 元/秒，含 36,000 秒免费额度（开通后 90 天有效）
- Fun-ASR 8K 实时：中国内地 0.00022 元/秒
- 国际地域价格通常为中国内地的 2 倍，且部分模型无免费额度

### 其他注意事项

- 不同地域的 API Key 不同（北京 vs 新加坡），请确保使用对应地域的 Key
- DashScope SDK 版本要求：Python SDK ≥ 1.25.6（Qwen-ASR Realtime），Java SDK ≥ 2.22.5（Qwen-ASR Realtime）
- 定制热词的 `target_model` 必须与实际调用语音识别时使用的模型一

## 来源文档

- [录音文件识别（Qwen-ASR）API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-api-reference.md)
- [Fun-ASR实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-websocket-api.md)
- [实时语音识别（Fun-ASR）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-client-events.md)
- [实时语音识别（Fun-ASR）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-server-events.md)
- [Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-java-sdk.md)
- [Fun-ASR实时语音识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/android-sdk-for-fun-asr-real-time-service.md)
- [Paraformer实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/websocket-for-paraformer-real-time-service.md)
- [Fun-ASR实时语音识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/ios-sdk-for-fun-asr-real-time-service.md)
- [实时语音识别（Paraformer）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-client-events.md)
- [实时语音识别（Paraformer）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-server-events.md)
- [Paraformer实时语音识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-real-time-speech-recognition-java-sdk.md)
- [Paraformer实时语音识别Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-real-time-speech-recognition-python-sdk.md)
- [Paraformer实时语音识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/android-sdk-for-paraformer-real-time-service.md)
- [Qwen-ASR实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-interaction-process.md)
- [Paraformer实时语音识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/ios-sdk-for-paraformer-real-time-service.md)
- [实时语音识别（Qwen-ASR-Realtime）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-client-events.md)
- [实时语音识别（Qwen-ASR-Realtime）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-server-events.md)
- [实时语音识别（Qwen-ASR-Realtime）Python SDK-API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-python-sdk.md)
- [实时语音识别（Qwen-ASR-Realtime）Java SDK-API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-java-sdk.md)
- [Paraformer录音文件识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-java-sdk.md)
- [Paraformer录音文件识别Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-python-sdk.md)
- [Paraformer录音文件识别RESTful API](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-restful-api.md)
- [Paraformer录音文件识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-android-sdk.md)
- [Paraformer录音文件识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-ios-sdk.md)
- [最佳实践](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-best-practices.md)
- [Fun-ASR录音文件识别Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/funauidio-asr-recorded-speech-recognition-python-sdk.md)
- [Fun-ASR录音文件识别HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-http-api.md)
- [Fun-ASR录音文件识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-android-sdk.md)
- [Fun-ASR录音文件识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-ios-sdk.md)
- [Fun-ASR录音文件识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-java-sdk.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)

