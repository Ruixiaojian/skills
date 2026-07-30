# 多模态

多模态是指模型能够同时理解、生成或处理多种类型数据（如文本、图像、音频、视频等）的能力。在百炼平台中，多模态不是单一模型的特性，而是一类跨模态协同能力的统称，体现为统一接口下的结构化输入支持、模态感知的参数配置及端到端的混合推理流程。

## 在百炼平台的不同场景中，这个概念如何使用

- **输入层面**：多模态模型接受结构化 `input` 或 `content`，而非纯字符串。例如：
  - `qwen3-vl-plus` 和 `qwen3.7-plus` 支持 `content: [{"type": "text", "text": "..."}, {"type": "image_url", "image_url": "..."}]`；
  - `qwen3.5-omni-plus` 可混合传入文本、图片 URL、音频 base64 或视频 URL；
  - `qwen3.5-omni-realtime` 通过 WebSocket 实时流式接收 PCM 音频帧与 JPG 图像帧；
  - 视频生成（如 `wan2.7-t2v`）和 3D 生成（如 `Tripo/Tripo-H3.1`）均要求 `input` 按模态明确声明 `prompt`/`image`/`images`/`media` 字段。

- **输出层面**：支持多模态响应组合。例如：
  - `qwen3.5-omni-realtime` 可同时返回 `text` 和 `audio`（PCM 流）；
  - `qwen-image-3.0-pro` 输出图像 URL；`Tripo` 输出 GLB 模型 + 渲染图；`vidu` 输出视频 URL + 字幕 JSON；
  - 全模态模型（如 `qwen3.5-omni-plus`）在 Function Calling 中可调用工具并融合多源结果生成结构化响应。

- **能力协同层面**：多模态是高级能力（如思考模式、Function Calling、联网搜索）的运行基础。例如：
  - `enable_thinking=true` 仅对 `qwen3.7-plus`、`qwen3.5-omni-plus` 等多模态模型生效，用于引导模型分步解析图文混合输入；
  - `qwen3.5-omni-realtime` 的 `semantic_vad` 和 `enable_search` 依赖语音+文本联合建模；
  - 视觉理解模型（`qwen3-vl-plus`）调用 OCR 工具后，将识别文本与原始图像共同参与后续推理。

> ⚠️ 注意：并非所有“支持图像/音频”的模型都属于严格意义上的多模态模型。例如 `cosyvoice-v3-flash` 是单模态 TTS 模型（仅生成语音），而 `qwen3.5-omni-plus` 是真正具备跨模态理解与生成能力的全模态模型。

## 关键参数和配置

- **必填字段**：
  - `model`：必须选用明确标注为多模态的模型 ID（如 `qwen3.7-plus`、`qwen3.5-omni-plus`、`qwen3-vl-plus`、`qwen3.5-omni-realtime`），不可混用纯文本模型（如 `qwen3-max`）。
  - `input` 或 `content`：必须为结构化对象，按模型文档要求组织模态项（`text`/`image_url`/`audio_url`/`video_url`/`media` 等），禁止传入纯字符串。

- **模态相关参数**（依模型而异，非通用）：
  - `max_images` / `max_videos`：限制单次请求最大图像/视频数量（视觉理解类模型）；
  - `duration` / `resolution` / `aspect_ratio`：控制视频/图像输出规格（生成类模型）；
  - `modalities: ["text", "audio"]`：指定实时 API 输出模态组合（`omni-realtime`）；
  - `turn_detection.type`：选择语音活动检测模式（`server_vad` 或 `semantic_vad`，后者需多模态语义理解支撑）。

- **通用约束**：
  - 所有多模态生成接口（图像、视频、3D）**强制启用异步模式**：必须设置请求头 `X-DashScope-Async: enable`；
  - 地域强绑定：`Tripo` 仅限华北2（北京），`omni-realtime` 需匹配 API Key 所属地域的 WebSocket Endpoint；
  - 文件限制：图像 URL 需公网可访问且 ≤20 MB；音频 base64 ≤256 KB；视频 URL 时长通常 ≤2 小时。

## 面向开发者，简洁实用

- ✅ **正确做法**：  
  调用前查模型文档确认是否标有“多模态”或“全模态”；使用 SDK 的 `MultiModalInput` 类或手动构造符合 schema 的 `input` 对象；异步任务务必轮询 `task_id`；实时流优先用官方 WebSocket SDK（Python/Node.js）。

- ❌ **常见错误**：  
  对 `qwen3-vl-plus` 传 `content: "hello"`（应为数组）；用 `qwen3-max` 调用 `image_url`（报错 `invalid content type`）；图像生成漏设 `X-DashScope-Async`（返回 400）；跨地域调用 Tripo（返回 404 或 `InvalidRegionId`）。

- 🛠️ **调试建议**：  
  开启 `debug: true`（SDK）或检查响应中的 `error_code`（如 `INVALID_INPUT_CONTENT_TYPE`）；用百炼 CLI 的 `bailian model invoke --debug` 查看原始请求/响应；小样本测试优先选 `qwen3.7-plus`（支持文本+图+视频+工具调用，覆盖最全）。

## 关联主题页

- [preparations](../api/preparations.md)
- [model experience](../guides/model-experience.md)
- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [omni realtime api](../api/omni-realtime-api.md)


