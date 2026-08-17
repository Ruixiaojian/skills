# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览与选型指南，覆盖文本、视觉、音频、视频、3D、向量与重排序等全模态场景。本文档聚焦核心能力矩阵、关键参数配置、标准化调用方式及实际部署约束，帮助开发者快速匹配业务需求与模型能力，避免因版本混淆或能力误判导致的集成问题。所有推荐均基于当前（2026年中）稳定可用的模型快照版本。

## 支持的模型与功能

百炼平台提供覆盖多模态的模型体系，按能力层级与场景适配性组织如下：

- **文本生成**：以 `qwen3.7-plus` 为平衡首选，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器）及结构化 JSON 输出；`qwen3.8-max` 适用于复杂推理任务；`qwen3.7-flash` 在效果接近旗舰的前提下显著降低成本 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 同样为视觉任务首选，支持图像（最高 1600 万像素）、视频（最长 2 小时）、OCR 及结构化输出；专用 OCR 模型 `qwen3.5-ocr` 适用于文档/手写体高精度提取 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片生成与编辑**：`qwen-image-3.0-pro` 支持复杂版面、小字渲染与多语言字体；`wan2.7-image-pro` 提供品牌色控制与角色一致性多图生成；`z-image-turbo` 适用于低成本、高吞吐的写实人像生成 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **视频生成与编辑**：`happyhorse-1.1-t2v` 和 `wan2.7-i2v-2026-04-25` 分别为文生视频与首尾帧生视频的推荐模型，支持 1080P 分辨率与 15 秒时长；`wan2.7-videoedit` 支持特效与运镜复刻 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。  
- **3D 生成**：`Tripo/Tripo-P1.0`（快速预览）与 `Tripo/Tripo-H3.1`（影视级精度）支持文生3D、单图生3D及多图生3D，仅限华北2（北京）地域使用 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音相关**：`qwen-audio-3.0-asr-flash-streaming`（实时 ASR）、`qwen-audio-3.0-tts-plus`（TTS+声音复刻）、`qwen-audio-3.0-realtime-plus`（S2S 对话）构成端到端语音链路；`fun-music-v1` 支持歌词/提示词驱动的歌曲生成（邀测中，仅北京地域） [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **向量与重排序**：`text-embedding-v4`（文本）、`qwen3-vl-embedding`（多模态融合）、`qwen3-rerank`（纯文本重排序）是 RAG 系统的核心组件 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。  
- **全模态**：`qwen3.5-omni-plus` 是能力最全的旗舰模型，支持文本/音频/图片/视频输入，具备 Function Calling、联网搜索与思考模式；`qwen3-omni-flash` 为轻量替代方案，支持思考模式但不支持联网搜索 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。

> **注意**：文档 1 与文档 2 均将 `qwen3.7-plus` 列为视觉理解首选，但文档 2 表格中明确其最大视频数为 64，而文档 1 未提及该限制；文档 11 中 `qwen3.5-omni-plus` 的“联网搜索”与“Function Calling”被标注为“不可同时开启”，而文档 8 明确指出 Qwen3.5-Omni 系列支持二者共存——此矛盾需以文档 11 的官方说明为准，即二者互斥。

## 关键参数

各模型通过标准化参数控制行为，核心参数如下：

- **上下文长度**：文本模型普遍支持 1M [Token](../concepts/token.md)（约 70 万汉字），`qwen-long` 达 10M；视觉模型 `qwen3.7-plus` 同样支持 1M 文本上下文 + 视频输入；向量模型 `text-embedding-v4` 支持 8,192 [Token](../concepts/token.md) 输入。  
- **思考模式**：通过 `enable_thinking`（Responses API）或 `reasoning.effort` 控制，所有 Qwen3 及以上通用模型均支持，但全模态模型中仅 `qwen3-omni-flash`（HTTP）支持，`qwen3.5-omni-plus` 不支持 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **结构化输出**：通过系统提示词声明 JSON Schema 或启用 `response_format` 参数，`qwen3.7-plus`、`qwen3.5-ocr`、`qwen3.5-omni-plus` 等均支持。  
- **音视频控制**：ASR 模型通过 `hotword`（热词）和 `prompt`（上下文注入）提升专业术语识别精度；TTS 模型通过自然语言指令（如“用温柔语气，语速稍慢”）动态调节表达风格；S2S 模型 `qwen-audio-3.0-realtime-plus` 支持 Function Calling，但不支持联网搜索与思考模式。  
- **3D 生成参数**：`parameters.texture_quality`（`standard`/`detailed`）控制贴图质量；`parameters.geometry_quality`（`standard`/`ultra`）仅 `Tripo-H3.1` 支持，控制几何面数（最高 200 万）。

## 使用方式

所有模型均通过统一 API 接口调用，遵循以下通用范式：

- **请求格式**：HTTP POST 或 WebSocket，`Authorization: Bearer $DASHSCOPE_API_KEY`，`Content-Type: application/json`。  
- **模型标识**：在 `model` 字段指定模型 ID，如 `"model": "qwen3.7-plus"` 或 `"model": "Tripo/Tripo-P1.0"`。  
- **输入结构**：  
  - 文本/视觉/全模态：`input.prompt`（文本）、`input.image`（单图 URL）、`input.images`（多图 URL 数组）、`input.video`（视频 URL）；  
  - 音频：ASR/TTS/S2S 模型使用 `input.audio_url` 或流式二进制传输；  
  - 3D：`input.prompt`（文生3D）、`input.image`（单图生3D）、`input.images`（多图生3D）；  
  - 音乐：`input.prompt`（风格描述）或 `input.lyrics`（自定义歌词）。  
- **[异步任务](../concepts/asynchronous-task.md)**：3D 生成、批量视频处理等耗时操作需先调用 `/3d-generation` 创建任务获取 `task_id`，再轮询 `/tasks/{task_id}` 获取结果，有效期 24 小时 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **SDK 支持**：DashScope SDK（Python/Java）覆盖绝大多数模型；Android/iOS SDK 适用于 ASR/TTS 实时场景；AOQ 协议可选用于低延迟语音交互。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型、Fun-Music、Qwen-Audio Realtime 等部分模型**仅限华北2（北京）地域**使用，跨地域调用将失败。  
- **输入约束**：  
  - 视觉模型单图最高 1600 万像素，[Token](../concepts/token.md) 消耗公式为 `h × w / (32 × 32) + 2`；  
  - ASR 文件转写最大 12 小时/2GB（`qwen-audio-3.0-asr-flash-filetrans`），实时流无时长限制；  
  - 视频生成最大 15 秒/1080P，3D 多图输入限 2–4 张；  
  - TTS 输入文本长度受模型限制，`qwen3-tts-flash` 系列建议单次 ≤ 500 字符。  
- **能力互斥**：  
  - Qwen3.5-Omni 的联网搜索与 Function Calling **不可同时启用**；  
  - 思考模式启用时，S2S 模型无法生成语音输出；  
  - `qwen-long` 不支持 Function Calling、内置工具及思考模式。  
- **版本稳定性**：推荐使用带日期后缀的快照版本（如 `qwen3.7-plus-2026-05-26`）而非 `latest`，避免因模型自动升级导致行为变更；旧版模型（如 `qwen3.5-max-preview`）已停止更新，新项目应避免选用 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **计费与配额**：所有模型按 Token/请求/时长计费，具体费率以控制台为准；API Key 需绑定业务空间（WorkspaceId），且不同地域需独立申请。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)


