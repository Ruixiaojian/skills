# 多模态

多模态（Multimodal）指模型能够同时理解、生成或关联两种及以上类型的数据模态（如文本、图像、音频、视频、3D几何、结构化数据等），并在此基础上完成跨模态对齐、推理与协同生成。在百炼平台中，多模态不是单一能力，而是贯穿模型设计、API协议与工程实践的核心范式——既体现为专用多模态大模型（如 Qwen-VL、Qwen-Omni）的原生能力，也体现为统一 API 层对异构输入输出的标准化封装。

## 在百炼平台的不同场景中，这个概念如何使用

- **统一 API 协议层**：所有多模态能力（图像生成、视频生成、3D生成、实时全模态对话等）均通过 `/api/v1/services/aigc/multimodal-generation/` 或 `/api/v1/services/aigc/video-generation/` 等统一路径接入，共用 `X-DashScope-Async: enable` 异步头字段和 `task_id` 任务生命周期管理，屏蔽底层模态差异，降低开发者集成成本。

- **输入模态灵活组合**：  
  - 文生图（T2I）、文生视频（T2V）、文生3D：以 `prompt`（文本）为核心输入；  
  - 图生图（I2I）、图生视频（I2V）、单图/多图生3D：以 `image` 或 `images`（图像 URL 数组）为主输入，可叠加 `prompt` 进行语义引导；  
  - 视频编辑、参考生视频（R2V）、数字人驱动：支持 `media` 数组混合输入（`type: "image_url"` / `"video_url"` / `"audio_url"`），实现多源模态对齐；  
  - Omni 实时 API：支持 WebSocket 流式输入 PCM 音频 + JPG 图像（Base64 编码），按事件时序提交，实现音画同步理解。

- **输出模态可声明控制**：  
  - 生成类 API（图像/视频/3D）通过 `parameters` 控制分辨率（`resolution`）、宽高比（`aspect_ratio`）、贴图开关（`texture`, `pbr`）、时长（`duration`）等模态属性；  
  - 实时 API（Omni/Realtime）通过 `session.update` 的 `modalities: ["text", "audio"]` 显式声明期望输出模态组合，服务端据此启用对应解码与合成模块；  
  - 全模态模型（如 `qwen3.5-omni-plus`）支持同一请求中返回结构化文本 + 合成语音流，无需拆分为多次调用。

- **模型能力分层复用**：  
  - 基础多模态理解：`qwen3.7-plus`、`qwen3.5-omni-plus` 等通用模型支持文本+图像/视频输入，输出文本响应，适用于图文问答、视频摘要；  
  - 专用多模态生成：`qwen-image-3.0-pro`（图像）、`Tripo/Tripo-H3.1`（3D）、`pixverse/pixverse-c1-t2v`（视频）等聚焦单一模态生成，但输入仍需文本或图像引导；  
  - 端到端多模态交互：`qwen3.5-omni-realtime` 支持语音输入 → 文本理解 → 工具调用 → 文本+语音双路输出，形成闭环交互链路。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 | 典型值 |
|------|----------|------|------|--------|
| `input.media` | 视频/3D/编辑类 API | array[object] | 多模态输入容器，每项含 `type`（`"image_url"`/`"video_url"`/`"audio_url"`）和 `url` | `[{"type":"image_url","url":"https://..."}]` |
| `input.prompt` | 文生类（T2X） | string | 文本提示词，最长1024字符，中英文均可 | `"一只穿宇航服的橘猫在火星上奔跑"` |
| `input.image` / `input.images` | 图生类（I2X） | string / array | 单图 URL 或固定长度为4的多视角图像数组（前/左/后/右） | `"https://..."` / `[{"type":"jpeg","file_token":"..."}, {}, {"type":"png","file_token":"..."}, {}]` |
| `modalities` | Omni/Realtime 实时 API | array[string] | **必填**，声明输出模态组合，仅支持 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `parameters.resolution` / `aspect_ratio` | 图像/视频/3D生成 | string | 控制输出尺寸，语义因模型而异：<br>- 图像：`"1024*1024"`、`"2K"`、`"16:9"`<br>- 视频：`"720P"`、`"1280*720"`、`"16:9"`<br>- 3D：无此参数 | `"1024*1024"`, `"16:9"`, `"720P"` |
| `parameters.duration` | 视频生成 | number | 视频时长（秒），范围通常为 2–10，部分模型支持至30秒 | `5.0` |
| `parameters.texture` / `pbr` | 3D生成 | boolean | 联动控制是否生成带贴图的 PBR 模型；设 `false` 时需同时设 `pbr: false` 才获得无贴图基础模型 | `true`, `false` |
| `X-DashScope-Async` | 所有多模态生成类 API | header | **必需头字段**，值必须为 `"enable"`，标识异步调用模式 | `"enable"` |

> ⚠️ 注意：  
> - `prompt` / `image` / `images` 三者互斥，不可共存于同一请求（3D生成明确校验，其他场景亦同）；  
> - `modalities` 不支持 `["audio"]` 单独选项，仅 `["text"]` 和 `["text","audio"]` 合法；  
> - 分辨率参数（`size`/`resolution`/`aspect_ratio`）在不同模型间不兼容，严禁跨模型复用参数格式。

## 面向开发者，简洁实用

- **选型优先看输入输出**：先确定你的输入是什么（纯文本？图+文？音+图？）、期望输出是什么（一张图？一段视频？文本+语音流？），再匹配对应能力矩阵中的模型，而非仅看模型名。  
- **异步是默认，同步需确认**：除文本生成、轻量图像生成（如 `z-image-turbo`）外，所有多模态生成任务（图像编辑、视频、3D、数字人）**必须**使用异步模式（`X-DashScope-Async: enable`），否则直接报错。  
- **地域强绑定**：Tripo 3D 仅限华北2（北京）；视频/图像生成推荐使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），避免跨地域失败。  
- **URL 是关键基础设施**：所有图像、视频、音频输入必须为公网可访问的 HTTPS URL（非本地文件路径）；生成结果中的 `pbr_model_url`、`rendered_image_url` 等链接有效期仅 2 小时，务必及时下载持久化。  
- **调试从最小可行输入开始**：测试图生视频时，先用单张清晰 JPG + 简短 [prompt](../guides/prompt.md)；测试 Omni 实时时，先禁用 `tools` 和 `enable_search`，验证基础音画流通路。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [model experience](../guides/model-experience.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


