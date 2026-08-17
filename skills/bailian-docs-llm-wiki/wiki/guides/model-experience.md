# model experience

`model experience` 是百炼平台面向开发者提供的统一模型能力体验层，涵盖文本、视觉、语音、音视频、3D、音乐等全模态模型服务。所有模型均通过标准化 API 接入，支持流式/非流式调用、结构化输出、Function Calling、思考模式等通用能力，并按场景提供推荐选型路径。开发者可基于任务目标（如生成、理解、转换、检索）快速定位适配模型，无需关注底层部署细节。

## 支持的模型/功能

百炼平台提供覆盖全模态的模型矩阵，按能力维度组织如下：

- **文本生成**：以 `qwen3.7-plus` 为平衡首选，支持 100 万上下文、Function Calling、内置工具（联网搜索/代码解释器）、结构化 JSON 输出及逐步推理（`enable_thinking`）；高推理需求场景推荐 `qwen3.8-max`；超长文档处理推荐 `qwen-long`（1000 万 [Token](../concepts/token.md)）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **视觉理解**：`qwen3.7-plus` 和 `qwen3.7-flash` 同时支持图像、视频（最长 2 小时）、OCR 及[多模态](../concepts/multi-modal.md) Function Calling；专用 OCR 场景推荐 `qwen3.5-ocr` [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **图片/视频生成与编辑**：文生图首选 `qwen-image-3.0-pro`（支持 agent [prompt](prompt.md) 改写与小字渲染），图生视频首选 `happyhorse-1.1-i2v`，首尾帧续写推荐 `wan2.7-i2v-2026-04-25` [原文标题](../../raw/model-user-guide/model-experience/image-model.md)。  
- **3D 生成**：仅限华北2（北京）地域，需使用 Tripo 模型（`Tripo/Tripo-P1.0` 快速预览，`Tripo/Tripo-H3.1` 影视级精度），支持文生3D、单图生3D、多图生3D 三种模式 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **语音与音频**：  
  - 语音合成：`qwen-audio-3.0-tts-plus` 支持声音复刻、声音设计及自然语言指令控制；  
  - 语音识别：实时场景用 `qwen-audio-3.0-asr-flash-streaming`，文件转写用 `qwen-audio-3.0-asr-flash-filetrans`（支持说话人分离）；  
  - 语音转语音（S2S）：低延迟对话用 `qwen-audio-3.0-realtime-plus`，同传用 `qwen3.5-livetranslate-flash-realtime`；  
  - 音乐生成：邀测模型 `fun-music-v1` 支持 [prompt](prompt.md)/lyrics 输入、性别选择及纯音乐生成 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **向量与重排序**：文本 Embedding 推荐 `text-embedding-v4`（维度可配），[多模态](../concepts/multi-modal.md) Embedding 推荐 `qwen3-vl-embedding`（融合向量）或 `tongyi-embedding-vision-plus`（独立向量），重排序推荐 `qwen3-rerank`（文本）或 `qwen3-vl-rerank`（[多模态](../concepts/multi-modal.md)） [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。  
- **全模态理解**：`qwen3.5-omni-plus` 为旗舰模型，支持文本/音频/图片/视频输入，输出文本+语音，具备联网搜索、Function Calling、113 种输入语言识别能力；轻量场景可用 `qwen3-omni-flash`（HTTP 模式支持思考模式）[原文标题](../../raw/model-user-guide/model-experience/omni.md)。

> **注意**：文档 9 与文档 11 对 `qwen3.5-omni-plus` 的联网搜索支持描述一致，但文档 9 明确指出“Qwen-Audio Realtime 不支持此功能”，而文档 11 未提及该限制，此处以文档 9 为准——联网搜索仅在 Qwen3.5-Omni 系列中可用，Qwen-Audio Realtime 确实不支持。

## 关键参数

各模型共性关键参数如下（具体值依模型而异）：

- **`model`**：必填，指定模型 ID（如 `"qwen3.7-plus"`）。快照版本需显式指定（如 `"qwen3.7-plus-2026-05-26"`）。  
- **`input`**：结构化输入字段，类型由模型决定：  
  - 文本模型：`{"prompt": "..."}`；  
  - 视觉模型：`{"prompt": "...", "image": "url"}` 或 `{"video": "url"}`；  
  - 3D 模型：三选一 `{"prompt": "..."}` / `{"image": "url"}` / `{"images": ["url1", ...]}`；  
  - 音乐模型：`{"prompt": "..."}` 或 `{"lyrics": "..."}`，`{"is_instrumental": true}` 控制纯音乐。  
- **`parameters`**：模型特有配置：  
  - 文本：`{"enable_thinking": true}`、`{"reasoning": {"effort": "high"}}`；  
  - TTS：`{"voice": "zh-CN-XiaoYiNeural"}`（系统音色）或 `{"voice_id": "xxx"}`（自定义音色）；  
  - ASR：`{"hotwords": ["阿里云", "百炼"]}`、`{"prompt": "会议场景，专业术语较多"}`；  
  - Tripo：`{"texture_quality": "detailed"}`、`{"geometry_quality": "ultra"}`（仅 H3.1）。  
- **协议与模式**：  
  - 实时流式：WebSocket + `X-DashScope-Async: enable` 头；  
  - 非实时：HTTP POST；  
  - 异步任务：返回 `task_id`，需轮询 `/api/v1/tasks/{id}` 获取结果（如 Tripo 3D 生成）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

## 使用方式

1. **开通与鉴权**：  
   - 在[模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)开通目标模型服务；  
   - 获取 API Key 并配置环境变量 `DASHSCOPE_API_KEY`；  
   - Tripo 3D 模型**仅限华北2（北京）地域**，且必须使用该地域 API Key [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  

2. **API 调用**：  
   - 构造请求 URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/{service}/{endpoint}`（`service` 如 `aigc/video-generation/3d-generation`，`endpoint` 如 `generation`）；  
   - 设置 Header：`Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`；  
   - 发送 JSON Body（含 `model`、`input`、`parameters`）。  

3. **结果处理**：  
   - 同步接口：直接解析响应 `output` 字段（如文本、URL、JSON）；  
   - 异步接口（如 Tripo）：轮询 `GET /api/v1/tasks/{task_id}`，状态为 `SUCCEEDED` 后提取 `pbr_model_url` 或 `audio.url`；  
   - 流式接口（WebSocket/TTS Realtime）：监听 `onmessage` 事件接收分块数据。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型、Fun-Music 模型**仅支持华北2（北京）地域**；部分旧版模型（如 `qwen-omni-turbo`）已停更，新项目应避免使用 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **输入约束**：  
  - 图像：单图最高 1600 万像素，[Token](../concepts/token.md) 消耗 = `h × w / (32 × 32) + 2`；  
  - 视频：`qwen3.7-plus` 支持最长 2 小时/2GB，`qwen-long` 仅支持文本；  
  - 音频：ASR `qwen-audio-3.0-asr-flash-filetrans` 最大 12 小时/2GB，TTS `qwen3-tts-flash` 单次输入限 5 分钟。  
- **能力冲突**：  
  - Qwen3.5-Omni 的联网搜索与 Function Calling **不可同时启用**；  
  - 思考模式启用时，**不支持生成语音输出**（仅文本）；  
  - `qwen-audio-3.0-realtime-plus` 支持 Function Calling，但**不支持联网搜索与思考模式**。  
- **版本管理**：推荐使用带日期后缀的快照版本（如 `qwen3.7-plus-2026-05-26`）保障稳定性；避免依赖无后缀的“latest”别名，因其可能随平台更新变更行为。  
- **成本提示**：`qwen3.7-flash` 在效果接近 `qwen3.7-plus` 的前提下显著降低成本，适用于效果验证后的规模化部署；`z-image-turbo` 生成速度比 `qwen-image-3.0-pro` 快 10 倍、价格约 1/5，但不支持编辑功能。

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)


