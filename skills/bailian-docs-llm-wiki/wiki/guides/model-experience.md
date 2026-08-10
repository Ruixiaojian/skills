# model experience

`model experience` 是百炼平台面向开发者提供的模型选型与使用指南集合，覆盖文本、视觉、语音、音视频、3D、音乐等全模态能力。本文档旨在帮助开发者根据具体场景（如办公、编程、客服、内容生成）快速匹配最优模型，并明确关键参数、调用方式及约束条件，避免因模型能力错配导致效果或成本问题。所有推荐均基于当前（2026年中）最新稳定版本，旧版模型仅在迁移场景下保留参考价值。

## 支持的模型/功能

百炼平台提供覆盖[多模态](../concepts/multi-modal.md)的模型矩阵，按核心能力划分为以下几类：

- **文本生成**：支持长上下文（最高1000万[Token](../concepts/token.md)）、Function Calling、结构化输出、深度思考（`enable_thinking` 参数控制）及批量推理。主力模型为 `qwen3.8-max`（最强推理）、`qwen3.7-plus`（平衡首选）和 `qwen3.7-flash`（低成本）。`qwen-long` 专用于超长文档处理（10M上下文），但不支持Function Calling或内置工具 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。
  
- **视觉理解**：支持图像、视频（最长2小时）、OCR及[多模态](../concepts/multi-modal.md)结构化输出。`qwen3.7-plus` 和 `qwen3.7-flash` 是通用首选，`qwen3.5-ocr` 专为文档/手写识别优化。注意：内置工具仅在 `qwen3.7-plus`、`qwen3.7-flash` 等少数模型上可用，`qwen3-vl-plus` 等旧版VL模型不支持 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。

- **图片与视频生成/编辑**：`qwen-image-3.0-pro` 和 `wan2.7-image-pro` 支持高保真文生图与复杂编辑；`happyhorse-1.1-t2v` 和 `wan2.7-i2v-2026-04-25` 分别适用于标准文生视频与首尾帧续写。所有视频模型输出均为MP4格式，时长限制在2–15秒。

- **语音与音频**：
  - **TTS**：`qwen-audio-3.0-tts-plus` 同时支持声音复刻、声音设计与指令控制；`qwen3-tts-instruct-flash-realtime` 仅支持指令控制，不支持音色定制 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。
  - **ASR**：实时场景用 `qwen-audio-3.0-asr-flash-streaming`（WebSocket），文件转写用 `qwen-audio-3.0-asr-flash-filetrans`（HTTP，支持说话人分离）。
  - **S2S（语音转语音）**：`qwen-audio-3.0-realtime-plus` 提供端到端低延迟对话；`qwen3.5-livetranslate-flash-realtime` 支持60种语言同传。

- **全模态与翻译**：`qwen3.5-omni-plus` 支持文本/音频/图片/视频输入，具备Function Calling与联网搜索；`qwen3.5-livetranslate-flash-realtime` 专注实时语音翻译（60种语言）。注意：`qwen3.5-omni-plus-realtime` 不支持思考模式，而 `qwen3-omni-flash` 在HTTP模式下支持思考模式但不支持联网搜索 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。

- **3D与音乐**：`Tripo/Tripo-P1.0`（快速预览）与 `Tripo/Tripo-H3.1`（高精度）支持文/图/多图生3D；`fun-music-v1` 支持带歌词/提示词的歌曲生成，但需邀测开通且仅限北京地域 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。

- **向量与重排序**：`text-embedding-v4` 为文本Embedding默认推荐；`qwen3-rerank` 用于纯文本RAG重排序；`qwen3-vl-rerank` 支持图文视频混合排序。

> **注意**：文档1与文档2中关于 `qwen3.7-plus` 是否支持“内置工具”的描述存在矛盾——文档1明确列出其支持，文档2则限定为 `qwen3.7-max-2026-06-08` 等特定快照版本。实际以模型广场最新快照为准，建议优先选用 `qwen3.7-plus-2026-05-26` 或更高日期版本。

## 关键参数

- **上下文窗口**：文本模型主流为1M [Token](../concepts/token.md)（≈70万汉字），`qwen-long` 达10M；视觉模型图像分辨率按 `h×w/(32×32)+2` 计算[Token](../concepts/token.md)；视频最大2GB/2小时。
- **输入/输出控制**：
  - `enable_thinking`（或 `reasoning.effort`）：开启深度思考，仅Qwen3及以上模型支持。
  - `texture_quality`（Tripo）：设为 `standard`（默认）或 `detailed` 控制贴图质量；设 `texture=false` & `pbr=false` 可输出无贴图模型。
  - `format`（Fun-Music）：`mp3`（小体积）或 `wav`（无损）。
- **能力开关**：
  - Function Calling：需在请求中定义 `tools` 字段，通用文本/视觉模型均支持，但部分旧版（如 `deepseek-v4-pro`）不支持内置工具。
  - 联网搜索：仅 `qwen3.5-omni-plus`（HTTP/WebSocket）支持，且与Function Calling互斥。
- **语言与方言**：ASR/TTS/翻译模型广泛支持中文方言（粤语、四川话等）及100+种外语，具体以各模型文档“支持的语言”子节为准。

## 使用方式

- **API调用**：
  - 实时场景（语音对话、视频流分析）统一使用 **WebSocket**，如 `qwen-audio-3.0-realtime-plus`、`qwen3.5-omni-plus-realtime`。
  - 非实时场景（文件转写、图片生成、3D建模）使用 **HTTP POST**，需设置 `X-DashScope-Async: enable` 触发[异步任务](../concepts/asynchronous-task.md)（如Tripo），再轮询 `task_id` 获取结果 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **SDK接入**：DashScope SDK（Python/Java）支持绝大多数模型；Android/iOS SDK 仅限 `qwen-audio-*` 和 `fun-asr` 系列。
- **协议选型**：
  - 对弱网/双工交互要求高：优先选 **AOQ**（Qwen-Audio-ASR/TTS系列支持）。
  - 需要流式返回音频：TTS可选 WebSocket 或 HTTP 流式响应；ASR实时模式必须WebSocket。
- **输入格式**：
  - [多模态](../concepts/multi-modal.md)：`input` 中 `prompt`（文本）、`image`（单图URL）、`images`（多图URL列表）三者互斥。
  - 3D生成：`Tripo/Tripo-P1.0` 接受 `prompt`/`image`/`images`，`Tripo/Tripo-H3.1` 仅支持 `prompt` 和 `image`。

## 限制和注意事项

- **地域限制**：Tripo 3D模型、Fun-Music 仅限华北2（北京）地域；部分模型（如 `qwen-omni-turbo`）已停更，新项目禁用。
- **资源约束**：
  - 视频生成：单次请求最多64个视频片段，每片段≤15秒。
  - ASR文件转写：`qwen-audio-3.0-asr-flash-filetrans` 支持最大12小时/2GB音频。
  - Tripo：`pbr_model_url` 有效期2小时，需及时下载。
- **能力冲突**：
  - 联网搜索与Function Calling不可同时启用。
  - 思考模式启用时，`qwen3-omni-flash` 无法生成语音输出。
- **计费差异**：`qwen3-tts-flash` 等旧版TTS按Token计费；`qwen-audio-3.0-tts-plus` 按请求+时长计费。
- **兼容性**：`text-embedding-v3` 与v4维度不兼容，迁移需重建索引；`qwen3.5-ocr` 不支持视频输入，仅限静态图像。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


