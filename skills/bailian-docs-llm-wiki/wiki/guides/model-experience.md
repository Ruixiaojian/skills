# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览与选型指南，覆盖文本、视觉、语音、音乐、3D、视频、图像、向量与重排序等全模态场景。本文档聚焦于模型能力边界、关键参数、调用方式及实践约束，帮助开发者快速匹配业务需求与最优模型，避免试错成本。所有推荐均基于当前（2026年中）稳定可用的模型版本。

## 支持的模型与功能

百炼平台提供覆盖多模态的模型矩阵，按核心能力分类如下：

- **文本生成**：支持长上下文（最高1000万[Token](../concepts/token.md)）、Function Calling、内置工具（联网搜索、代码解释器等）、结构化JSON输出及深度思考模式。主力模型为 `qwen3.7-plus`（平衡型）、`qwen3.7-max`（高推理）和 `qwen-long`（超长文档）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：支持图像、视频（最长2小时）、OCR及多模态结构化输出。`qwen3.7-plus` 为通用首选，`qwen3.5-ocr` 专用于文档/手写识别 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **3D生成**：Tripo 系列（`Tripo/Tripo-P1.0`、`Tripo/Tripo-H3.1`）支持文生3D、单图/多图生3D，仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音与音频**：  
  - 语音识别（ASR）：`qwen-audio-3.0-asr-flash-streaming`（实时）、`qwen-audio-3.0-asr-flash-filetrans`（文件转写，支持说话人分离）；  
  - 语音合成（TTS）：`qwen-audio-3.0-tts-plus`（标准+复刻）、`cosyvoice-v3.5-plus`（设计+复刻）；  
  - 语音转语音（S2S）：`qwen-audio-3.0-realtime-plus`（低延迟对话）、`qwen3.5-omni-flash`（多模态分析+翻译）。  
- **音乐生成**：Fun-Music（`fun-music-v1`）支持提示词/歌词驱动的歌曲生成，目前处于邀测阶段，仅限华北2（北京）[原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **向量与重排序**：`text-embedding-v4`（文本检索）、`qwen3-vl-embedding`（图文融合）、`qwen3-rerank`（RAG后处理）[原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。  
- **视频与图像**：  
  - 视频生成：`happyhorse-1.1-t2v`（文生视频）、`wan2.7-i2v-2026-04-25`（首尾帧续写）；  
  - 图像生成：`wan2.7-image-pro`（全能型）、`z-image-turbo`（高速低成本）；  
  - 编辑能力：`wan2.7-image-pro` 支持多图参考编辑，`qwen-image-3.0-pro`（邀测）支持负向提示词。

> **注意**：文档 2（视觉理解）中称 `qwen3.7-plus` 支持“最长2小时视频”，而文档 1（文本生成）未提及视频能力。实际以文档 2 的定义为准——视频理解是 `qwen3.7-plus` 的明确能力，但其在纯文本场景下不启用视频解析模块。

## 关键参数

不同模型类型的关键参数差异显著，需按场景显式配置：

| 类别         | 参数名                     | 说明                                                                 | 示例值/范围                                                                 |
|--------------|----------------------------|----------------------------------------------------------------------|----------------------------------------------------------------------------|
| **通用**     | `model`                    | 模型ID，必须精确匹配                                                 | `"qwen3.7-plus"`, `"Tripo/Tripo-P1.0"`                                     |
| **文本/视觉**| `enable_thinking` / `reasoning.effort` | 控制深度思考模式开关与强度（仅Qwen3+系列）                          | `true`, `"high"`                                                           |
| **视觉**     | `max_pixels_per_image`     | 单图最大像素数（影响[Token](../concepts/token.md)消耗）                                      | 计算公式：`h × w / (32 × 32) + 2`                                          |
| **3D**       | `parameters.texture_quality` | 贴图质量（`standard`/`detailed`），`parameters.geometry_quality`（`standard`/`ultra`，仅H3.1） | `"detailed"`, `"ultra"`                                                    |
| **语音**     | `format`                   | 音频输出格式（`mp3`/`wav`）                                          | `"wav"`（高质量后期处理）                                                  |
| **音乐**     | `input.gender`             | 声音性别（仅 `fun-music-v1` 支持）                                   | `"female"`                                                                 |
| **向量**     | `dimension`                | Embedding维度（`text-embedding-v4` 可选64–2048）                     | `1024`（默认）                                                             |
| **重排序**   | `top_n`                    | 待重排序的文档数量（`qwen3-rerank` 最多500条）                       | `100`                                                                      |

## 使用方式

所有模型均通过统一 API 接入，但协议与流程因场景而异：

- **同步请求（HTTP）**：适用于非实时任务（如批量文本生成、图片生成、文件转写）。发送完整输入，接收完整响应。  
- **流式请求（WebSocket）**：适用于[实时交互](../concepts/realtime-interaction.md)（如语音助手、实时字幕、S2S对话）。建立长连接，音频/文本分块输入，结果分块返回。  
- **异步任务（Async）**：适用于耗时操作（如3D生成、长视频处理）。先提交任务获取 `task_id`，再轮询或配置回调获取结果 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **多模态输入**：视觉/全模态模型需将图片URL、视频URL、音频URL嵌入 `input` 字段（如 `{"image": "https://..."}`），不可上传二进制文件。  
- **地域限制**：Tripo 3D 和 Fun-Music 仅支持华北2（北京）地域，API Endpoint 必须使用 `cn-beijing.maas.aliyuncs.com`。

## 限制和注意事项

- **地域与权限**：Tripo 和 Fun-Music 模型需单独申请开通，且仅限华北2（北京）地域；其他模型在各Region普遍可用，但部分旧版模型（如 `qwen2.5-omni-7b`）已停止更新 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。  
- **输入约束**：  
  - 视频：`qwen3.7-plus` 支持最长2小时/2GB，但单次请求最多64个视频；  
  - 图片：视觉模型单图最高1600万像素，超限将触发[Token](../concepts/token.md)超额计费；  
  - 音频：ASR `qwen-audio-3.0-asr-flash-filetrans` 支持最大12小时/2GB，`qwen-audio-3.0-asr-flash` 仅5分钟/2GB。  
- **功能互斥**：  
  - S2S模型中，`qwen3.5-omni-flash` 同时支持 Function Calling 和联网搜索，但二者不可共存；  
  - 思考模式开启时，`qwen3-omni-flash` 不支持语音输出（仅文本）；  
  - `fun-music-v1` 的 `is_instrumental=true` 会忽略 `lyrics` 和 `gender` 参数。  
- **版本兼容性**：快照版本（如 `qwen3.7-plus-2026-05-26`）保证稳定性，但新特性仅在最新版（如 `qwen3.7-plus`）发布；迁移时需验证参数兼容性。  
- **成本提示**：`qwen3.8-max-preview` 仅 Token Plan 用户可用；`qwen-long`（1000万Token）虽上下文极大，但推理成本显著高于 `qwen3.7-plus`（100万Token）。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)


