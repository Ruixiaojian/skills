# model experience

`model experience` 是百炼平台面向开发者提供的统一模型能力体验层，涵盖文本、视觉、音视频、3D、向量等全模态模型服务。所有模型均通过标准化 API（HTTP/WebSocket）接入，支持结构化输出、Function Calling、思考模式等通用能力，并按场景提供明确的选型路径与参数控制。开发者可基于具体任务需求（如生成、理解、编辑、检索）快速定位适配模型，无需关注底层部署细节。

## 支持的模型/功能

百炼平台提供覆盖生成、理解、编辑、检索四大范式的模型能力：

- **文本生成**：以 `qwen3.7-plus` 为旗舰，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化 JSON 输出及逐步推理（`enable_thinking`）。轻量替代方案 `qwen3.7-flash` 在效果接近的前提下显著降低成本 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 同时支持图像与视频输入（最长 2 小时），具备 OCR（`qwen3.5-ocr` 专用）、多图理解、结构化输出等能力 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片/视频生成与编辑**：`wan2.7-image-pro` 支持文生图（4096×4096）、多图参考编辑；`happyhorse-1.1-t2v` 和 `wan2.7-i2v-2026-04-25` 分别覆盖文生视频与首尾帧续写等专业场景 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **3D 生成**：Tripo 系列（`Tripo/Tripo-P1.0` / `Tripo/Tripo-H3.1`）支持文生3D、单图/多图生3D，需在华北2（北京）地域调用，且必须使用该地域 API Key [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音与音乐**：`fun-music-v1` 支持提示词或歌词驱动的歌曲生成（含男/女声选择）；`qwen-audio-3.0-asr-flash-streaming`（实时）与 `qwen-audio-3.0-asr-flash-filetrans`（非实时）构成 ASR 主力；TTS 推荐 `qwen-audio-3.0-tts-plus`（标准合成）与 `cosyvoice-v3.5-plus`（声音设计） [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。  
- **全模态与 S2S**：`qwen3.5-omni-plus` 支持文本/音频/图片/视频联合理解与输出，兼具 Function Calling 与联网搜索；`qwen-audio-3.0-realtime-plus` 实现端到端低延迟语音对话 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。  
- **向量与重排序**：`text-embedding-v4`（文本）、`qwen3-vl-embedding`（多模态）、`qwen3-rerank`（纯文本重排）构成 RAG 检索链核心组件 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

> **注意**：文档 1 与文档 2 均将 `qwen3.7-plus` 列为视觉理解首选，但文档 2 表格中 `qwen3.7-plus` 的“最大像素/图”为 16M，而文档 1 未提及该参数；文档 4 中 `happyhorse-1.1-t2v` 标注输出为“有声视频”，但文档 9 的 S2S 对比表中将其归类为“S2S 单模型”，而文档 4 明确其属于“文生视频”（T2V），二者模型类型归属存在不一致，应以模型实际能力（T2V vs S2S）为准。

## 关键参数

各模型通过标准化参数控制行为，关键参数如下：

- **通用控制**：`enable_thinking`（开启逐步推理）、`response_format`（指定 JSON Schema 结构化输出）、`tools`（声明 Function Calling 工具列表）。  
- **视觉相关**：图像 [Token](../concepts/token.md) 计算公式为 `h × w / (32 × 32) + 2`；视频最大时长/大小因模型而异（如 `qwen3.7-plus` 支持 2 小时/2GB）[原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **语音相关**：ASR 支持 `hotword`（热词）与 `prompt`（上下文注入）提升专业术语识别精度；TTS 支持自然语言指令控制语速/情绪（如“用温柔的语气，语速稍慢”）[原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **3D 相关**：`parameters.texture_quality` 控制贴图质量（`standard`/`detailed`）；`parameters.geometry_quality`（仅 `Tripo-H3.1`）控制面数（`standard`/`ultra`）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **Embedding**：`text-embedding-v4` 支持 64~2048 维可选（默认 1024），`qwen3-vl-embedding` 默认 2560 维，维度直接影响存储与检索性能 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

## 使用方式

所有模型均通过 RESTful API 调用，遵循统一请求结构：

```json
{
  "model": "qwen3.7-plus",
  "input": { /* 输入内容，如 prompt、image URL、audio URL 等 */ },
  "parameters": { /* 模型特有参数，如 texture_quality、format 等 */ }
}
```

- **协议选择**：实时交互（语音助手、直播翻译）优先选用 WebSocket；批量处理（文件转写、视频分析）使用 HTTP。Qwen-Audio-TTS/CosyVoice 系列模型同时支持两种协议，而 Qwen3-TTS 系列需通过 `-realtime` 后缀区分 [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。  
- **异步任务**：3D 生成、长视频处理等耗时操作需先创建任务获取 `task_id`，再轮询结果（建议间隔 ≥15 秒）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **地域限制**：Tripo 3D 模型与 Fun-Music 仅在华北2（北京）地域可用，调用时 endpoint 必须为 `cn-beijing.maas.aliyuncs.com` [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **认证方式**：统一使用 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需提前在控制台开通并配置至环境变量。

## 限制和注意事项

- **地域与权限**：Tripo（文档 5）、Fun-Music（文档 6）严格限定华北2（北京）地域；部分模型（如 `qwen3.8-max-preview`）需 [Token](../concepts/token.md) Plan 权限方可调用 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **输入约束**：ASR 文件模式最大支持 12 小时/2GB 音频；TTS 输入文本长度受模型限制（如 `qwen3-tts-flash` 单次 ≤ 1000 字符）；图片生成分辨率上限为 `wan2.7-image-pro` 的 4096×4096 [原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **能力边界**：`qwen3.7-max` 不支持结构化输出；`qwen-long`（10M 上下文）不支持 Function Calling 与内置工具；Qwen-Audio Realtime 不支持联网搜索与思考模式 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **版本管理**：推荐使用快照版本（如 `qwen3.7-plus-2026-05-26`）保障稳定性，避免 `latest` 标签导致行为突变；旧版模型（如 `qwen2.5-omni-7b`）已停止更新，新项目应避免选用 [原文标题](../../raw/model-user-guide/model-experience/omni.md)。  
- **成本提示**：`z-image-turbo` 生成速度比 `wan2.7-image-pro` 快 10 倍、成本约 1/5，但不支持编辑功能；`qwen3.7-flash` 在保持 1M 上下文与完整功能前提下，成本显著低于 `qwen3.7-plus` [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。

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


