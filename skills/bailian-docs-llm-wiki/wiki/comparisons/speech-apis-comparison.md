# 语音合成、识别与翻译 API 对比

百炼平台的语音类 API 由三大互补能力组成：**语音合成（TTS）**、**语音识别（ASR）** 与 **语音/音视频翻译（Speech Translation）**。它们共用相同的鉴权、地域端点规范与流式 WebSocket 协议体系，但面向的输入输出形态、可选模型族、关键参数与典型业务链路差异较大。本页从开发者技术选型角度，横向梳理三类 API 在协议、模型、参数、SDK 与场景上的差异，便于在「文字 → 语音」「语音 → 文字」「语音/视频 → 跨语言文字/语音」三种诉求之间做出最合适的选择。

## 关键维度对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音/音视频翻译 |
| --- | --- | --- | --- |
| 核心任务 | 文本 → 语音音频 | 语音音频 → 文字（可带时间戳） | 语音/视频 → 跨语言文字（可叠加语音输出） |
| 主要模型族 | Qwen-TTS / Qwen-TTS-Realtime、CosyVoice v1-v3.5-plus、Sambert、MiniMax；配套 Voice Design / Voice Clone | Qwen-ASR（`qwen3-asr-flash` 同步 / `-filetrans` 异步 / `-realtime`）、Paraformer（`paraformer-v2`、`paraformer-realtime-v2/v1`、8k 版本）、Fun-ASR（`fun-asr` 多日期快照 / `fun-asr-mtl` / `fun-asr-realtime`） | Qwen-LiveTranslate：`qwen3-livetranslate-flash`（非实时）、`qwen3.5-livetranslate-flash-realtime`（实时） |
| 输入 | 文本 + 音色 / 风格指令；声音复刻额外需要音色样本 | 音频文件 URL（异步）或 PCM/Opus 流（实时） | 音频文件（mp3/wav）、视频文件（URL/Base64）或麦克风/摄像头实时流 |
| 输出 | wav / mp3 / pcm / opus 音频（采样率 22050/24000/48000 等） | 文本结果（含可选时间戳、热词、ITN 处理） | 翻译文本（必出），可选同步语音（modalities 含 `audio` 时输出 wav） |
| 交互形态 | HTTP（非实时）、WebSocket（实时/流式）；MiniMax 仅 HTTP | RESTful 异步「提交-轮询」、WebSocket 流式实时；Qwen-ASR 额外支持 OpenAI 兼容 / DashScope 同步 | OpenAI 兼容 SSE 流式（非实时）、原生 WebSocket（实时） |
| 协议入口 | `MultiModalConversation`（Qwen-TTS）、`wss://.../api-ws/v1/inference`（CosyVoice/Sambert/Qwen-TTS-Realtime）、HTTP（MiniMax） | `POST /api/v1/services/audio/asr/transcription`（异步，需 `X-DashScope-Async: enable`）、`wss://.../api-ws/v1/inference`（Paraformer/Fun-ASR）、`wss://.../api-ws/v1/realtime?model=...`（Qwen-ASR-Realtime）；Qwen-ASR 还可走 `/compatible-mode/v1/chat/completions` 与 `/services/aigc/multimodal-generation/generation` | `POST ${base_url}/chat/completions`（必须 `stream=true`）、`wss://.../api-ws/v1/realtime`；**不支持** `/services/aigc/multimodal-generation/generation` |
| 中国内地端点 | HTTP `https://dashscope.aliyuncs.com`，WebSocket `wss://dashscope.aliyuncs.com/api-ws/v1/inference` | HTTP `https://dashscope.aliyuncs.com/...`，WebSocket `wss://dashscope.aliyuncs.com/api-ws/v1/inference`（或 `/realtime?model=...`） | OpenAI 兼容 `https://dashscope.aliyuncs.com/compatible-mode/v1`，WebSocket `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` |
| 新加坡端点 | 新版 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；旧版 `dashscope-intl.aliyuncs.com` 即将下线 | 新版 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...` 与对应 `wss://`；Qwen-ASR OpenAI 兼容仍走 `dashscope-intl` | OpenAI 兼容 `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`；实时 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`，旧版 `dashscope-intl` 即将下线 |
| 关键参数 | `model`、`text`、`voice`、`format`、`sample_rate`、`instructions`（Qwen-TTS-Instruct）、`language_type` | `model`、`input.file_urls`（异步）、`parameters`（热词/ITN/时间戳等）；实时含采样率与编码格式 | `model`、`messages.content`（`input_audio` / `video_url`）、`stream=true`、`modalities`、`audio.voice/format`、`translation_options.{source_lang,target_lang}`（Python SDK 放 `extra_body`） |
| SDK 覆盖 | Python / Java；CosyVoice 与 Sambert 额外提供 Android / iOS；MiniMax 仅 HTTP | Java / Python 全线覆盖；Paraformer 与 Fun-ASR 额外提供 Android / iOS | OpenAI 兼容路径：任意 OpenAI SDK；DashScope `OmniRealtimeConversation` Python / Java SDK 封装 WebSocket |
| 流式语义 | 服务端事件 `response.audio.delta` / `result-generated` 增量回传音频，`response.done` / `task-finished` 结束 | 实时事件持续返回中间/最终识别结果；异步任务以 `SUCCEEDED/FAILED` 终态结束 | SSE chunk 分文本（`delta.content`）、音频（`delta.audio.data` Base64）、用量（最后一个 chunk 的 `usage`）三类 |
| 自定义能力 | Voice Design（自然语言定义音色）、Voice Clone（`voice-enrollment` 复刻音色） | 热词增强、ITN 文本规整、自定义语种与采样率 | 通过 `source_lang/target_lang` 控制源/目标语种；`voice` 决定输出音色；不建议调温度等采样参数以保稳定 |
| 鉴权方式 | `Authorization: Bearer <API_KEY>`，北京/新加坡 Key 不通用 | 同左 | 同左 |
| 典型场景 | 语音播报、配音、IVR 提示音、低延迟语音助手、个性化音色品牌 | 客服质检、会议/直播字幕、语音搜索、智能录音转写、IoT 唤醒后命令识别 | 跨境会议同传、多语种短视频翻译、双语客服、面向海外用户的实时音视频字幕 |

