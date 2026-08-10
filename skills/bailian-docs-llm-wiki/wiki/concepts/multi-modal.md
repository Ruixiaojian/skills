# 多模态

多模态（Multimodal）指模型能够同时理解、生成或处理多种类型数据（如文本、图像、音频、视频、3D 模型等）的能力。在百炼平台中，多模态不是单一模型的标签，而是贯穿模型选型、API 设计与应用构建的核心能力范式——它体现为输入/输出模态的组合灵活性、跨模态语义对齐能力，以及统一调度框架下的协同调用支持。

## 在百炼平台的不同场景中，这个概念如何使用

多模态能力在百炼平台中以三种典型方式落地，开发者需根据任务目标主动选择适配路径：

- **多模态理解（Multimodal Understanding）**：  
  使用 `qwen3.7-plus`、`qwen3.7-flash` 等通用大模型，通过单次请求传入文本 + 图片/视频/音频 URL，模型返回结构化分析结果（如图文摘要、OCR识别、视频关键帧描述、语音转写+意图识别）。适用于客服工单解析、教育课件问答、电商图文审核等场景。注意：视觉输入分辨率影响 [Token](token.md) 消耗，计算公式为 `h×w/(32×32)+2`，建议预处理至合理尺寸。

- **多模态生成（Multimodal Generation）**：  
  调用专用生成类 API（如图像、视频、3D、音乐），其输入本身即为多模态组合：  
  - 图生图/图生视频：`input.media` 数组可混合 `image_url` 与 `video_url`；  
  - 参考生视频（R2V）：支持同时传入参考图、参考视频、音频文件及文本提示词；  
  - Tripo 3D：严格支持 `prompt`（文本）、`image`（单图）或 `images`（4视角图数组）三者之一，但每种输入模式均触发跨模态重建（文本→几何+纹理，图像→三维拓扑+材质）。  
  所有生成类 API 均需显式声明 `X-DashScope-Async: enable`，返回 `task_id` 后轮询结果。

- **多模态协同工作流（Multimodal Orchestration）**：  
  在工作流应用或高代码服务中，将不同模态能力串联：例如先用 `qwen3.5-omni-plus` 解析用户上传的“产品说明书PDF+实物照片”，提取需求后调用 `wan2.7-t2v` 生成宣传视频，再用 `pixverse/pixverse-lipsync` 合成口型同步语音。此时，多模态体现为模型间的数据格式契约（如统一使用公网可访问的 HTTPS URL 作为媒体输入）和错误码一致性（如 `BadRequest.InputDownloadFailed` 通用于所有媒体下载失败场景）。

> ⚠️ 关键约束：**所有多模态输入的媒体资源（图片、视频、音频、3D图）必须为公网可访问的 HTTP/HTTPS URL，且不含中文字符或特殊编码；OSS/Bucket 链接需开放匿名读权限。**

## 关键参数和配置

| 参数 | 作用 | 典型取值 | 注意事项 |
|------|------|----------|----------|
| `input.media`（视频/参考生视频） | 统一媒体输入容器，支持混合类型 | `[{"type":"image_url","url":"https://..."}, {"type":"video_url","url":"https://..."}]` | 数组长度无硬限制，但总大小 ≤2GB；`type` 必须精确为 `image_url` / `video_url` / `audio_url` |
| `input.prompt`（文生类） | 文本提示词，驱动跨模态生成 | `"一只穿唐装的机械猫在故宫屋顶奔跑，4K超现实风格"` | 中英文混合支持；Tripo 最大1024字符；万相/VIDU/Kling 等建议≤512字符以保质量 |
| `texture` & `pbr`（Tripo 3D） | 控制是否生成贴图及PBR材质 | `texture: false, pbr: false` → 返回无贴图基础模型 | 二者必须同设为 `false` 才生效；设 `pbr: true` 时自动启用贴图 |
| `enable_thinking`（Qwen3系列） | 开启深度推理链，提升多模态指令遵循能力 | `true` | 仅 Qwen3 及以上模型支持；增加响应延迟，但显著改善复杂图文指令（如“对比两张发票差异并生成报销说明”） |
| `format`（Fun-Music） | 输出音频格式 | `"mp3"`（默认）或 `"wav"` | 影响文件体积与音质，`wav` 无损但体积大，适合后期编辑 |

## 面向开发者，简洁实用

- ✅ **首选统一入口**：多模态任务优先使用 `qwen3.5-omni-plus`（HTTP/WebSocket）或 `qwen3.7-plus`（文本+视觉），避免碎片化调用；专用生成任务（如高清图、长视频、高精度3D）再切至对应 API。
- ✅ **URL 是生命线**：所有媒体输入必须是**公网可直连、无重定向、无鉴权头**的 HTTPS URL；本地文件请先上传至 OSS 并设置 `public-read` 权限。
- ✅ **异步是铁律**：图像、视频、3D、音乐生成一律异步；同步调用仅适用于纯文本或轻量图文理解（如 `qwen3.7-flash` 处理单张图+短文本）。
- ✅ **地域强绑定**：API Key、Endpoint、模型服务三者必须同地域（北京/新加坡/弗吉尼亚）；跨地域调用必报错，无降级方案。
- ❌ **勿混用旧域名**：务必使用业务空间专属域名 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，禁用 `dashscope.aliyuncs.com` —— 即使参数完全正确，旧域名也会导致鉴权失败。

## 关联主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [model experience](../guides/model-experience.md)
- [start using](../guides/start-using.md)


