# model experience

`model experience` 是百炼平台面向开发者提供的模型选型与使用指南集合，覆盖文本、视觉、语音、音乐、向量、重排序及全模态等核心能力。本文档聚焦模型能力边界、关键参数与工程实践要点，不包含营销性描述，所有推荐均基于当前（2026年中）稳定可用的模型版本与API行为。

## 支持的模型/功能

百炼提供覆盖多模态的模型矩阵，按任务类型划分如下：

- **文本生成**：以 `qwen3.7-plus` 为默认推荐，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化 JSON 输出及逐步推理（`enable_thinking`）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。`qwen3.7-max` 和 `qwen3.8-max-preview`（Token Plan 专属）适用于高推理强度场景；`qwen-long`（10M 上下文）专用于超长文档处理。
  
- **视觉理解**：`qwen3.7-plus` 同时支持图像、视频（最长 2 小时）、OCR 及结构化输出，是通用视觉任务首选；`qwen3.5-ocr` 为文档/表格/手写体文字提取专项优化 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。

- **图片生成与编辑**：`wan2.7-image-pro` 支持文生图（4096×4096）、多图参考编辑及角色一致性生成；`qwen-image-3.0-pro`（邀测）支持负向提示词与多语言字体渲染；`z-image-turbo` 适用于低成本、高吞吐的写实人像生成。

- **视频生成与编辑**：`happyhorse-1.1-t2v` 和 `wan2.7-t2v-2026-06-12` 支持文生视频（1080P，3–15 秒）；`wan2.7-i2v-2026-04-25` 支持首尾帧续写；`happyhorse-1.0-video-edit` 和 `wan2.7-videoedit` 分别覆盖基础与高级视频编辑能力。

- **3D 生成**：`Tripo/Tripo-P1.0`（快速预览）与 `Tripo/Tripo-H3.1`（影视级精度）支持文生3D、单图生3D、多图生3D三种模式，仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

- **语音识别（ASR）**：实时场景首选 `qwen-audio-3.0-asr-flash-streaming`（WebSocket，支持热词/Prompt上下文）；非实时文件转写首选 `qwen-audio-3.0-asr-flash-filetrans`（HTTP，支持说话人分离）。

- **语音合成（TTS）**：标准合成用 `qwen-audio-3.0-tts-plus`；声音复刻用 `qwen-audio-3.0-tts-flash` 或 `MiniMax/speech-2.8-hd`；声音设计用 `cosyvoice-v3.5-plus`；均支持指令控制（如“温柔语速稍慢”）。

- **音乐生成**：`fun-music-v1`（邀测）支持 [prompt](prompt.md)/lyrics 输入、性别选择及纯音乐模式；`fun-music-preview` 仅支持 [prompt](prompt.md)，不支持 gender 参数 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。

- **向量与重排序**：文本 Embedding 推荐 `text-embedding-v4`（维度可配）；多模态 Embedding 推荐 `qwen3-vl-embedding`（融合向量）或 `tongyi-embedding-vision-plus`（独立向量）；重排序推荐 `qwen3-rerank`（纯文本）或 `qwen3-vl-rerank`（多模态）。

- **语音转语音（S2S）**：实时对话用 `qwen-audio-3.0-realtime-plus`；同传用 `qwen3.5-livetranslate-flash-realtime`；音视频分析用 `qwen3.5-omni-flash`（HTTP，支持思考模式）。

- **全模态**：`qwen3.5-omni-plus` 是能力最全的旗舰模型，支持文本/音频/图片/视频输入，输出文本+语音，具备 Function Calling 与联网搜索能力；`qwen3-omni-flash` 成本更低，仅 HTTP 模式支持思考模式 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。

> **注意**：文档 1 中提及 `qwen3.8-max-preview` 仅 Token Plan 可用，而文档 2 未提及其视觉能力支持；实际调用前请以模型广场最新快照为准，避免依赖未公开的 preview 版本能力。

## 关键参数

各模型共性关键参数如下（具体值依模型而异）：

- **上下文长度**：文本模型最高 10M（`qwen-long`），视觉模型最高 1M，ASR/TTS 模型无固定上下文限制但受音频时长约束。
- **输入格式**：
  - 图像：单图最高 1600 万像素，Token 数 ≈ `h × w / (32 × 32) + 2`；
  - 视频：`qwen3.7-plus` 支持最长 2 小时 / 2GB；
  - 音频：ASR 实时流无时长限制，非实时文件最大 12 小时 / 2GB（`qwen-audio-3.0-asr-flash-filetrans`）；
  - 3D 输入：单图需 JPEG/PNG（20–6000 像素，≤20MB），多图需 2–4 张。
- **输出控制**：
  - 结构化输出：通过 `response_format={"type": "json_object"}` 或系统提示词启用（文本/视觉模型）；
  - 思考模式：文本/视觉模型通过 `enable_thinking=true` 或 `reasoning.effort` 控制；
  - 指令控制（TTS）：在 `input.text` 中嵌入自然语言指令，如 `"用激动的播报风格"`；
  - 纯音乐生成：`fun-music-v1` 设置 `"is_instrumental": true`。
- **性能权衡参数**：
  - Embedding 维度：`text-embedding-v4` 支持 64–2048 维，默认 1024；
  - TTS 音色：`cosyvoice-v3.5-plus` 支持声音复刻与声音设计双路径；
  - 3D 贴图质量：`parameters.texture_quality="standard"`（默认）或 `"detailed"`。

## 使用方式

- **API 调用**：所有模型均通过 DashScope REST API 或 WebSocket 接入。HTTP 模型使用 `POST /api/v1/services/{service}/{endpoint}`；WebSocket 模型需建立长连接（如 ASR/TTS/S2S 实时流）。务必配置 `Authorization: Bearer $DASHSCOPE_API_KEY` 及正确 `WorkspaceId`。
- **异步任务**：3D 生成、批量视频生成等耗时操作需先调用创建任务接口（含 `X-DashScope-Async: enable` header），再轮询 `GET /api/v1/tasks/{task_id}` 获取结果（有效期 24 小时）。
- **多模态输入**：视觉/全模态模型接受 `input` 中混合字段（如 `{"prompt": "...", "image": "url", "video": "url"}`），但同一请求中互斥字段（如 `prompt` 与 `lyrics`）需按文档约定优先级使用。
- **SDK 支持**：Python/Java SDK 全面支持 ASR/TTS/S2S 实时流；Android/iOS SDK 仅支持部分 ASR/TTS 模型；其余模型建议直接调用 HTTP/WebSocket。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型仅限华北2（北京）；Fun-Music 仅限华北2（北京）；部分模型（如 `qwen-omni-turbo`）已归档，新项目禁用 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。
- **能力冲突**：Qwen3.5-Omni 的联网搜索与 Function Calling 不可同时启用；思考模式下 S2S 模型不生成语音输出；`qwen3.7-max` 不支持结构化输出。
- **计费与配额**：Token Plan 用户方可访问 `qwen3.8-max-preview`；`qwen-long` 和 `Tripo-H3.1` 属高成本模型，需评估面数/时长对账单影响；`z-image-turbo` 价格约为 `wan2.7-image-pro` 的 1/5，但不支持编辑。
- **兼容性**：`text-embedding-v3` 与 v4 维度兼容，可用于索引迁移；旧版 `qwen2.5-omni-7b` 已停更，不建议新项目接入。
- **安全与合规**：所有模型默认禁止生成违法、色情、暴力内容；TTS 声音复刻需用户明确授权音频样本；Tripo 3D 输出 GLB 文件含 PBR 材质，有效期仅 2 小时，需及时下载。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)


