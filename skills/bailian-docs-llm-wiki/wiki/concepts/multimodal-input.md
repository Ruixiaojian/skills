# 多模态输入

多模态输入是指在一次请求中同时提供两种或以上类型的数据（如文本、图像、音频、视频、3D 图像等），供模型协同理解与生成。百炼平台通过统一的 API 设计与标准化输入结构，支持跨模型、跨场景的多模态能力调用，是构建智能体、AIGC 应用和实时交互系统的核心基础能力。

## 在百炼平台的不同场景中，这个概念如何使用

多模态输入并非单一模型能力，而是贯穿多个服务层的通用输入范式，具体体现为以下四类典型模式：

- **图文混合输入**：用于视觉理解、图生文、图文联合推理等任务。例如调用 `qwen3.5-omni-plus` 进行商品图+文字描述分析；或在 `application call` 中向智能体传入含 `image_url` 的消息对象，触发 VL 模型处理。
- **图像作为主输入**：在图像/视频/3D 生成类 API 中，图像常作为核心输入（如 `image-generation` 的图生图、`video-generation` 的图生视频、`3d-generation` 的单图生3D）。此时文本提示（`prompt`）为辅助信息，图像承载主要语义。
- **多图结构化输入**：特定场景要求严格格式的多图输入，如 `3d-generation` 的 `images` 字段必须为长度为 4 的数组（前/左/后/右视角），空位用 `{}` 占位；`video-generation` 的首尾帧需分别标记 `"first_frame"` 和 `"last_frame"` 类型。
- **实时多模态流式输入**：`omni-realtime-api` 支持在 WebSocket 会话中按序发送 `input_audio_buffer.append`（PCM 音频）和 `input_image.append`（Base64 编码 JPEG 图像），实现语音+图像同步输入，适用于带视觉反馈的语音助手。

> ⚠️ 注意：并非所有模型都支持多模态输入。仅明确标注支持 VL（Vision-Language）、Omni 或对应能力的模型（如 `qwen3.5-omni-plus`、`wan2.7-image-pro`、`Tripo/Tripo-H3.1`）才可正确解析多模态 `input`；调用不支持的模型时，多余模态字段将被忽略或导致报错。

## 关键参数和配置

多模态输入的结构与约束由 `input` 字段定义，其格式因服务类型而异，开发者需严格遵循：

- **通用结构（推荐用于 `application call` 和部分 Omni 接口）**：
  ```json
  "input": [
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "请分析这张图中的产品设计亮点" },
        { "type": "image_url", "image_url": "https://example.com/product.jpg" }
      ]
    }
  ]
  ```
  - `content` 为数组，支持 `text` / `image_url` / `file_url` 混合；
  - `image_url` 必须为公网可访问 HTTPS 地址，格式为 JPEG/PNG，尺寸建议 ≤1080p（实时 API）或 ≤6000px（3D/API）；
  - 文件类输入（如 PDF、DOCX）仅在 `application call` 的智能体应用中支持，且需提前配置文件处理方式。

- **生成类 API 的专用结构（如 image/video/3d-generation）**：
  - 图像生成：`"input": { "prompt": "...", "image": "url" }`（图生图）或 `"images": [...]`（多图编辑）；
  - 视频生成：`"input": { "media": [{ "type": "image_url", "url": "..." }, { "type": "first_frame", "url": "..." }], "prompt": "..." }`；
  - 3D 生成：`"input": { "prompt": "..." }` 或 `{ "image": "url" }` 或 `{ "images": [{}, {}, {}, {}] }` —— 三者互斥，不可混用。

- **实时 API 的流式结构（`omni-realtime-api`）**：
  - 图像需 Base64 编码后通过 `input_image.append` 事件发送，大小 ≤256 KB；
  - 音频为 16 kHz PCM 流，分块发送（每块 ≤100ms）；
  - 图像必须在首次音频 buffer 发送后、会话 `session.created` 后发送，否则被丢弃。

- **必填与校验约束**：
  - 所有含图像的请求，`X-DashScope-Async: enable` 头在异步服务（video/3D）中为强制要求；
  - 多图输入（如 3D 的 `images` 数组）长度必须严格为 4，否则返回 `InvalidParameter`；
  - `application call` 中若启用多模态，智能体/工作流必须选用支持 VL 的模型（如 `qwen3.5-omni-plus`），并在应用配置中开启对应能力。

## 面向开发者，简洁实用

- ✅ **优先检查模型能力**：调用前确认模型文档是否明确支持“多模态”、“VL”、“图文输入”或“图像输入”——不要依赖模型名猜测（如 `qwen3.7-plus` 不支持图像，`qwen3.5-omni-plus` 才支持）。
- ✅ **URL 安全第一**：所有 `image_url` 必须为 HTTPS 公网地址，禁止内网、localhost 或临时签名过期链接；建议上传至 OSS 并设置公共读。
- ✅ **结构宁缺勿滥**：生成类 API（image/video/3D）的 `input` 字段严格互斥（`prompt` / `image` / `images` 三选一），多传字段将触发校验失败。
- ✅ **异步任务注意轮询**：视频、3D、部分图像工具模型（如 `wanx-x-painting`）必须异步调用，获取 `task_id` 后主动轮询，不可等待同步响应。
- ❌ **避免跨地域混用**：API Key、Endpoint URL、模型必须同地域（如华北2北京），否则多模态请求会因鉴权失败或路由错误直接拒绝。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [application call](../api/application-call.md)
- [model experience](../guides/model-experience.md)
- [omni realtime api](../api/omni-realtime-api.md)


