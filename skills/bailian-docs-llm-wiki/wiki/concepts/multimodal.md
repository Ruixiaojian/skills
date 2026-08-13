# 多模态

多模态是指模型能够同时理解、生成和关联多种类型数据（如文本、图像、音频、视频、3D 网格等）的能力。在百炼平台中，多模态不是单一功能，而是贯穿于多个模型系列与 API 范式的核心能力范式——它体现为输入模态的混合支持、输出模态的灵活组合，以及跨模态语义对齐的底层建模能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **文本+图像理解与生成**：`qwen-vl` 是百炼原生支持的多模态大模型，通过 DashScope 原生接口接收 `messages` 中混合的 `text` 和 `image_url` / `image`（base64）内容，实现图文问答、视觉推理、图像描述等任务；注意：[OpenAI 兼容接口](openai-compatibility.md)（如 `/v1/chat/completions`）**不支持**该能力，必须使用 DashScope 原生 endpoint。

- **实时语音+文本+图像交互**：Qwen-Omni-Realtime 系列（如 `qwen3.5-omni-plus-realtime`）将多模态扩展至流式实时场景。支持同步输入 PCM/WAV 音频、JPG/JPEG 图像（≤256KB base64）、文本指令，并可按需配置输出模态组合（如 `["text", "audio"]`），适用于智能座舱、会议助手等低延迟闭环系统。

- **图像生成与编辑**：`qwen-image-3.0-pro` 等模型通过 `input.messages` 接收“文本提示 + 图像”联合输入（如图生图、局部重绘），实现跨模态条件控制；其 `parameters.size`、`aspect_ratio` 等参数直接影响多模态输出的空间结构一致性。

- **视频生成与驱动**：文生视频（T2V）、图生视频（I2V）、首尾帧生成等均依赖模型对文本语义与视觉时序的联合建模。例如 `wan3.0-video` 接收 `{"prompt": "...", "media": [{"type": "image_url", "url": "..."}]}`，即显式声明文本与图像两种输入模态的协同关系。

- **3D 生成**：Tripo 模型支持文生3D（text→3D）、单图生3D（image→3D）、多视角图生3D（4-view images→3D），本质是将非结构化信号（语言/像素）映射到三维几何空间，是多模态向空间维度的延伸；`pbr` 和 `texture_quality` 参数则控制生成结果在材质（物理渲染）与几何（网格精度）两个子模态上的表现。

> ✅ 关键共识：百炼平台中，“多模态”始终以 **明确的模态标识**（如 `{"type": "image_url"}`, `"audio.input.format"`）和 **结构化输入格式**（如 `messages` 中含 `content: [{text: "..."}, {image: "..."}]`）为前提，不支持隐式或自由格式的混合输入。

## 关键参数和配置

| 场景 | 参数名 | 类型 | 说明 | 注意事项 |
|------|--------|------|------|----------|
| **通用多模态输入** | `messages[].content[]` | array of objects | 每项为 `{text: string}` 或 `{image: string}`（URL/base64）或 `{audio: string}`（base64） | 必须严格按对象结构传入，不可拼接为字符串；`qwen-vl` 仅支持 `image`，Omni 支持 `audio`+`image`+`text` 混合 |
| **实时多模态输出控制** | `modalities` | `["text"]` \| `["text","audio"]` \| `["text","audio","video"]` | 指定服务端应返回的模态组合 | `video` 输出需模型显式支持（当前 Omni 系列暂未开放）；`audio` 输出需配套配置 `voice` 和 `audio.output.format` |
| **图像/视频分辨率控制** | `parameters.size` / `parameters.resolution` / `parameters.aspect_ratio` | string | 控制输出图像/视频的空间规格 | `qwen-image-3.0-pro` 支持 `"1024*1024"` 自由设定；`wan3.0-video` 支持 `"720P"`、`"16:9"` 等语义化值 |
| **3D 生成质量控制** | `parameters.pbr`, `parameters.texture`, `parameters.geometry_quality` | boolean / string | 分别控制 PBR 材质启用、贴图生成、网格面数精度 | `pbr=true` 会强制启用贴图，若需无贴图模型，必须同时设 `texture: false` 且 `pbr: false` |

## 面向开发者，简洁实用

- ✅ **首选 DashScope 原生接口**：所有多模态能力（除 Omni Realtime WebSocket 外）均仅在 DashScope 原生 endpoint（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/...`）可用，[OpenAI 兼容接口](openai-compatibility.md)不支持。
- ✅ **输入必须结构化**：不要将图片 base64 直接塞进 `content: "data:image/png;base64,..."` 字符串；务必使用 `content: [{"type": "image_url", "url": "..."}, {"type": "text", "text": "..."}]` 格式（图像生成类）或 `content: [{"image": "..."}, {"text": "..."}]`（Qwen-VL 类）。
- ✅ **检查模型兼容性**：`qwen-vl` 支持图文，`qwen3.5-omni-*` 支持音图文，`qwen-image-*` 支持图文生成，`Tripo/*` 支持文/图→3D——没有“万能多模态模型”，请按任务选型。
- ⚠️ **地域强绑定**：Omni Realtime、Video、3D 等服务均要求 API Key、Endpoint、模型开通地域三者严格一致（如华北2），跨地域调用必失败。
- ⚠️ **异步任务注意轮询**：Video 和 3D 生成均为异步，需用 `task_id` 主动轮询或配置回调，勿等待 HTTP 响应体直接返回结果。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


