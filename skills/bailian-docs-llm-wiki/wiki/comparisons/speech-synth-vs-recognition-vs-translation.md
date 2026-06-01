# 语音合成、语音识别与语音翻译对比

## 概述

百炼平台提供三大核心语音能力：**语音合成（TTS）**、**语音识别（ASR）** 和 **语音翻译（Live Translate）**。三者分别解决"文字转语音"、"语音转文字"和"跨语言语音转换"的需求。本文从输入输出格式、支持模型、API 端点、调用方式、计费和典型场景等维度进行对比，帮助开发者根据业务需求快速完成技术选型。

## 核心维度对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Live Translate） |
|------|----------------|----------------|--------------------------|
| **核心能力** | 将文本转换为语音音频 | 将语音音频转换为文本 | 将一种语言的语音翻译为另一种语言的文本和/或语音 |
| **输入格式** | 文本（支持流式文本输入） | 音频流或音频文件（pcm/wav/mp3/opus/speex/aac/amr） | 音频流、音频文件或视频文件 |
| **输出格式** | 音频（mp3/wav/pcm/opus 等） | 文本（含时间戳、标点等） | 翻译后的文本 + 可选音频（wav/pcm） |
| **支持模型系列** | Qwen-TTS、CosyVoice、Sambert、MiniMax | Qwen-ASR、Fun-ASR、Paraformer | qwen3-livetranslate-flash、qwen3.5-livetranslate-flash-realtime |
| **实时模式** | ✅ WebSocket 流式合成 | ✅ WebSocket 实时识别 | ✅ WebSocket 实时翻译 |
| **非实时/离线模式** | ✅ HTTP 同步调用 | ✅ HTTP 同步/异步调用 | ✅ [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（流式） |
| **HTTP 协议** | DashScope REST API | OpenAI 兼容 + DashScope 异步 API | 仅 [OpenAI 兼容接口](../concepts/openai-compatible-api.md) |
| **WebSocket 协议** | DashScope WebSocket / Realtime API | DashScope WebSocket / Realtime API | Realtime API |
| **多语种支持** | 取决于模型和音色 | 20+ 语种（Qwen-ASR 最丰富） | 支持多语种对翻译（source_lang ↔ target_lang） |
| **声音复刻** | ✅ 支持上传音频创建专属音色 | — | ✅ 支持实时声音复刻（once/always/never） |
| **热词定制** | — | ✅ 所有模型系列均支持 vocabulary_id | ✅ 通过 translation.corpus.phrases 设置 |
| **SDK 覆盖** | Python、Java、Android、iOS | Python、Java、Android、iOS | Python、Java（通过 OpenAI 兼容 SDK） |
| **国际地域支持** | ✅（Sambert 除外） | ✅ | ✅ |

## API 端点对比

| 端点类型 | 语音合成 | 语音识别 | 语音翻译 |
|---------|---------|---------|---------|
| **HTTP（北京）** | `https://dashscope.aliyuncs.com/api/v1` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| **HTTP（新加坡）** | `https://dashscope-intl.aliyuncs.com/api/v1` | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| **WebSocket（北京）** | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` 或 `/realtime` | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` 或 `/realtime` | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` |
| **WebSocket（新加坡）** | `wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference` 或 `/realtime` | `wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference` 或 `/realtime` | `wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime` |

> **说明**：三类服务均使用 `Authorization: Bearer <your_api_key>` 统一鉴权。不同地域需使用对应地域的 API Key。

## 模型选择对比

### 语音合成模型

| 模型系列 | 推荐模型 | 特点 |
|---------|---------|------|
| Qwen-TTS | qwen3-tts-flash / qwen3-tts-flash-realtime | 支持指令控制（instruct），实时与非实时双模式 |
| CosyVoice | cosyvoice-v3.5-plus / cosyvoice-v3.5-flash | 成熟稳定，支持移动端 SDK，低延迟版本可选 |
| Sambert | sambert-zhichu-v1 | 仅北京地域，不支持流式文本输入 |
| MiniMax | speech-2.8-hd / speech-2.8-turbo | 第三方模型，按字符计费（2～3.5 元/万字符） |

### 语音识别模型

| 模型系列 | 推荐模型 | 特点 |
|---------|---------|------|
| Qwen-ASR | qwen3-asr-flash / qwen3-asr-flash-realtime | 语种覆盖最广（20+），支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md) |
| Fun-ASR | fun-asr-realtime / fun-asr-mtl-2025-08-25 | 支持中文方言，移动端 SDK 完整 |
| Paraformer | paraformer-realtime-v2 / paraformer-v2 | 支持情感识别，移动端 SDK 完整 |

### 语音翻译模型

| 模型 | 接口类型 | 特点 |
|------|---------|------|
| qwen3-livetranslate-flash | HTTP（OpenAI 兼容） | 离线翻译，支持音频和视频文件输入 |
| qwen3.5-livetranslate-flash-realtime | WebSocket | 实时翻译（推荐），支持声音复刻和热词 |

## 计费方式对比

| 服务 | 计费单位 | 说明 |
|------|---------|------|
| 语音合成 | 按字符数计费 | MiniMax 明确标价 2～3.5 元/万字符；其他模型请参考官方定价页 |
| 语音识别 | 按音频时长计费 | 实时识别按流式时长计费，录音文件按文件时长计费 |
| 语音翻译 | 按 [Token](../concepts/token.md) 消耗计费 | 离线翻译返回 prompt_tokens 和 completion_tokens 统计 |

> 具体定价以百炼平台官方计费文档为准。

## 适用场景建议

### 语音合成（TTS）适用场景

- **智能客服/语音助手**：将 AI 生成的文字回复转为语音播报
- **有声读物/播客生成**：批量将文本内容转化为自然语音
- **导航/通知播报**：实时将文本信息转为语音提示
- **个性化音色**：通过声音复刻创建品牌专属语音形象

### 语音识别（ASR）适用场景

- **会议纪要/字幕生成**：实时将语音转写为文字
- **语音搜索/语音指令**：将用户口语输入转为文本供后续处理
- **电话录音质检**：批量转写呼叫中心录音并分析内容
- **多语种场景**：使用 Qwen-ASR 支持 20+ 语种的跨语言转写

### 语音翻译（Live Translate）适用场景

- **跨语言实时会议**：在多国参会者之间提供实时语音翻译
- **直播同声传译**：为多语言观众提供实时翻译字幕和语音
- **音视频内容本地化**：将已有音频/视频文件翻译为目标语言
- **跨境客服**：实时将客户语音翻译为客服人员能理解的语言

## 技术选型决策参考

```
需要将文本转为语音？
  └── 是 → 语音合成（TTS）
        ├── 需要实时[流式输出](../concepts/streaming.md)？ → Qwen-TTS Realtime / CosyVoice WebSocket
        ├── 需要移动端集成？ → CosyVoice / Sambert（支持 Android/iOS SDK）
        └── 需要指令控制语气风格？ → Qwen-TTS Instruct

需要将语音转为文字？
  └── 是 → 语音识别（ASR）
        ├── 需要实时转

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)

