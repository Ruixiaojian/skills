# image generation

百炼平台的图像生成能力覆盖文生图、图生图、图像编辑、背景生成、局部重绘、扩图、擦除补全等全链路视觉创作任务，支持多模型、多地域、同步/异步调用方式。开发者可根据精度、速度、成本与功能需求选择合适模型，并通过统一 API 协议集成到业务系统中。

## 支持的模型与功能

平台提供两类核心图像模型体系：**万相（WanX）系列**与**千问（Qwen）系列**，以及面向垂直场景的专用模型（如 Vidu、Kling、FaceChain 等），功能覆盖全面：

- **文生图（T2I）**：支持多分辨率（512×512 至 4K）、多宽高比（1:4 至 4:1）、复杂文本渲染（如千问-文生图支持段落级文字生成）[千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)。
- **图生图/图像编辑（I2I）**：包括通用编辑（wan2.5-i2i-preview、qwen-image-2.0-pro）、局部重绘（wanx-x-painting）、涂鸦作画（wanx-sketch-to-image-lite）、风格迁移、超分、上色等 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。
- **专业工具类模型**：
  - 虚拟模特（wanx-virtualmodel）、鞋靴模特（shoemodel-v1）用于电商商品图生成；
  - 图像画面扩展（image-out-painting）支持旋转扩图、指定方向扩图；
  - 图像背景生成（wanx-background-generation-v2）支持文本+图像+边缘引导三重控制；
  - 创意海报生成（wanx-poster-generation-v1）提供标题/副标题/正文结构化输入；
  - AI试衣（aitryon-plus）、人物写真（FaceChain）、创意文字（WordArt锦书）等场景化模型。

> **注意**：部分模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion`、`wanx-poster-generation-v1`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确推荐使用 [千问-图像编辑](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md) 或 [万相2.1图像编辑](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md) 替代。

## 关键参数

所有图像 API 均通过 `parameters` 字段控制生成行为，常用参数如下：

| 参数名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `size` | string | 输出图像尺寸，支持像素格式（如 `"1024*1024"`）、预设规格（如 `"1K"`、`"2K"`、`"4K"`）或比例约束（如 `"16:9"`） | `"2048*2048"`、`"2K"`、`"16:9"` |
| `n` | integer | 生成图片张数（部分模型支持 1–9 张） | `1`（默认）、`2` |
| `watermark` | boolean | 是否添加水印（多数模型默认 `true`） | `false` |
| `prompt_extend` | boolean | 是否启用智能提示词扩展（提升语义理解，但增加延迟） | `true` |
| `aspect_ratio` | string | 宽高比（仅部分模型支持，如 Kling） | `"1:1"`、`"9:16"` |
| `resolution` | string | 分辨率等级（Vidu/Kling 等模型专用） | `"1k"`、`"4k"` |

> **注意**：`size` 参数在不同模型间存在兼容性差异。例如 `wan2.6-t2i` 要求总像素在 `[1280×1280, 1440×1440]` 区间且宽高比 ∈ `[1:4, 4:1]`；而 `qwen-image-3.0-pro` 允许 `512×512` 至 `2048×2048` 任意组合。务必查阅对应模型文档确认约束范围。

## 使用方式

### 调用协议与地址
- **同步调用**（推荐）：适用于 `wan2.6-t2i`、`z-image-turbo`、`qwen-image-2.0-pro` 等支持模型，单次请求返回结果。  
  地址格式（北京/新加坡）：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`  
  > 注意：美国（弗吉尼亚）地域同步接口为 `https://dashscope-us.aliyuncs.com/...`，法兰克福仅支持异步。

- **异步调用**（必需）：适用于 `wanx-v1`、`wanx-sketch-to-image-lite`、`wanx-x-painting` 等耗时较长模型，需两步操作：  
  1. `POST /api/v1/services/aigc/xxx/generation` 创建任务，获取 `task_id`；  
  2. `GET /api/v1/tasks/{task_id}` 轮询查询结果（URL 有效期 24 小时）。

### 必选请求头
```http
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```
- 异步调用**必须**添加 `X-DashScope-Async: enable`，缺失将报错 `current user api does not support synchronous calls`。
- 同步调用图文混排（`enable_interleave=true`）时，**必须**同时设置 `X-DashScope-Sse: enable` 和 `parameters.stream: true`。

### 输入结构
- **文生图**：`input.messages[].content[]` 中包含 `{"text": "prompt"}`；
- **图生图/编辑**：`content[]` 可混合 `{"text": "指令"}` 与 `{"image": "url"}`（最多支持 14 张参考图，如 Vidu）；
- **局部重绘/擦除**：需传入 `base_image_url` + `mask_image_url`（掩码图非0区域为操作区）。

## 限制和注意事项

- **地域与域名隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域拥有独立 API Key 与请求地址，**不可混用**。强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高稳定性与性能 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。
- **图片 URL 要求**：所有输入图片 URL 必须为公网可访问、HTTP/HTTPS 协议、无中文路径；OSS 等云存储需配置公开读权限。
- **限流规则**：主账号与 RAM 子账号共享限流（如 QPS/RPS 与并发任务数），具体数值见各模型文档的“计费与限流”章节。
- **免费额度**：仅对**成功生成的输出图片**计数，失败、输入图下载失败、超时等不占用额度；额度有效期 90 天，自动发放。
- **错误排查**：常见报错 `BadRequest.InputDownloadFailed` 表明图片 URL 不可达，请检查网络可达性与 CORS 配置；`InvalidApiKey` 表示密钥错误或地域不匹配。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)


