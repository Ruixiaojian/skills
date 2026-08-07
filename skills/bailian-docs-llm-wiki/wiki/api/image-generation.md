# image generation

百炼平台的图像生成能力覆盖文生图、图生图、图像编辑、局部重绘、背景生成、扩图、擦除补全等全链路场景，支持多模型并行调用。所有图像API均采用统一的[异步任务](../concepts/asynchronous-task.md)模型（部分新模型支持同步调用），需通过 `task_id` 轮询获取最终结果。开发者需注意地域隔离、业务空间专属域名迁移及免费额度限制。

## 支持的模型/功能

平台提供三大类图像模型：**通用生成模型**（如千问系列、万相系列、Z-Image）、**垂直领域模型**（如可灵、Vidu、FaceChain、WordArt锦书）和**创意工具模型**（如虚拟模特、鞋靴模特、人像风格重绘、图像画面扩展等）。其中：

- **千问系列**（`qwen-image-*`）支持文生图（T2I）与图生图（I2I）双模态，具备强文本渲染与语义遵循能力，推荐使用 `qwen-image-3.0-pro` 或 `qwen-image-max` [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；
- **万相系列**（`wanx-*`, `wan2.*`）覆盖从极速版（`wanx2.1-t2i-turbo`）到专业版（`wan2.7-image-pro`）的完整谱系，支持4K高清输出与图文混排，但V1版已 deprecated，应优先选用V2版 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)；
- **轻量与专用模型**包括 `z-image-turbo`（快速生图）、`kling/kling-v3-*`（分镜组图）、`vidu/*`（UI/图表像素级还原）、`facechain`（人物写真微调）及 `wordart`（创意文字生成）等；
- **创意工具类**如 `wanx-x-painting`（局部重绘）、`image-out-painting`（扩图）、`shoemodel-v1`（鞋靴试穿）等均为免费体验模型，额度用尽后不可调用 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

> **注意**：文档中 `wanx-v1` 模型在[万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)中标注为“仅适用于华北2（北京）地域”，而同系列其他模型（如 `wan2.6-t2i`）明确支持北京、新加坡、弗吉尼亚三地；实际调用时务必确认模型与地域的匹配性，跨地域调用将导致鉴权失败。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 备注 |
|------|------|----------------|------|
| `model` | 模型标识符 | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `z-image-turbo` 等 | 必填，需与地域和业务空间匹配 |
| `size` | 输出分辨率 | `"1024*1024"`, `"2K"`, `"4K"`, `"1:1"` | 不同模型约束不同：`qwen-image-*` 要求总像素 512×512–2048×2048；`wan2.6-t2i` 要求 1280×1280–1440×1440；`kling` 仅支持 `"1k"/"2k"/"4k"` 及宽高比 |
| `n` | 生成张数 | `1–9`（多数模型） | `qwen-image-max` 固定为1；`wanx-poster-generation-v1` 默认1 |
| `prompt` / `messages` | 提示词输入 | 文本字符串或含 `text`/`image` 的消息数组 | `qwen-image-3.0` 和 `wan2.7` 使用 `messages` 结构；`wanx-v1` 使用 `input.prompt` 字段 |
| `X-DashScope-Async` | 异步开关 | `"enable"` | **HTTP调用必填**，缺失将报错 `"current user api does not support synchronous calls"` |
| `watermark` | 水印开关 | `true`（默认）/ `false` | 部分模型（如 `wan2.7-image-pro`）支持关闭 |

## 使用方式

所有图像API均需通过 HTTP 请求调用，**必须配置业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用但性能与稳定性较低。调用流程分两类：

- **同步调用**（推荐）：适用于 `wan2.6`、`wan2.7-image-pro`、`qwen-image-3.0`、`z-image-turbo` 等新模型，一次请求直接返回结果（含图片URL或base64），Endpoint 为 `/api/v1/services/aigc/multimodal-generation/generation`；
- **异步调用**（兼容）：适用于 `wanx-v1`、`wanx-sketch-to-image-lite`、`wanx-x-painting` 等老模型，需两步操作：<br>1. `POST /api/v1/services/aigc/{service}/image-synthesis` 创建任务，获取 `task_id`；<br>2. `GET /api/v1/tasks/{task_id}` 轮询状态，成功后返回 `output.results[].url`（有效期24小时）。

> **注意**：`image-erase-completion` 模型在[图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)中使用的 Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`（未带 WorkspaceId），与其他模型不一致，实际调用时应统一迁移到业务空间域名。

## 限制和注意事项

- **地域与密钥隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key、Endpoint、模型列表完全独立，**不可混用**。例如，北京地域的 Key 无法调用新加坡模型；
- **免费额度**：所有模型均提供 500 张免费额度（部分如 `shoemodel-v1`、`wanx-x-painting` 明确标注“仅免费体验，额度用尽后不可调用”），额度按主账号与 RAM 子账号共享，有效期 90 天；
- **图片 URL 要求**：输入图片必须为公网可访问的 HTTPS/HTTP 地址，OSS 等云存储需设置公开读权限；URL 中**禁止含中文字符**，否则报错 `"Reference image download failed"`；
- **限流策略**：主账号与 RAM 子账号共用 QPS/RPS 限制（通常为 2），同时处理中任务数上限为 1–5（依模型而定），超限请求将返回 `429 Too Many Requests`；
- **错误处理**：常见错误如 `"BadRequest.InputDownloadFailed"`（图片 URL 不可达）、`"InvalidApiKey"`（密钥错误）、`"current user api does not support synchronous calls"`（缺少 `X-DashScope-Async: enable`）需针对性排查。

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
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)


