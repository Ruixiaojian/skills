# 语音合成、语音识别与语音翻译对比

百炼平台围绕语音场景提供了三大核心能力：**语音合成（TTS）**、**语音识别（ASR）** 和 **语音翻译（Live Translate）**。三者分别解决"文本转语音""语音转文本"和"语音跨语言转换"的需求，但在输入输出格式、支持模型、接口协议、计费方式等方面存在显著差异。本文从多个关键维度对三者进行系统对比，帮助开发者在技术选型时做出准确判断。

---

## 核心维度对比

### 基本定位

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Live Translate） |
|------|----------------|----------------|--------------------------|
| **核心功能** | 将文本转换为语音音频 | 将语音音频转换为文本 | 将一种语言的语音翻译为另一种语言的文本或语音 |
| **信息流方向** | 文本 → 语音 | 语音 → 文本 | 语音 → 翻译文本 / 翻译语音 |
| **典型使用者** | 内容播报、客服外呼、有声书制作 | 会议记录、字幕生成、语音指令 | 同声传译、跨语言会议、多语种视频翻译 |

### 输入与输出格式

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Live Translate） |
|------|----------------|----------------|--------------------------|
| **输入格式** | 文本（纯文本 / 流式文本片段） | 音频流或音频文件（pcm、wav、mp3、opus、speex、aac、amr） | 音频流（pcm、opus）或音频/视频文件（mp3、wav、视频 URL / Base64） |
| **输出格式** | 音频（mp3、wav、pcm、opus 等） | 文本（JSON 中的识别结果） | 文本 + 音频（wav / pcm），或仅文本 |
| **流式支持** | 支持流式文本输入 + 流式音频输出（Sambert 除外） | 支持实时音频流输入 + 流式文本输出 | 支持实时音频流输入 + 流式文本/音频输出 |

### 支持的模型系列

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Live Translate） |
|------|----------------|----------------|--------------------------|
| **主力模型系列** | Qwen-TTS、CosyVoice、Sambert、MiniMax | Qwen-ASR、Fun-ASR、Paraformer | qwen3-livetranslate-flash、qwen3.5-livetranslate-flash-realtime |
| **模型数量** | 10+ 款模型可选 | 10+ 款模型可选 | 4 款模型 |
| **实时模型** | qwen3-tts-flash-realtime、qwen3-tts-instruct-flash-realtime、CosyVoice 系列 | qwen3-asr-flash-realtime、fun-asr-realtime、paraformer-realtime-v2 等 | qwen3.5-livetranslate-flash-realtime、qwen3-livetranslate-flash-realtime |
| **非实时/离线模型** | qwen3-tts-flash、qwen3-tts-instruct-flash、MiniMax 系列 | qwen3-asr-flash、qwen3-asr-flash-filetrans、fun-asr、paraformer-v2 等 | qwen3-livetranslate-flash |

### 接口协议与端点

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Live Translate） |
|------|----------------|----------------|--------------------------|
| **HTTP 端点** | `https://dashscope.aliyuncs.com/api/v1`（DashScope） | `https://dashscope.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容）及 DashScope 异步接口 | `https://dashscope.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容） |
| **WebSocket 端点** | CosyVoice/Sambert：`wss://…/api-ws/v1/inference`；Qwen-TTS Realtime：`wss://…/api-ws/v1/realtime?model=<model>` | Fun-ASR/Paraformer：`wss://…/api-ws/v1/inference`；Qwen-ASR Realtime：`wss://…/api-ws/v1/realtime?model=<model>` | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` |
| **[OpenAI 兼容接口](../concepts/openai-compatible-api.md)** | 不支持 | 支持（Qwen-ASR 录音文件识别） | 支持（离线翻译） |
| **国际端点（新加坡）** | 支持（Sambert 除外） | 支持（热词功能受限） | 支持 |
| **鉴权方式** | `Authorization: Bearer <api_key>` | `Authorization: Bearer <api_key>` | `Authorization: Bearer <api_key>` |

### SDK 支持情况

| SDK | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Live Translate） |
|-----|----------------|----------------|--------------------------|
| **Python SDK** | ✅ 全系列 | ✅ 全系列 | ✅（OpenAI SDK / WebSocket） |
| **Java SDK** | ✅ 全系列 | ✅ 全系列 | ✅ |
| **Android SDK** | ✅ CosyVoice 实时、Sambert | ✅ Fun-ASR、Paraformer | — |
| **iOS SDK** | ✅ CosyVoice 实时、Sambert | ✅ Fun-ASR、Paraformer | — |

### 特色功能对比

| 功能 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Live Translate） |
|------|----------------|----------------|--------------------------|
| **音色选择/定制** | ✅ 系统预置音色 + 声音复刻 + 声音设计 | — | ✅ 系统预置音色 + 声音复刻（once / always / never） |
| **指令控制** | ✅ qwen3-tts-instruct-flash 系列支持 instructions 控制语气、风格 | — | — |
| **热词定制** | — | ✅ 所有模型系列均支持 `vocabulary_id` | ✅ 实时翻译支持 `translation.corpus.phrases` 热词映射 |
| **多语种** | 取决于音色与模型 | ✅ Qwen-ASR 支持 20+ 语种 | ✅ 通过 `source_lang` / `target_lang` 指定源和目标语言 |
| **语义断句** | — | ✅ Fun-ASR、Paraformer 支持语义断句 | — |
| **VAD（语音活动检测）** | — | ✅ 可配置静音阈值和检测灵敏度 | — |
| **视频文件输入** | — | — | ✅ 离线翻译支持视频 URL 输入 |
| **图像输入** | — | — | ✅ 实时翻译支持追加图像数据 |

### 计费方式

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Live Translate） |
|------|----------------|----------------|--------------------------|
| **计费单位** | 按字符数计费（每万字符） | 按音频时长 / Token 数计费 | 按 Token 数计费（prompt_tokens + completion_tokens） |
| **价格示例** | MiniMax speech-2.8-hd：3.5 元/万字符；MiniMax speech-2.8-turbo：2 元/万字符 | 详见各模型定价页 | 详见各模型定价页 |

---

## 适用场景建议

### 语音合成（TTS）—— 适合"让机器开口说话"

- **有声内容生产**：新闻播报、有声书、播客自动生成
- **智能客服外呼**：配合对话系统实现语音交互
- **无障碍辅助**：为视障用户提供文本朗读
- **个性化语音**：通过声音复刻或声音设计打造品牌专属音色
- **选型提示**：低延迟场景选 CosyVoice flash 或 Qwen-TTS Realtime；高质量长文选 Qwen-TTS 非实时；需要精细语气控制选 qwen3-tts-instruct-flash 系列

### 语音识别（ASR）—— 适合"让机器听懂语音"

- **会议纪要 / 字幕生成**：将录音或实时语音转为文字
- **语音指令**：语音输入控制应用操作
- **呼叫中心质检**：将客服通话录音批量转写分析
- **多语种场景**：Qwen-ASR 支持 20+ 语种，适合国际化业务
- **选型提示**：高精度多语种选 Qwen-ASR；低延迟中英日场景选 Fun-ASR 或 Paraformer 实时版；大批量录音文件选异步接口（filetrans）

### 语音翻译（Live Translate）—— 适合"跨语言语音沟通"

- **同声传译**：多语种实时会议翻译
- **跨语言视频制作**：为已有视频生成目标语言的配音
- **客服跨语言支持**：实时翻译客户语音以辅助多语种客服
- **声音保真翻译**：启用声音复刻，让翻译后的语音保留说话者的音色特征
- **选型提示**：实时场景选 qwen3.

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)

