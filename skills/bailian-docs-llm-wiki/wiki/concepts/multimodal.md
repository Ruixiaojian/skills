# 多模态

多模态（Multimodal）指模型能够同时理解、生成或联合理解多种类型数据（如文本、图像、音频、视频等）的能力。在百炼平台中，多模态不是单一模型特性，而是一类跨模态协同能力的统称，涵盖输入融合、跨模态对齐、联合推理与多模态输出等核心行为。

## 在百炼平台的不同场景中，这个概念如何使用

多模态能力在百炼平台中以**模型能力维度**和**系统协同维度**双轨落地：

- **模型级多模态**：  
  - `qwen3.5-omni-plus`、`qwen3.5-omni-realtime` 等 Omni 系列模型支持文本+音频+图像+视频的**端到端联合理解与生成**，可处理混合输入（如语音提问+截图上传），并按需输出文本、音频或音视频流；  
  - `qwen-vl-plus`、`qwen3-vl-plus` 专注**视觉语言理解**，支持单图/多图/长视频（最长2小时）输入，返回结构化描述、OCR结果或推理结论；  
  - `qwen-image-3.0-pro`、`wan2.7-image-pro` 等图像模型虽属“生成”范畴，但其提示词解析、风格控制、局部编辑等能力依赖文本与图像的**双向语义对齐**，本质是文-图多模态协同；  
  - `qwen-audio-3.0-realtime-plus`（S2S）实现语音输入→文本理解→工具调用→语音合成的**全链路语音多模态闭环**。

- **系统级多模态支撑**：  
  - **文件管理 API** 是多模态输入的基础设施：通过 `file_id` 引用上传的图片、音频、PDF、视频等文件，供 `qwen-vl-plus`、`qwen2-audio` 等模型直接消费，解耦文件托管与模型推理；  
  - **Omni Realtime API** 定义了多模态实时交互协议：支持 PCM 音频（16 kHz）与 Base64 编码 JPG/JPEG 图像（≤1080p，≤256 KB）在同一 WebSocket 会话中交错发送，服务端按时间戳与语义上下文进行联合建模；  
  - **Video/3D/Embedding API** 提供多模态输出适配：视频生成返回 `video_url` + `audio_url`（可选），3D 生成返回 `pbr_model_url` + `rendered_image_url`，跨模态检索使用 `qwen3-vl-embedding` 统一向量空间对齐图文音视频特征。

> ⚠️ 注意：并非所有标称“多模态”的模型都支持全部模态组合。例如 `qwen3.5-omni-realtime` 支持语音+图像输入，但 `qwen3.5-omni-flash-realtime` 仅支持语音输入；`qwen-image-3.0-pro` 是文生图模型，不接受视频输入。务必查阅具体模型文档确认支持的输入/输出模态集合。

## 关键参数和配置

多模态能力的启用与控制高度依赖以下参数，开发者需严格遵循格式与约束：

- **输入结构（`messages` 或 `input`）**：  
  - 文本模型：`messages` 中 `content` 必须为字符串；  
  - 多模态模型：`messages` 中 `content` 必须为数组，每项含 `type` 字段（`"text"` / `"image_url"` / `"audio_url"` / `"video_url"`），且 `image_url` 必须指向已通过 File Management API 上传并返回 `file_id` 的资源 URL（格式：`https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/...?Expires=...`）；  
  - 视频/3D API：`input` 字段采用结构化对象，如 `{"media": [{"type": "image_url", "url": "..."}]}` 或 `{"images": [...]}`，严禁混用 `prompt` 与 `image` 等互斥字段。

- **模态声明与控制**：  
  - `modalities`（Omni Realtime）：显式指定输出模态数组，仅支持 `["text"]` 或 `["text","audio"]`；  
  - `enable_search` / `tools`：仅部分 Omni 模型（如 `qwen3.5-omni-realtime`）支持，且二者不可同时启用；  
  - `response_format={"type": "json_object"}`：多模态模型同样支持结构化输出，但需在提示词中明确要求 JSON 格式（如 “请以 JSON 格式返回…”）。

- **资源约束**：  
  - 图像：单图 ≤1080p（Omni Realtime）、≤1600万像素（视觉理解），Base64 编码时 ≤256 KB；  
  - 音频：PCM 格式，16 kHz 采样率，单次输入 ≤60 秒（Omni Realtime）；  
  - 视频：`qwen3.7-plus` 支持最长 2 小时 / 2 GB；  
  - 文件管理：单文件 ≤100 MB，`purpose` 仅支持 `"retrieval"`（用于多模态输入准备）。

## 面向开发者，简洁实用

- ✅ **必做三步**：  
  1. 用 File Management API 上传媒体文件，获取 `file_id`；  
  2. 构造符合规范的多模态 `messages` 或 `input`，确保 `type` 字段准确、URL 可访问；  
  3. 选择明确支持所需模态组合的模型（查 [模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market) 或各 API 文档）。

- ❌ **常见错误规避**：  
  - 不要将本地文件路径或未上传的公网 URL 直接填入 `image_url`；  
  - 不要对纯文本模型（如 `qwen3.7-max`）传入数组型 `content`；  
  - 不要跨地域混用 API Key、Endpoint 和模型（如北京 Key 调用新加坡模型）；  
  - 不要忽略 `X-DashScope-Async: enable` 头——所有视频、3D、部分图像 API 强制异步。

- 🛠️ **调试建议**：  
  - 使用百炼 CLI 快速验证：`bl multimodal chat --model qwen3.5-omni-plus --image ./test.jpg --prompt "描述这张图"`；  
  - 查看响应中的 `usage.input_tokens` 和 `usage.output_tokens`，多模态输入 [Token](token.md) 消耗远高于纯文本（图像按分辨率估算）；  
  - 遇到 `400 Bad Request`，优先检查 `messages` 结构、`file_id` 有效性及模型是否真支持该模态组合。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [image generation](../api/image-generation.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [preparations](../api/preparations.md)
- [model experience](../guides/model-experience.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


