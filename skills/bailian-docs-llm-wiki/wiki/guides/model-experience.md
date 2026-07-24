# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览，涵盖文本、视觉、音视频、3D、Embedding 等全模态模型的选型指南、关键参数与使用规范。本文档聚焦实用性，帮助开发者根据具体场景（如编程、办公、OCR、实时对话、RAG）快速匹配最优模型，并明确各模型的能力边界与调用约束。

## 支持的模型与功能

百炼提供覆盖多模态的模型体系，按核心能力分类如下：

- **文本生成**：支持长上下文（最高 1000 万 [Token](../concepts/token.md)）、Function Calling、内置工具（联网搜索/代码解释器）、结构化 JSON 输出及深度思考模式。旗舰模型 `qwen3.7-plus` 与 `qwen3.7-max` 均支持完整能力栈，而 `qwen-long` 专为超长文档（如合同、文献）设计 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：支持图像、视频（最长 2 小时）、OCR 及多图分析。`qwen3.7-plus` 和 `qwen3.6-flash` 同时支持 Function Calling 与内置工具；`qwen3.5-ocr` 专为文档/手写识别优化 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片/视频生成与编辑**：`wan2.7-image-pro` 支持文生图（4096×4096）、多图参考编辑；`happyhorse-1.1-t2v` 与 `wan2.7-i2v-2026-04-25` 分别适用于通用文生视频与首尾帧续写 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **3D 生成**：Tripo 系列（`Tripo/Tripo-P1.0`、`Tripo/Tripo-H3.1`）支持文生3D、单图/多图生3D，需在华北2（北京）地域调用，且必须使用该地域 API Key [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音与音乐**：`fun-asr-realtime` 支持热词增强与方言识别；`qwen-audio-3.0-tts-plus` 支持声音复刻与指令控制；`fun-music-v1` 支持歌词驱动歌曲生成（邀测中）[原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **全模态与 S2S**：`qwen3.5-omni-plus` 支持文本/音频/图片/视频联合理解与 Function Calling；`qwen3.5-livetranslate-flash-realtime` 提供 60 种语言实时语音翻译 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。  
- **向量与重排序**：`text-embedding-v4`（文本）、`qwen3-vl-embedding`（多模态）、`qwen3-rerank`（纯文本重排）构成 RAG 检索链核心组件 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 1 与文档 2 对 `qwen3.7-plus` 的上下文窗口描述一致（1M），但文档 2 中表格将 `qwen3.7-plus` 的“最大输出”列为 64k，而文档 1 未明确该参数；实际调用应以模型广场或 API 文档为准。此外，文档 9 和文档 10 均列出 `qwen3.5-livetranslate-flash-realtime`，但文档 10 表格中该模型的“联网搜索”列为 `\--`，而文档 9 明确其不支持联网搜索——二者一致，属正确约束。

## 关键参数

各模型共性关键参数如下（具体值依模型而异）：

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model` | 模型 ID，必填 | `qwen3.7-plus`, `wan2.7-image-pro`, `text-embedding-v4` |
| `input` | 输入内容结构体，字段因模态而异 | `{"prompt": "..."}`, `{"image": "url"}`, `{"audio": "url"}` |
| `parameters` | 模型特有配置 | `{"texture_quality": "standard"}`（Tripo）、`{"format": "mp3"}`（Fun-Music） |
| `enable_thinking` / `reasoning.effort` | 控制深度思考模式开关与强度 | `true`, `"high"`（仅 Qwen3+ 文本模型） |
| `X-DashScope-Async: enable` | [异步任务](../concepts/asynchronous-task.md)必需 Header（如 Tripo 3D） | — |
| `is_instrumental` | Fun-Music 纯音乐开关 | `true` |

- **[Token](../concepts/token.md) 限制**：文本模型最大上下文从 8k（旧版）至 10M（`qwen-long`）；视觉模型单图像素上限 1600 万（`h × w / (32 × 32) + 2` 计算 [Token](../concepts/token.md)）；音频/视频文件大小上限因模型而异（如 `qwen3.5-omni-plus` 视频限 2GB）。
- **地域约束**：Tripo 3D 模型仅支持华北2（北京）；部分模型（如 `fun-music-v1`）亦限定地域 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

## 使用方式

- **同步调用（HTTP）**：适用于非实时场景（如文档摘要、批量图片生成）。构造 POST 请求，`Content-Type: application/json`，`Authorization: Bearer $DASHSCOPE_API_KEY`。示例见 [原文标题](../../raw/model-user-guide/model-experience/image-model.md) 中 `wan2.7-image-pro` 调用。
- **流式调用（WebSocket）**：适用于实时交互（语音助手、直播字幕）。需建立 WebSocket 连接，发送二进制音频流或文本事件。`qwen-audio-3.0-realtime-plus` 和 `fun-asr-realtime` 均采用此模式 [原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。
- **[异步任务](../concepts/asynchronous-task.md)（HTTP + Polling）**：适用于耗时操作（3D 生成、长视频处理）。先调用 `/3d-generation` 获取 `task_id`，再轮询 `/tasks/{task_id}` 查询状态（建议间隔 ≥15s）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **SDK 集成**：DashScope SDK（Python/Java）支持多数模型；Fun-ASR 和 Qwen-Audio 还提供 Android/iOS SDK。

## 限制和注意事项

- **模型可用性**：Tripo 3D、Fun-Music 处于邀测阶段，需单独申请开通；`qwen3.8-max-preview` 仅 Token Plan 用户可用 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。
- **功能互斥**：联网搜索与 Function Calling 不可同时启用（Qwen3.5-Omni）；思考模式下不支持语音输出（Qwen3-Omni-Flash）；`is_instrumental=true` 时 `lyrics` 和 `gender` 参数被忽略（Fun-Music）。
- **输入约束**：Tripo 多图输入限 2–4 张；Fun-Music 歌词需含 `[verse]`/`[chorus]` 标签；视觉模型单图宽高需在 20–6000 像素间。
- **版本管理**：推荐使用无后缀模型 ID（如 `qwen3.7-plus`），平台自动路由至最新稳定版；若需锁定版本，使用快照 ID（如 `qwen3.7-plus-2026-05-26`）。
- **计费差异**：Qwen-TTS 旧版按 Token 计费；Qwen3-TTS 系列按请求/时长计费；批量推理可降低成本（文本生成场景）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


