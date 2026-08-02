# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览与选型指南，涵盖文本、视觉、音视频、3D、Embedding 等全模态模型服务。本文档聚焦于核心模型能力、关键参数、标准化使用方式及明确限制，帮助开发者快速匹配业务场景与最优模型，避免因版本混淆或能力误判导致的集成问题。

## 支持的模型/功能

百炼提供覆盖多模态的模型矩阵，按能力维度可划分为以下几类：

- **文本生成**：以 `qwen3.7-plus` 为旗舰，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化 JSON 输出及逐步推理（`enable_thinking`）；轻量场景可选用 `qwen3.7-flash`，效果接近且成本更低 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 同时支持图像与视频理解（最长 2 小时），最高 1600 万像素/图，且具备 Function Calling 与结构化输出能力；OCR 场景专用 `qwen3.5-ocr` [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片/视频生成与编辑**：图片生成推荐 `wan2.7-image-pro`（支持文字渲染、角色一致性、多图编辑）；视频生成按需求选择 `happyhorse-1.1-t2v`（文生视频）或 `wan2.7-i2v-2026-04-25`（首尾帧续写）；所有视频模型均输出 720P/1080P MP4，时长 2–15 秒 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)、[视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。  
- **3D 与音频生成**：Tripo 模型（`Tripo/Tripo-P1.0`）支持文/图/多图生 3D，仅限华北2（北京）地域；Fun-Music（`fun-music-v1`）支持歌词/提示词生成带人声的完整歌曲，当前为邀测状态 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)、[音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **语音与多模态**：S2S 场景首选 `qwen-audio-3.0-realtime-plus`（WebSocket，支持 Function Calling）；全模态理解推荐 `qwen3.5-omni-plus`（HTTP/WebSocket，支持音视频+图片+文本输入，含联网搜索）；语音识别按实时性选 `qwen-audio-3.0-asr-flash-streaming`（流式）或 `qwen-audio-3.0-asr-flash-filetrans`（文件转写，支持说话人分离） [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)、[全模态](../../raw/model-user-guide/model-experience/omni.md)、[语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **向量与重排序**：文本 Embedding 首选 `text-embedding-v4`（维度可配，默认 1024）；跨模态检索用 `qwen3-vl-embedding`（融合向量）或 `tongyi-embedding-vision-plus`（独立向量）；RAG 重排序用 `qwen3-rerank`（纯文本）或 `qwen3-vl-rerank`（多模态） [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 1 与文档 2 对 `qwen3.7-plus` 的上下文窗口描述一致（1M），但文档 1 表格中 `qwen3.7-max` 标注“不支持结构化输出”，而文档 2 表格中同名模型未列出该字段，存在信息缺失风险，实际使用请以模型广场最新快照为准。

## 关键参数

各模型共性关键参数如下（具体值依模型而异）：

- **`model`**：必需，模型 ID（如 `qwen3.7-plus`、`wan2.7-image-pro`），必须与调用 API 的协议（HTTP/WebSocket）匹配。  
- **`input`**：必需，结构依模型类型变化：  
  - 文本模型：`{"messages": [...]}` 或 `{"prompt": "..."}`；  
  - 视觉模型：`{"image": "url"}` 或 `{"video": "url"}`；  
  - Tripo：`{"prompt": "..."}` / `{"image": "url"}` / `{"images": ["url1", ...]}`（三者互斥）；  
  - Fun-Music：`{"prompt": "..."}` 或 `{"lyrics": "..."}`（至少传其一）；  
  - S2S/ASR：音频二进制或 URL，需符合格式要求（见[音频规格](../../raw/model-user-guide/model-experience/asr-model.md)）。  
- **`parameters`**：可选，控制生成行为：  
  - `texture_quality`（Tripo）：`standard`（默认）或 `detailed`；  
  - `format`（Fun-Music）：`mp3` 或 `wav`；  
  - `gender`（Fun-Music v1）：`male`/`female`；  
  - `is_instrumental`（Fun-Music）：`true` 生成纯音乐；  
  - `reasoning.effort`（Qwen3+ 文本模型）：控制思考深度（需配合 `enable_thinking`）。  
- **`X-DashScope-Async: enable`**：Tripo 等异步任务必需头，返回 `task_id` 后轮询结果 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

## 使用方式

- **同步调用（HTTP）**：适用于文本生成、Embedding、TTS、ASR 文件转写等。发送 POST 请求至对应 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation`），响应体直接返回结果。  
- **流式调用（WebSocket）**：适用于实时语音对话（`qwen-audio-3.0-realtime-plus`）、实时 ASR（`qwen-audio-3.0-asr-flash-streaming`）、实时 TTS。建立 WebSocket 连接后，按协议发送音频流或文本，接收分块响应。  
- **异步调用（HTTP + 轮询）**：适用于 Tripo 3D 生成、长视频处理等耗时任务。先发 POST 获取 `task_id`，再 GET `https://.../api/v1/tasks/{task_id}` 查询状态（`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`），建议轮询间隔 ≥15 秒 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **SDK 接入**：DashScope SDK（Python/Java）支持大部分 HTTP/WebSocket 模型；Android/iOS SDK 仅限 Qwen-Audio-TTS/CosyVoice 及部分 ASR 模型 [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)、[语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。

## 限制和注意事项

- **地域限制**：Tripo 模型仅支持华北2（北京）；Fun-Music 仅限北京地域且需邀测开通；部分模型（如 `wan2.6-t2v-us`）专用于美国地域 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)、[音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **输入约束**：  
  - 图像：单图 ≤1600 万像素，格式 JPEG/PNG；  
  - 视频：`qwen3.7-plus` 最长 2 小时/2GB，`qwen3-vl-plus` 最长 1 小时/2GB；  
  - Tripo 多图输入：2–4 张，每张 ≤20MB；  
  - ASR 文件：`qwen-audio-3.0-asr-flash-filetrans` 支持 12 小时/2GB，`qwen-audio-3.0-asr-flash` 限 5 分钟/2GB。  
- **能力冲突**：Qwen3.5-Omni 的联网搜索与 Function Calling 不可同时启用；思考模式开启时，S2S 模型不支持语音输出 [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。  
- **版本兼容性**：旧版模型（如 `qwen2.5-omni-7b`、`qwen-omni-turbo`）已停止更新，新项目必须使用 Qwen3.5 或更高系列；`qwen3.7-max-preview` 仅 Token Plan 用户可用 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **计费差异**：Qwen3-TTS Flash 系列按请求计费，旧版 `qwen-tts` 按 Token 计费；Tripo 按任务计费，非实时 ASR 按音频时长计费 [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)、[语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)


