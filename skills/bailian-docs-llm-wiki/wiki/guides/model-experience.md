# model experience

`model experience` 是百炼平台面向开发者提供的模型选型与使用指南集合，覆盖文本、视觉、语音、音视频、3D、音乐等全模态能力。本文档聚焦核心模型能力、参数配置、接入方式及关键约束，帮助开发者快速匹配业务场景并规避常见陷阱。所有模型均需通过 DashScope API 调用，支持同步/异步、流式/非流式等多种接入模式。

## 支持的模型/功能

百炼提供五大类模型能力，按场景划分如下：

- **文本生成**：覆盖通用对话、AI编程、办公文档处理等。主力模型为 `qwen3.7-plus`（100万上下文、完整工具调用、结构化输出），高推理需求可选 `qwen3.7-max` 或 `qwen3.8-max-preview`（仅 [Token](../concepts/token.md) Plan 可用）；轻量场景推荐 `qwen3.7-flash` [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：支持图像分析、OCR、长视频理解（最长2小时）。`qwen3.7-plus` 和 `qwen3.7-flash` 均支持 1600 万像素/图、2048 张图片输入及内置工具调用 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。OCR 专用模型为 `qwen3.5-ocr`。  
- **图像/视频生成与编辑**：文生图推荐 `wan2.7-image-pro`（支持4096×4096、多图参考编辑）；图生视频首选 `happyhorse-1.1-i2v`（1080P、3–15秒有声视频）；视频编辑推荐 `happyhorse-1.0-video-edit` [原文标题](../../raw/model-user-guide/model-experience/image-model.md) 和 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。  
- **语音与音频**：  
  - 语音识别（ASR）：实时场景用 `fun-asr-realtime`（热词支持）或 `qwen3.5-omni-plus-realtime`（Prompt 上下文注入）；非实时文件转写用 `fun-asr`（支持说话人分离）或 `qwen3.5-omni-plus`（支持情感识别）[原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
  - 语音合成（TTS）：标准合成用 `qwen-audio-3.0-tts-plus`；声音复刻用 `qwen-audio-3.0-tts-flash`；声音设计用 `cosyvoice-v3.5-plus`。  
  - 语音转语音（S2S）：低延迟对话用 `qwen-audio-3.0-realtime-plus`；同传翻译用 `qwen3.5-livetranslate-flash-realtime`（60种语言）；音视频分析用 `qwen3.5-omni-flash`（支持思考模式）[原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。  
- **其他模态**：  
  - 3D生成：仅华北2（北京）地域可用，模型 `Tripo/Tripo-P1.0`（快速预览）和 `Tripo/Tripo-H3.1`（影视级精度）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
  - 音乐生成：邀测中，模型 `fun-music-v1`（支持歌词/提示词输入、男女声选择）和 `fun-music-preview`（纯音乐模式）[原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
  - 向量与重排序：文本 Embedding 推荐 `text-embedding-v4`；多模态 Embedding 推荐 `qwen3-vl-embedding`；重排序推荐 `qwen3-rerank`（文本）或 `qwen3-vl-rerank`（多模态）[原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 1 和文档 2 中对 `qwen3.7-plus` 的视频最大时长描述存在不一致——文档 1 写“最长2小时”，文档 2 明确列出“最长2小时 / 2GB”；而文档 4 中 `happyhorse-1.1-i2v` 的时长为“3–15秒”。此处以文档 2 的量化指标为准，即 `qwen3.7-plus` 视频理解上限为 **2小时或2GB（取先到者）**，非绝对时长。

## 关键参数

不同模型系列的关键参数差异显著，开发者需按需配置：

- **上下文窗口**：文本模型中 `qwen3.7-plus`/`qwen3.7-flash` 为 1M token；`qwen-long` 达 10M token；视觉模型如 `qwen3.7-plus` 同样支持 1M token 文本上下文 + 图像/视频输入；语音模型（如 `qwen3.5-omni-plus`）支持音频最长 3 小时、视频最长 1 小时。  
- **输入格式控制**：  
  - 视觉模型：单张图片 [Token](../concepts/token.md) 数 = `h × w / (32 × 32) + 2`，最高支持 1600 万像素 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
  - 3D模型：`input` 字段互斥，`prompt`（文生3D）、`image`（单图生3D）、`images`（2–4张多角度图）三选一 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
  - 音乐模型：`fun-music-v1` 支持 `prompt` 或 `lyrics` 至少传入其一；`fun-music-preview` 则要求必传 `prompt` [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **输出控制**：  
  - 结构化输出：`qwen3.7-plus` 等 Qwen3.7+ 模型在非思考模式下支持 JSON 输出；视觉模型同样支持 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
  - 音频格式：TTS 模型通过 `format` 参数指定 `mp3`（体积小）或 `wav`（无损）；音乐模型同理 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **高级能力开关**：  
  - 思考模式：通过 `enable_thinking`（Responses API）或 `reasoning.effort` 控制，Qwen3 及以上模型均支持 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
  - Function Calling：通用文本/视觉模型普遍支持；但 `qwen3.7-max` 不支持结构化输出，`deepseek-v4-pro` 不支持内置工具 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
  - 联网搜索：仅 `qwen3.5-omni-plus`（HTTP/WebSocket）支持，且与 Function Calling 不可同时启用 [原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。

## 使用方式

所有模型均通过统一的 DashScope API 接入，核心流程为：开通服务 → 获取 API Key → 构造请求 → 处理响应。

- **认证与端点**：API Key 必须配置为环境变量 `DASHSCOPE_API_KEY`；地域强约束（如 Tripo 仅限华北2），端点需替换 `{WorkspaceId}` 为实际业务空间 ID [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **同步 vs 异步**：  
  - 同步：适用于低延迟场景（如 TTS 实时合成、ASR 实时识别），直接返回结果。  
  - 异步：适用于长耗时任务（如 3D 生成、视频生成），需先调用任务创建接口获取 `task_id`，再轮询查询结果（建议间隔 ≥15 秒）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **流式传输**：WebSocket 协议（如 `qwen-audio-3.0-realtime-plus`、`fun-asr-realtime`）支持音频/文本边输入边输出，降低端到端延迟；HTTP 流式（如 `qwen-audio-3.0-tts-plus`）支持分块返回音频 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。  
- **SDK 支持**：Python/Java SDK 全面覆盖；移动端（Android/iOS）仅 `qwen-audio` 和 `fun-asr` 系列支持 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型、Fun-Music 音乐模型、部分语音模型（如 `fun-asr`）仅在华北2（北京）地域可用，跨地域调用将失败 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **资源约束**：  
  - 视频生成：`happyhorse-1.1-t2v` 单次输出最长 15 秒，分辨率限 1080P；`wan2.7-t2v` 支持 2–15 秒 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。  
  - ASR 文件大小：`fun-asr` 非实时模型支持最大 2GB/12 小时；`qwen3.5-omni-plus` 限 2GB/3 小时 [原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **功能互斥**：  
  - S2S 模型中，`qwen-audio-3.0-realtime-plus` 支持 Function Calling 但不支持联网搜索和思考模式；`qwen3.5-omni-plus` 支持后两者，但联网搜索与 Function Calling 不可共存 [原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。  
  - 思考模式启用时，`qwen3-omni-flash` 仅输出文本，不生成语音 [原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。  
- **模型演进**：旧版模型（如 `qwen2.5-omni-7b`、`qwen-omni-turbo`）已停止更新，新项目必须使用 Qwen3.5+ 系列 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。  
- **计费差异**：Qwen3-TTS 系列中，`qwen3-tts-flash` 等 HTTP 模型按 [Token](../concepts/token.md) 计费；而 `qwen-audio-3.0-tts-plus` 按音频时长计费，需注意成本模型切换 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