## 协议形态差异

- **TTS** 强调「文本进、音频出」，因此 Qwen-TTS / CosyVoice / Sambert 走 `inference` 通道，并通过 `run-task` / `continue-task` / `finish-task` 事件做长文本分片；Qwen-TTS-Realtime 则采用 `session.update` + `response.create` 的对话式事件流，便于做交互式语音机器人。
- **ASR** 异步与实时严格分线：长音频（小时级）必须走「提交-轮询」的 RESTful 异步流程，强实时（毫秒级反馈）只能走 WebSocket；同时 Qwen-ASR 是唯一兼容 OpenAI Chat Completions 协议的 ASR 路径，便于复用现有 OpenAI 客户端。
- **Speech Translation** 选择了「OpenAI 兼容 + 原生 WebSocket」两条窄通道：非实时必须 `stream=true` 走 SSE chunk；实时模型沿用 Realtime 事件协议（`session.update` / `input_audio_buffer.append` / `response.created` 等），并显式不支持 DashScope 经典多模态 generation 协议。

## 输入输出与计费基准

- **TTS 计费**通常按字符（或 token）+ 音色类型计量，CosyVoice 自定义音色（声音复刻）会单独计算训练或推理费用。
- **ASR 计费**多按音频时长（分钟）阶梯计费，异步与实时、8k 与 16k+ 版本费率不同；Paraformer 8k 版主要用于电话音频。
- **Speech Translation 计费**按 token 计量，最后一个 chunk 的 `usage` 字段给出 `prompt_tokens` / `completion_tokens` / `total_tokens` 与音频 / 文本细分，便于做用量监控。

## 适用场景与选型建议

