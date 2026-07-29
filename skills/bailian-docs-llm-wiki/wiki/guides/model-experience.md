# model experience

`model experience` 是百炼平台面向开发者提供的模型能力概览与选型指南，覆盖文本、视觉、语音、音视频、3D、音乐等全模态场景。本文档聚焦核心能力矩阵、关键参数约束与工程化使用要点，帮助开发者快速匹配业务需求与模型能力边界，避免常见误用。

## 支持的模型/功能

百炼提供覆盖多模态的模型家族，按能力层级与场景聚焦分为以下几类：

- **文本生成**：以 `qwen3.7-plus` 为旗舰，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码执行）及结构化 JSON 输出；轻量替代方案 `qwen3.7-flash` 在保持相同上下文长度和功能集的前提下显著降低成本 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。编程与 Agent 场景推荐 `qwen3.7-max`（百万 token 上下文）或 `qwen3.8-max-preview`（[Token](../concepts/token.md) Plan 可用）[文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。
  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 支持图像（最高 1600 万像素）、视频（最长 2 小时 / 2GB）、OCR（`qwen3.5-ocr` 专优）及结构化输出；`qwen3.5-omni-plus` 支持音频输入，适用于多模态内容分析 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

- **图片/视频生成与编辑**：`wan2.7-image-pro` 支持文生图（4096×4096）、多图参考编辑；`happyhorse-1.1-t2v` 支持文生视频（1080P，3–15 秒）；`wan2.7-i2v-2026-04-25` 支持首尾帧续写，适用于长视频构建 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)、[视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。

- **语音与音频**：
  - 语音识别（ASR）：`fun-asr`（非实时，支持说话人分离）与 `qwen3.5-omni-plus`（Prompt 上下文注入，支持情感识别）[语音识别](../../raw/model-user-guide/model-experience/asr-model.md)；
  - 语音合成（TTS）：`qwen-audio-3.0-tts-plus`（标准合成+声音复刻）与 `cosyvoice-v3.5-plus`（声音设计+指令控制）[语音合成](../../raw/model-user-guide/model-experience/tts-model.md)；
  - 语音转语音（S2S）：`qwen-audio-3.0-realtime-plus`（低延迟对话）与 `qwen3.5-livetranslate-flash-realtime`（60 语言同传）[语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。

- **3D 与音乐**：`Tripo/Tripo-P1.0`（快速预览，2 万面）与 `Tripo/Tripo-H3.1`（高精度，200 万面），仅限华北2（北京）地域 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)；`fun-music-v1` 支持歌词/提示词生成带声歌曲，`is_instrumental=true` 可生成纯音乐 [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。

- **向量与重排序**：`text-embedding-v4`（文本检索）、`qwen3-vl-embedding`（图文融合向量）、`qwen3-rerank`（文本重排序，最多 500 文档）[向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 1 与文档 2 对 `qwen3.7-max` 的结构化输出支持描述矛盾——文档 1 表格中标注其“不支持”，而文档 2 表格中标注“支持”。实际以 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 中最新表格为准：`qwen3.7-max` 系列**不支持**结构化输出。

## 关键参数

各模型核心参数需严格遵循约束，否则请求将失败：

- **上下文窗口**：`qwen3.7-plus`/`qwen3.7-flash` 为 1M token；`qwen-long` 达 10M token；`qwen3.5-omni-plus` 非实时模式支持视频最长 1 小时、音频最长 3 小时 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)、[文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。
  
- **多模态输入限制**：
  - 图像：单张最高 1600 万像素，[Token](../concepts/token.md) 消耗公式为 `h × w / (32 × 32) + 2`；
  - 视频：`qwen3.7-plus` 支持最多 64 段视频，每段最长 2 小时 / 2GB；
  - 图片数：`qwen3.7-plus` 最多 2048 张，`qwen3.7-flash` 限 256 张 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

- **音频规格**：
  - ASR：`fun-asr` 非实时最大 12 小时 / 2GB；`qwen3.5-omni-plus` 非实时限 3 小时 / 2GB；
  - S2S：`qwen3.5-omni-plus-realtime` 实时模式限 2 小时音频流 [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)、[语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。

- **3D 与音乐**：
  - Tripo：仅支持华北2（北京）地域，API Key 必须配置该地域；`Tripo/Tripo-P1.0` 单图输入宽高 20–6000 像素，≤20MB [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)；
  - Fun-Music：`fun-music-v1` 支持 `gender` 参数（男/女声），`fun-music-preview` 不支持；`is_instrumental=true` 时忽略 `lyrics` 和 `gender` [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。

## 使用方式

- **统一调用协议**：所有模型均通过 DashScope API 调用，HTTP 或 WebSocket 接入取决于场景。WebSocket 用于实时流式交互（如语音助手、视频编辑），HTTP 用于批量/文件处理（如文档摘要、视频转写）。
  
- **参数传递规范**：
  - 多模态输入：视觉模型通过 `input.images`（数组）或 `input.video_url` 传入；S2S 模型通过 `input.audio_url` 或流式二进制传输；
  - 功能开关：`enable_thinking` 控制思考模式（文本模型）；`is_instrumental` 控制纯音乐生成（Fun-Music）；`texture_quality` 控制 Tripo 贴图质量 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)、[音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)、[Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

- **异步任务处理**：Tripo 3D 生成必须使用异步 API（`X-DashScope-Async: enable`），轮询 `task_id` 获取结果，有效期 24 小时 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

## 限制和注意事项

- **地域与服务开通**：Tripo 3D 仅限华北2（北京）；Fun-Music 处于邀测阶段，需在模型广场申请开通 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)、[音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。

- **功能互斥性**：
  - Qwen3.5-Omni 的联网搜索与 Function Calling **不可同时启用**；
  - 思考模式下不支持语音生成（S2S 场景）；
  - `qwen-audio-3.0-realtime-plus` 不支持联网搜索和思考模式 [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。

- **旧版模型弃用**：`qwen2.5-omni-7b`、`qwen-omni-turbo`、`paraformer` 等已明确标注为“不再更新”或“不推荐新项目使用”，应优先选用 Qwen3.5/Qwen3.6 系列 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)、[全模态](../../raw/model-user-guide/model-experience/omni.md)、[语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。

- **成本与性能权衡**：`qwen3.7-flash` 在效果接近 `qwen3.7-plus` 的前提下显著降低成本，但图片数上限降至 256 张；`z-image-turbo` 生成速度快 10 倍、价格约 1/5，但不支持图片编辑 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。

## 来源文档

- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)


