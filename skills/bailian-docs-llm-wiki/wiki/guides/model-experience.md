# model experience

`model experience` 是百炼平台面向开发者提供的模型选型与使用指南集合，覆盖视觉理解、文本生成、语音处理、[多模态](../concepts/multi-modal.md)交互、3D生成、音乐合成等核心AI能力。本文档聚焦于模型能力边界、关键参数、调用方式及实际限制，帮助开发者快速匹配业务场景与最优模型，避免因参数误配或能力误判导致的集成失败。

## 支持的模型与功能

百炼提供全栈式模型能力，按模态与任务类型组织：

- **视觉理解**：支持图像/视频分析、OCR、结构化输出、Function Calling 和内置工具（联网搜索、代码执行）。旗舰模型 `qwen3.7-plus` 和 `qwen3.8-max` 均支持 1M 上下文、2 小时视频输入、2048 张图片及 64 段视频；`qwen3.5-ocr` 专为文档与手写识别优化 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。  
- **文本生成**：覆盖 AI 编程、办公助理、长文档处理等场景。`qwen3.7-plus`（1M 上下文）为通用首选；超长文档推荐 `qwen-long`（10M 上下文）；编程场景可选 `qwen3-coder-plus` [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)。  
- **语音能力**：包括 ASR（语音识别）、TTS（语音合成）、S2S（语音转语音）和全模态 Omni 模型。`qwen-audio-3.0-asr-flash-filetrans` 支持 12 小时音频转写与说话人分离；`qwen-audio-3.0-tts-plus` 同时支持声音复刻与指令控制；`qwen3.5-omni-plus` 支持文本/音频/图片/视频四模态输入与 Function Calling [原文标题](../../raw/model-user-guide/model-experience/asr-model.md)。  
- **生成类模型**：  
  - *图片*：`qwen-image-3.0-pro`（2048×2048，支持编辑）、`wan2.7-image-pro`（4096×4096，品牌色控制）；  
  - *视频*：`happyhorse-1.1-t2v`（1080P，3–15 秒）、`wan2.7-i2v-2026-04-25`（首尾帧续写）；  
  - *3D*：`Tripo/Tripo-P1.0`（2 万面，快速预览）、`Tripo/Tripo-H3.1`（200 万面，影视级）；  
  - *音乐*：`fun-music-v1`（支持歌词输入与性别选择），当前仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)。  
- **向量与重排序**：`text-embedding-v4`（文本检索）、`qwen3-vl-embedding`（图文融合）、`qwen3-rerank`（纯文本重排序）、`qwen3-vl-rerank`（[多模态](../concepts/multi-modal.md)重排序）。

> **注意**：文档 1 中 `qwen3.5-omni-plus` 的视频支持时长为“1小时”，而文档 8 中同模型在“使用场景”部分明确标注“视频最长1小时”，但在“推荐模型”表格中未列出视频时长字段，存在信息缺失。以文档 8 的场景描述为准，该模型视频输入上限为 1 小时。

## 关键参数

各模型核心参数需严格遵循约束，否则请求将失败：

- **上下文长度**：`qwen3.7-plus`、`qwen3.7-flash` 等主流模型为 1M [Token](../concepts/token.md)；`qwen-long` 达 10M；旧版 `qwen3-30b-a3b` 仅 80k。  
- **视觉输入**：  
  - 单图最大像素 = 1600 万（如 4000×4000），[Token](../concepts/token.md) 消耗公式为 `h × w / (32 × 32) + 2`；  
  - 视频最长 2 小时（`qwen3.7-plus` 系列）或 1 小时（`qwen3.5-omni-plus`）；  
  - 最大图片数：`qwen3.7-plus` 支持 2048 张，`qwen3.7-flash` 为 256 张。  
- **音频/视频文件限制**：  
  - ASR 文件转写：`qwen-audio-3.0-asr-flash-filetrans` 支持 12 小时 / 2GB；  
  - 全模态分析：`qwen3.5-omni-plus` 支持音频最长 3 小时、视频最长 1 小时；  
  - Tripo 3D：单图尺寸 20–6000 像素，≤20MB；多图限 2–4 张。  
- **输出控制**：  
  - 结构化输出（JSON）：Qwen3.x 及 Qwen3-VL 系列均支持；  
  - 思考模式：通过 `enable_thinking`（Responses API）或 `reasoning.effort` 控制，Qwen3 及以上模型均支持；  
  - 贴图质量（Tripo）：`parameters.texture_quality` 可设 `standard` 或 `detailed`；几何精度（仅 H3.1）：`parameters.geometry_quality` 可设 `standard` 或 `ultra`。

## 使用方式

所有模型统一通过 DashScope API 调用，需配置 `DASHSCOPE_API_KEY` 并指定 `WorkspaceId`：

- **同步调用**：适用于文本生成、TTS、ASR 文件转写等。HTTP POST 请求体包含 `model`、`input`（内容）、`parameters`（可选配置）。例如 Tripo 文生3D：  
  ```json
  {
    "model": "Tripo/Tripo-P1.0",
    "input": {"prompt": "一只可爱的猫"},
    "parameters": {"texture_quality": "standard"}
  }
  ```
- **异步调用**：适用于 3D 生成、长视频处理等耗时任务。需先调用 `/3d-generation` 获取 `task_id`，再轮询 `/tasks/{task_id}` 查询状态（有效期 24 小时）[原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。  
- **流式调用**：WebSocket 协议用于实时场景（语音助手、直播字幕）。`qwen-audio-3.0-realtime-plus`、`qwen3.5-livetranslate-flash-realtime` 等模型需建立长连接，接收分块响应。  
- **协议选择**：  
  - TTS：带 `-realtime` 后缀的模型为 WebSocket；无后缀为 HTTP；  
  - S2S：`qwen-audio-3.0-realtime-plus` 为端到端低延迟方案；Pipeline 方案（ASR+LLM+TTS）需分别调用三类模型 [原文标题](../../raw/model-user-guide/model-experience/s2s-model.md)。

## 限制和注意事项

- **地域限制**：Tripo 3D 模型、Fun-Music 仅支持华北2（北京）地域；部分 Wan 视频模型（如 `wan2.6-t2v-us`）专用于美国地域。  
- **功能互斥**：  
  - `qwen3.5-omni-plus` 的联网搜索与 Function Calling 不可同时启用；  
  - 思考模式启用时，`qwen3-omni-flash` 不支持语音输出；  
  - `is_instrumental=true` 时，`fun-music-v1` 的 `lyrics` 和 `gender` 参数被忽略。  
- **版本管理**：快照版本（如 `qwen3.7-plus-2026-05-26`）提供稳定性，但文档 3 中 `qwen3.7-plus` 行对应“查看快照版本”，未列出具体 ID，需在模型广场确认可用版本。  
- **计费差异**：旧版 `qwen-tts` 按 [Token](../concepts/token.md) 计费，新版 `qwen3-tts` 系列按请求或时长计费，迁移时需更新计费逻辑。  
- **语言支持**：`qwen3.5-livetranslate-flash-realtime` 支持 60 种语言（29 种语音+文本），但 `qwen3-omni-flash` 仅支持 11 种输出语言，选型时需核对目标语种是否在“支持的语言”列表中标注为“支持”而非“仅文本”。

## 来源文档

- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)


