# 多模态输入

多模态输入是指在一次请求中同时提交两种或以上类型的数据（如文本、图像、音频、视频、3D 图像等），使模型能够联合理解并处理跨模态语义信息。百炼平台通过统一的 API 设计与模型能力支持，将多模态输入作为核心交互范式，覆盖智能体调用、图像/视频/3D 生成、实时音视频对话等全场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）与工作流（Workflow）调用**：  
  通过 `input` 字段传入消息数组，支持混合 `text`、`image`、`file` 类型内容。图像输入需选用通义千问 VL 系列模型，并在智能体中配置为“自定义处理”，或在工作流模型节点入参中显式填写 `imageList`；文件输入仅限智能体应用，且需在应用内启用“全文引用”或“切片检索”。

- **图像生成（Image Generation）**：  
  支持 `prompt`（文本）+ `input.messages[].content[].image`（图像）联合输入，用于图生图、局部编辑、风格迁移等任务。`qwen-image-3.0-pro` 等新模型推荐使用结构化 `messages` 格式，最多支持 14 张参考图（Vidu 模型）。

- **视频生成（Video Generation）**：  
  文生视频、图生视频、参考生视频均依赖多模态输入组合：例如 `input.prompt` + `input.image`（首帧）+ `input.audio`（可选配音）；数字人驱动类模型（如 `liveportrait`、`emo`）还需配合检测模型验证输入合规性。

- **3D 生成（3D Generation）**：  
  支持三类互斥输入模式：纯文本（`input.prompt`）、单张图像（`input.image`）、四视角图像数组（`input.images`，固定顺序为「前、左、后、右」）。所有输入均参与三维几何与纹理联合建模。

- **Omni 实时 API（WebSocket）**：  
  原生支持语音（PCM 音频流）、文本、图像（JPG/JPEG，Base64 编码 ≤256 KB）、视频帧（通过 `append_video` 事件）的实时混合输入，服务端按事件流动态融合处理，实现低延迟多模态交互。

- **视觉理解与大模型推理（Qwen-VL / Qwen3.7-plus）**：  
  支持文本 + 多图（≤2048 张）+ 多视频（≤64 个，总时长 ≤2 小时）联合输入，适用于复杂文档分析、视频摘要、跨模态检索等任务，输出支持结构化 JSON 与 Function Calling。

## 关键参数和配置

- **通用输入结构**：  
  - `input` 字段为 `string`（纯文本）或 `array`（多轮/多模态消息），后者需遵循 `[{"role": "user", "content": [...]}, ...]` 格式；  
  - `content` 内部为数组，每个元素含 `type`（`text` / `image_url` / `image` / `audio` / `video`）及对应值（如 `{"type": "text", "text": "描述一下这张图"}` 或 `{"type": "image_url", "image_url": {"url": "https://..."}}`）；  
  - 图像 URL 必须可公开访问，或使用 Base64 编码（`data:image/jpeg;base64,...`）。

- **模型级约束**：  
  - VL 模型（如 `qwen3.7-plus`, `qwen3.5-omni-realtime`）要求图像分辨率 ≤1600万像素，单次请求总图像数 ≤2048；  
  - 视频输入最大时长 2–3 小时（依模型而定），文件大小 ≤2GB；  
  - Omni 实时 API 中图像尺寸 ≤1080p，Base64 编码后 ≤256 KB；  
  - Tripo 3D 输入图像分辨率范围 [20, 6000] 像素，单图 ≤20MB。

- **协议与头信息**：  
  - HTTP 请求需设置 `Content-Type: application/json`；  
  - [异步任务](asynchronous-task.md)（Tripo、视频生成等）必须携带请求头 `X-DashScope-Async: enable`；  
  - Omni 实时 API 使用 WebSocket 连接，无需额外头，但需正确发送 `input_audio_buffer.append`、`input_image.append` 等结构化事件。

- **注意事项**：  
  - 多模态输入不支持跨模型混用（如向纯文本模型传图像）；  
  - 文件类输入（PDF/DOCX 等）仅在智能体应用中生效，且需提前上传至百炼知识库或通过 `input_file` 参数传入；  
  - 所有图像/视频 URL 有效期需覆盖整个请求生命周期，建议使用 CDN 或临时直传链接。

## 关联主题页

- [application call](../api/application-call.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [model experience](../guides/model-experience.md)


