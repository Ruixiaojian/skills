# model experience

`model experience` 是百炼平台面向开发者提供的模型选型与使用指南集合，覆盖文本、视觉、语音、音频、3D、向量、重排序等全模态能力。其核心目标是帮助开发者根据具体场景（如OCR、视频理解、实时对话、RAG检索）快速匹配最适配的模型，并明确关键参数、调用方式与约束边界。所有模型均通过统一 API 接口接入，支持流式/非流式、同步/异步等多种交互模式。

## 支持的模型/功能

百炼提供覆盖多模态的模型矩阵，按能力层级与场景聚焦划分：

- **文本生成**：以 `qwen3.7-plus` 和 `qwen3.8-max` 为代表，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码执行）及结构化 JSON 输出；轻量场景可选用 `qwen3.7-flash` [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.8-max` 支持图像（最高 1600 万像素）、视频（最长 2 小时/2GB）、OCR（推荐专用 `qwen3.5-ocr`）及结构化输出；`qwen3.5-omni-plus` 支持音视频输入 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **语音处理**：ASR 推荐 `qwen-audio-3.0-asr-flash-streaming`（实时）或 `qwen-audio-3.0-asr-flash-filetrans`（文件转写）；TTS 推荐 `qwen-audio-3.0-tts-plus`（标准合成）或 `cosyvoice-v3.5-plus`（声音设计）；S2S（语音→语音）首选 `qwen-audio-3.0-realtime-plus` 或 `qwen3.5-omni-flash` [原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **生成类模型**：  
  - 图像：`qwen-image-3.0-pro`（复杂版面/小字渲染）、`wan2.7-image-pro`（品牌色/高分辨率）、`z-image-turbo`（低成本快速生成）；  
  - 视频：`happyhorse-1.1-i2v`（首帧生视频）、`wan2.7-i2v-2026-04-25`（首尾帧续写）；  
  - 音乐：`fun-music-v1`（支持歌词/提示词/纯音乐生成，仅华北2可用）；  
  - 3D：`Tripo/Tripo-P1.0`（快速预览）、`Tripo/Tripo-H3.1`（高精度，仅北京地域）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **嵌入与重排序**：文本 Embedding 使用 `text-embedding-v4`（维度可配），多模态 Embedding 使用 `qwen3-vl-embedding`（融合向量）或 `tongyi-embedding-vision-plus`（独立向量），重排序使用 `qwen3-rerank`（文本）或 `qwen3-vl-rerank`（多模态）[原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 10 与文档 11 对 `qwen3.5-omni-flash` 的输入模态描述存在不一致——文档 10 称其支持“文本、音频、图片、视频”，而文档 11 的表格中明确标注为“文本、音频、图片”（不含视频）。实际调用应以文档 11 的 `All models` 表格为准，即该模型 HTTP 模式下不支持视频输入。

## 关键参数

不同模型系列的关键参数需按场景显式配置：

- **上下文长度**：文本模型普遍支持 1M [Token](../concepts/token.md)（如 `qwen3.7-plus`），`qwen-long` 达 10M；视觉模型上下文与视频时长强相关（`qwen3.7-plus` 支持 2 小时视频）；Embedding 模型最大 [Token](../concepts/token.md) 数为 `text-embedding-v4` 的 8,192 或 `qwen3-vl-embedding` 的 32,000。  
- **分辨率与时长限制**：  
  - 图像：`qwen-image-3.0-pro` 最大 2048×2048，`wan2.7-image-pro` 文生图支持 4096×4096；  
  - 视频：`qwen3.7-plus` 支持最长 2 小时/2GB，`qwen3.5-omni-plus` 限 1 小时；  
  - 音频：ASR `qwen-audio-3.0-asr-flash-filetrans` 支持最长 12 小时/2GB，TTS `qwen-audio-3.0-tts-plus` 无时长硬限制。  
- **输出控制**：  
  - TTS 支持 `format`（`mp3`/`wav`）、`gender`（`fun-music-v1`）、`is_instrumental`（`true` 生成纯音乐）；  
  - Tripo 3D 支持 `parameters.texture_quality`（`standard`/`detailed`）和 `parameters.geometry_quality`（`Tripo-H3.1` 专属）；  
  - 重排序模型 `qwen3-rerank` 单次最多处理 500 个文档。  
- **语言与方言**：ASR/TTS/S2S 模型广泛支持中文方言（粤语、四川话等）及 100+ 外语，但需注意 `fun-music-v1` 仅支持中英文，`qwen3-livetranslate-flash` 仅支持 18 种语言 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。

## 使用方式

所有模型均通过统一 RESTful API 调用，核心流程为：获取 API Key → 构造请求 → 解析响应。关键实践如下：

- **异步任务**：Tripo 3D 生成必须使用异步模式（`X-DashScope-Async: enable`），轮询 `task_id` 获取结果，有效期 24 小时 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **流式传输**：实时场景（ASR、TTS、S2S）优先使用 WebSocket；HTTP 流式需设置 `Accept: text/event-stream` 并解析 SSE 响应。  
- **多模态输入**：视觉/全模态模型需在 `input` 中按字段区分——`prompt`（文本）、`image`（单图 URL）、`images`（多图列表）、`video`（视频 URL）；Tripo 3D 严格互斥 `prompt`/`image`/`images` 字段。  
- **协议选择**：S2S 场景若需低延迟选 WebSocket，若需 Function Calling 或思考模式则选 HTTP；语音识别中，实时字幕用 `qwen-audio-3.0-asr-flash-streaming`（WebSocket），会议录音转写用 `qwen-audio-3.0-asr-flash-filetrans`（HTTP）。  
- **SDK 支持**：Qwen-Audio-TTS/CosyVoice 系列支持 Python/Java/Android/iOS SDK；Tripo 3D 仅支持原生 HTTP 调用。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型、`fun-music-v1` 仅在华北2（北京）地域可用，且需使用对应地域的 API Endpoint 和 API Key [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **模型弃用**：`qwen-omni-turbo`、`qwen-vl-max`、`qwen2.5-omni-7b` 等旧版模型已停止更新，新项目应避免选用 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。  
- **功能冲突**：Qwen3.5-Omni 的联网搜索与 Function Calling 不可同时启用；思考模式开启后不支持语音输出 [原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。  
- **成本与性能权衡**：`qwen3.7-flash` 在效果接近 `qwen3.7-plus` 的前提下显著降低成本，但 `qwen3.7-flash` 的最大图片数为 256（`qwen3.7-plus` 为 2048），需评估输入规模 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **文件规格**：Tripo 3D 输入图片需为 JPEG/PNG，宽高 20–6000 像素，单张 ≤20MB；ASR 文件转写最大 2GB；TTS 输入文本长度无硬限制，但过长文本建议分段处理。

## 来源文档

- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)


