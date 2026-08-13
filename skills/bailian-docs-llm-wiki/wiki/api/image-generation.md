# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图（T2I）、图生图（I2I）、局部编辑、背景生成、风格迁移等全栈场景。所有模型均通过统一的 DashScope API 接口调用，支持 HTTP 同步/异步及 SDK 集成，适用于电商、设计、内容创作等开发者场景。

## 支持的模型/功能

平台当前提供三大类图像模型能力：

- **通用文生图与编辑**：`qwen-image-3.0-pro`（推荐）、`wan2.7-image-pro`、`z-image-turbo` 等支持高质量 T2I 与 I2I，其中 `qwen-image-3.0-pro` 明确支持总像素 512×512 至 2048×2048 的自由分辨率 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；`wan2.7-image-pro` 在文生图场景下支持 4K 输出 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。
  
- **垂直场景专用模型**：包括虚拟模特（`virtualmodel-v2`）、鞋靴试穿（`shoemodel-v1`）、创意海报（`wanx-poster-generation-v1`）、人物写真（`FaceChain`）、AI试衣（`aitryon-plus`）等，均聚焦特定业务需求，如 `virtualmodel-v2` 支持 2048 像素短边输出与多长宽比选择 [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)。

- **图像处理与增强工具**：覆盖局部重绘（`wanx-x-painting`）、画面扩展（`image-out-painting`）、擦除补全（`image-erase-completion`）、实例分割（`image-instance-segmentation`）、图像翻译（`qwen-mt-image`）等，例如 `qwen-mt-image` 可精准保留原始排版完成中英日韩等语种互译 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

> **注意**：部分模型（如 `wanx-virtualmodel`、`shoemodel-v1`、`wanx-poster-generation-v1`、`image-erase-completion`、`wanx-x-painting`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确建议使用 `qwen-image-edit` 或 `wanx2.1-imageedit` 替代 [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)、[鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)、[创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)、[图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)、[万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

## 关键参数

所有模型共用核心参数结构，关键字段如下：

- `model`：必填字符串，指定模型名称（如 `"qwen-image-3.0-pro"`、`"wan2.7-image-pro"`），需与所选地域匹配。
- `input`：必填对象，结构因任务类型而异：
  - 文生图：`{"messages": [{"role": "user", "content": [{"text": "prompt"}]}]}`（推荐）或旧式 `{"prompt": "..."}`；
  - 图生图/编辑：`{"messages": [{"role": "user", "content": [{"image": "url"}, {"text": "instruction"}]}]}`；
  - 单图工具（如擦除、分割）：`{"image_url": "..."}`。
- `parameters`：可选对象，常用参数包括：
  - `size`：字符串，指定分辨率（如 `"1024*1024"`、`"2K"`），部分模型（如 `qwen-image-3.0-pro`）允许在 512×512–2048×2048 范围内自由设置 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；
  - `n`：整数，生成图片张数（通常为 1–9）；
  - `watermark`：布尔值，控制是否添加水印（默认 `true`）；
  - `aspect_ratio` / `wh_ratios`：字符串，指定宽高比（如 `"1:1"`、`"竖版"`）；
  - `resolution`：字符串，用于 `kling` 系列模型（如 `"1k"`）。

## 使用方式

### 地域与认证
- **必须同地域**：模型、API Key、Endpoint URL 必须属于同一地域（北京、新加坡、弗吉尼亚等），跨地域调用将失败 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **推荐域名**：华北2（北京）和新加坡地域应优先使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，性能与稳定性更优 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

### 调用模式
- **同步调用**：适用于 `wan2.6`、`wan2.7-image-pro`、`qwen-image-3.0-pro`、`z-image-turbo` 等支持新协议的模型，单次请求返回结果，Endpoint 为 `/multimodal-generation/generation`。
- **异步调用**：适用于 `wanx-v1`、`wanx-sketch-to-image-lite`、`image-out-painting` 等耗时较长的模型，流程为两步：
  1. 创建任务（POST 到 `/image-synthesis` 或 `/generation` 等路径），响应含 `task_id`；
  2. 轮询 `task_id` 查询状态，成功后返回图片 URL（有效期 24 小时）。

### 请求头
- `Authorization`: `Bearer $DASHSCOPE_API_KEY`（必填）；
- `Content-Type`: `application/json`（必填）；
- `X-DashScope-Async`: `"enable"`（异步调用必填，缺失将报错 `"current user api does not support synchronous calls"`）。

## 限制和注意事项

- **限流策略**：主账号与 RAM 子账号共享限流，常见为 QPS/RPS ≤ 2，同时处理任务数 ≤ 1–5，具体见各模型文档 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **图片 URL 要求**：输入图片 URL 必须公网可访问、无中文路径、支持 HTTP/HTTPS，否则报错 `"Reference image download failed"` [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **免费额度**：所有模型均提供 500 张免费额度（部分如 `shoemodel-v1` 为 500 张），额度按成功生成图片计数，失败或输入无效不扣减，有效期 90 天 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **分辨率约束**：不同模型有严格像素范围限制（如 `qwen-image-3.0-pro` 为 512²–2048²，`wan2.6-t2i` 为 1280²–1440²），超出将被拒绝 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
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
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)


