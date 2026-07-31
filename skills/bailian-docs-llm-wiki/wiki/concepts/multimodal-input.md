# 多模态输入

多模态输入是指在一次请求中同时提供两种或以上类型的数据（如文本、图像、音频、视频、3D 图像等），供模型联合理解与处理的能力。百炼平台通过统一的 API 设计与模型架构，原生支持跨模态信息融合，使智能体、生成模型及实时交互系统能够基于多源信号完成复杂任务。

## 在百炼平台的不同场景中，这个概念如何使用

- **应用调用（Application Call）**：智能体或工作流可接收混合输入，例如文本指令 + 一张商品图（用于视觉问答），或文本 + 多个 PDF 文件（用于全文检索）。需在应用配置中启用对应能力（如 VL 模型、文件解析模式），并在 `input` 字段中按规范组织数据结构（如 `{"prompt": "...", "imageList": [...], "fileList": [...]}`）。

- **图像生成（Image Generation）**：支持文生图（T2I）、图生图（I2I）、局部重绘等，输入可为纯文本 [prompt](../guides/prompt.md)、单张/多张图像 URL，或图文混合（如 `"请将这张图中的天空替换为星空"` + `image_url`）。部分编辑类模型（如 `wanx-x-painting`）还要求额外提供 mask 图像。

- **3D 生成（3D Generation）**：Tripo 模型严格区分输入模态：仅支持三选一——纯文本（`prompt`）、单图（`image`）或四视角图组（`images` 数组，长度固定为 4）。多模态在此场景体现为“模态互斥但能力并存”，开发者需根据任务目标选择最适配的输入形式。

- **视频生成（Video Generation）**：输入结构高度灵活，典型组合包括：
  - 文本 + 首帧图（I2V）
  - 首帧图 + 尾帧图（KF2V）
  - 多张参考图 + 文本描述（R2V）
  - 视频 URL + 音频 URL（对口型）
  所有输入均通过 `input.media` 数组声明，每项含 `type`（如 `"image_url"`、`"video_url"`、`"audio_url"`）和 `url`。

- **Omni 实时 API（Realtime）**：面向语音交互场景，强制要求音频输入（16kHz PCM），并可选择性追加图像（JPG/JPEG）作为上下文。图像必须在音频流开始后、会话首次 `response.text.delta` 之前发送，且仅被用于增强当前轮次理解（如“描述我刚拍的这张照片”）。

- **通用模型调用（Model Experience）**：旗舰模型（如 `qwen3.7-plus`、`qwen3.5-omni-plus`）支持文本、图像、视频、音频任意组合输入。例如向 `qwen3.7-plus` 提交一段视频 URL + 问题文本，即可执行视频内容理解；向 `qwen3.5-omni-plus` 提交语音流 + 截图，可同步完成 ASR、OCR 与语义推理。

## 关键参数和配置

- **输入结构统一约定**：  
  所有多模态输入均通过 `input` 字段承载，其值为对象（非字符串），具体子字段依场景而异：
  - `prompt` / `text`：文本内容（必填或条件必填）  
  - `imageList` / `images` / `media`：图像数组，每项为 `{ "url": "https://..." }` 或 base64 编码字符串（需带 `data:image/jpeg;base64,` 前缀）  
  - `fileList`：文件数组（仅智能体支持），每项为 `{ "url": "oss://..." }` 或上传后的 `file_token`  
  - `audio_url` / `video_url`：音视频资源公网可访问 URL  
  - `base_image_url` + `mask_image_url`：局部编辑必需的双图输入  

- **模型兼容性硬约束**：  
  - 图像理解/生成必须选用 VL 或 multimodal 模型（如 `qwen3.7-plus`、`qwen-image-3.0-pro`、`wan2.7-image-pro`）；纯文本模型（如 `qwen3.7-flash`）拒绝图像输入。  
  - 3D 生成仅支持 `Tripo/*` 系列，且 `input` 中 `prompt`/`image`/`images` 三者互斥，同时传入将返回 `400 Bad Request`。  
  - Omni Realtime 要求 `input_audio_format` 固定为 `"pcm"`，图像格式仅支持 JPG/JPEG，不支持 PNG 或 WebP。

- **地域与域名要求**：  
  多模态能力普遍依赖业务空间（Workspace）专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），尤其在图像、视频、3D、Omni 等高带宽场景。跨地域调用（如北京 Workspace 的 API Key 用于新加坡 Endpoint）将失败。

- **安全与合规提示**：  
  所有外部 URL 必须可公开访问（HTTP/HTTPS），内网地址、需鉴权的私有链接、临时签名过期链接均不可用。百炼不缓存用户原始媒体文件，但生成结果 URL 默认带水印（可通过 `parameters.watermark: false` 关闭，部分模型不支持）。

## 关联主题页

- [application call](../api/application-call.md)
- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [model experience](../guides/model-experience.md)


