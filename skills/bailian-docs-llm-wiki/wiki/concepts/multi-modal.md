# 多模态

多模态（Multimodal）指模型能够同时理解、生成和推理多种类型数据的能力，包括文本、图像、音频、视频等不同模态的信息，并在它们之间建立语义关联。在百炼平台中，“多模态”不是单一模型能力标签，而是贯穿模型设计、API 协议与调用规范的核心架构范式——它定义了输入内容结构、参数约束逻辑及服务端处理流程。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型选型层面**：  
  多模态能力由模型本身决定。`qwen3.5-omni-plus`、`qwen3.7-plus`、`qwen-image-3.0-pro`、`qwen-audio-3.0-realtime-plus` 等均为原生多模态模型，支持混合输入（如图文并存、音画协同）；而 `qwen3.7-max`（纯文本）、`text-embedding-v2`（仅文本）则明确不支持非文本 `content` 元素。调用前必须确认模型是否已开通且具备对应模态支持（如未开通 `qwen3.5-omni-plus` 将返回 `Model not exist`）。

- **API 输入结构层面**：  
  多模态模型要求 `messages` 中的 `content` 字段为对象数组，每个元素需指定 `type`（如 `"text"`、`"image_url"`、`"video_url"`、`"audio_url"`），不可为纯字符串。例如：
  ```json
  {
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "描述这张图"},
          {"type": "image_url", "image_url": "https://example.com/1.jpg"}
        ]
      }
    ]
  }
  ```
  纯文本模型若传入此类结构，将直接报错 `InvalidParameter`。

- **实时交互场景（Omni Realtime API）**：  
  `qwen3.5-omni-realtime` 系列通过 WebSocket 支持语音流 + 文本 + 图像（≤1080p，Base64 ≤256KB）同步输入，并实时输出文本与 PCM 音频（24 kHz）。此时“多模态”体现为事件驱动的动态模态组合（如 `input_audio_buffer.append` + `input_image.append`），而非静态请求体。

- **生成类任务（图像/视频/3D）**：  
  虽然图像生成（`qwen-image-3.0-pro`）、视频生成（`wan2.7-i2v`）、3D 生成（`Tripo/Tripo-P1.0`）各自独立建模，但其输入均遵循多模态语义——`input` 字段可包含 `prompt`（文本）、`image_url`（图像）、`media` 数组（含 `image_url`/`first_frame`/`last_frame` 等）等异构字段，构成跨模态条件控制。

- **向量与重排序场景**：  
  `qwen3-vl-embedding` 和 `qwen3-vl-rerank` 是典型的多模态嵌入/排序模型，能将图文对统一映射到联合语义空间，支撑跨模态检索（如“用图片搜相似文本”或“用文本搜相关图片”）。

## 关键参数和配置

- **`content` 结构（必需）**：  
  多模态模型的 `messages[].content` 必须是数组，每个元素含 `type` 和对应字段（`text`、`image_url`、`video_url`、`audio_url`）。URL 必须公网可访问，且符合各模态尺寸/时长限制（如图像 ≤1600 万像素，视频 ≤2 小时，音频 ≤3 小时）。

- **`modalities`（Realtime API 专用）**：  
  控制会话支持的输入/输出模态组合，值为 `["text"]` 或 `["text", "audio"]`（默认），不支持纯音频输出。

- **`enable_search` / `tools`（互斥）**：  
  在 Omni Realtime 场景中，启用联网搜索或工具调用需显式设置，二者不可共存，且仅部分多模态模型（如 `qwen3.5-omni-realtime`）支持。

- **`parameters` 中的模态相关字段**：  
  - 图像生成：`size`（分辨率）、`n`（张数）、`watermark`；  
  - 视频生成：`duration`（秒）、`resolution`、`aspect_ratio`；  
  - 3D 生成：`texture_quality`、`geometry_quality`；  
  - 所有生成类 API 均需 `X-DashScope-Async: enable` 头（异步模式）。

- **地域与 Key 绑定**：  
  多模态模型（尤其视频、3D、音乐）常有强地域约束（如 3D 仅限华北2），API Key 必须与模型开通地域一致，否则请求失败。

## 面向开发者，简洁实用

- ✅ **必做**：调用前查模型市场确认开通状态；检查 `messages.content` 是否为合法对象数组；确保 URL 公网可达且格式合规。
- ❌ **禁做**：对纯文本模型传 `image_url`；在 `qwen-omni-turbo-realtime` 中尝试修改 `temperature` 等采样参数；跨地域混用 Key 与模型。
- ⚠️ **注意**：CLI 工具 `bl` 默认支持全模态命令，但 SDK 调用需严格按模型文档构造 `content`；异步任务（视频/3D）务必及时下载结果 URL（有效期仅 2 小时）。
- 🔧 **调试技巧**：所有失败请求记录 `Request ID`；`InvalidParameter` 错误优先检查 `content` 结构与模态兼容性；`Model not exist` 错误请前往模型市场手动开通。

## 关联主题页

- [preparations](../api/preparations.md)
- [model experience](../guides/model-experience.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


