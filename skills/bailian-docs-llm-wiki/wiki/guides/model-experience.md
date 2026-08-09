# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览与选型指南，涵盖文本、视觉、语音、音视频、3D、音乐等全模态模型的适用场景、核心参数、调用方式及关键限制。本文档聚焦实际工程落地，不包含营销性描述，所有推荐均基于当前（2026年中）稳定可用的模型版本与API行为。

## 支持的模型与功能

百炼提供覆盖[多模态](../concepts/multimodal.md)的模型矩阵，按能力层级与使用场景划分：

- **文本生成**：以 `qwen3.7-plus` 为平衡首选，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化输出与思考模式；`qwen3.8-max` 适用于复杂推理任务；`qwen-long` 专用于超长文档（10M [Token](../concepts/token.md)）处理 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 同时支持图像、视频（最长2小时）、OCR及结构化输出；`qwen3.5-ocr` 为专用OCR优化模型 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片生成与编辑**：`qwen-image-3.0-pro` 支持高保真文生图与复杂版面编辑；`wan2.7-image-pro` 提供品牌色控制与4096×4096分辨率；`z-image-turbo` 适用于低成本快速生成 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **视频生成与编辑**：`happyhorse-1.1-t2v` 和 `wan2.7-t2v-2026-06-12` 支持带音频的1080P文生视频；`wan2.7-i2v-2026-04-25` 支持首尾帧续写；`happyhorse-1.0-video-edit` 提供基础视频编辑能力 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。  
- **3D生成**：`Tripo/Tripo-P1.0`（快速预览，2万面）与 `Tripo/Tripo-H3.1`（高精度，200万面）均支持文生3D、单图生3D、多图生3D三种模式，仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音与音频**：`qwen-audio-3.0-tts-plus` 支持声音复刻与指令控制；`fun-music-v1` 支持歌词/提示词驱动的歌曲生成；`qwen-audio-3.0-asr-flash-streaming` 为实时ASR首选；`qwen3.5-livetranslate-flash-realtime` 覆盖60种语言实时翻译 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。  
- **向量与重排序**：`text-embedding-v4`（文本嵌入，维度可配）、`qwen3-vl-embedding`（图文融合）、`qwen3-rerank`（纯文本重排序）构成RAG检索链核心组件 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。  
- **全模态**：`qwen3.5-omni-plus` 是旗舰级[多模态](../concepts/multimodal.md)模型，支持文本/音频/图片/视频输入，具备Function Calling、联网搜索与深度推理能力；`qwen3-omni-flash` 为轻量HTTP版，支持思考模式但不支持联网搜索 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。

> **注意**：文档 1 与文档 2 均将 `qwen3.7-plus` 列为视觉理解推荐模型，但文档 2 表格中明确其“内置工具”支持状态为“支持”，而文档 1 表格中对应项为“支持”——二者一致；但文档 1 中 `deepseek-v4-pro` 的“内置工具”列为“不支持”，而文档 2 未列出该模型在视觉场景下的内置工具支持情况，故以文档 1 为准。  
> **注意**：文档 8（S2S）称 `qwen3.5-omni-flash` 支持“联网搜索”，而文档 11（全模态）表格中同模型在“联网搜索”列标注为“支持”，但文档 8 的文字说明又指出“Qwen3-Omni-Flash 和 Livetranslate 模型不支持此功能”——此处存在矛盾。经查证，文档 11 的表格数据更准确，且与文档 8 中“Qwen3.5-Omni（HTTP 和 WebSocket），包括 Plus 和 Flash 系列”表述一致，故以文档 11 为准，即 `qwen3.5-omni-flash` 支持联网搜索。

## 关键参数

各模型系列的关键可配置参数如下：

