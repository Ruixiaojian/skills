# model inference

百炼平台提供覆盖文本、图像、视频、音频、3D 等多种模态的模型推理能力，通过统一的 API 接口调用。开发者可根据业务场景选择合适的模型系列，实现文本生成、视觉理解、图片/视频生成与编辑、语音识别与合成、语音对话、3D 建模、向量检索等功能。

## 支持的模型与功能概览

百炼平台的模型推理能力按模态和任务类型划分为以下几大类：

### 文本生成

推荐使用 `qwen3.6-plus`，它在能力与成本之间取得平衡，拥有 100 万 Token 上下文窗口，支持 Function Calling、内置工具（联网搜索、代码解释器）、结构化输出和批量推理。如需最强推理能力可选 `qwen3.7-max`，如需降低成本可尝试 `qwen3.6-flash`。平台还提供 DeepSeek、GLM、Kimi、MiniMax 等第三方模型。详见 [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)。

### 视觉理解

推荐从 `qwen3.6-plus` 开始，支持 1M 上下文、最长 2 小时视频、每张图片最高 1600 万像素，并支持 Function Calling 和结构化输出。OCR 与文档提取场景可使用专用的 `qwen-vl-ocr` 模型。详见 [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)。

### 图片生成与编辑

推荐使用 `wan2.7-image-pro`，集成文字渲染、品牌色控制、角色一致性多图生成和图片编辑，文生图最高支持 4096×4096 分辨率。快速低成本场景可用 `z-image-turbo`（速度快 10 倍，价格约 1/5）；需要负向提示词或最多 6 张变体的场景可用 `qwen-image-2.0-pro`。详见 [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)。

### 视频生成与编辑

文生视频推荐 `happyhorse-1.0-t2v`（支持有声视频、1080P、最长 15 秒），图生视频推荐 `happyhorse-1.0-i2v`。如需传入自定义音频文件或首尾帧生视频，推荐 `wan2.7` 系列。视频编辑推荐 `happyhorse-1.0-video-edit`，角色动画推荐 `wan2.2-animate-move`。

### 语音识别（ASR）

实时场景推荐 `fun-asr-realtime`（支持热词、方言）或 `qwen3.5-omni-plus-realtime`（支持 Prompt 上下文注入）。非实时场景推荐 `fun-asr`（支持说话人分离、最长 12 小时音频）。情感识别可用 Qwen-ASR 系列。

### 语音合成（TTS）

标准语音合成推荐 `cosyvoice-v3-plus`；自定义音色（声音复刻 + 声音设计）推荐 `cosyvoice-v3.5-plus`。支持 WebSocket（流式输入输出，延迟最低）和 HTTP（完整文本输入，流式音频返回）两种接入方式。CosyVoice 系列还支持指令控制，可用自然语言动态调整语速、情绪和风格。

### 语音转语音（S2S）与全模态

端到端语音对话推荐 `qwen3.5-omni-plus-realtime`（低延迟、能感知语调情绪）。同声传译推荐 `qwen3.5-livetranslate-flash-realtime`（支持 60 种语言）。全模态模型支持文本、音频、图片、视频的混合输入，并输出文本和语音。

### 3D 模型生成

通过 Tripo 模型支持文生 3D、单图生 3D 和多图生 3D。`Tripo/Tripo-P1.0` 适合快速预览（最高 2 万面），`Tripo/Tripo-H3.1` 适合高精度资产（最高 200 万面）。

> **注意**：Tripo 3D 模型生成仅适用于"中国内地（北京）"地域，且必须使用该地域的 API Key。

### 向量与重排序

文本 Embedding 推荐 `text-embedding-v4`（支持 64~2048 维），多模态 Embedding 推荐 `qwen3-vl-embedding`（支持融合向量和独立向量）。重排序推荐 `qwen3-rerank`（纯文本）或 `qwen3-vl-rerank`（多模态）。

## 关键参数与能力

### 上下文窗口

