# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图（T2I）、图生图（I2I）、局部重绘、背景生成、扩图、风格迁移、AI试衣等数十种专业场景。所有模型均通过统一的 HTTP API 或 DashScope SDK 调用，支持同步与异步两种模式，适配不同耗时需求。

## 支持的模型/功能

平台当前提供以下主流图像模型与能力：

- **通用文生图**：`qwen-image-3.0-pro`（推荐）、`wan2.6-t2i`、`z-image-turbo`、`kling/kling-v3-image-generation`  
- **图生图与编辑**：`qwen-image-3.0`、`wan2.7-image-pro`、`wan2.5-i2i-preview`、`qwen-image-edit` 系列  
- **专用工具类**：  
  - 局部重绘：`wanx-x-painting`（[万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)）  
  - 涂鸦作画：`wanx-sketch-to-image-lite`（[万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)）  
  - 图像擦除补全：`image-erase-completion`（[图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)）  
- **创意增强类**：虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）、人物写真（FaceChain）、创意海报（`wanx-poster-generation-v1`）、WordArt锦书文字生成  
- **辅助能力**：人物实例分割（`image-instance-segmentation`）、图像背景生成（`wanx-background-generation-v2`）、AI试衣（`aitryon-plus`）  

> **注意**：部分模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确建议迁移到 [千问-图像编辑](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide) 或 [万相2.1图像编辑](https://help.aliyun.com/zh/model-studio/wanx-image-edit) 替代方案（见[万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)、[虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)等文档）。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | string | 必填，指定模型名称 | `"qwen-image-3.0-pro"`, `"wan2.6-t2i"` |
| `size` / `resolution` / `aspect_ratio` | string | 控制输出分辨率或宽高比。不同模型约束不同：<br>- `qwen-image-3.0-pro`：总像素需在 `512*512` 至 `2048*2048` 之间<br>- `wan2.6-t2i`：支持 `1024*1024`、`2K`、`4K` 等符号化尺寸<br>- `kling` 系列：支持 `"1k"`、`"2k"`、`"4k"` 及 `"16:9"`、`"1:1"` 等宽高比 | `"1024*1024"`, `"2K"`, `"16:9"` |
| `n` | integer | 生成图片张数（若模型支持） | `1`（默认），`2`（部分模型支持最多9张） |
| `watermark` | boolean | 是否添加水印（部分模型支持） | `false` |
| `prompt_extend` | boolean | 启用智能提示词扩展（如 `z-image-turbo`） | `true` |
| `X-DashScope-Async` | header | 异步调用必需头字段，值必须为 `"enable"` | `"enable"` |

> **注意**：`size` 参数在不同模型中语义不一致——`wan2.6-t2i` 支持 `"1024*1024"` 和 `"2K"` 符号，而 `kling` 系列使用 `"resolution"` 字段配合 `"aspect_ratio"`；`qwen-image-3.0-pro` 则要求显式指定总像素范围。开发者需严格按各模型文档定义传参，不可跨模型复用参数格式。

## 使用方式

### 调用协议
- **同步调用**：适用于 `wan2.6-t2i`、`qwen-image-3.0`、`z-image-turbo`、`wan2.7-image-pro` 等低延迟模型，单次请求返回结果。Endpoint 为：  
  `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（北京）  
  `POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（新加坡）
- **异步调用**：适用于耗时较长的模型（如局部重绘、虚拟模特、海报生成），需两步操作：  
  1. 创建任务获取 `task_id`（Endpoint 因模型而异，例如 `image2image/image-synthesis` 或 `background-generation/generation`）  
  2. 轮询 `GET /api/v1/tasks/{task_id}` 获取结果（`task_id` 有效期 24 小时）

### 地域与认证
- **地域强绑定**：API Key、Endpoint URL、Workspace ID 必须同地域（北京/新加坡/弗吉尼亚）。跨地域调用必然失败（见[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)）。
- **推荐域名**：优先使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧域名 `dashscope.aliyuncs.com`。

## 限制和注意事项

- **免费额度与计费**：所有模型均提供 500 张免费额度（90 天有效期），主账号与 RAM 子账号共享。超出后按模型单价计费（如 `wanx-v1` 0.16元/张，`image-out-painting` 0.18元/张），仅对成功生成的图片计费（见[常见问题](../../raw/model-api-reference/image-generation/image-faq.md)）。
- **图片URL要求**：输入图片 URL 必须公网可访问、无中文路径、支持 HTTP/HTTPS 协议；OSS 等云存储需配置公开读权限（见[常见问题](../../raw/model-api-reference/image-generation/image-faq.md)中“图像无法下载”章节）。
- **限流策略**：主账号与 RAM 子账号共用 QPS/RPS 限制（常见为 2 QPS），同时处理中任务数上限通常为 1–5（依模型而定）。
- **输入格式限制**：  
  - 图像尺寸：多数模型要求单边 ≥512px 且 ≤4096px（如 `image-instance-segmentation`）  
  - 图像格式：PNG/JPEG/WEBP/BMP/AVIF（`shoemodel-v1` 明确支持 AVIF）  
  - 文件大小：通常 ≤10MB（`shoemodel-v1` 要求 <5MB）  
- **错误处理**：HTTP 错误码 `400 BadRequest.InputDownloadFailed` 表示图片 URL 不可达；`401 InvalidApiKey` 表示密钥无效或地域不匹配。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
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
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)


