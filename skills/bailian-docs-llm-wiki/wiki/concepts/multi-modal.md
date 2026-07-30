# 多模态

多模态（Multimodal）指模型能够同时理解、生成或关联多种类型数据（如文本、图像、音频、视频等）的能力。在百炼平台中，多模态不是单一模型，而是一套贯穿模型选型、输入组织、参数配置与输出处理的统一能力范式，支撑跨模态感知、推理与生成任务。

## 在百炼平台的不同场景中，这个概念如何使用

多模态能力在百炼平台中按使用方式分为三类典型场景，开发者需根据目标选择对应模型与调用路径：

- **多模态理解（Multimodal Understanding）**  
  用于图文/音视频联合分析，如文档解析、视觉问答、视频摘要。需选用 `qwen3-vl-plus`、`qwen3.7-plus`（支持图像/视频输入）、`qwen3.5-ocr` 等 VL（Vision-Language）系列模型；输入格式为 `{"messages": [{"role": "user", "content": [{"type": "text", "text": "..."}, {"type": "image_url", "image_url": {"url": "..."}}]}]}`，支持单图或多图。

- **多模态生成（Multimodal Generation）**  
  用于文生图、图生图、文生视频、语音+文本同步输出等。需选用 `qwen-image-3.0-pro`、`wan2.7-image-pro`、`happyhorse-1.1-t2v`、`qwen3.5-omni-plus-realtime` 等专用生成模型；输入以 `prompt` 或 `messages` 结构承载文本指令，并可附加图像 URL、Base64 编码图像（≤256 KB，≤1080p）或音频 PCM 数据（16 kHz）。

- **多模态向量与排序（Multimodal Embedding & Rerank）**  
  用于跨模态检索与语义对齐，如“用一张产品图搜索相似文案”或“用语音描述召回相关视频”。需选用 `qwen3-vl-embedding`（支持文本+图像/视频混合输入，可启用 `enable_fusion=true` 生成融合向量）或 `qwen3-vl-rerank`（支持 query/document 任意模态组合，如文本 query + 图像 document）。

> ⚠️ 注意：并非所有模型或 API 路径均默认支持多模态。例如：
> - `application call` 中，仅当应用底层模型为 VL 系列（如 `qwen-vl-plus`）且配置为“自定义处理”时，才支持图像输入；
> - `realtime api` 中，`qwen3.5-omni-plus-realtime` 支持图像+语音+文本输入，但 `qwen-audio-3.0-realtime-plus` 仅支持语音，不属多模态范畴；
> - `vector and sort` 中，`text-embedding-v4` 仅支持文本，`qwen3-vl-embedding` 才是真正的多模态向量模型。

## 关键参数和配置

以下参数在多模态场景中高频出现，需严格按规范设置：

| 参数 | 位置 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | 请求体/URL | 必填，必须为明确标注多模态能力的模型 ID | `"qwen3-vl-plus"`, `"qwen-image-3.0-pro"`, `"qwen3-vl-embedding"` |
| `input.messages` | 请求体 | 多模态理解/生成的标准输入结构，`content` 为数组，含 `text`/`image_url`/`audio_url` 等对象 | `[{"role":"user","content":[{"type":"text","text":"描述这张图"},{"type":"image_url","image_url":{"url":"https://..."}}]}]` |
| `imageList`（工作流） | 应用节点入参 | 工作流中图像输入的专用变量名，值为 Base64 字符串数组 | `["data:image/jpeg;base64,/9j..."]` |
| `enable_fusion` | 请求体（`qwen3-vl-embedding`） | 控制是否将多模态输入融合为单个向量（`true`）或分别输出各模态向量（`false`） | `true` |
| `modalities` | `realtime api` 的 `session.update` 事件 | 指定输出模态组合，决定服务端返回内容类型 | `["text", "audio"]`（支持文本+音频流式同步输出） |
| `X-DashScope-Async` | 请求头 | 多模态生成/向量批处理等长耗时任务必需，设为 `"enable"` 启用异步模式 | `"enable"` |

- **图像输入限制**：JPG/JPEG 格式，分辨率 ≤1080p，Base64 编码后 ≤256 KB；URL 形式需确保公网可访问且无防盗链。
- **音频输入限制**：PCM 格式，16-bit，16 kHz 单声道，时长 ≤60 秒。
- **文件输入（仅智能体应用）**：需在控制台配置“全文引用”或“切片检索”，API 中通过 `input.files` 传入文件 token（非原始文件）。

## 面向开发者，简洁实用

- ✅ **快速验证**：在控制台「应用调试」或「模型体验」页面，直接粘贴带 `image_url` 的 `messages` 示例，无需写代码即可测试多模态理解效果。
- ✅ **SDK 推荐**：Python 开发优先使用 `dashscope` SDK（原生支持 `messages` 多模态结构）；若复用 OpenAI 生态，确保 `openai>=1.0.0` 并使用兼容 endpoint（`/compatible-mode/v1/chat/completions`），注意 `input` 字段需为 `messages` 数组。
- ✅ **错误排查重点**：
  - 返回 `400 Bad Request` 且提示 `invalid input format` → 检查 `messages` 结构是否为数组、`content` 是否为对象数组、`type` 字段是否拼写正确（如 `image_url` 不是 `image_url`）；
  - 返回 `404 Model not found` → 确认 `model` ID 完全匹配（区分大小写、含版本号如 `-plus`），且该模型在所选地域可用；
  - 图像无法识别 → 先用 `qwen3.5-ocr` 单独测试图像可读性，排除模糊、遮挡或格式问题。
- ✅ **性能提示**：多模态理解（如 `qwen3-vl-plus`）延迟高于纯文本模型，建议对高并发场景启用 `stream=true` 流式响应，或预热会话（`session_id` 复用）降低首字延迟。

## 关联主题页

- [application call](../api/application-call.md)
- [image generation](../api/image-generation.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [model experience](../guides/model-experience.md)
- [use cases](../guides/use-cases.md)
- [vector and sort](../api/vector-and-sort.md)


