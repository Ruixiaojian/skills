# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，涵盖文本、视觉、语音、音乐、3D、向量等全模态能力。所有模型均通过标准化 API（HTTP/WebSocket）接入，支持结构化输出、Function Calling、思考模式等通用能力，并按场景提供推荐选型路径。开发者可基于任务目标（如生成、理解、检索）和约束条件（延迟、成本、精度）快速定位最优模型。

## 支持的模型与功能

百炼平台提供覆盖多模态的模型矩阵，核心能力按类型组织：

- **文本生成**：以 `qwen3.7-plus` 和 `qwen3.8-max` 为代表，支持 100 万上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化 JSON 输出及逐步推理（`enable_thinking`）。轻量场景可选用 `qwen3.7-flash` [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.8-max` 同时支持图像、视频（最长 2 小时）、OCR（`qwen3.5-ocr` 专用）及结构化输出；`qwen3-vl-plus` 系列专注多模态融合 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。
- **图片/视频生成与编辑**：`qwen-image-3.0-pro` 支持高保真文生图与复杂版面编辑；`happyhorse-1.1-i2v` 和 `wan2.7-i2v-2026-04-25` 分别适用于首帧与首尾帧视频生成 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。
- **语音与音频**：`qwen-audio-3.0-asr-flash-streaming`（实时识别）、`qwen-audio-3.0-tts-plus`（指令控制合成）、`fun-music-v1`（歌词/提示词驱动歌曲生成）构成端到端音频链路 [原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。
- **全模态与 S2S**：`qwen3.5-omni-plus` 支持文本/音频/图片/视频联合理解与输出，兼具 Function Calling 和联网搜索；`qwen3.5-livetranslate-flash-realtime` 提供 60 种语言实时翻译 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。
- **向量与重排序**：`text-embedding-v4`（文本）、`qwen3-vl-embedding`（多模态）、`qwen3-rerank`（纯文本重排）支撑 RAG 检索精度提升 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。
- **3D 生成**：`Tripo/Tripo-P1.0`（快速预览）与 `Tripo/Tripo-H3.1`（影视级精度）支持文生 3D、单图/多图生 3D，仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

> **注意**：文档 9 与文档 10 对 `qwen3.5-omni-flash` 的联网搜索支持描述存在矛盾——文档 9 明确标注其支持联网搜索，而文档 10 在“推荐模型”表格中将该能力标记为 `\--`（不支持）。实际以文档 9 为准，即 `qwen3.5-omni-flash`（HTTP/WebSocket）支持联网搜索。

## 关键参数

不同模态模型共用部分通用参数，同时具备领域特有参数：

- **通用参数**：
  - `enable_thinking`（文本/全模态）：开启逐步推理，适用于复杂逻辑推演 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。
  - `response_format`：指定结构化输出格式（如 `{"type": "json_object"}`），所有支持结构化输出的模型均适用。
  - `tools`：定义 Function Calling 工具列表，模型自动选择并调用。
- **视觉参数**：
  - 图像分辨率影响 [Token](../concepts/token.md) 消耗：公式为 `h × w / (32 × 32) + 2`；视频最大时长为 2 小时（`qwen3.7-plus` 等）或 1 小时（`qwen3-vl-plus`）[原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。
- **语音参数**：
  - ASR：`hotword`（热词）、`prompt`（上下文注入）提升专业术语识别精度；`speaker_diarization`（说话人分离）仅 `qwen-audio-3.0-asr-flash-filetrans` 支持。
  - TTS：`voice_id`（音色 ID）、自然语言指令（如 `"用温柔语气，语速稍慢"`）控制表达风格。
- **3D 参数**：
  - `parameters.texture_quality`：`standard`（标清贴图）或 `detailed`（高清贴图）；`parameters.geometry_quality`（仅 `Tripo-H3.1`）：`standard`（150 万面）或 `ultra`（200 万面）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **Embedding 参数**：
  - `dimension`：`text-embedding-v4` 支持 64~2048 维，推荐 1024（默认）；多模态模型维度固定，不可调整。

## 使用方式

所有模型均通过 RESTful API 调用，遵循统一鉴权与异步流程：

- **同步调用**：适用于低延迟场景（如实时对话、TTS 流式合成）。使用 `POST /api/v1/services/{service}/{action}`，设置 `Authorization: Bearer {API_KEY}`，请求体包含 `model`、`input` 和 `parameters`。
- **异步调用**：适用于长耗时任务（如 3D 生成、视频分析）。先 `POST` 创建任务获取 `task_id`，再 `GET /api/v1/tasks/{task_id}` 轮询状态（建议间隔 ≥15 秒），成功后返回结果 URL [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **协议选择**：
  - WebSocket：用于实时流式交互（ASR/TTS/S2S），降低端到端延迟。
  - HTTP：支持同步响应与异步轮询，兼容性更广。
- **地域限制**：Tripo 3D 模型仅在华北2（北京）可用；部分模型（如 `fun-music-v1`）处于邀测阶段，需单独申请开通 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。

## 限制和注意事项

- **地域与服务开通**：Tripo 3D、Fun-Music 等模型严格限定地域（华北2）且需手动开通服务；未开通则返回 `403 Forbidden` [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **输入约束**：
  - 视频：最大 2GB/2 小时（`qwen3.7-plus`），但 `qwen3-vl-plus` 限 1 小时/2GB；图片分辨率上限 1600 万像素。
  - 音频：ASR 文件模式最大 12 小时/2GB（`qwen-audio-3.0-asr-flash-filetrans`），实时流无时长限制。
  - 3D 输入：单图需 JPEG/PNG 格式（20~6000 像素，≤20MB）；多图需 2~4 张，格式要求相同。
- **能力冲突**：联网搜索与 Function Calling 不可同时启用（Qwen3.5-Omni）；思考模式下不支持语音输出（S2S 场景）[原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。
- **版本管理**：快照版本（如 `qwen3.7-plus-2026-05-26`）确保稳定性，但旧版模型（Qwen3、Qwen2.5 系列）已停止更新，新项目应优先选用 Qwen3.5+ 系列 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。
- **计费差异**：Qwen-TTS 旧版按 [Token](../concepts/token.md) 计费，而 Qwen-Audio-TTS/CosyVoice 系列按请求或时长计费，需注意迁移成本。

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
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


