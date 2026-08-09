# image generation

百炼平台提供多种图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、背景生成、局部重绘等全链路场景。所有服务均基于统一的[多模态](../concepts/multimodal.md)推理架构，支持同步/异步调用，并通过业务空间专属域名提升稳定性与性能。开发者需按地域获取对应 API Key 并配置环境变量，方可调用。

## 支持的模型/功能

平台当前提供三大类图像模型体系：

- **通用文生图与编辑模型**：包括千问系列（`qwen-image-*`、`qwen-image-edit-*`、`qwen-image-3.0-*`）、万相系列（`wan2.6-t2i`、`wan2.7-image-pro`、`wan2.5-i2i-preview`）、Z-Image（`z-image-turbo`）及 Vidu（`vidu/vidu-image_reference2image` 等）。其中 `qwen-image-3.0-pro` 和 `wan2.7-image-pro` 支持文生图与图生图双模态任务 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)，而 `wan2.6-t2i` 仅支持纯文本输入 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

- **垂直场景专用模型**：覆盖创意工具与行业应用，如可灵（`kling/kling-v3-*`）支持分镜组图生成；虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）、AI试衣（`aitryon-plus`）面向电商；人像风格重绘（`wanx-style-repaint-v1`）、创意海报（`wanx-poster-generation-v1`）、图像背景生成（`wanx-background-generation-v2`）等聚焦特定任务。

- **辅助与基础能力模型**：包括人物实例分割（`image-instance-segmentation`）、图像擦除补全（`image-erase-completion`）、涂鸦作画（`wanx-sketch-to-image-lite`）、图像翻译（`qwen-mt-image`）等，多为免费体验模型，额度用尽后不可调用 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

> **注意**：部分模型存在地域限制。例如 `qwen-mt-image`、`wanx-x-painting`、`wanx-poster-generation-v1` 等明确限定仅华北2（北京）地域可用，且必须使用该地域 API Key；而 `wan2.6-t2i`、`qwen-image-3.0-pro` 等则支持北京、新加坡、弗吉尼亚等多地域部署，但需确保模型、Endpoint 与 API Key 地域一致 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

## 关键参数

核心参数按功能维度归类如下：

- **分辨率与尺寸**：  
  - `size`：支持字符串格式（如 `"1024*1024"`、`"1K"`、`"2K"`）或宽高比（如 `"16:9"`），具体取值范围因模型而异。`qwen-image-3.0-pro` 要求总像素在 `512*512` 至 `2048*2048` 之间；`wan2.6-t2i` 限定为 `[1280*1280, 1440*1440]`；`kling` 系列仅支持预设档位（`1k`/`2k`/`4k`）。  
  - `aspect_ratio`：仅 `kling` 和 `virtualmodel-v2` 显式支持，后者可选 `2:1`、`16:9`、`1:1` 等 8 种比例。  
  - `resolution`：`kling` 和 `vidu` 模型专用参数，值为 `"1k"`/`"2k"`/`"4k"`。

- **输出控制**：  
  - `n`：生成图像张数，范围通常为 `1–9`（`kling`）、`1–6`（`qwen-image-*`）、`1–4`（`shoemodel-v1`），默认为 `1`。  
  - `watermark`：布尔值，控制是否添加水印（`wan2.7-image-pro`、`vidu` 等支持）。  
  - `prompt_extend`：启用智能提示词扩展（`z-image-turbo`、`wan2.6-image` 支持），返回优化后提示词但增加延迟。

- **任务模式**：  
  - `X-DashScope-Async: enable`：**所有 HTTP 异步调用必需**，缺失将报错 `"current user api does not support synchronous calls"` [涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)。  
  - `result_type`：`kling/kling-v3-omni-image-generation` 特有，设为 `"series"` 可生成保持角色连续性的分镜组图。  
  - `generate_mode`：`wanx-poster-generation-v1` 支持 `"generate"`/`"sr"`/`"hrf"`，用于基础生成或后续超分/修复。

## 使用方式

### 调用协议
- **同步调用**：适用于 `wan2.6`、`qwen-image-3.0`、`z-image-turbo` 等支持快速响应的模型，单次请求直接返回图像 Base64 或 URL。Endpoint 为 `POST /api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**：适用于耗时较长的任务（如虚拟模特、局部重绘、背景生成），需两步操作：  
  1. 提交任务获取 `task_id`（Endpoint 因模型而异，如 `image2image/image-synthesis`、`background-generation/generation`）；  
  2. 轮询 `GET /api/v1/tasks/{task_id}` 获取结果，`task_id` 有效期 24 小时 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

### 地域与域名
- 必须严格匹配地域：API Key、模型、Endpoint 均属同一地域（北京/新加坡/弗吉尼亚/法兰克福/东京）。跨地域调用将鉴权失败 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **强烈推荐使用业务空间专属域名**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`（新加坡），性能与稳定性优于公共域名 `dashscope.aliyuncs.com`。

### 输入格式
- 文生图：`input.messages` 中 `content` 包含 `text` 字段（如 `qwen-image-3.0-pro`）；旧版模型（如 `wanx-v1`）使用 `input.prompt`。  
- 图生图/编辑：`content` 数组中混合 `text` 与 `image` 对象，顺序决定参考优先级（最后一张图常作为主参考）[万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)。  
- 图像 URL：必须公网可访问、无中文路径、格式合规（PNG/JPG/WEBP 等），否则报错 `"Reference image download failed"` [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

## 限制和注意事项

- **计费与额度**：  
  - 免费额度按模型独立发放（如 `wanx-v1` 500 张、`qwen-mt-image` 500 张），主账号与 RAM 子账号共享，有效期 90 天 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。  
  - “限时免费”模型（如 `wanx-x-painting`、`wanx-poster-generation-v1`）额度用尽后不可调用，且不支持付费续用 [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)。

- **技术限制**：  
  - 所有异步接口必须携带 `X-DashScope-Async: enable` 请求头，否则拒绝服务。  
  - 图像 URL 下载失败是高频报错原因，务必确保链接可公开访问且无防盗链 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。  
  - `wan2.5` 及以下版本不支持 HTTP 同步调用，仅 `wan2.6` 及以上支持 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

- **兼容性提醒**：  
  - `qwen-image-edit` 系列已迭代为 `qwen-image-edit-*`（如 `qwen-image-edit-max`），旧模型名可能失效。  
  - `wanx-v1` 为 V1 版本，官方推荐迁移至 V2 版本 `wan2.6-t2i` 以获得更优性能与功能 [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)


