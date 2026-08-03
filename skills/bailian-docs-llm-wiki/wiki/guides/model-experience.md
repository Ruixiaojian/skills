# model experience

`model experience` 是百炼平台面向开发者提供的模型能力总览，涵盖文本、视觉、语音、音视频、3D、音乐等全模态模型的选型指南、核心参数与使用规范。本文档聚焦实际工程落地，不包含营销性描述，所有推荐均基于当前（2026年中）稳定可用的模型版本与能力边界。关键能力如 Function Calling、思考模式、结构化输出、内置工具等在主流模型上已形成统一支持矩阵，但具体实现细节需结合模型类型与接入方式确认。

## 支持的模型/功能

百炼平台提供覆盖多模态的模型体系，按能力域划分如下：

- **文本生成**：以 `qwen3.7-plus` 为平衡首选，支持 1M 上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化输出与 `enable_thinking` 控制的混合推理模式；`qwen3.8-max` 适用于复杂逻辑推演场景；超长文档处理推荐 `qwen-long`（10M 上下文）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 同时支持图像、视频（最长2小时）、OCR及结构化输出；`qwen3.5-ocr` 专用于高精度文档/手写体识别 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片生成与编辑**：`wan2.7-image-pro` 支持文生图（4096×4096）、多图参考编辑与角色一致性；`qwen-image-2.0-pro` 更适合需负向提示词或小字渲染的场景 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **3D生成**：仅限华北2（北京）地域，通过异步 API 调用 `Tripo/Tripo-P1.0`（快速预览）或 `Tripo/Tripo-H3.1`（影视级精度），支持文生3D、单图生3D、多图生3D三种模式 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音与音视频**：  
  - 语音合成：`qwen-audio-3.0-tts-plus`（标准+复刻+指令控制）、`cosyvoice-v3.5-plus`（复刻+设计+指令控制）；  
  - 语音识别：`qwen-audio-3.0-asr-flash-streaming`（实时）、`qwen-audio-3.0-asr-flash-filetrans`（非实时+说话人分离）；  
  - 语音转语音（S2S）：`qwen-audio-3.0-realtime-plus`（低延迟对话）、`qwen3.5-livetranslate-flash-realtime`（60语种同传）；  
  - 全模态理解：`qwen3.5-omni-plus`（旗舰，支持音视频分析、联网搜索、Function Calling）[原文标题](../../raw/model-user-guide/model-experience/omni.md)。  
- **音乐与向量**：`fun-music-v1`（邀测中，支持歌词/提示词生成带声歌曲）；`text-embedding-v4`（文本检索/RAG默认选择）、`qwen3-rerank`（纯文本重排序）、`qwen3-vl-rerank`（多模态重排序）。

> **注意**：文档 1 与文档 2 中对 `qwen3.7-plus` 的上下文窗口描述一致（1M），但文档 2 表格中“最大输出”列为 `64k`，而文档 1 未明确该限制；实际使用中应以模型广场标注的 `max_output_tokens` 为准，避免假设性溢出。  
> **注意**：文档 8（S2S）与文档 10（全模态）均提及 `qwen3.5-omni-flash` 支持联网搜索，但文档 8 明确说明“Qwen3-Omni-Flash 和 Livetranslate 模型不支持此功能”，此处存在矛盾；以文档 10 的表格为准（`qwen3.5-omni-flash` 行“联网搜索”列为“支持”），文档 8 的说明属过时信息。

## 关键参数

各模型共性关键参数如下（具体值依模型而异）：

| 参数名 | 说明 | 示例值/范围 |
|--------|------|-------------|
| `model` | 模型 ID，必须精确匹配快照版本（如 `qwen3.7-plus-2026-05-26`）或别名（如 `qwen3.7-plus`） | `"qwen3.7-plus"` |
| `input` | 输入内容载体，结构因模态而异：<br>- 文本：`{"messages": [...]}`<br>- 视觉：`{"image": "url"}` 或 `{"video": "url"}`<br>- 音频：`{"audio": "url"}` 或流式二进制<br>- 3D：`{"prompt": "..."}` 或 `{"images": [...]}` | `{ "prompt": "夏日清新民谣" }` |
| `parameters` | 模型行为控制：<br>- `enable_thinking`: bool（文本模型）<br>- `texture_quality`: `"standard"`/`"detailed"`（Tripo）<br>- `format`: `"mp3"`/`"wav"`（Fun-Music）<br>- `is_instrumental`: bool（Fun-Music） | `{"texture_quality": "detailed"}` |
| `X-DashScope-Async` | 异步任务必需头（如 Tripo、Fun-Music），值为 `"enable"` | `"enable"` |
| `max_output_tokens` | 输出长度硬上限，超出将被截断 | `64000`（`qwen3.7-plus`） |

## 使用方式

- **同步调用**：适用于文本生成、TTS、ASR 等低延迟场景，直接 POST 到 `/api/v1/services/xxx`，响应含完整结果。  
- **异步调用**：适用于 3D 生成、视频生成、批量推理等耗时操作：  
  1. 发起请求获取 `task_id`；  
  2. 轮询 `/api/v1/tasks/{task_id}`（建议间隔 ≥15s）；  
  3. 状态为 `SUCCEEDED` 后解析 `output.results` 中的 URL（如 `pbr_model_url`、`audio.url`）。  
- **流式接入**：WebSocket 协议用于实时语音（ASR/TTS/S2S）、实时对话（Omni）；HTTP 流式（`Transfer-Encoding: chunked`）适用于 TTS 非实时场景。  
- **SDK 与协议**：Python/Java SDK 支持主流模型；客户端可选 AOQ 协议（低延迟/弱网优化）或标准 WebSocket/HTTP [原文标题](../../raw/model-user-guide/model-experience/tts-model.md)。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型、Fun-Music 仅支持华北2（北京）；部分模型（如 `qwen-omni-turbo`）在其他地域不可用。  
- **输入约束**：  
  - 图像：单图 ≤1600万像素，[Token](../concepts/token.md) 数 = `h×w/(32×32)+2`；  
  - 视频：`qwen3.7-plus` 最长 2 小时 / 2GB；  
  - 音频文件：ASR `qwen-audio-3.0-asr-flash-filetrans` 最大 12 小时 / 2GB；  
  - 3D 多图输入：2~4 张 PNG/JPEG，单张 ≤20MB。  
- **能力边界**：  
  - `qwen-long` 不支持 Function Calling、思考模式、内置工具；  
  - `qwen3.5-ocr` 仅支持 OCR，不可用于通用视觉理解；  
  - `z-image-turbo` 不支持图片编辑；  
  - `qwen3-rerank` 最多处理 500 个文档，单条输入 ≤4000 tokens。  
- **版本管理**：生产环境强烈建议使用带日期后缀的快照模型 ID（如 `qwen3.7-flash-2026-07-15`），避免别名自动升级导致行为变更。  
- **计费差异**：Qwen3-TTS 系列中 `-realtime` 模型按 [Token](../concepts/token.md) 计费，而 Qwen-Audio-TTS/CosyVoice 系列按请求+时长计费，需按场景选型。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)


