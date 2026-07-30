# 多模态

多模态（Multimodal）指模型能够同时理解、生成或关联两种及以上类型的数据模态（如文本、图像、音频、视频、3D几何、结构化数据等），并在此基础上完成跨模态对齐、推理与协同生成。在百炼平台中，多模态不是单一模型能力，而是贯穿文本、视觉、音视频、3D等全栈AI服务的统一设计范式——既体现为原生支持多模态输入/输出的VL（Vision-Language）、VA（Voice-Audio）、V3D（Vision-3D）等联合模型，也体现为通过标准化API协议实现的跨模态工作流编排能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **多模态理解（Multimodal Understanding）**：以 `qwen3.7-plus`、`qwen3-vl-plus`、`qwen3.5-omni-plus` 为代表，支持单次请求中混合输入文本 + 图像（最多16张）、视频（最长2小时）、音频、PDF/OCR内容，并统一输出结构化JSON或自然语言响应。例如：上传一张产品图+一段需求描述，直接生成带规格参数的电商文案；上传会议录像+字幕文件，输出带时间戳的摘要与决策点。

- **多模态生成（Multimodal Generation）**：覆盖图像、视频、3D三大生成域，均以“多模态输入驱动单模态输出”为典型模式：
  - **文+图 → 图**：`qwen-image-3.0-pro` 支持 `messages` 中同时传入文本提示与图像URL（`{"role": "user", "content": [{"type": "text", "text": "..." }, {"type": "image_url", "image_url": "https://..."}]}`），实现精准图文混控；
  - **文+图 → 视频**：`wan2.7-t2v-*` 和 `vidu/viduq3-ad_reference2video` 允许 `input.media` 数组中混合 `text`, `image_url`, `first_frame`, `reference_image` 等多种类型，实现“文字定调 + 参考图控风格 + 首帧定构图”的三重约束；
  - **文+图 → 3D**：`Tripo/Tripo-H3.1` 的 `input` 字段可灵活切换为纯文本（`prompt`）、单图（`image`）或多图数组（`images`），系统自动识别输入模态并路由至对应生成子流程。

- **多模态编排（Multimodal Orchestration）**：通过百炼“无限画布”低代码工作流或 SDK 自定义链路，将不同模态模型串联为端到端管道。例如：`ASR → Qwen-VL图文理解 → Wan2.7-图像生成 → Pixverse-视频超清`，各节点间自动转换数据格式（语音→文本→图像→视频），开发者无需手动解析中间产物。

- **多模态交互（Multimodal Interaction）**：`qwen3.5-omni-plus-realtime` 等实时模型支持 WebRTC 音视频流 + 文本消息同步输入，实现边说话、边传图、边打字的真·多模态对话，适用于智能硬件、远程协作等场景。

> ⚠️ 注意：并非所有模型都原生支持多模态输入。例如 `wan2.6-t2i` 仅支持纯文本输入（T2I），而 `qwen-image-3.0-pro` 才是其多模态升级版。调用前请确认模型文档中标注的 `input` 类型支持范围。

## 关键参数和配置

- **统一输入结构 `input`**：  
  多模态模型要求 `input` 字段采用结构化对象而非扁平字符串。通用格式为：
  ```json
  {
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "请将这张图转为线稿风格"},
          {"type": "image_url", "image_url": "https://example.com/photo.jpg"},
          {"type": "audio_url", "audio_url": "https://example.com/voice.mp3"}
        ]
      }
    ]
  }
  ```
  各模态字段名固定（`text`/`image_url`/`audio_url`/`video_url`/`file_token`），不可自定义别名。

- **必需请求头**：  
  - `X-DashScope-Async: enable`：所有耗时 >3s 的多模态生成任务（图像/视频/3D）必须启用异步模式；  
  - `Content-Type: application/json`：严格要求 JSON 格式，不支持 `multipart/form-data`；  
  - `Authorization: Bearer $DASHSCOPE_API_KEY`：API Key 必须与业务空间地域一致（如北京地域需用华北2的Key）。

- **模型选择约束**：  
  - 模型ID必须精确匹配（含版本后缀），例如 `qwen-image-3.0-pro` ≠ `qwen-image-2.0-pro`；  
  - 多模态能力仅存在于明确标注“VL”、“Omni”、“Pro”、“3.0+”等后缀的模型，旧版模型（如 `wan2.5-i2i-preview`）不支持混合输入。

- **输入限制（硬性）**：  
  | 模态 | 限制 | 说明 |
  |------|------|------|
  | 图像URL | ≤20MB，公网可访问，格式 JPG/PNG | 不支持本地文件或私有OSS直传（需先上传至公开CDN） |
  | 视频URL | ≤500MB，H.264编码，MP4/WebM | `qwen3.7-plus` 视频理解支持最长2小时，但生成类模型（如 `happyhorse-1.1-t2v`）仅支持≤10秒输入 |
  | 多图输入 | `images` 数组长度=4（Tripo多图生3D），或 0–14 张（Vidu参考生图） | 缺失视角必须填 `{}` 占位，不可省略 |

- **输出控制**：  
  - `parameters.watermark: false`：关闭水印（部分模型默认开启）；  
  - `parameters.format: "glb"` / `"mp4"` / `"png"`：显式指定输出格式（若模型支持多格式）；  
  - `parameters.texture: false` & `pbr: false`：Tripo模型中用于返回无贴图基础网格（`base_model_url`）。

## 面向开发者，简洁实用

- ✅ **第一步：选对模型** —— 查阅 [模型体验指南](guides/model-experience.md) 中“视觉理解”“多模态生成”章节，认准 `qwen3-vl-*`、`qwen-image-3.0-pro`、`qwen3.5-omni-plus` 等标识；  
- ✅ **第二步：构造标准 input** —— 始终用 `messages[].content[]` 数组承载多模态元素，按 `type` 区分，勿拼接字符串；  
- ✅ **第三步：强制异步** —— 所有生成类多模态请求必须加 `X-DashScope-Async: enable`，同步调用会直接报错；  
- ✅ **第四步：处理长链路** —— 异步任务返回 `task_id` 后，轮询 `GET /api/v1/tasks/{task_id}`，成功响应中的 `output.results[0].xxx_url` 即为结果地址（注意有效期：图片24h，3D模型2h，视频72h）；  
- ❌ **避坑提醒**：不要复用文本模型的 `input.prompt` 字段调用多模态模型；不要在 `wan2.6-t2i` 上尝试传 `image_url`；不要跨地域混用 API Key 与 WorkspaceId。

## 关联主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [model experience](../guides/model-experience.md)
- [use cases](../guides/use-cases.md)
- [release notes](../guides/release-notes.md)