- **上下文长度**：文本模型普遍支持 128K–1M [Token](../concepts/token.md)；`qwen-long` 达 10M；视觉模型如 `qwen3.7-plus` 支持 1M 文本上下文 + 最长2小时视频；3D模型无传统上下文概念，但受面数（`geometry_quality`）和贴图质量（`texture_quality`）控制。  
- **输入规格**：  
  - 图像：多数视觉模型支持单图最高1600万像素，[Token](../concepts/token.md)消耗公式为 `h × w / (32 × 32) + 2`；  
  - 视频：`qwen3.7-plus` 等支持最长2小时/2GB；  
  - 音频：ASR模型如 `qwen-audio-3.0-asr-flash-filetrans` 支持最长12小时/2GB；TTS模型对输入文本长度无硬性上限，但需考虑响应延迟；  
  - 3D：单图生3D要求图片为 JPEG/PNG，宽高20–6000像素，≤20MB；多图生3D需2–4张图片。  
- **输出控制**：  
  - 结构化输出：通过 `response_format={"type": "json_object"}` 或系统提示词启用，`qwen3.7-plus` 等主流模型均支持；  
  - 思考模式：文本模型通过 `reasoning.effort`（Responses API）或 `enable_thinking` 参数开启；全模态模型中仅 `qwen3-omni-flash`（HTTP）支持思考模式，且开启后不生成语音；  
  - 音频格式：TTS与音乐模型通过 `format` 参数指定 `mp3`（小体积）或 `wav`（无损）；  
  - 3D贴图：通过 `parameters.texture_quality`（`standard`/`detailed`）或禁用 `texture`+`pbr` 控制。

## 使用方式

所有模型均通过统一的 DashScope API 调用，核心流程一致：

1. **开通服务**：在[模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)开通目标模型（部分如 `fun-music-v1`、`Tripo` 需邀测）；  
2. **获取凭证**：创建并配置 `DASHSCOPE_API_KEY`（环境变量或请求头）；  
3. **构造请求**：  
   - **同步调用（HTTP）**：适用于非实时场景（如文件转写、批量生成）。示例（文本生成）：  
     ```bash
     curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation' \
       -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
       -H "Content-Type: application/json" \
       -d '{
         "model": "qwen3.7-plus",
         "input": {"messages": [{"role":"user","content":"你好"}]},
         "parameters": {"temperature": 0.8}
       }'
     ```  
   - **异步调用（HTTP + 轮询）**：适用于耗时较长任务（如3D生成）。先调用 `/3d-generation` 获取 `task_id`，再轮询 `/tasks/{task_id}` 查询状态 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)；  
   - **流式调用（WebSocket）**：适用于实时交互（如语音助手、实时字幕）。需建立长连接，发送音频/文本流，接收逐token或逐chunk响应；  
4. **解析响应**：关注 `output` 字段（文本/URL/二进制流），注意异步任务返回的 `task_status`（`SUCCEEDED`/`FAILED`）及结果有效期（如3D模型URL通常2小时过期）。

## 限制和注意事项

- **地域限制**：`Tripo` 模型与 `fun-music-v1` 仅支持华北2（北京）地域；部分模型（如 `wanx2.1-imageedit`）明确标注“仅支持北京地域”；  
- **协议与接入方式**：  
  - WebSocket 模型（如 `qwen-audio-3.0-realtime-plus`）不支持 HTTP 调用；  
  - Qwen-Audio-TTS/CosyVoice 系列模型同时支持 WebSocket 和 HTTP；Qwen-TTS 系列则通过 `-realtime` 后缀区分协议 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)；  
- **能力互斥**：  
  - 联网搜索与 Function Calling 在 `qwen3.5-omni` 系列中不可同时启用；  
  - 思考模式启用时，`qwen3-omni-flash` 不生成语音输出；  
- **版本稳定性**：文档中大量模型ID含日期快照（如 `qwen3.7-plus-2026-05-26`），生产环境建议优先使用无日期后缀的稳定别名（如 `qwen3.7-plus`），避免因快照失效导致中断；  
- **旧版模型弃用**：`qwen3`、`qwen3-coder`、`qwen-vl` 等旧系列模型已明确标注“不再作为首选推荐”，新项目应使用 `qwen3.5+` 或 `qwen3.6+` 系列；  
- **成本与性能权衡**：`qwen3.7-flash` 在效果接近 `qwen3.7-plus` 的前提下显著降低成本，是大多数通用场景的默认推荐起点。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)


