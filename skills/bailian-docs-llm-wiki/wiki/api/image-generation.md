# image generation

百炼平台提供多种图像生成与编辑能力，涵盖文生图（T2I）、图生图（I2I）、局部重绘、风格迁移、背景生成、海报设计等场景。所有模型均通过统一的HTTP API或DashScope SDK调用，支持异步与同步两种模式，适用于开发者快速集成到生产环境。核心能力由千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 等系列模型支撑，覆盖效果、速度、成本多维需求。

## 支持的模型/功能

平台当前提供以下主流图像模型及对应能力：

- **文生图（T2I）**：`qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo`、`kling/kling-v3-image-generation`、`vidu/vidu-image_reference2image` 等，支持自由分辨率设置（总像素 512×512 至 2048×2048），部分模型（如 `wan2.7-image-pro`）支持 4K 输出 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **图生图/图像编辑（I2I）**：`qwen-image-2.0-pro`、`wan2.7-image-pro`、`wan2.5-i2i-preview`、`kling/kling-v3-omni-image-generation`、`vidu/viduq3-fast_reference2image`，支持单图/多图输入、指令编辑、风格迁移、图文混排等 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)。
- **专用工具类模型**：
  - 局部重绘：`wanx-x-painting`（免费体验，额度用尽后不可用）；
  - 涂鸦作画：`wanx-sketch-to-image-lite`；
  - 虚拟模特/鞋靴试穿：`wanx-virtualmodel`、`shoemodel-v1`（均仅限免费体验）；
  - 图像擦除补全、画面扩展、背景生成、人物实例分割：均为华北2（北京）地域专属，需使用业务空间域名调用 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **创意工具**：`wordart-quick-start`（文字变形与纹理生成）、`facechain-portrait-generation`（人物写真LoRA训练与生成）、`outfitanyone`（AI试衣全链路组合）。

> **注意**：`wanx-v1`（V1版）已明确标注“推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”；而 `wan2.6-t2i` 及更高版本（如 `wan2.7-image-pro`）支持 HTTP 同步调用，但 `wan2.5` 及以下版本**不支持同步调用**，仅支持异步流程 —— 此矛盾点已在文档中显式区分，开发者需按模型版本选择对应调用方式。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | string | 必填。模型标识符，需与地域支持列表一致 | `"qwen-image-3.0-pro"`, `"wan2.6-t2i"` |
| `size` | string | 可选。输出图像尺寸，格式为 `"宽*高"` 或 `"1K"/"2K"/"4K"`；部分模型（如 `wan2.5-i2i-preview`）默认生成 `1280*1280` 并保持输入图宽高比 | `"1024*1024"`, `"2K"` |
| `n` | integer | 可选。生成图片张数，范围因模型而异：`qwen-image-*` 支持 1–6 张；`kling` 支持 1–9；`z-image-turbo` 固定为 1 张 | `1`, `2` |
| `prompt` / `messages.text` | string / array | 必填。提示词字段。`qwen-image-3.0-pro` 和 `wan2.7+` 使用 `messages` 结构；旧版 `wanx-v1`、`wan2.6-t2i` 使用 `input.prompt` 字段 | `{"text": "一间花店..."}` |
| `negative_prompt` | string | 可选（仅部分模型）。用于排除不希望出现的内容 | `"不要红色元素"` |
| `watermark` | boolean | 可选。是否添加水印，默认 `true`；多数生产场景建议设为 `false` | `false` |
| `prompt_extend` | boolean | 可选。启用智能提示词优化（返回增强后的 [prompt](../guides/prompt.md)），会增加响应时间 | `true` |

> **注意**：`aspect_ratio`（如 `"1:1"`）和 `resolution`（如 `"1k"`）为 `kling` 系列特有参数；`style_index`、`style_ref_url` 为人像风格重绘专用；`mask_image_url` 为局部重绘/擦除补全必需字段 —— 开发者应严格依据目标模型文档传参，跨模型复用参数将导致失败。

## 使用方式

### 1. 基础准备
- 获取并配置 API Key：必须通过 [阿里云百炼控制台](https://bailian.console.aliyun.com/) 获取对应地域（华北2/新加坡/弗吉尼亚）的 API Key，并设置为环境变量 `DASHSCOPE_API_KEY`。
- 使用业务空间专属域名：强烈建议迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`（新加坡），以获得更高性能与稳定性；`{WorkspaceId}` 在控制台「业务空间详情」中获取。

### 2. 调用模式选择
- **同步调用（推荐多数场景）**：适用于 `wan2.6+`、`qwen-image-3.0-pro`、`z-image-turbo` 等支持模型。一次 HTTP POST 即返回结果（含图片 URL 或 base64），无需轮询。示例 endpoint：  
  `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- **异步调用（必需场景）**：适用于 `wanx-v1`、`wanx-sketch-to-image-lite`、`wanx-x-painting`、`image-out-painting` 等耗时较长的模型。流程为两步：
  1. 创建任务：`POST .../image-synthesis`（或对应路径），返回 `task_id`；
  2. 轮询结果：`GET .../tasks/{task_id}`，直至 `task_status == "SUCCEEDED"`，获取 `output.results[0].url`（有效期 24 小时）。

### 3. 请求头要求
所有请求必须包含：
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- 异步调用**必须**添加 `X-DashScope-Async: enable`；缺失将报错 `"current user api does not support synchronous calls"`。

## 限制和注意事项

- **地域与密钥绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key 和请求地址**完全独立，不可混用**；跨地域调用将导致鉴权失败或服务报错。
- **免费额度与计费**：所有模型均提供 500 张免费额度（主账号与 RAM 子账号共享），有效期 90 天；额度用尽后，商业化模型（如 `wanx-v1` 0.16元/张、`image-out-painting` 0.18元/张）开始计费，限时免费模型（如 `wanx-x-painting`）则直接不可用。
- **图片 URL 要求**：输入图片必须为**公网可访问**的 HTTPS/HTTP 链接；OSS、自建存储等需确保外网可直连，否则报错 `"Reference image download failed"`。
- **输入限制**：
  - 图像分辨率：多数模型要求 `[512, 4096]` 像素单边长度，总像素 `512×512` 至 `2048×2048`；
  - 文件大小：通常 ≤10MB；
  - 格式：PNG/JPEG/WEBP/BMP/AVIF（具体见各模型文档）；
  - URL 中**禁止中文字符**（见 [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)）。
- **模型可用性**：部分模型（如 `wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation`）当前**仅限免费体验**，额度用尽后无付费通道，文档明确建议迁移到 `qwen-image-edit` 或 `wanx-image-edit` 等替代方案。

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
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)


