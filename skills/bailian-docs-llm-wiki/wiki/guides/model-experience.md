# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览，涵盖文本、视觉、音视频、3D、向量等全模态模型的选型指南、核心参数与使用规范。本文档聚焦实际工程落地，不包含营销性描述，所有推荐均基于当前（2026年中）稳定可用的模型版本与接口行为。

## 支持的模型与功能

百炼提供覆盖多模态的模型矩阵，按能力层级与场景划分：

- **文本生成**：以 `qwen3.7-plus` 为平衡首选，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器）及结构化 JSON 输出；`qwen3.8-max` 适用于复杂推理任务；`qwen-long` 专用于超长文档（10M [Token](../concepts/token.md)）处理 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 同时支持图像、视频（最长2小时）、OCR及结构化输出；`qwen3.5-ocr` 为专用OCR优化模型 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片/视频生成与编辑**：`qwen-image-3.0-pro` 支持高保真文生图与复杂版面编辑；`happyhorse-1.1-i2v` 和 `wan2.7-i2v-2026-04-25` 分别适用于首帧与首尾帧视频生成；`z-image-turbo` 为低成本快速生成选项 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **3D生成**：Tripo 系列仅限华北2（北京）地域，`Tripo/Tripo-P1.0` 适合快速预览（2万面），`Tripo/Tripo-H3.1` 适用于影视级资产（200万面），需异步轮询获取结果 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音与音频**：`qwen-audio-3.0-asr-flash-streaming`（实时ASR）、`qwen-audio-3.0-tts-plus`（TTS+声音复刻）、`fun-music-v1`（歌词/提示词生成歌曲）均需 API Key 并配置 WorkspaceId；`fun-music` 当前处于邀测阶段，仅限北京地域 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **全模态与翻译**：`qwen3.5-omni-plus` 支持文本/音频/图片/视频输入与文本/语音输出，具备 Function Calling 和联网搜索能力；`qwen3.5-livetranslate-flash-realtime` 支持60种语言实时语音翻译（29种含语音输出） [原文标题](../../raw/model-user-guide/model-experience/omni.md)。  
- **向量与重排序**：`text-embedding-v4` 为文本Embedding默认推荐，支持64–2048维可调；`qwen3-rerank` 用于RAG后重排序（最多500文档）；`qwen3-vl-rerank` 支持图文视频混合排序 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 1 中将 `qwen3.7-plus` 列为“办公场景推荐”，而文档 2 中明确其支持视频输入（最长2小时）；但文档 10 的“全模态”章节未将 `qwen3.7-plus` 归入 Omni 系列，且其模型ID未出现在文档 10 的推荐表中。实际能力以模型广场最新快照为准，建议优先参考 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md) 中的视觉能力说明。

## 关键参数

各模型共性关键参数如下（具体值依模型而异）：

- **上下文窗口**：文本模型主流为 1M [Token](../concepts/token.md)（如 `qwen3.7-plus`），视觉模型同；`qwen-long` 达 10M；`qwen3.5-ocr` 仅 32k。  
- **输入限制**：  
  - 图像：单图最高 1600 万像素，[Token](../concepts/token.md) 数 ≈ `h × w / (32 × 32) + 2`；  
  - 视频：`qwen3.7-plus` 支持最长 2 小时 / 2GB；  
  - 音频：ASR 模型 `qwen-audio-3.0-asr-flash-filetrans` 支持 12 小时 / 2GB；  
  - 3D：Tripo 输入图片宽高 20–6000 像素，单次请求最多 4 张。  
- **输出控制**：  
  - `enable_thinking` 或 `reasoning.effort` 控制思考模式（Qwen3+ 系列）；  
  - `format=mp3/wav` 指定音乐输出格式；  
  - `parameters.texture_quality=standard/detailed` 控制 Tripo 贴图质量；  
  - `is_instrumental=true` 生成纯音乐（`fun-music`）。  

## 使用方式

- **API 调用统一路径**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/{service}/{endpoint}`，其中 `region` 如 `cn-beijing`，`service` 如 `audio/music/generation`。  
- **认证**：通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 传递密钥，API Key 必须在对应地域开通（如 Tripo 仅限北京）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **协议选择**：  
  - 实时交互（语音助手、直播翻译）→ WebSocket；  
  - 批量/离线处理（视频分析、文件转写）→ HTTP；  
  - 异步任务（3D生成）→ 先 POST 创建任务，再 GET 轮询 `task_id` 状态。  
- **SDK 支持**：DashScope SDK（Python/Java）覆盖 Qwen-Audio、Fun-ASR、Qwen-ASR 等主流模型；移动端需确认 CosyVoice 是否启用 AOQ 协议 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型、`fun-music`、部分 TTS/ASR 模型（如 `qwen-audio-3.0-tts-plus`）仅在华北2（北京）可用，跨地域调用将失败。  
- **模型兼容性**：旧版模型（如 `qwen3`、`qwen2.5-omni-7b`）已停止更新，新项目应使用 Qwen3.5+ 系列；文档 1 中列出的 `qwen3-coder-plus` 等 coder 专用模型未在其他文档中被交叉验证，建议优先选用通用旗舰模型。  
- **功能互斥性**：  
  - `qwen3.5-omni-flash` 在 WebSocket 模式下不支持联网搜索，HTTP 模式下不支持思考模式；  
  - `qwen-audio-3.0-realtime-plus` 支持 Function Calling，但不支持联网搜索与思考模式；  
  - Tripo 模型必须启用 `X-DashScope-Async: enable` 头部，否则返回错误。  
- **成本与性能权衡**：`qwen3.7-flash` 在效果接近 `qwen3.7-plus` 的前提下降低成本，但 `qwen3.7-flash` 的最大图片数为 256（`qwen3.7-plus` 为 2048），需根据输入规模选型 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


