# 多模态能力

多模态能力指百炼平台支持同时理解、生成或处理多种类型数据（如文本、图像、视频、音频、3D 模型等）的统一技术能力，其核心在于模型能跨模态对齐语义、联合推理并协同输出，而非简单拼接单模态服务。

## 在百炼平台的不同场景中，这个概念如何使用

多模态能力在百炼平台体现为**输入模态可混合、输出模态可组合、底层模型可统一调度**，具体落地于以下四类典型场景：

- **多模态理解（Multimodal Understanding）**：  
  如 `qwen3.5-omni-plus`、`qwen3.7-plus` 等旗舰模型支持**文本 + 图像 + 视频 + 音频**混合输入（单次请求最多含 1 张图/1 段视频/1 段音频），自动完成跨模态内容解析、问答、摘要与结构化提取。适用于智能客服、教育批改、工业质检等需综合感知的场景。

- **多模态生成（Multimodal Generation）**：  
  平台提供按输入模态自动路由的生成能力：  
  - 文本输入 → 图像/视频/3D/音乐（如 `wan2.7-image-pro` 文生图、`vidu/viduq3-turbo_text2video` 文生视频、`Tripo/Tripo-H3.1` 文生3D、`fun-music-v1` 文生歌）；  
  - 图像输入 → 图像/视频/3D（如 `wanx-x-painting` 局部重绘、`wan2.7-i2v-2026-04-25` 图生视频、`Tripo/Tripo-P1.0` 单图生3D）；  
  - 视频/音频输入 → 视频/音频（如 `videoretalk` 口型同步、`pixverse/pixverse-lipsync` 嘴型驱动）；  
  - 多图输入 → 3D（`Tripo` 多视角重建）或视频（`pixverse/pixverse-c1-kf2v` 首尾帧插值）。

- **多模态编辑与增强（Multimodal Editing）**：  
  支持跨模态条件控制的精细化操作：  
  - 图像+文本 → 局部重绘（`wanx-x-painting`）、风格迁移（`wanx-style-repaint-v1`）、背景生成（`wanx-background-generation-v2`）；  
  - 视频+文本 → 风格重绘（`video-style-transform`）、超分增强（`pixverse/pixverse-upscale`）；  
  - 图像+3D参数 → AI试衣（`aitryon-plus` 输入人像+服装图+姿态参数）；  
  - 音频+文本 → S2S语音合成（`qwen-audio-3.0-realtime-plus` 支持带情感提示词的语音生成）。

- **多模态工作流编排（Multimodal Workflow Orchestration）**：  
  在百炼控制台可视化工作流中，可自由串联不同模态节点（如：OCR识别图片文字 → 文本模型润色 → 文生图生成海报 → 视频模型转为宣传短片），各节点间自动完成格式转换与上下文透传，无需开发者手动解析/序列化中间结果。

> ⚠️ 注意：多模态能力**不等于“所有模型都支持所有模态”**。实际调用时，必须严格匹配模型能力边界——例如 `qwen3.7-plus` 支持图文音视频理解，但**不支持生成视频**；`vidu/viduq3-turbo_text2video` 仅支持文生视频，**不接受图像输入**。请始终以[模型市场](https://bailian.console.aliyun.com)中标注的“输入模态”和“输出模态”为准。

## 关键参数和配置

多模态能力的启用与控制依赖以下通用参数与头信息，开发者需按需设置：

| 参数/头 | 类型 | 必填 | 说明 | 典型值示例 |
|---------|------|------|------|------------|
| `model` | string | ✅ | 指定具备目标多模态能力的模型 ID，**不可复用单模态模型** | `"qwen3.5-omni-plus"`, `"wan2.7-image-pro"`, `"vidu/viduq3-turbo_text2video"` |
| `input` | object | ✅ | 结构化承载多模态输入，**字段名由模型约定，非固定** | `{ "messages": [...], "image": "url" }`（图文理解）<br>`{ "prompt": "...", "media": [{"type":"image_url","url":"..."}] }`（图生图） |
| `X-DashScope-Async: enable` | header | ⚠️（异步必需） | 所有耗时 >10s 的多模态任务（视频/3D/复杂编辑）**必须携带**，否则返回 400 | `"enable"` |
| `parameters.watermark` | boolean | ❌（推荐显式设） | 控制生成内容是否添加平台水印，生产环境建议设为 `false` | `false` |
| `parameters.size` / `parameters.resolution` / `parameters.duration` | string/number | ❌（按模态选填） | 分辨率（图像/视频）、时长（视频）、面数（3D）等输出规格，**各模型约束不同，需查对应文档** | `"1024*1024"`, `"720P"`, `5`（秒） |

- **输入结构关键规则**：  
  - 文本输入统一用 `messages` 数组（role/content）或 `prompt` 字符串，旧模型兼容 `prompt`，新模型（如 `qwen-image-3.0-pro`）强制要求 `messages`；  
  - 多媒体输入必须通过 `media` 数组（视频/图生视频）或独立字段（`image`, `video`, `audio`）传递，URL 需公网可访问且 HTTPS；  
  - Tripo 的 `prompt`/`image`/`images` **三者严格互斥**，混用将报错；  
  - Fun-Music 的 `prompt` 与 `lyrics` **至少传其一**。

- **地域与认证强约束**：  
  - 多模态能力**按模型绑定地域**：`qwen3.5-omni-plus` 全地域可用，`Tripo` 仅限华北2（北京），`kling` 系列仅限北京/新加坡；  
  - API Key **必须与调用地域一致**，跨地域调用会返回 `401 Unauthorized`；  
  - 推荐使用**业务空间专属域名**（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`），避免通用域名性能波动。

## 面向开发者，简洁实用

- ✅ **快速验证多模态能力**：用 `qwen3.5-omni-plus` 模型发起一次图文混合请求（`input.messages` 含文本 + `input.image` 含 URL），5 秒内即可获得结构化理解结果，是验证端到端链路最简路径。  
- ✅ **生成类任务选型口诀**：  
  > “文生什么？→ 选对应 T2X 模型（T2I/T2V/T23D）；  
  > 图生什么？→ 选 I2X 模型（I2I/I2V/I23D）；  
  > 要快？→ 优先 `turbo`/`flash`/`lite` 后缀模型；  
  > 要精？→ 选 `pro`/`ultra`/`max` 后缀模型，并配高 `geometry_quality` 或 `texture_quality`。”  
- ✅ **避坑清单**：  
  - 不要假设 `qwen3.7-plus` 能生成视频——它只理解，不生成；  
  - 不要省略 `X-DashScope-Async: enable` 头调用 Tripo 或 Vidu，否则必失败；  
  - 不要复用同一 API Key 调用跨地域模型，务必在控制台按地域分别开通服务并获取 Key；  
  - 提示词（[prompt](../guides/prompt.md)）质量直接影响多模态效果，推荐参考 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 和 [文生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [model experience](../guides/model-experience.md)
- [use cases](../guides/use-cases.md)


