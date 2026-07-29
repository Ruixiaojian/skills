# model experience

`model experience` 是百炼平台面向开发者提供的模型能力概览与使用指南，涵盖文本、视觉、音视频、3D、嵌入与重排序等全模态模型体系。本文档聚焦模型选型逻辑、关键参数配置与工程化接入要点，帮助开发者快速匹配业务场景与最优模型，避免因版本混淆或能力误判导致的集成问题。

## 支持的模型/功能

百炼平台提供覆盖多模态的模型矩阵，按能力维度可划分为以下几类：

- **文本生成**：以 `qwen3.7-plus` 为旗舰，支持 100 万上下文、Function Calling、内置工具（联网搜索/代码解释器）及结构化 JSON 输出；`qwen3.7-flash` 在效果接近的前提下显著降低成本；超长文档处理推荐 `qwen-long`（1000 万 [Token](../concepts/token.md)）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 同时支持图像、视频（最长 2 小时）、OCR 及结构化输出；专用 OCR 模型 `qwen3.5-ocr` 针对表格与手写内容优化 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片/视频生成与编辑**：`wan2.7-image-pro` 支持文生图（4096×4096）、多图参考编辑；`happyhorse-1.1-t2v` 和 `wan2.7-t2v-2026-06-12` 分别适用于通用文生视频与自定义音频驱动场景 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **语音与音乐**：`qwen-audio-3.0-tts-plus` 支持声音复刻与指令控制；`fun-music-v1` 支持 [prompt](prompt.md)/lyrics 两种输入方式生成带人声歌曲；`qwen3.5-omni-plus-realtime` 实现端到端语音对话与音视频理解 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。  
- **向量与重排序**：`text-embedding-v4` 为文本 Embedding 默认推荐，支持 64–2048 维灵活配置；`qwen3-rerank` 用于 RAG 场景 Top-N 结果精排；跨模态检索推荐 `qwen3-vl-embedding` [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。  
- **全模态与 S2S**：`qwen3.5-omni-plus` 支持文本/音频/图片/视频四模态输入与文本/语音双模态输出，具备联网搜索与 Function Calling；`qwen-audio-3.0-realtime-plus` 专为低延迟语音助手设计，支持语义 VAD 与 Function Calling [原文标题](../../raw/model-user-guide/model-experience/omni.md)。

> **注意**：文档 1 与文档 2 均将 `qwen3.7-plus` 列为视觉理解首选，但文档 2 明确其支持“最长2小时视频”，而文档 1 未提及视频能力——该差异源于文档 1 聚焦纯文本生成场景，视觉能力属文档 2 范畴，非矛盾，而是模块化分工体现。

## 关键参数

各模型系列通过标准化参数控制行为，核心参数如下：

- **上下文长度**：文本模型如 `qwen3.7-plus` 固定为 1M [Token](../concepts/token.md)；视觉模型同样继承该上下文，但实际消耗受图像分辨率影响（公式：`h × w / (32 × 32) + 2`）；`qwen-long` 独立支持 10M [Token](../concepts/token.md)。  
- **思考模式**：通过 `enable_thinking`（Responses API）或 `reasoning.effort` 控制，所有 Qwen3+ 模型均支持，但 `qwen-long` 和 `qwen3-vl-*` 系列明确标注“不支持”。  
- **结构化输出**：需在请求中声明 `response_format: { "type": "json_object" }`，仅 `qwen3.7-plus`、`qwen3.7-flash` 等部分模型原生支持，`qwen3.7-max` 明确标注“不支持” [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **多模态输入字段**：视觉/全模态模型通过 `input.image`、`input.images`、`input.video` 区分输入类型；Tripo 3D 模型严格互斥 `prompt`/`image`/`images` 字段 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **音频处理参数**：ASR 模型通过 `hotword`（Fun-ASR）或 `system_prompt`（Qwen3.5-Omni）增强专业术语识别；TTS 模型通过 `format`（`mp3`/`wav`）和 `gender`（`male`/`female`）控制输出；S2S 模型通过 `is_instrumental=true` 生成纯音乐。

## 使用方式

- **API 接入**：统一使用 DashScope SDK 或 HTTP/WebSocket 直调。所有模型需配置 `DASHSCOPE_API_KEY` 及 `{WorkspaceId}`（华北2地域专属），Tripo 3D 模型强制要求北京地域 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **[异步任务](../concepts/asynchronous-task.md)**：Tripo 3D、视频生成等耗时操作必须启用 `X-DashScope-Async: enable` 头，并轮询 `task_id` 获取结果（有效期 24 小时）。  
- **[流式输出](../concepts/streaming-output.md)**：WebSocket 接口（如 `qwen-audio-3.0-realtime-plus`、`fun-asr-realtime`）支持音频/文本流式传输；HTTP 接口（如 `qwen3.5-omni-plus`）支持 `stream=true` 流式响应。  
- **文件上传**：ASR/TTS/S2S 文件模式需通过 `multipart/form-data` 提交音频，或传入公网可访问 URL；Tripo 3D 的 `images` 字段要求传入 URL 列表（2–4 张，JPEG/PNG，≤20MB）。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型仅限华北2（北京）地域；Fun-Music 邀测阶段亦限定北京地域；部分模型（如 `wan2.6-t2v-us`）明确标注“适用于美国部署范围”。  
- **能力冲突**：Qwen3.5-Omni 的联网搜索与 Function Calling **不可同时开启**；思考模式启用时，S2S 模型 **不支持生成语音输出**；`qwen3.7-max` 不支持结构化 JSON 输出，与 `qwen3.7-plus` 形成能力取舍。  
- **版本兼容性**：`text-embedding-v3` 与 `v4` 维度不兼容，迁移需重建索引；旧版模型（如 `qwen2.5-omni-7b`、`qwen-omni-turbo`）已停止更新，新项目应避免选用 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。  
- **资源约束**：视频生成最大时长为 15 秒（`happyhorse-1.1-t2v`），Tripo 3D 多图输入限 4 张；Fun-ASR 非实时模型支持单文件最长 12 小时/2GB，而 Qwen3.5-Omni 限 3 小时/2GB。  
- **计费差异**：Qwen-TTS 旧版按 Token 计费，Qwen3-TTS 系列改为按请求/时长计费；Tripo 3D 按任务计费，H3.1 模型成本高于 P1.0。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)


