# image generation

百炼平台提供多种图像生成与编辑能力，覆盖文生图（T2I）、图生图（I2I）、局部重绘、背景生成、风格迁移、AI试衣等场景。所有模型均通过统一的 DashScope API 接口调用，支持 HTTP 同步/异步及 SDK 方式，但需注意地域隔离、API Key 绑定与业务空间专属域名迁移要求。

## 支持的模型/功能

平台当前提供三类核心图像能力：

- **通用文生图与编辑模型**：包括 `qwen-image-3.0-pro`（支持 T2I/I2I 双模态）、`wan2.6-t2i`（V2 文生图主力）、`z-image-turbo`（轻量快速）、`vidu/vidu-image_reference2image`（高精度 UI/图表渲染）和 `kling/kling-v3-omni-image-generation`（支持分镜组图）。其中千问系列模型强调复杂文本渲染与语义遵循，万相系列侧重艺术风格与电商适配 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
  
- **专业图像编辑工具链**：涵盖 `wan2.7-image-pro`（4K 文生图与图像编辑）、`qwen-image-edit-max`（工业设计与角色一致性）、`wanx-x-painting`（局部重绘）、`image-out-painting`（画面扩展）、`image-erase-completion`（擦除补全）及 `wanx-background-generation-v2`（背景生成）等。部分模型如 `wanx-x-painting` 和 `image-erase-completion` 当前仅限免费体验，额度用尽后不可调用 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

- **垂直场景专用模型**：包括 `wanx-style-repaint-v1`（人像风格重绘）、`virtualmodel-v2`（虚拟模特）、`shoemodel-v1`（鞋靴试穿）、`facechain-portrait-generation`（人物写真训练与生成）、`outfitanyone`（AI 试衣多模型组合）及 `wordart-quick-start`（创意文字生成）。这些模型普遍限定华北2（北京）地域调用，且多数采用异步流程 [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)。

> **注意**：文档中 `wanx-v1`（V1 版）明确标注“推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”，而 `wan2.6-t2i` 等 V2 模型已支持同步调用，V1 及部分旧版（如 `wanx2.1-t2i-turbo`）仅支持异步，实际开发应优先选用 V2 或更新版本。

## 关键参数

所有图像 API 的核心参数结构一致，但具体含义与约束因模型而异：

- **`model`**：必填字符串，指定模型 ID（如 `"qwen-image-3.0-pro"`、`"wan2.6-t2i"`）。不同地域支持的模型列表不同，需在控制台确认 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。
  
- **`input`**：必填对象，结构依任务类型变化：
  - 文生图：通常为 `{"prompt": "描述文本"}` 或 `{"messages": [{"role":"user","content":[{"text":"..."}]}]}`；
  - 图生图/编辑：需包含 `image` 字段（URL 或 base64），部分模型支持多图输入（如 `wan2.7-image-pro` 最多 3 张）；
  - 局部操作（重绘、擦除）：需 `base_image_url` + `mask_image_url`；
  - 虚拟模特/试衣：需 `template_image_url` + `shoe_image_url` 等专用字段。

- **`parameters`**：可选对象，常用参数包括：
  - `size`：分辨率，格式为 `"1024*1024"`、`"1K"`、`"2K"` 或 `"4K"`；各模型支持范围不同（如 `qwen-image-3.0-pro` 要求总像素 512×512 至 2048×2048，`wan2.6-t2i` 限定 1280×1280 至 1440×1440）；
  - `n`：生成张数，范围通常为 1–6（`kling` 支持 1–9，`vidu` 固定为 1）；
  - `aspect_ratio`：宽高比（如 `"1:1"`、`"16:9"`），仅部分模型（如 `kling`）支持；
  - `watermark`：布尔值，控制是否添加水印（默认 `true`）；
  - `prompt_extend`：布尔值，启用智能提示词优化（如 `z-image-turbo`）。

- **请求头**：`Authorization`（Bearer [Token](../concepts/token.md)）、`Content-Type: application/json` 为必需；异步调用必须设置 `X-DashScope-Async: enable`。

## 使用方式

### 调用协议与端点
- **同步调用**：适用于 `wan2.6`、`qwen-image-3.0`、`z-image-turbo` 等新模型，单次请求返回结果。Endpoint 为 `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**：适用于 `wanx-v1`、`wanx-x-painting`、`image-out-painting` 等耗时较长的模型，分两步：① 创建任务获取 `task_id`；② 轮询 `task_id` 查询结果。Endpoint 因功能而异（如 `image2image/image-synthesis`、`background-generation/generation`）。

### 地域与认证
- **严格地域绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立 API Key 与 Endpoint，**不可混用**。跨地域调用将导致鉴权失败 [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)。
- **推荐使用业务空间专属域名**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`（新加坡），性能与稳定性优于旧域名 `dashscope.aliyuncs.com`。

### 开发准备
- 获取对应地域的 [API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并配置至环境变量 `DASHSCOPE_API_KEY`；
- 安装 [DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)（Python/Java）或直接构造 HTTP 请求；
- 确保输入图片 URL 公网可访问，且符合格式（JPG/PNG/WEBP）、尺寸（通常 512×512 至 4096×4096）、大小（≤10MB）限制。

## 限制和注意事项

- **免费额度与计费**：多数模型提供 500 张免费额度（有效期 90 天），额度用尽后按单价计费（如 `wanx-style-repaint-v1` 0.12 元/张，`image-out-painting` 0.18 元/张）。限时免费模型（如 `wanx-x-painting`）额度用尽即停用，不支持付费续订。
  
- **限流策略**：主账号与 RAM 子账号共享限流，常见为 QPS/RPS ≤ 2、并发任务数 ≤ 1。高频调用需自行实现退避逻辑。

- **输入校验失败**：若图片 URL 无法公网访问或下载超时，将返回 `BadRequest.InputDownloadFailed` 错误；URL 中含中文字符、图片格式不支持（如 TIFF）、分辨率超限均会导致失败。务必上传至 OSS 或自建公网存储并验证链接可用性。

- **异步任务管理**：`task_id` 有效期 24 小时，需轮询查询状态（`PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED`），成功响应中 `output.results[0].url` 为图片直链（有效期 24 小时）。

- **模型能力边界**：`qwen-mt-image` 仅支持中/英与其他语种互译，不支持非中/英语种直译；`kling` 的组图模式（`result_type=series`）需使用 `kling-v3-omni-image-generation` 模型；`facechain` 需先完成人物形象训练再生成写真。

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
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)


