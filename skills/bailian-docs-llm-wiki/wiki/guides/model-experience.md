# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览，涵盖文本、视觉、音频、视频、3D、[多模态](../concepts/multimodal.md)及向量检索等全栈AI模型服务。它提供统一的API接入方式、标准化的参数体系和跨模态协同能力，支持从简单文本生成到复杂音视频理解与生成的多样化场景。所有模型均按能力档位（高能力/平衡/轻量）组织，并明确标注上下文窗口、功能支持与地域限制。

## 支持的模型/功能

百炼平台提供覆盖[多模态](../concepts/multimodal.md)的模型矩阵，按任务类型划分如下：

- **文本生成**：以 `qwen3.8-max`（最强推理）、`qwen3.7-plus`（能力与成本均衡）、`qwen3.7-flash`（低成本）为核心，全部支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器等）及结构化 JSON 输出；`qwen-long` 专用于超长文档（10M [Token](../concepts/token.md)）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 支持图像（最高1600万像素）、视频（最长2小时/2GB）输入，具备 Function Calling 与结构化输出能力；`qwen3.5-ocr` 专用于高精度文档/表格/手写体 OCR [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片生成与编辑**：`qwen-image-3.0-pro` 支持复杂版面、小字渲染与图中图；`wan2.7-image-pro` 支持品牌色控制与角色一致性多图生成；`z-image-turbo` 适用于快速低成本写实人像生成 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **视频生成与编辑**：`happyhorse-1.1-t2v`（文生视频）、`wan2.7-i2v-2026-04-25`（首尾帧生视频）、`happyhorse-1.0-video-edit`（指令式编辑）构成主力组合，均支持 1080P 有声视频输出 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。  
- **语音与音频**：  
  - 语音合成（TTS）：`qwen-audio-3.0-tts-plus` 同时支持声音复刻与声音设计；`cosyvoice-v3.5-plus` 支持 SSML 与 LaTeX 公式朗读 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。  
  - 语音转语音（S2S）：`qwen-audio-3.0-realtime-plus`（低延迟对话）、`qwen3.5-livetranslate-flash-realtime`（60语种实时翻译）为首选 [原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。  
  - 语音识别（ASR）：`qwen-audio-3.0-asr-flash-streaming`（实时流式）、`qwen-audio-3.0-asr-flash-filetrans`（支持说话人分离）覆盖主流需求 [原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **3D生成**：`Tripo/Tripo-P1.0`（快速预览，2万面）与 `Tripo/Tripo-H3.1`（影视级，200万面）支持文生3D、单图生3D、多图生3D三种模式，仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **音乐生成**：`fun-music-v1`（支持自定义歌词与性别）与 `fun-music-preview`（仅 [prompt](prompt.md) 输入）处于邀测阶段，仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **全模态**：`qwen3.5-omni-plus`（旗舰，支持音视频+图文+Function Calling+联网搜索）、`qwen3-omni-flash`（轻量，支持思考模式）、`qwen3.5-livetranslate-flash`（专业翻译）构成三支柱 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。  
- **向量与重排序**：`text-embedding-v4`（文本嵌入，默认1024维）、`qwen3-vl-embedding`（图文融合）、`qwen3-rerank`（纯文本重排序）支撑 RAG 与语义搜索 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 1 与文档 2 均将 `qwen3.7-plus` 列为视觉理解推荐模型，但文档 2 表格中其“内置工具”列为“支持”，而文档 1 明确说明“所有通用模型均支持 Function Calling”，且“内置工具（联网搜索、代码解释器等）”需单独确认支持状态——二者一致，无矛盾。  
> **注意**：文档 9（全模态）称 `qwen3.5-omni-plus` 支持“音频最长3小时、视频最长1小时”，而文档 2（视觉理解）称 `qwen3.7-plus` 支持“最长2小时视频”，此处存在不一致。根据模型命名逻辑（Qwen3.7 > Qwen3.5），应以文档 2 的 `qwen3.7-plus` 视频能力为准；文档 9 中的 `qwen3.5-omni-plus` 视频时长描述可能过时或指代 HTTP 模式下的文件上传限制，建议以模型广场实时参数为准。

## 关键参数

各模型通过标准化参数控制行为，核心参数如下：

- **通用控制**：  
  - `enable_thinking` 或 `reasoning.effort`：开启/调节深度思考模式（Qwen3及以上文本模型）；  
  - `response_format` / `output_schema`：声明结构化输出 JSON Schema；  
  - `tools`：定义 Function Calling 工具列表（JSON Schema 格式）。  

- **[多模态](../concepts/multimodal.md)输入**：  
  - 图像：`"image": "https://..."` 或 base64 编码；  
  - 视频：`"video": "https://..."`（需符合时长/大小限制）；  
  - 多图：`"images": [{"type": "png", "file_token": "..."}, ...]`（Tripo）；  
  - 音频：`"audio": "https://..."`（S2S/ASR/OMNI）。  

- **生成类模型特有**：  
  - 图片/视频：`parameters.texture_quality`（`standard`/`detailed`）、`parameters.geometry_quality`（`standard`/`ultra`）；  
  - 音乐：`input.prompt`、`input.lyrics`、`input.gender`（`female`/`male`）、`input.is_instrumental`（`true`/`false`）；  
  - TTS：`input.voice_id`（音色ID）、`input.text`、`input.style`（指令控制，如“温柔语速稍慢”）；  
  - ASR：`input.hotwords`（热词表）、`input.context_prompt`（领域上下文）。  

- **异步任务**：  
  - `X-DashScope-Async: enable` 头 + 轮询 `GET /api/v1/tasks/{task_id}`（Tripo、部分视频模型）。

## 使用方式

- **同步调用**：HTTP POST 到 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/...`（文本、TTS、ASR、Embedding 等）；WebSocket 连接用于实时流式交互（Realtime TTS、S2S、ASR Streaming）。  
- **异步调用**：适用于耗时较长任务（3D生成、视频生成），先发请求获取 `task_id`，再轮询结果（间隔 ≥15 秒）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **地域与权限**：  
  - Tripo、Fun-Music 仅限华北2（北京）；  
  - 所有模型需开通对应服务并配置有效 `DASHSCOPE_API_KEY`；  
  - 部分模型（如 `qwen3.5-livetranslate-flash-realtime`）需在模型广场手动开通。  
- **SDK 支持**：DashScope Python/Java SDK 支持绝大多数模型；Android/iOS SDK 主要覆盖 Qwen-Audio-TTS、Qwen-Audio-ASR 及 Fun-ASR。

## 限制和注意事项

- **地域限制**：Tripo 3D、Fun-Music、Qwen-Audio Realtime 系列强制要求华北2（北京）地域；其他模型在新加坡、美国、法兰克福等区域可用，但功能与版本可能不同。  
- **输入约束**：  
  - 图像：单图 ≤1600万像素（视觉模型），Tripo 单图宽高 20~6000px；  
  - 视频：`qwen3.7-plus` 最长2小时/2GB，`qwen3.5-omni-plus` 最长1小时（文档冲突见上）；  
  - 音频：ASR 文件最大 12 小时/2GB（`qwen-audio-3.0-asr-flash-filetrans`），TTS 输入文本长度依模型而定。  
- **功能兼容性**：  
  - Function Calling 与联网搜索不可同时启用（Qwen3.5-Omni）；  
  - 思考模式下不支持语音输出（S2S）；  
  - `qwen-long` 不支持 Function Calling、内置工具或思考模式；  
  - `qwen3-vl-rerank` 仅支持多模态重排序，纯文本请用 `qwen3-rerank` 或 `gte-rerank-v2`。  
- **版本管理**：快照版本（如 `qwen3.7-plus-2026-05-26`）用于稳定性保障，但非最新能力；推荐优先使用无日期后缀的模型 ID，其自动指向最新稳定快照。  
- **计费差异**：Qwen3-TTS 系列（如 `qwen3-tts-flash`）按 [Token](../concepts/token.md) 计费，而 Qwen-Audio-TTS/CosyVoice 系列按请求/时长计费，选型时需注意成本模型。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


