# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图（T2I）、图生图（I2I）、局部编辑、背景生成、风格迁移等全栈场景。所有模型均通过统一的 HTTP API 或 DashScope SDK 调用，支持同步与异步两种模式，适用于从快速原型到高并发生产环境的各类需求。

## 支持的模型/功能

平台当前提供三大类图像模型能力：

- **通用文生图与编辑**：`qwen-image-3.0-pro`（推荐）、`wan2.6-t2i`、`z-image-turbo`、`kling/kling-v3-omni-image-generation` 等，支持多分辨率、多宽高比及中英文精准文本渲染；  
- **专业编辑与创意工具**：包括万相系列（如 `wan2.7-image-pro` 图像编辑、`wanx-x-painting` 局部重绘、`wanx-style-repaint-v1` 人像风格重绘）、Vidu 系列（`vidu/vidu-image_reference2image`）、可灵（`kling/kling-v3-image-generation`）及千问图像编辑（`qwen-image-edit-plus`）；  
- **垂直场景工具**：虚拟模特（`virtualmodel-v2`）、鞋靴试穿（`shoemodel-v1`）、AI试衣（`aitryon-plus`）、人物实例分割（`image-instance-segmentation`）、图像擦除补全（`image-erase-completion`）、创意海报生成（`wanx-poster-generation-v1`）等 [原文标题](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)。

> **注意**：部分模型（如 `wanx-x-painting`、`shoemodel-v1`、`image-erase-completion`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确建议参考 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md) 或 [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md) 获取替代方案。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | string | 必填，指定调用模型名 | `"qwen-image-3.0-pro"` |
| `size` / `resolution` / `aspect_ratio` | string | 控制输出尺寸与比例。`size` 支持像素格式（如 `"1024*1024"`）、语义规格（如 `"1K"`、`"2K"`）或宽高比（如 `"16:9"`）；不同模型支持范围不同，详见各模型文档 | `"2K"`、`"16:9"` |
| `n` | integer | 生成图片张数（1–9），部分模型固定为 1 | `2` |
| `watermark` | boolean | 是否添加水印（默认 `true`） | `false` |
| `prompt_extend` | boolean | 启用智能提示词扩展（如 `z-image-turbo`），返回优化后 [prompt](../guides/prompt.md) | `true` |

> **注意**：`size` 参数在不同模型间存在不一致定义：`wan2.6-t2i` 要求总像素在 `[1280*1280, 1440*1440]` 区间，而 `qwen-image-3.0-pro` 要求总像素在 `[512*512, 2048*2048]` 区间，使用前务必查阅对应模型文档 [原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

## 使用方式

### 接口调用模式
- **同步调用**：适用于 `wan2.6-t2i`、`qwen-image-3.0-pro`、`z-image-turbo`、`wan2.7-image-pro` 等支持新协议的模型，一次请求即返回结果，Endpoint 为 `/api/v1/services/aigc/multimodal-generation/generation`；  
- **异步调用**：适用于 `wanx-v1`、`wan2.5-i2i-preview`、`wanx-sketch-to-image-lite`、`image-out-painting` 等耗时较长的模型，需两步操作：① 创建任务获取 `task_id`；② 轮询 `task_id` 查询结果，Endpoint 因功能而异（如 `/api/v1/services/aigc/image2image/image-synthesis`）[原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。

### 地域与域名
- 所有模型必须**地域、API Key、Endpoint 三者严格匹配**，跨地域调用将失败；  
- 强烈推荐使用业务空间专属域名（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧域名 `https://dashscope.aliyuncs.com`；  
- Workspace ID 在控制台「业务空间详情」中获取，不可省略。

## 限制和注意事项

- **免费额度与计费**：多数模型提供 500 张免费额度（有效期 90 天），额度用尽后按单价计费（如 `wanx-v1` 0.16 元/张、`image-out-painting` 0.18 元/张）。计费仅针对**成功生成的输出图片**，失败或输入图片不计入 [原文标题](../../raw/model-api-reference/image-generation/image-faq.md)；  
- **图片 URL 要求**：所有输入图片 URL 必须公网可访问、无中文路径、支持 HTTP/HTTPS，否则报错 `BadRequest.InputDownloadFailed`；建议上传至 OSS 或使用临时公网 URL；  
- **限流规则**：主账号与 RAM 子账号共享限流（如 QPS/RPS 限制为 1–2），同时处理中任务数通常为 1–5；  
- **图像格式与尺寸**：输出格式以 PNG 为主（`qwen-mt-image` 为 JPG）；输入图像分辨率、大小、格式均有严格限制（如 `image-instance-segmentation` 要求 512×512 至 4096×4096 像素，≤10MB），超限将导致 400 错误。

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
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)


