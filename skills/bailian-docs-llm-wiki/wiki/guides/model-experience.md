# model experience

`model experience` 是百炼平台面向开发者提供的模型选型与使用指南集合，覆盖文本、图像、视频、语音、音乐、3D生成及向量检索等全模态能力。本文档聚焦核心模型能力、关键参数、标准化接入方式及实际限制，帮助开发者快速匹配业务场景与最优模型，避免因版本混淆或能力误判导致的集成问题。

## 支持的模型与功能

百炼提供覆盖多模态的通用与专用模型，按能力层级和场景适配性组织：

- **文本生成**：以 `qwen3.7-plus` 为旗舰（1M上下文、Function Calling、内置工具、结构化输出），`qwen3.6-flash` 为高性价比替代；`qwen3.7-max` 和 `qwen3.8-max-preview`（仅 Token Plan 可用）适用于强推理需求 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.6-flash` 同时支持图像/视频理解（最长2小时/2GB）、OCR提取及结构化输出；专用 OCR 模型 `qwen3.5-ocr` 针对文档/手写优化 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片生成与编辑**：`wan2.7-image-pro` 支持文生图（4096×4096）、多图参考编辑及角色一致性；`qwen-image-3.0-pro`（邀测中）支持负向提示词与复杂版面渲染 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **视频生成与编辑**：`happyhorse-1.1-t2v`（文生视频）、`wan2.7-i2v-2026-04-25`（首尾帧续写）、`happyhorse-1.0-video-edit`（指令编辑）构成主流能力矩阵。  
- **语音与音频**：  
  - 语音合成：`qwen-audio-3.0-tts-plus`（支持声音复刻+指令控制）、`cosyvoice-v3.5-plus`（支持声音设计）；  
  - 语音识别：`fun-asr`（支持说话人分离）、`qwen3.5-omni-plus`（Prompt上下文注入）；  
  - 语音转语音（S2S）：`qwen-audio-3.0-realtime-plus`（端到端低延迟）、`qwen3.5-livetranslate-flash-realtime`（60语种实时翻译）；  
  - 音乐生成：`fun-music-v1`（支持歌词输入+性别选择），当前仅华北2（北京）地域邀测可用 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **3D生成**：`Tripo/Tripo-P1.0`（快速预览，2万面）、`Tripo/Tripo-H3.1`（影视级，200万面），**仅限华北2（北京）地域**，需配置对应地域 API Key [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **向量与重排序**：`text-embedding-v4`（文本检索默认）、`qwen3-vl-embedding`（图文融合）、`qwen3-rerank`（RAG后处理），支持跨模态检索与精度提升。

> **注意**：文档 1 中 `qwen3.7-max` 的“结构化输出”列为“不支持”，但文档 3 明确 `qwen3.7-plus` 支持该功能；实际开发中应以 `qwen3.7-plus` 或 `qwen3.6-flash` 作为结构化输出首选，避免使用 `qwen3.7-max`。

## 关键参数

各模型通过标准化参数控制行为，开发者需关注以下核心字段：

- **上下文长度**：文本模型普遍支持 1M Token（如 `qwen3.7-plus`），但 `qwen-long` 达 10M；视觉模型单图最高 1600 万像素，Token 消耗公式为 `h × w / (32 × 32) + 2`。  
- **输入格式**：  
  - 图片/视频：URL 必须可公开访问，本地文件需先上传至 OSS 并传入 URL；  
  - 3D 生成：`input.prompt`（文生3D）、`input.image`（单图）、`input.images`（2–4 张多角度图）三者互斥；  
  - 音乐生成：`fun-music-v1` 要求 `prompt` 或 `lyrics` 至少传入其一，`fun-music-preview` 则强制 `prompt`。  
- **输出控制**：  
  - 贴图质量：3D 模型通过 `parameters.texture_quality`（`standard`/`detailed`）控制；  
  - 音频格式：TTS 与音乐生成通过 `format` 参数指定 `mp3`（小体积）或 `wav`（无损）；  
  - 分辨率/时长：图片生成最大 4096×4096，视频生成单片段最长 15 秒（`happyhorse-1.1-*` 系列）。  
- **能力开关**：  
  - 思考模式：通过 `enable_thinking`（Responses API）或 `reasoning.effort` 控制，Qwen3 及以上模型均支持；  
  - Function Calling：所有通用文本/视觉模型支持，但 `deepseek-v4-pro` 等三方模型明确标注“不支持内置工具”。

## 使用方式

统一采用 RESTful API 调用，遵循百炼标准鉴权与异步流程：

- **同步调用**：适用于文本生成、TTS、ASR 等低延迟场景，直接返回结果（HTTP POST）。  
- **异步调用**：适用于 3D 生成、视频生成等耗时任务（>1s），需两步：  
  1. 提交任务获取 `task_id`（如 Tripo 3D 的 `/api/v1/services/aigc/video-generation/3d-generation`）；  
  2. 轮询 `GET /api/v1/tasks/{task_id}` 获取状态（`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`），有效期 24 小时。  
- **协议选择**：  
  - 实时交互（语音助手、直播翻译）：必须使用 WebSocket（如 `qwen-audio-3.0-realtime-plus`）；  
  - 批量/离线处理（会议转写、视频分析）：推荐 HTTP（支持 Function Calling、联网搜索等附加能力）。  
- **SDK 支持**：DashScope SDK（Python/Java）覆盖全部模型；Android/iOS SDK 仅限 `qwen-audio-*` 和 `fun-asr-*` 系列。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型**仅支持华北2（北京）地域**，且必须使用该地域 API Key；Fun-Music 同样仅限北京地域 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **能力冲突**：  
  - Qwen3.5-Omni 的联网搜索与 Function Calling **不可同时启用**；  
  - 思考模式下**不支持生成语音输出**（S2S 场景需关闭 `enable_thinking`）；  
  - `qwen3.7-max` 不支持结构化输出，而同系列 `qwen3.7-plus` 支持。  
- **输入约束**：  
  - ASR 非实时模型 `fun-asr` 支持最大 12 小时/2GB 音频，但 `qwen3-asr-flash` 仅限 5 分钟/10MB；  
  - 视频理解最大 2 小时/2GB（`qwen3.7-plus`），但 `qwen3-vl-flash` 限 1 小时/2GB；  
  - 3D 多图输入要求 2–4 张 PNG/JPEG，单图宽高 20–6000 像素，≤20MB。  
- **版本管理**：快照版本（如 `qwen3.7-plus-2026-05-26`）用于稳定性保障，但旧版模型（Qwen3.3 及更早）已停止更新，新项目应选用 Qwen3.6+ 系列。  
- **计费差异**：`qwen3.8-max-preview` 仅 Token Plan 用户可用；`qwen-tts`（旧版）按 Token 计费，而 `qwen-audio-3.0-tts-*` 系列按请求计费。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


