# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图（T2I）、图生图（I2I）、局部重绘、风格迁移、背景生成、人物写真、AI试衣等数十种专业场景。所有模型均通过统一的 HTTP API 或 DashScope SDK 调用，支持华北2（北京）、新加坡、美国（弗吉尼亚）等多地域部署，并推荐使用业务空间专属域名以获得更高性能与稳定性。开发者需先开通对应模型服务并配置 API Key，方可调用。

## 支持的模型/功能

百炼平台当前提供三大类图像能力：

- **通用文生图与编辑模型**：包括千问系列（`qwen-image-3.0-pro`、`qwen-image-2.0-pro`、`qwen-image-edit-max`）、万相系列（`wan2.7-image-pro`、`wan2.6-t2i`、`wanx2.1-t2i-turbo`）、Z-Image（`z-image-turbo`）及可灵（`kling/kling-v3-omni-image-generation`）、Vidu（`vidu/vidu-image_reference2image`）等。其中 `qwen-image-3.0-pro` 同时支持 T2I 与 I2I，而 `wan2.7-image-pro` 在文生图场景下支持 4K 输出 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

- **垂直场景专用模型**：覆盖电商与设计需求，如虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）、创意海报生成（`wanx-poster-generation-v1`）、图像背景生成（`wanx-background-generation-v2`）、人像风格重绘（`wanx-style-repaint-v1`）、涂鸦作画（`wanx-sketch-to-image-lite`）、图像局部重绘（`wanx-x-painting`）等。部分模型（如 `wanx-x-painting`、`wanx-poster-generation-v1`）当前仅限免费体验，额度用尽后不可调用 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

- **图像处理与增强工具**：包括人物实例分割（`image-instance-segmentation`）、图像擦除补全（`image-erase-completion`）、图像画面扩展（`image-out-painting`）、AI试衣（`aitryon-plus`、`aitryon-refiner`）、FaceChain 人物写真、WordArt 锦书文字艺术等。这些工具多采用异步调用模式，适用于需高精度掩码或复杂后处理的场景 [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)。

> **注意**：文档中存在模型地域支持不一致的矛盾信息。例如，`wan2.6-t2i` 明确支持美国（弗吉尼亚）地域 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)，但 `qwen-image-3.0-pro` 和 `kling` 系列仅声明支持华北2（北京）和新加坡地域。实际调用前请务必在[百炼控制台模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)确认目标地域可用模型。

## 关键参数

所有图像 API 均通过 `model`、`input` 和 `parameters` 三部分组织请求体。核心参数如下：

- **`model`**：必填字符串，指定具体模型名称（如 `"qwen-image-2.0-pro"`、`"wan2.7-image-pro"`），不同模型对参数支持度不同。
- **`input.prompt` / `input.messages`**：文本提示词。`qwen-image-3.0-pro`、`wan2.7-image-pro` 等新模型要求使用 `messages` 数组格式（含 `role` 和 `content`），而旧模型（如 `wanx-v1`）仍支持扁平 `prompt` 字段。
- **`parameters.size`**：输出分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）或预设值（如 `"1K"`、`"2K"`、`"4K"`）。各模型约束不同：`qwen-image-3.0-pro` 要求总像素在 512×512 至 2048×2048 之间；`wan2.6-t2i` 要求总像素在 1280×1280 至 1440×1440 之间；`z-image-turbo` 同样支持 512×512 至 2048×2048。
- **`parameters.n`**：生成图片张数，范围通常为 1–6（`kling` 支持 1–9），部分模型（如 `qwen-image-max`、`qwen-mt-image`）固定为 1。
- **`parameters.watermark`**：布尔值，控制是否添加水印，默认 `true`，多数生产场景建议设为 `false`。
- **`parameters.prompt_extend`**：布尔值，启用后模型将返回优化后的提示词及推理过程（如 `z-image-turbo`、`qwen-image-3.0-pro`），但会增加响应时间。

## 使用方式

图像 API 分为**同步调用**与**异步调用**两类，选择依据模型类型与耗时预期：

- **同步调用**：适用于响应快（通常 < 10s）的模型，如 `wan2.6-t2i`（V2版）、`z-image-turbo`、`qwen-image-3.0-pro` 及 `wan2.7-image-pro`。请求地址统一为 `POST https://{WorkspaceId}.<region>.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`，一次请求即返回结果。示例见 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

- **异步调用**：适用于耗时较长（通常 1–2 分钟）的模型，如 `wanx-v1`、`wanx-x-painting`、`kling`、`Vidu`、`image-out-painting` 等。流程分两步：
  1. **创建任务**：向 `.../generation` 或 `.../image-synthesis` 等端点发送请求，携带 `X-DashScope-Async: enable` 头，获取 `task_id`；
  2. **轮询结果**：用 `task_id` 定期调用查询接口（如 `GET /api/v1/tasks/{task_id}`），直至状态为 `SUCCEEDED` 并返回图像 URL（有效期 24 小时）。

所有调用均需设置标准请求头：`Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`。强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代通用域名（`dashscope.aliyuncs.com`），以提升稳定性和性能。

## 限制和注意事项

- **地域与密钥隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key 与请求地址**完全独立，不可混用**。跨地域调用将导致鉴权失败。`qwen-mt-image` 等部分模型仅限华北2（北京）地域 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

- **URL 访问要求**：所有输入图片 URL（`image_url`、`sketch_image_url`、`mask_image_url` 等）必须为**公网可访问、支持 HTTP/HTTPS 协议的地址**。私有存储（如内网 OSS）需配置公网访问权限或使用临时 URL。报错 `"Reference image download failed"` 通常源于此 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

- **免费额度与计费**：多数模型提供 500 张/90 天免费额度（主账号与 RAM 子账号共享），额度用尽后按单价计费（如 `wanx-v1` 0.16 元/张、`wanx-style-repaint-v1` 0.12 元/张）。部分模型（如 `wanx-x-painting`、`shoemodel-v1`）明确标注“仅供免费体验”，额度用尽后不可付费续用。

- **图像格式与尺寸**：输出格式统一为 PNG（`qwen-mt-image` 例外，输出 JPG）。输入图像需满足格式（JPG/PNG/WEBP/BMP）、大小（通常 ≤10MB）、分辨率（如 `image-instance-segmentation` 要求 512×512 至 4096×4096）等硬性限制，否则直接报错。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)


