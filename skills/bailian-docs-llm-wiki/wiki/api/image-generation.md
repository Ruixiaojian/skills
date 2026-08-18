# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图（T2I）、图生图（I2I）、局部重绘、背景生成、扩图、风格迁移、AI试衣等数十种场景。所有模型均通过统一的 HTTP API 或 DashScope SDK 调用，支持同步与异步两种模式，适用于从快速原型验证到高并发生产部署的各类开发者需求。

## 支持的模型/功能

平台当前提供三大类图像能力：

- **通用文生图与编辑**：包括 `qwen-image-3.0-pro`（推荐）、`wan2.6-t2i`、`z-image-turbo`、`kling/kling-v3-omni-image-generation` 等主流模型，支持自由分辨率、多尺寸输出（1K/2K/4K）、宽高比控制（如 `1:1`, `16:9`, `9:16`）及图文混排；其中千问系列尤其擅长复杂中英文文本渲染与语义遵循 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **垂直场景工具链**：覆盖电商与设计高频需求，如 `wanx-background-generation-v2`（背景生成）、`image-out-painting`（画面扩展）、`wanx-style-repaint-v1`（人像风格重绘）、`shoemodel-v1`（鞋靴模特）、`outfitanyone`（AI试衣）等，多数为华北2（北京）地域专属服务 [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)。
- **创意与辅助模型**：如 `facechain-portrait-generation`（人物写真训练与生成）、`wordart-quick-start`（创意文字变形与纹理）、`qwen-mt-image`（图像翻译）等，强调特定任务精度与艺术表达 [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)。

> **注意**：部分模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`wanx-poster-generation-v1`）明确标注“仅提供免费体验”，额度用尽后不可调用且不支持付费，需切换至替代方案（如千问图像编辑或万相2.1图像编辑）。

## 关键参数

所有图像API共用核心参数结构，关键字段如下：

- **`model`**（必选）：字符串，指定模型ID，如 `"qwen-image-3.0-pro"`、`"wan2.6-t2i"`。不同地域支持的模型列表需查阅控制台，跨地域调用将失败。
- **`input`**（必选）：对象，内容依模型类型而异：
  - 文生图：`{"messages": [{"role": "user", "content": [{"text": "prompt"}]}]}` 或旧式 `{"prompt": "..."}`；
  - 图生图/编辑：`{"messages": [{"content": [{"image": "url"}, {"text": "instruction"}]}]}`；
  - 局部重绘/擦除：`{"base_image_url": "...", "mask_image_url": "...", "prompt": "..."}`。
- **`parameters`**（可选）：
  - `size` / `resolution` / `aspect_ratio`：控制输出规格。`size` 格式为 `"1024*1024"` 或 `"2K"`；`aspect_ratio` 如 `"1:1"`；`resolution` 取值 `"1k"/"2k"/"4k"`。各模型约束不同，例如 `wan2.6-t2i` 要求总像素在 `[1280*1280, 1440*1440]`，而 `qwen-image-3.0-pro` 支持 `[512*512, 2048*2048]`。
  - `n`：生成图片张数，范围通常为 `1–9`（如 `kling` 模型），部分模型固定为 `1`（如 `z-image-turbo`）。
  - `watermark`：布尔值，控制是否添加水印，默认 `true`。
  - `prompt_extend`：布尔值，启用后返回优化提示词及推理过程（如 `z-image-turbo`）。
- **请求头**（必选）：
  - `Authorization: Bearer $DASHSCOPE_API_KEY`
  - `Content-Type: application/json`
  - 异步调用必须含 `X-DashScope-Async: enable`；同步调用则省略此头。

## 使用方式

### 地域与域名
- **必须保证模型、API Key、Endpoint 三者地域一致**。华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立 API Key 与 Endpoint，混用将鉴权失败 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。
- **强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于公共域名 `https://dashscope.aliyuncs.com`。

### 调用模式
- **同步调用**（推荐用于 `wan2.6+`、`qwen-image-3.0+`、`z-image-turbo`）：单次 HTTP POST 直接返回结果，响应快，适合简单任务。
- **异步调用**（适用于耗时较长的模型，如 `wanx-v1`、`wanx-sketch-to-image-lite`、`image-erase-completion`）：分两步：
  1. 创建任务：POST 到 `/generation` 或 `/image-synthesis`，获取 `task_id`；
  2. 轮询结果：GET `/tasks/{task_id}`，直至 `task_status` 为 `"SUCCEEDED"`，返回图片 URL（有效期 24 小时）。

### 开发准备
- 获取并配置 API Key：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key) → [配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
- 安装 SDK（可选）：[DashScope Python SDK](https://help.aliyun.com/zh/model-studio/install-sdk) 提供封装方法，简化调用。

## 限制和注意事项

- **免费额度与计费**：所有模型均提供 500 张免费额度（主账号与 RAM 子账号共享），有效期 90 天。额度用尽后，商业化模型（如 `wan2.6-t2i`）按单价计费（如 0.02 元/张），限时免费模型（如 `wanx-x-painting`）则不可用。账单由主账号统一支付。
- **图片URL要求**：输入图片 URL 必须公网可访问、支持 HTTP/HTTPS、无中文路径，且建议上传至 OSS 等云存储以确保稳定性；否则报错 `"Reference image download failed"`。
- **限流策略**：主账号与 RAM 子账号共用 QPS 与并发任务数限制（常见为 QPS=2，同时处理任务数=1），超限将返回 `429 Too Many Requests`。
- **图像格式与尺寸**：输出默认为 PNG（少数如 `qwen-mt-image` 为 JPG）；输入图像需符合格式（JPG/PNG/WEBP 等）、大小（通常 ≤10MB）及分辨率（如 `image-instance-segmentation` 要求 `[512, 4096]` 像素）。
- **错误处理**：常见错误包括 `InvalidApiKey`（密钥无效）、`BadRequest.InputDownloadFailed`（图片下载失败）、`current user api does not support synchronous calls`（异步模型误用同步调用）。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)