- **1M Token**（约 70 万汉字）：`qwen3.7-max`、`qwen3.6-plus`、`qwen3.6-flash`、`deepseek-v4-pro` 等
- **256k Token**：`qwen3.6-max-preview`、`kimi-k2.6` 等
- **128k~198k Token**：`glm-5.1`（198k）、`MiniMax-M2.5`（192k）等

### 思考模式

通过 `enable_thinking` 参数开启逐步推理，适用于多步数学计算、代码调试等场景。所有 Qwen3 及以上模型均支持。各模型的思考预算（thinking budget）不同，如 `qwen3.7-max` 为 256k、`qwen3.6-flash` 为 128k。

### Function Calling 与内置工具

- **Function Calling**：所有通用文本模型均支持，部分视觉/全模态模型也支持
- **内置工具**（联网搜索、代码解释器等，无需额外配置）：仅 Qwen3.6 和 Qwen3.5 系列的 plus/flash 版本支持

### 结构化输出

从文本或视觉输入中获取有效 JSON 返回。Qwen3.6、Qwen3.5 和 Qwen3-VL 系列在非思考模式下支持。

### 批量推理

适用于大量请求且对延迟要求不高的场景，可降低成本。支持的模型包括 `qwen3.7-max`、`qwen3.6-plus`、`qwen3.6-flash` 等。

## 使用方式

### API 调用协议

| 协议 | 适用场景 | 典型模型 |
|------|---------|---------|
| HTTP（OpenAI 兼容） | 文本生成、视觉理解、非实时 ASR/TTS、图片生成 | `qwen3.6-plus`、`fun-asr`、`cosyvoice-v3-plus` |
| WebSocket | 实时语音识别、实时语音合成、实时语音对话 | `fun-asr-realtime`、`cosyvoice-v3.5-plus`、`qwen3.5-omni-plus-realtime` |
| 异步任务 | 视频生成、3D 生成、音乐生成 | `happyhorse-1.0-t2v`、`Tripo/Tripo-P1.0`、`fun-music-v1` |

[异步任务模式](../concepts/async-task-pattern.md)通过提交任务获取 `task_id`，然后轮询获取结果。任务状态流转为：`PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED`。

### SDK 支持

- Fun-ASR 和 Qwen-ASR 的实时模型支持 DashScope SDK（Java、Python）接入
- Fun-ASR 还支持 Android、iOS SDK
- CosyVoice WebSocket 模型支持 DashScope SDK 及 Android、iOS SDK

## 限制和注意事项

- **地域限制**：Tripo 3D 生成和音乐生成（`fun-music-v1`）仅在中国内地（北京）地域可用；`wanx2.1-imageedit` 仅支持北京地域
- **音乐生成邀测**：`fun-music-v1` 目前处于邀测阶段，需在模型广场申请开通
- **异步任务有效期**：3D 生成的 `task_id` 查询有效期为 24 小时，输出文件（GLB、预览图）有效期为 2 小时
- **视觉理解 Token 消耗**：图片 Token 数 = `h × w / (32 × 32) + 2`，更高分辨率会消耗更多 Token
- **S2S 思考模式**：思考模式下不支持生成语音，仅输出文本
- **联网搜索与 Function Calling**：在 Qwen3.5-Omni 中不可同时开启

> **注意**：语音转语音文档中 `deepseek-v4-pro` 和 `deepseek-v4-flash` 在文本生成推荐表中标注为支持 Function Calling，但在详细模型列表中标注为不支持。以详细模型列表为准，这两个模型**不支持** Function Calling。

> **注意**：`qwen3.5-omni-plus-realtime` 的输入在推荐模型表中列为"文本、音频、图片"，但在所有模型详细列表中列为"文本、音频、图片、视频"。WebSocket 实时模式下视频输入的支持程度请以最新 API 文档为准。

## 来源文档

- [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)
- [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)
- [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-inference/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-inference/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-inference/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-inference/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)

