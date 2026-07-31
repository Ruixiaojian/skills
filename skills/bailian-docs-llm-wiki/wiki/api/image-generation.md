# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图（T2I）、图生图（I2I）、局部重绘、风格迁移、背景生成、扩图、擦除补全等数十种功能。所有模型均通过统一的 HTTP API 接口调用，支持同步与异步两种模式，并已适配 DashScope SDK（Python/Java）。开发者需先开通对应模型服务、获取 API Key 并配置环境变量，再根据模型特性选择地域专属域名发起请求。

## 支持的模型/功能

百炼平台当前提供三类图像能力模型：

- **通用文生图模型**：包括 `qwen-image-*` 系列（如 `qwen-image-2.0-pro`、`qwen-image-max`）、`wan2.6-t2i`、`z-image-turbo`、`qwen-image-3.0-pro` 等，支持多分辨率、多张数输出及复杂文本渲染；其中 `qwen-image-3.0-pro` 同时支持 T2I 和 I2I [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **专业编辑与工具模型**：覆盖图像局部重绘（`wanx-x-painting`）、涂鸦作画（`wanx-sketch-to-image-lite`）、虚拟模特（`wanx-virtualmodel`）、鞋靴试穿（`shoemodel-v1`）、人像风格重绘（`wanx-style-repaint-v1`）、图像画面扩展（`image-out-painting`）、图像背景生成（`wanx-background-generation-v2`）、图像擦除补全（`image-erase-completion`）等垂直场景 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **创意生成与辅助模型**：如创意海报生成（`wanx-poster-generation-v1`）、人物实例分割（`image-instance-segmentation`）、FaceChain 人物写真、WordArt 锦书文字艺术、AI试衣 OutfitAnyone 等，部分模型处于免费体验阶段，额度用尽后不可调用 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。

> **注意**：`wanx-v1`（V1版）文档明确提示“推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”，而 `wan2.6-t2i` 及更高版本（如 `wan2.7-image-pro`）已支持同步调用，V1/V2 模型在调用协议和参数结构上存在显著差异，不可混用。

## 关键参数

- **`model`**：必填，指定模型名称（如 `"qwen-image-2.0-pro"`），需与所选地域支持的模型列表一致。
- **`input`**：必填，结构因任务类型而异：
  - 文生图：`{"messages": [{"role": "user", "content": [{"text": "prompt"}]}]}`（推荐）或旧式 `{"prompt": "..."}`；
  - 图生图/编辑：`{"messages": [...]}` 中可混合 `{"text"}` 与 `{"image": "url"}`；
  - 局部重绘/擦除：需提供 `base_image_url` + `mask_image_url`；
  - 虚拟模特/鞋靴试穿：需 `template_image_url` + `shoe_image_url` 等专用字段。
- **`parameters`**：可选，常用参数包括：
  - `size`：字符串，如 `"1024*1024"`、`"2K"`、`"4K"`；部分模型（如 `wan2.5-i2i-preview`）默认 `1280*1280`，`qwen-image-2.0-pro` 默认 `2048*2048`；
  - `n`：整数，生成图片张数（`qwen-image-2.0-pro` 支持 1–6 张，`z-image-turbo` 固定为 1 张）；
  - `aspect_ratio`：字符串，如 `"1:1"`、`"16:9"`（`kling/kling-v3-image-generation` 支持）；
  - `watermark`：布尔值，控制是否添加水印（默认 `true`）；
  - `prompt_extend`：布尔值，启用提示词优化（增加响应时间）；
  - `thinking_mode`：布尔值，开启智能思考（仅 `wan2.7-image-pro` 支持）。

## 使用方式

- **同步调用**：适用于 `wan2.6-t2i`、`qwen-image-3.0-pro`、`z-image-turbo`、`wan2.7-image-pro` 等新版模型，单次请求直接返回图像 Base64 或 URL。Endpoint 为 `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**：适用于绝大多数模型（如 `wanx-v1`、`wanx-x-painting`、`image-out-painting`），需两步操作：
  1. 发起 `POST /api/v1/services/.../generation`（或 `/image-synthesis` 等）创建任务，**必须携带 `X-DashScope-Async: enable` 请求头**，返回 `task_id`；
  2. 轮询 `GET /api/v1/tasks/{task_id}` 获取结果，图像 URL 有效期 24 小时。
- **地域与域名**：华北2（北京）、新加坡地域**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），不可混用 `dashscope.aliyuncs.com`；美国（弗吉尼亚）等地域仍使用通用域名。各模型对地域支持不一，调用前须查阅 [各地域支持的模型列表](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。

## 限制和注意事项

- **计费与额度**：多数模型按成功生成图片张数计费（如 `wanx-v1` 0.16元/张），部分模型限时免费或仅限免费体验（如 `wanx-x-painting`、`shoemodel-v1`、`wanx-poster-generation-v1`），额度用尽后不可调用 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **图片URL要求**：输入图片 URL 必须公网可访问、无中文路径、支持 HTTP/HTTPS；若下载失败，将返回 `BadRequest.InputDownloadFailed` 错误。
- **图像规格限制**：
  - 分辨率：总像素通常需在 `512*512` 至 `2048*2048` 之间（`wan2.6-t2i` 要求 `1280*1280`–`1440*1440`，`wan2.7-image-pro` 文生图支持 4K）；
  - 格式：PNG 为主，少数模型支持 JPG（如 `qwen-mt-image`）；
  - 大小：单图建议 ≤5MB（`shoemodel-v1`）或 ≤10MB（`image-erase-completion`）。
- **异步调用强制要求**：所有异步接口**必须设置 `X-DashScope-Async: enable`**，否则报错 “current user api does not support synchronous calls”；未设置该头将导致请求失败。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)


