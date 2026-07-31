# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览与选型指南，涵盖文本、视觉、语音、音乐、3D、向量等全模态模型的适用场景、核心参数、调用方式及关键限制。本文档聚焦技术事实，不包含营销性描述，所有推荐均基于当前（2026年中）稳定可用的模型版本与API行为。

## 支持的模型与功能

百炼提供覆盖[多模态](../concepts/multi-modal.md)的模型矩阵，按能力层级与使用场景组织：

- **文本生成**：以 `qwen3.7-plus` 为旗舰，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化 JSON 输出及逐步推理（`enable_thinking`）；轻量替代方案 `qwen3.7-flash` 在效果接近的前提下显著降低成本 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 同时支持图像、视频（最长 2 小时）、OCR 及结构化输出；专用 OCR 模型 `qwen3.5-ocr` 针对文档/手写内容优化 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片/视频生成与编辑**：`wan2.7-image-pro` 支持文生图（4096×4096）、多图参考编辑；`happyhorse-1.1-t2v` 和 `wan2.7-i2v-2026-04-25` 分别适用于文生视频与首尾帧续写 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **3D 生成**：Tripo 系列仅限华北2（北京）地域，需异步任务轮询，支持文生/单图生/多图生三种模式，`Tripo/Tripo-P1.0`（2万面）适合快速验证，`Tripo/Tripo-H3.1`（200万面）用于高精度资产 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音与音频**：`qwen-audio-3.0-asr-flash-streaming`（实时）、`qwen-audio-3.0-asr-flash-filetrans`（非实时）覆盖多语种及方言；`qwen-audio-3.0-realtime-plus` 实现端到端 S2S，支持 Function Calling；`fun-music-v1` 支持 [prompt](prompt.md)/lyrics 双输入及 gender 控制 [原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **向量与重排序**：`text-embedding-v4` 为文本 Embedding 默认推荐，支持 64–2048 维可调；`qwen3-rerank` 用于 RAG 后重排序，最大支持 500 文档；`qwen3-vl-rerank` 支持图文视频混合排序 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 1 中 `qwen3.8-max-preview` 标注“[Token](../concepts/token.md) Plan 可用”，但文档 2、9、10 均未提及该模型在视觉或全模态场景的实际支持，且其快照版本未出现在任何模型能力表中。建议以模型广场实时列表为准，避免依赖未广泛验证的预览版。

## 关键参数

各模型共性参数与行为如下：

- **上下文窗口**：文本模型普遍支持 1M [Token](../concepts/token.md)（如 `qwen3.7-plus`），视觉模型同样继承该长度；`qwen-long` 为特例，达 10M [Token](../concepts/token.md)，专用于超长文档处理。  
- **输入格式控制**：  
  - 视觉模型：单图像素上限 1600 万（`h × w / (32 × 32) + 2` 计算 Token）；视频最大 2 小时/2GB（`qwen3.7-plus`）。  
  - 3D 模型：`input` 字段互斥（`prompt`/`image`/`images`），`images` 接收 2–4 张 URL 列表。  
  - 音乐模型：`fun-music-v1` 支持 `gender`（male/female），`fun-music-preview` 不支持；`is_instrumental=true` 时忽略 `lyrics` 和 `gender`。  
- **输出控制**：  
  - 结构化输出：需显式启用（如 `response_format: { "type": "json_object" }`），仅部分模型支持（`qwen3.7-plus` 支持，`qwen3.7-max` 不支持）。  
  - 音频格式：TTS 和音乐模型通过 `format` 参数指定 `mp3`（小体积）或 `wav`（无损）。  
- **异步任务**：Tripo 3D、Fun-Music 等生成类模型必须使用 `X-DashScope-Async: enable` 头，并轮询 `task_id` 获取结果，有效期 24 小时。

## 使用方式

- **API 调用**：所有模型统一通过 `/api/v1/services/...` 路径接入，需配置 `DASHSCOPE_API_KEY` 和 `WorkspaceId`。HTTP 模型使用 POST 请求体传参；WebSocket 模型（如 `qwen-audio-3.0-realtime-plus`）需建立长连接流式通信。  
- **SDK 支持**：Qwen-Audio-TTS/CosyVoice、Qwen-Audio-ASR、Qwen-Audio-Realtime 等系列支持 DashScope Python/Java SDK；部分还支持 Android/iOS SDK。旧版 Qwen-TTS（按 Token 计费）已逐步被 Qwen3-TTS 替代 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。  
- **地域限制**：Tripo 3D、Fun-Music 仅限华北2（北京）；部分模型（如 `wan2.6-t2v-us`）明确标注适用于美国地域部署。  
- **认证与配额**：所有请求需 `Authorization: Bearer $DASHSCOPE_API_KEY`；异步任务需提前开通对应模型服务（如 Tripo）并确保 API Key 具备权限。

## 限制和注意事项

- **地域与服务开通**：Tripo 3D、Fun-Music 为邀测服务，需单独申请；`qwen-long` 等长上下文模型在部分地域可能不可用，须查模型广场状态。  
- **功能兼容性冲突**：  
  - Qwen3.5-Omni 的联网搜索与 Function Calling **不可同时开启**；  
  - 思考模式（`reasoning.effort`）启用时，S2S 模型 **不支持生成语音输出**；  
  - `qwen3.7-max` 支持思考模式与 Function Calling，但 **不支持结构化输出**（对比 `qwen3.7-plus`）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **输入约束**：  
  - ASR 非实时模型 `qwen-audio-3.0-asr-flash-filetrans` 最大支持 12 小时/2GB 音频；  
  - TTS `qwen3-tts-flash` 系列 HTTP 接口最大输入 5 分钟/10MB，WebSocket 版本无时长限制但受内存约束；  
  - 图片生成 `z-image-turbo` 仅支持文生图，**不支持编辑功能**。  
- **版本稳定性**：文档中大量快照版本（如 `qwen3.7-plus-2026-05-26`）可用于生产环境锁定，但推荐优先使用无日期后缀的稳定入口模型（如 `qwen3.7-plus`），由平台自动路由至最新可用快照。

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


