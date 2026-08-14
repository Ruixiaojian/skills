# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览与选型指南，涵盖文本、视觉、语音、音视频、3D、音乐等全模态模型的适用场景、核心参数、调用方式及关键限制。本文档聚焦实用选型逻辑，不包含营销性描述，所有推荐均基于当前（2026年中）稳定发布的模型能力快照。

## 支持的模型/功能

百炼平台提供覆盖多模态的模型能力矩阵，按任务类型划分如下：

- **文本生成**：支持通用对话、代码生成、办公文档处理、结构化输出（JSON）、Function Calling 与内置工具（联网搜索、代码解释器等）。旗舰模型 `qwen3.8-max` 具备最强推理能力；`qwen3.7-plus` 是能力与成本均衡的首选；`qwen3.7-flash` 在效果接近旗舰的前提下显著降低成本，三者均支持 100 万 [Token](../concepts/token.md) 上下文、思考模式与完整工具链 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：支持图像分析、OCR、长视频理解（最长 2 小时）、多图输入。`qwen3.7-plus` 和 `qwen3.7-flash` 是视觉任务的主力推荐，二者均支持 Function Calling、内置工具及结构化输出；专用 OCR 模型 `qwen3.5-ocr` 针对文档/表格/手写内容优化 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片生成与编辑**：`qwen-image-3.0-pro` 支持复杂版面、小字渲染与高保真编辑；`wan2.7-image-pro` 侧重品牌色控制与角色一致性多图生成；`z-image-turbo` 适用于低成本、高吞吐的写实人像生成 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **语音合成（TTS）**：支持标准合成（内置音色库）、声音复刻（Voice Cloning）与声音设计（Voice Design），并可通过自然语言指令动态控制语速、情绪和风格。`qwen-audio-3.0-tts-plus` 和 `cosyvoice-v3.5-plus` 均支持全部三种能力 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。  
- **语音识别（ASR）**：区分实时流式（WebSocket）与非实时文件转写（HTTP）。`qwen-audio-3.0-asr-flash-streaming` 适用于实时字幕与语音助手；`qwen-audio-3.0-asr-flash-filetrans` 支持说话人分离，适用于会议录音分析 [原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **语音转语音（S2S）**：端到端低延迟语音交互，`qwen-audio-3.0-realtime-plus` 支持 Function Calling；`qwen3.5-omni-flash` 在 HTTP 模式下支持联网搜索与思考模式，适用于视频分析等非实时场景 [原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。  
- **3D 生成**：Tripo 系列支持文生3D、单图生3D、多图生3D 三种模式，仅限华北2（北京）地域，需异步轮询获取结果 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **音乐生成**：Fun-Music 处于邀测阶段，支持 [prompt](prompt.md)/lyrics 输入生成带人声或纯音乐，仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **向量与重排序**：`text-embedding-v4` 是文本 Embedding 的默认推荐；`qwen3-vl-embedding` 适用于图文融合检索；`qwen3-rerank` 用于 RAG 后的 Top-N 结果精排 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 1 与文档 2 对 `qwen3.7-plus` 是否支持“内置工具”的描述存在不一致——文档 1 明确列出其支持，而文档 2 在“Function Calling与内置工具”小节中仅将内置工具支持范围限定为 `qwen3.7-max-2026-06-08`、`qwen3.7-plus`、`qwen3.6-plus` 等，但未在表格中明确标注。根据文档 1 的权威性（作为主干文本生成文档）及上下文一致性，以文档 1 为准：`qwen3.7-plus` 支持内置工具。

## 关键参数

各模态模型的关键可配置参数如下：

- **上下文窗口**：文本/视觉模型主流为 1M [Token](../concepts/token.md)（如 `qwen3.7-plus`），超长文档推荐 `qwen-long`（10M [Token](../concepts/token.md)）；视频理解最大支持 2 小时；3D 生成无上下文概念，但受输入图片分辨率（20–6000 像素）与数量（单图/2–4 张）约束。  
- **输入规格**：  
  - 图像：多数视觉模型支持单图最高 1600 万像素，Token 消耗公式为 `h × w / (32 × 32) + 2`；  
  - 视频：`qwen3.7-plus` 等支持最长 2 小时、2GB；  
  - 音频：ASR 实时流无时长限制，文件转写最大 12 小时/2GB；TTS 输入文本长度依模型而异，Qwen-Audio-TTS 系列通常支持数千字符。  
- **输出控制**：  
  - 结构化输出：通过 `response_format={"type": "json_object"}` 或系统提示词启用，适用于文本与视觉模型；  
  - 贴图质量：Tripo 模型通过 `parameters.texture_quality`（`standard`/`detailed`）控制；  
  - 音频格式：Fun-Music 通过 `format` 参数指定 `mp3`（体积小）或 `wav`（无损）；  
  - 分辨率与时长：图像生成模型（如 `qwen-image-3.0-pro`）最大输出 2048×2048；视频生成（如 `happyhorse-1.1-t2v`）最长 15 秒、1080P。  
- **能力开关**：  
  - 思考模式：通过 `enable_thinking: true`（Responses API）或 `reasoning.effort` 控制，仅 Qwen3 及以上模型支持；  
  - 联网搜索：仅 `qwen3.5-omni-*` 系列在 HTTP/WebSocket 模式下支持，且与 Function Calling 互斥；  
  - 说话人分离：仅 `qwen-audio-3.0-asr-flash-filetrans` 和 `fun-asr` 系列非实时模型支持。

## 使用方式

- **API 接入**：所有模型均通过统一的 DashScope API 调用，需配置 `DASHSCOPE_API_KEY` 环境变量及正确的 `WorkspaceId`。  
- **协议选择**：  
  - 实时交互（语音助手、直播翻译）：优先使用 WebSocket（低延迟、流式）；  
  - 批量/离线处理（文档摘要、视频分析）：使用 HTTP（支持异步、更高精度）；  
  - 3D 生成：必须使用异步 API（`X-DashScope-Async: enable`），轮询 `task_id` 获取结果。  
- **输入构造**：  
  - 多模态输入（如图文混合）需在 `input` 中按字段组织：`text`、`image`、`images`、`video`、`audio` 互斥或组合，具体依模型文档要求；  
  - Tripo 3D 生成严格区分 `prompt`（文生3D）、`image`（单图生3D）、`images`（多图生3D），三者不可共存；  
  - Fun-Music 要求 `prompt` 与 `lyrics` 至少传入其一，若同时传入则 `lyrics` 优先生效。  
- **SDK 支持**：DashScope SDK（Python/Java）覆盖绝大多数模型；Android/iOS SDK 主要支持 Qwen-Audio-TTS、Qwen-Audio-ASR 及 CosyVoice 系列；Tripo 和 Fun-Music 需直接调用 REST API。

## 限制和注意事项

- **地域限制**：Tripo 3D 生成与 Fun-Music 仅支持华北2（北京）地域，其他模型需按文档说明确认可用区域（如部分视觉模型在新加坡、美国等地域亦可用）。  
- **[异步任务](../concepts/async-task.md)时效性**：Tripo 3D 生成的 `task_id` 查询有效期为 24 小时；Fun-Music 生成结果 URL 有效期未明确说明，建议及时下载。  
- **能力互斥**：Qwen3.5-Omni 的联网搜索与 Function Calling 不可同时启用；思考模式启用时，S2S 模型不支持语音输出。  
- **旧版模型弃用**：文档 1 明确标注 `Qwen3.6` 及更早版本（如 `Qwen3`、`Qwen3-Coder`、`Qwen3-VL`）为“不再作为首选推荐”，新项目应避免选用；同理，文档 10 标注 `qwen-omni-turbo` 等旧版全模态模型已停止更新。  
- **计费差异**：Qwen3-TTS 系列中，`qwen3-tts-flash` 等旧版按 Token 计费，而 `qwen-audio-3.0-tts-*` 系列按请求+时长计费，选型时需注意成本模型差异。  
- **语言支持边界**：虽多数模型宣称支持“多语种及方言”，但实际能力存在梯度——例如 `qwen3.5-livetranslate-flash` 支持 60 种语言，但其中 31 种仅输出文本（无语音）；`qwen3-omni-flash` 仅支持 11 种输出语言，选型时务必核对目标语言是否在“支持”而非“仅文本”列表中。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


