# model experience

`model experience` 是百炼平台面向开发者提供的模型选型与使用指南，覆盖文本、视觉、语音、音乐、3D、向量等全模态能力。本文档聚焦模型能力边界、关键参数与工程实践要点，帮助开发者快速匹配业务场景与最优模型，避免常见配置陷阱。

## 支持的模型与功能

百炼提供覆盖[多模态](../concepts/multi-modal.md)的模型矩阵，按核心能力分类如下：

- **文本生成**：以 `qwen3.8-max`（最强推理）、`qwen3.7-plus`（能力/成本均衡）、`qwen3.7-flash`（轻量高效）为代表，均支持 100 万 [Token](../concepts/token.md) 上下文、Function Calling、内置工具（联网搜索/代码解释器）及结构化 JSON 输出 [文本生成 (raw/model-user-guide/model-experience/text-generation-model.md)](../../raw/model-user-guide/model-experience/text-generation-model.md)。`qwen-long` 专为超长文档设计，上下文达 1000 万 [Token](../concepts/token.md)。
  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 同时支持图像、视频（最长 2 小时）、OCR 及结构化输出；`qwen3.5-ocr` 专用于高精度文档文字提取 [视觉理解 (raw/model-user-guide/model-experience/vision-model.md)](../../raw/model-user-guide/model-experience/vision-model.md)。

- **图片/视频生成与编辑**：`qwen-image-3.0-pro` 支持复杂版面与小字渲染；`wan2.7-image-pro` 提供品牌色控制与角色一致性；视频生成推荐 `happyhorse-1.1-i2v`（首帧生视频）或 `wan2.7-i2v-2026-04-25`（首尾帧续写）。

- **3D 生成**：`Tripo/Tripo-P1.0`（快速预览，2 万面）与 `Tripo/Tripo-H3.1`（影视级，200 万面），仅限华北2（北京）地域，需异步轮询获取结果 [Tripo 3D模型生成 (raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

- **语音处理**：ASR 推荐 `qwen-audio-3.0-asr-flash-streaming`（实时）或 `qwen-audio-3.0-asr-flash-filetrans`（非实时，支持说话人分离）；TTS 推荐 `qwen-audio-3.0-tts-plus`（支持声音复刻+指令控制）；S2S 场景优先选用 `qwen-audio-3.0-realtime-plus`（端到端低延迟）。

- **全模态与翻译**：`qwen3.5-omni-plus` 支持文本/音频/图片/视频输入与文本/语音输出，并具备 Function Calling 和联网搜索能力；`qwen3.5-livetranslate-flash-realtime` 支持 60 种语言实时语音翻译。

- **向量与重排序**：文本 Embedding 使用 `text-embedding-v4`（维度可调，默认 1024）；跨模态检索用 `qwen3-vl-embedding`（融合向量）或 `tongyi-embedding-vision-plus`（独立向量）；RAG 重排序首选 `qwen3-rerank`（纯文本）或 `qwen3-vl-rerank`（[多模态](../concepts/multi-modal.md)）。

> **注意**：文档 9 与文档 11 均提及 `qwen3.5-omni-plus` 支持联网搜索，但文档 9 明确说明“联网搜索与 Function Calling 不可同时开启”，而文档 11 未提此限制。实际使用中应以文档 9 的约束为准。

## 关键参数

不同模态模型的关键参数差异显著，需严格按规范设置：

- **上下文长度**：文本模型如 `qwen3.7-plus` 默认 1M [Token](../concepts/token.md)；视觉模型同样支持 1M，但视频输入受时长（2 小时）和大小（2GB）双重限制；Tripo 3D 模型无 Token 概念，以面数（2 万 / 200 万）和输入图片分辨率（20–6000 像素）为约束。

- **输入格式与限制**：
  - 视觉：单图最高 1600 万像素，Token 数 ≈ `h × w / (32 × 32) + 2`；
  - ASR：实时流无时长限制，非实时文件最大 12 小时 / 2GB；
  - TTS：`qwen-audio-3.0-tts-plus` 支持方言指令控制，但系统音色因版本而异；
  - 音乐生成：`fun-music-v1` 支持 `prompt` 或 `lyrics` 至少其一，`fun-music-preview` 则要求必填 `prompt`。

- **输出控制**：
  - 结构化输出：需在请求中声明 `response_format: { "type": "json_object" }`（文本/视觉模型）；
  - 音频格式：音乐生成通过 `format=mp3` 或 `format=wav` 指定；
  - 3D 贴图：`parameters.texture_quality=standard/detailed` 控制贴图质量，`texture=false & pbr=false` 可禁用贴图。

## 使用方式

所有模型均通过统一 API 接入，但协议与流程因场景而异：

- **同步调用（HTTP）**：适用于文本生成、图片生成、非实时 ASR/TTS、Embedding 等。直接 POST 请求，等待完整响应。例如文本生成：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "qwen3.7-plus",
      "input": { "messages": [{"role":"user","content":"你好"}] }
    }'
  ```

- **异步调用（HTTP + 轮询）**：适用于 Tripo 3D、长视频生成等耗时任务。先创建任务获取 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 查询状态（`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`），有效期 24 小时。

- **流式调用（WebSocket）**：适用于实时语音对话、S2S、实时翻译。建立长连接后，音频/文本分块发送，模型边处理边返回语音或文本流。Qwen-Audio Realtime 系列支持语义 VAD（smart_turn），避免无效打断。

- **SDK 接入**：DashScope Python/Java SDK 支持 WebSocket 和 HTTP，Android/iOS SDK 仅支持部分模型（如 Qwen-Audio-TTS、Fun-ASR）。AOQ 协议适用于对弱网稳定性要求极高的客户端场景。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型仅在华北2（北京）可用；部分语音模型（如 `fun-music-v1`）也限定该地域。

- **功能互斥**：`qwen3.5-omni-plus` 的联网搜索与 Function Calling 不可同时启用；思考模式（`enable_thinking`）启用时，S2S 场景无法生成语音输出。

- **版本兼容性**：旧版模型（如 `qwen2.5-omni-7b`、`qwen-omni-turbo`）已停止更新，新项目必须使用 Qwen3.5 或更高系列；`text-embedding-v3` 仅用于迁移存量索引，新索引应使用 `text-embedding-v4`。

- **资源约束**：
  - 视频理解：`qwen3.7-plus` 最多支持 2048 张图片或 64 个视频片段；
  - 音乐生成：`fun-music-v1` 的 `lyrics` 字段需符合 `[verse]`/`[chorus]` 等标准格式；
  - 重排序：`qwen3-rerank` 单次最多处理 500 个文档，每条最大 4000 Token。

- **计费与配额**：所有模型按 Token/请求/时长计费，具体见控制台定价页；API Key 需绑定业务空间（WorkspaceId），且不同地域的 Key 不通用。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)


