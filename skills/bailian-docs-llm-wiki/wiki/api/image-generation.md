# image generation

百炼平台提供多种图像生成与编辑能力，覆盖文生图（T2I）、图生图（I2I）、局部编辑、背景生成、风格迁移等场景。所有服务均基于阿里云统一的 DashScope API 框架，支持 HTTP 同步/异步调用及 SDK 集成，适用于开发者快速构建创意内容生成应用。

## 支持的模型/功能

平台当前提供三类核心图像能力：

- **通用文生图与编辑模型**：包括千问系列（`qwen-image-3.0-pro`, `qwen-image-2.0-pro`）、万相系列（`wan2.6-t2i`, `wan2.7-image-pro`）、Vidu（`vidu/vidu-image_reference2image`）、可灵（`kling/kling-v3-omni-image-generation`）和轻量级 Z-Image（`z-image-turbo`）。其中 `qwen-image-3.0-pro` 同时支持 T2I 和 I2I，而 `wan2.7-image-pro` 在文生图场景下支持 4K 输出 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
  
- **垂直场景工具模型**：涵盖涂鸦作画（`wanx-sketch-to-image-lite`）、图像局部重绘（`wanx-x-painting`）、虚拟模特（`wanx-virtualmodel`）、鞋靴模特（`shoemodel-v1`）、创意海报生成（`wanx-poster-generation-v1`）、人物实例分割（`image-instance-segmentation`）、图像擦除补全（`image-erase-completion`）等。需注意，部分工具模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`）当前仅限免费体验，额度用尽后不可调用 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

- **创意增强与辅助模型**：如 WordArt 锦书（文字变形与纹理生成）、FaceChain（人物写真定制）、AI试衣 OutfitAnyone（试衣+精修+分割组合）等，面向特定设计需求。

> **注意**：文档中 `wanx-v1`（V1版）明确标注“推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”；而 `wan2.6-t2i` 在 V2 文档中被列为推荐模型，表明 V1 已进入维护阶段，新项目应优先选用 V2 及更高版本 [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)。

## 关键参数

- **`model`**：必填字符串，指定调用模型名（如 `"qwen-image-3.0-pro"`），不同地域支持的模型列表需查阅控制台 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。
- **`size`**：图像分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）或语义值（如 `"1K"`, `"2K"`, `"4K"`）。各模型约束不同：`qwen-image-3.0-pro` 要求总像素在 512×512 至 2048×2048 之间；`wan2.6-t2i` 要求总像素在 1280×1280 至 1440×1440 之间；`vidu` 系列支持 1K/2K/4K；`z-image-turbo` 支持 512×512 至 2048×2048。
- **`n`**：生成图片张数，范围因模型而异：`qwen-image-2.0-pro` 支持 1–6 张；`kling/kling-v3-omni-image-generation` 单图模式支持 1–9 张，组图模式通过 `series_amount` 指定 2–9 张。
- **`prompt` / `input.messages`**：文本提示词。`qwen-image-3.0-pro` 和 `wan2.7-image-pro` 等新版模型采用 `messages` 数组结构（含 `role` 和 `content`），而旧版（如 `wanx-v1`）使用扁平 `prompt` 字段。
- **`X-DashScope-Async`**：HTTP 异步调用必需头，值必须为 `"enable"`；缺失将报错 `"current user api does not support synchronous calls"`。
- **`watermark`**：布尔值，控制是否添加水印（默认 `true`），部分模型（如 `wan2.7-image-pro`）支持设为 `false`。

## 使用方式

- **同步调用（推荐）**：适用于 `wan2.6`、`wan2.7-image-pro`、`qwen-image-3.0-pro`、`z-image-turbo` 等支持新版 `multimodal-generation/generation` 接口的模型。单次请求返回结果，URL 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（北京）或对应新加坡/弗吉尼亚域名。
- **异步调用**：适用于 `wanx-v1`、`wanx-sketch-to-image-lite`、`wanx-x-painting`、`image-out-painting` 等耗时较长的模型。流程分两步：
  1. `POST` 创建任务（如 `/api/v1/services/aigc/text2image/image-synthesis`），获取 `task_id`；
  2. 轮询 `GET` 查询结果（如 `/api/v1/tasks/{task_id}`），直至 `task_status` 为 `"SUCCEEDED"`，返回带有效期（通常 24 小时）的图片 URL。
- **地域与认证**：华北2（北京）、新加坡、美国（弗吉尼亚）地域拥有独立 API Key 和请求地址，**不可混用**；强烈建议使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代通用 `dashscope.aliyuncs.com`，以获得更高性能与稳定性。

## 限制和注意事项

- **免费额度与计费**：多数模型提供 500 张免费额度（如 `wanx-v1`、`wanx-sketch-to-image-lite`、`wanx-x-painting`），额度按成功生成图片计数，失败或输入错误不扣减；商业化模型（如 `wan2.6-t2i`）按张计费（0.02 元/张起），主账号统一付费，RAM 子账号不独立计量 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **图片 URL 要求**：所有需传入图片 URL 的接口（如 `image_url`、`mask_image_url`），要求链接**公网可访问、无中文字符、支持 HTTPS/HTTP**；内网或私有存储链接将导致 `"Reference image download failed"` 报错。
- **输入格式限制**：图像文件大小通常 ≤10 MB，格式支持 JPG/PNG/WEBP/BMP；分辨率有上下限（如 `image-instance-segmentation` 要求 512×512 至 4096×4096）；多图输入时，`kling/kling-v3-omni-image-generation` 最多支持 14 张参考图。
- **模型可用性**：部分模型（如 `qwen-image-3.0-pro`）处于邀测阶段，需前往模型广场申请开通；`wanx-x-painting`、`virtualmodel-v2` 等明确标注“免费体验”，无付费通道，额度用尽即不可用。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
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
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)


