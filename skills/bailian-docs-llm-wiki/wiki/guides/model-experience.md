# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览，涵盖文本、视觉、音视频、3D、向量等全模态模型的选型指南、关键参数与使用约束。本文档聚焦实用信息，不包含营销话术，所有推荐均基于当前（2026年中）稳定可用的模型版本，并明确标注能力边界与兼容性要求。

## 支持的模型/功能

百炼平台提供覆盖多模态的模型能力矩阵，按任务类型划分如下：

- **文本生成**：支持[长上下文](../concepts/long-context.md)（最高1000万[Token](../concepts/token.md)）、Function Calling、内置工具（联网搜索/代码解释器）、结构化JSON输出及逐步推理（`enable_thinking`）。主力模型为 `qwen3.8-max`（最强推理）、`qwen3.7-plus`（平衡）、`qwen3.7-flash`（低成本），详见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。
- **视觉理解**：支持图像、视频（最长2小时）、OCR（专用 `qwen3.5-ocr`）及多模态结构化输出。`qwen3.7-plus` 和 `qwen3.8-max` 为通用首选，`qwen3.5-omni-plus` 适用于需音频输入的视频理解场景 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。
- **图片/视频生成与编辑**：`qwen-image-3.0-pro` 支持高保真文生图与复杂版面编辑；`happyhorse-1.1-t2v` 和 `wan2.7-i2v-2026-04-25` 分别覆盖文生视频与首尾帧续写；`Tripo/Tripo-P1.0` 提供文/图/多图生3D能力，仅限华北2（北京）地域 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **语音与音乐**：`qwen-audio-3.0-asr-flash-streaming`（实时ASR）、`qwen-audio-3.0-tts-plus`（TTS+声音复刻）、`fun-music-v1`（邀测中，仅北京地域）构成端到端语音链路 [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)、[语音合成](../../raw/model-user-guide/model-experience/tts-model.md)、[音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。
- **全模态与S2S**：`qwen3.5-omni-plus` 支持文本/音频/图片/视频联合理解与Function Calling；`qwen3.5-livetranslate-flash-realtime` 提供60语种实时语音翻译；`qwen-audio-3.0-realtime-plus` 实现低延迟语音对话 [全模态](../../raw/model-user-guide/model-experience/omni.md)、[语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。
- **向量与重排序**：`text-embedding-v4`（文本）、`qwen3-vl-embedding`（图文融合）、`qwen3-rerank`（纯文本重排）支撑RAG检索优化 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 1 中 `qwen-long` 的上下文窗口标为“10M”，而文档 2 中同模型未列此项，且其功能栏明确标注“不支持 Function Calling / 内置工具”。实际使用时应以模型广场实时参数为准，该模型仅适用于纯长文档摘要，不可用于工具调用场景。

## 关键参数

各模型核心参数需在调用时显式指定或隐含于模型ID中：

- **上下文长度**：文本模型如 `qwen3.7-plus` 为1M [Token](../concepts/token.md)（约70万汉字），`qwen-long` 为10M [Token](../concepts/token.md)；视觉模型统一支持1M上下文；视频模型最大处理2小时/2GB；Tripo 3D模型无Token概念，但受面数限制（`Tripo-P1.0` 最高2万面，`Tripo-H3.1` 最高200万面）。
- **输入格式约束**：
  - 图像：单图最高1600万像素，Token数 ≈ `h × w / (32 × 32) + 2`；
  - 视频：`qwen3.7-plus` 等支持最长2小时，但需≤2GB；
  - 音频：ASR模型 `qwen-audio-3.0-asr-flash-filetrans` 支持12小时/2GB，而 `qwen-audio-3.0-asr-flash` 仅限5分钟/2GB；
  - 3D生成：单图输入需JPEG/PNG格式、20–6000像素宽高、≤20MB；多图输入限2–4张。
- **输出控制**：
  - 结构化输出：通过 `response_format={"type": "json_object"}` 或系统提示词触发，`qwen3.7-plus` 及以上文本模型、Qwen3-VL系列均支持；
  - 思考模式：文本模型通过 `enable_thinking=true`（Responses API）或 `reasoning.effort` 控制，但 `qwen3.5-omni-flash` 等Omni模型在WebSocket模式下不支持思考模式（见文档 9 和 11）；
  - 音频格式：TTS模型通过 `format=mp3` 或 `wav` 指定，`fun-music-v1` 同样支持此参数。

## 使用方式

- **API接入**：所有模型均通过统一HTTP/WebSocket接口调用，URL格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/{service}/{endpoint}`。`{region}` 必须匹配模型部署地域（如Tripo仅支持 `cn-beijing`），`{service}` 如 `text-generation`、`audio/music/generation`。
- **异步任务**：3D生成（Tripo）、批量视频生成等耗时操作需先创建任务（返回 `task_id`），再轮询结果（建议间隔≥15秒），详见 [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。
- **协议选择**：
  - 实时交互（语音助手、直播字幕）：优先选用WebSocket（如 `qwen-audio-3.0-asr-flash-streaming`）；
  - 文件处理（会议录音转写、视频分析）：使用HTTP（如 `qwen-audio-3.0-asr-flash-filetrans`）；
  - S2S场景：`qwen-audio-3.0-realtime-plus` 仅支持WebSocket，而 `qwen3-livetranslate-flash` 仅支持HTTP。
- **SDK支持**：DashScope SDK（Python/Java）覆盖全部主流模型；Android/iOS SDK仅支持Qwen-Audio系列（ASR/TTS/S2S）及Fun系列（ASR/Music）。

## 限制和注意事项

- **地域限制**：`fun-music-v1`、`Tripo/Tripo-P1.0` 仅在华北2（北京）地域可用；部分旧版模型（如 `qwen-omni-turbo`）已停更，新项目必须使用 `qwen3.5-omni-plus` 或 `qwen3-omni-flash`。
- **功能互斥**：Omni模型中，联网搜索与Function Calling不可同时启用；思考模式启用时，S2S模型无法输出语音（文档 9 明确说明）。
- **成本与性能权衡**：
  - `qwen3.7-flash` 在效果接近 `qwen3.7-plus` 的前提下降低成本，但 `deepseek-v4-flash` 不支持内置工具，需自行集成；
  - `z-image-turbo` 生成速度快10倍、价格约1/5，但不支持图片编辑；
  - `qwen3-rerank` 支持最多500个文档重排，超限时需分批处理。
- **兼容性风险**：`text-embedding-v3` 与 `v4` 维度不兼容，迁移存量索引需重新向量化；`qwen3.5-ocr` 专为文档优化，通用场景应优先用 `qwen3.7-plus`。
- **安全与合规**：所有模型调用需配置有效API Key及业务空间ID；语音复刻需用户授权音频样本；生成内容需符合中国法律法规及平台内容安全策略。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)


