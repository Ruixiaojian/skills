# 多模态

多模态是指模型能够同时理解、生成或处理多种类型的数据（如文本、图像、音频、视频、3D 网格等），并在不同模态间建立语义关联与联合推理的能力。在百炼平台中，“多模态”既是一种能力范式，也是一类模型的统称——它不局限于单一输入/输出组合，而是覆盖从跨模态理解（如图文问答）、多模态生成（如文生图、音画同步）到全模态交互（如语音+图像+文本实时对话）的完整技术栈。

## 在百炼平台的不同场景中，这个概念如何使用

多模态能力在百炼平台中按**任务类型**和**交互形态**分层落地，开发者需根据具体需求选择对应模型与协议：

- **多模态理解（Multimodal Understanding）**  
  适用于图文/音视频内容解析、结构化提取等场景。典型模型：`qwen3.7-plus`、`qwen3.5-ocr`、`qwen3.7-flash`。支持输入 `messages` 中混合 `text` 和 `image_url`（或 `video_url`、`audio_url`），模型返回文本响应；要求 `content` 字段为数组格式，元素类型严格限定为 `text`/`image_url`/`video_url`/`audio_url` 等合法模态对象。

- **多模态生成（Multimodal Generation）**  
  指从一种模态生成另一种或多种模态内容。包括：  
  - *文生图/图生图*：`qwen-image-3.0-pro`、`wan2.7-image-pro`，输入 `prompt` 或 `input.image`，输出图像 Base64 或 URL；  
  - *文生视频/图生视频*：`wan2.7-t2v`、`kling/kling-v3-*`，输入 `prompt` + `media` 数组（含 `image_url`/`first_frame`/`last_frame`），输出视频 URL；  
  - *文生3D/图生3D*：`Tripo/Tripo-H3.1`，输入 `prompt` 或 `input.image`/`input.images`（固定长度为 4 的数组），输出 GLB 模型 URL；  
  - *语音+文本+图像联合生成*：`qwen3.5-omni-realtime`，通过 WebSocket 实时接收 PCM 音频与 JPG 图像（≤256 KB Base64），同步输出文本流与 24 kHz PCM 音频流。

- **全模态交互（Omni-Modal Interaction）**  
  支持多通道并发输入与多模态协同输出，面向低延迟智能体场景。代表模型：`qwen3.5-omni-realtime`（WebSocket）、`qwen3.5-omni-plus`（HTTP）。支持同时输入语音、图像、文本指令，并可启用工具调用（`tools`）、联网搜索（`enable_search`）、声音复刻（`voice` 参数）等高级能力，输出模态可配置为 `["text"]` 或 `["text", "audio"]`。

> ⚠️ 注意：纯文本模型（如 `qwen3.7-max`）**拒绝** `content` 为数组的请求；而多模态模型若传入非法模态类型（如 `content` 中含 `pdf_url`），将直接报错 `InvalidParameter`。务必按模型文档校验输入结构。

## 关键参数和配置

多模态能力的启用与行为控制依赖以下核心参数（非全局统一，需按模型类型区分）：

| 场景 | 参数名 | 类型 | 说明 | 示例值 |
|------|--------|------|------|--------|
| **通用输入约束** | `content`（messages 内） | array | 多模态输入必须为数组，元素为 `{ "type": "text", "text": "..." }` 或 `{ "type": "image_url", "image_url": { "url": "https://..." } }` | `[{"type":"text","text":"描述这张图"},{"type":"image_url","image_url":{"url":"https://x.jpg"}}]` |
| **图像输入** | `size` / `aspect_ratio` / `resolution` | string | 控制生成图像尺寸，取值因模型而异（如 `qwen-image-3.0-pro`: `"1024*1024"`；`kling`: `"2k"`） | `"16:9"`、`"2k"` |
| **3D 输入** | `input.images` | array[4] | 多图生3D强制要求长度为 4 的数组，空视角填 `{}` | `[{"type":"image_url","url":"front.jpg"},{},{"type":"image_url","url":"back.jpg"},{}]` |
| **实时交互** | `modalities` | array | Omni-Realtime API 输出模态开关 | `["text", "audio"]` |
| **异步必需头** | `X-DashScope-Async` | header | 所有图像、视频、3D 生成接口**必须**携带此 Header，值为 `"enable"` | `"enable"` |
| **URL 安全访问** | `X-DashScope-OssResourceResolve` | header | 当输入为临时 OSS URL 时，需添加此 Header 启用资源解析 | `"enable"` |

- ✅ **必配项**：多模态模型调用前，务必确认 `API Key` 已开通对应模型权限，且地域一致（如 `qwen-mt-image` 仅限北京）；  
- ❌ **互斥项**：`enable_search` 与 `tools` 在 Omni-Realtime 中互斥；`pbr: true` 会强制启用贴图（忽略 `texture: false`）；  
- 📏 **尺寸限制**：图像输入 ≤256 KB（Base64 编码后），视频 ≤2 GB，单图 ≤20 MB（3D），分辨率均需在模型允许范围内。

## 面向开发者，简洁实用

- **快速验证是否支持多模态**：检查模型 ID 是否含 `-vl-`（Vision-Language）、`-omni-`（Omni）、`-image-`、`-video-`、`-3d-` 等标识，或查阅 [模型体验指南](model-experience.md) 中“全模态”“视觉理解”“图像生成”等分类；
- **调试技巧**：  
  - 使用 `dashscope` SDK 的 `MultimodalConversation` 类（Python）或 `MultimodalClient`（Java）简化 `content` 数组构造；  
  - CLI 调用图像生成时，用 `bl image generate --prompt "..." --size 1024x1024` 自动处理格式；  
  - 实时 API 开发建议先用 `session.update` 设置 `modalities` 和 `voice`，再发送 `input_audio_buffer.append`，避免图像晚于音频触发失败；
- **避坑清单**：  
  - 不要对 `qwen3.7-max` 传 `content` 数组；  
  - 不要遗漏 `X-DashScope-Async: enable`（否则报错 `current user api does not support synchronous calls`）；  
  - 不要传 `input.images` 长度 ≠ 4（Tripo 3D 将返回 `InvalidParameter`）；  
  - 图像 URL 必须以 `http://`、`https://` 或 `data:` 开头，本地路径用 `file://`。

多模态不是功能叠加，而是语义贯通。在百炼平台，它意味着一次请求即可完成“看图说话、听音绘图、言出成片”，开发者只需聚焦业务逻辑，底层跨模态对齐、[Token](token.md) 化与联合建模均由平台透明承载。

## 关联主题页

- [preparations](../api/preparations.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [model experience](../guides/model-experience.md)