- **想做「文字 → 语音」**：
  - 普通文案播报、营销视频配音、IVR 提示 → 选 **Qwen-TTS 非实时**（`qwen3-tts-flash`），实现简单、整段返回；需要风格指令时用 `qwen3-tts-instruct-flash`。
  - 语音助手 / 对话机器人 / 朗读交互 → 选 **Qwen-TTS-Realtime** 或 **CosyVoice WebSocket**（流式低延迟）。
  - 需要品牌专属音色或个性化语音 → 用 **Voice Design**（设计风格）或 **Voice Clone**（复刻真人）。
  - 已有海外存量代码 / 习惯纯 HTTP → 选 **MiniMax 系列**（同步 HTTP，无 WebSocket 依赖）。
  - 历史 Sambert 业务建议逐步迁移到 Qwen-TTS / CosyVoice。

- **想做「语音 → 文字」**：
  - 长音频离线转写（会议录音、客服录音质检）→ 用 **Qwen-ASR `-filetrans` 异步** 或 **Paraformer `paraformer-v2`** 走异步 RESTful。
  - 直播 / 通话 / 字幕等实时场景 → 选 **Paraformer Realtime v2**（任意采样率）、**Fun-ASR Realtime** 或 **Qwen-ASR Realtime**；8k 电话音频选 Paraformer 8k 版。
  - 想复用现有 OpenAI 客户端、做轻量同步识别 → 选 **Qwen-ASR `qwen3-asr-flash`** + OpenAI 兼容 / DashScope 同步路径。
  - 多语种（含小语种） → 优先评估 **Fun-ASR `fun-asr-mtl`** 与 **Qwen-ASR 多语种能力**。

- **想做「语音/视频 → 跨语言」**：
  - 已录制音视频 → 选 **`qwen3-livetranslate-flash`**（OpenAI 兼容 + 流式 SSE），通过 `translation_options` 设定目标语种，可同时输出译文文本与 wav 语音。
  - 实时同传 / 实时字幕 / 跨境双向通话 → 选 **`qwen3.5-livetranslate-flash-realtime`**，通过 `OmniRealtimeConversation` Python / Java SDK 减少自实现 WebSocket 的成本。
  - 仅做「ASR + 后翻译」可能更灵活，但对延迟敏感、需要保留韵律或同时输出语音时，建议直接用 Speech Translation 单步完成。

## 与三个 API 协同的常见组合

- **「实时同传系统」**：客户端采集音频 → Speech Translation 实时 API 直接产出译文 + 语音（一步到位）；或客户端 → ASR 实时识别 → 业务侧调 LLM 翻译 → TTS 流式合成（灵活，可插入自定义润色）。
- **「短视频本地化」**：视频 URL → `qwen3-livetranslate-flash`（OpenAI 兼容）拿到译文与音频；如需多个目标语种，可并行多次调用。
- **「会议纪要 + 多语版本」**：录音 → Paraformer / Qwen-ASR 异步转写 → LLM 摘要 → Qwen-TTS 合成播报版；翻译版本可由 LLM 完成或由 Speech Translation 端到端生成。
- **「语音助手」**：ASR Realtime（拿到用户问题）→ 业务大模型 → Qwen-TTS-Realtime（流式语音回复），全链路 WebSocket 形成最低端到端延迟。

## 迁移与共性注意事项

- **域名迁移**：三类 API 的新加坡地域旧版 `dashscope-intl.aliyuncs.com` 域名均在下线进程中，新接入请直接使用 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` 新版多租域名；仅 Qwen-ASR OpenAI 兼容入口暂保留 `dashscope-intl`。
- **鉴权一致**：均通过 `Authorization: Bearer <API_KEY>` 携带，北京与新加坡 Key 不通用，多地域部署需分别申请。
- **协议命名差异**：Sambert / 早期 CosyVoice 属于 DashScope 经典 TTS 协议，与 Qwen-TTS / Qwen-TTS-Realtime 字段不通用；ASR 同理，`paraformer-v1` 系列正在被 `v2` 取代；Speech Translation 必须流式调用，不允许走 generation 协议。
- **SDK 选择**：移动端（Android / iOS）目前仅 CosyVoice / Sambert / Paraformer / Fun-ASR 提供官方 SDK；Speech Translation 移动端需自行实现 WebSocket 或托管在后端转发。

综合来看：**TTS 解决「说出来」，ASR 解决「听明白」，Speech Translation 解决「跨语言听说」**——三者协议互相对齐、可灵活组合，但单个业务诉求通常只需要选定其中一条链路即可，避免过度叠加。

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)


