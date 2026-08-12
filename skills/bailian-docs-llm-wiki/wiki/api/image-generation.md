# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图（T2I）、图生图（I2I）、局部编辑、背景生成、风格迁移等全栈场景。所有模型均通过统一的 DashScope API 接口调用，支持 HTTP 同步/异步及 SDK 集成，适用于创意设计、电商、营销、AIGC 应用等开发者场景。

## 支持的模型/功能

平台当前提供三类核心能力：

- **通用文生图与编辑**：`qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo` 等支持高质量文本到图像生成；`qwen-image-3.0` 和 `wan2.7-image-pro` 同时支持文生图、图生图、多图融合与图文混排输出 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **垂直场景工具链**：包括涂鸦作画（`wanx-sketch-to-image-lite`）、局部重绘（`wanx-x-painting`）、虚拟模特（`virtualmodel-v2`）、鞋靴试穿（`shoemodel-v1`）、图像擦除补全（`image-erase-completion`）、人物实例分割（`image-instance-segmentation`）等专用模型，均需通过异步流程调用 [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)。
- **创意增强与生成**：如创意海报生成（`wanx-poster-generation-v1`）、AI试衣（`aitryon-plus`）、FaceChain人物写真、WordArt锦书文字艺术等，部分模型处于免费体验阶段，额度用尽后不可调用 [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)。

> **注意**：`wanx-v1`（V1版）已明确标注为“推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”；而 `wan2.6-t2i` 及更高版本（如 `wan2.7-image-pro`）支持同步调用，V1/V2早期模型仅支持异步，存在显著能力断代，开发者应优先选用 V2 或 3.0 系列。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | string | 必填。模型标识符，严格区分大小写与斜杠（如 `vidu/vidu-image_reference2image`） | `"qwen-image-3.0-pro"` |
| `size` | string | 可选。分辨率规格，支持像素格式（`"1024*1024"`）、预设档位（`"1K"`/`"2K"`/`"4K"`）或宽高比（`"16:9"`） | `"2K"` 或 `"1024*1024"` |
| `n` | integer | 可选。生成张数（部分模型固定为1）。`qwen-image-2.0-pro` 支持 1–6 张；`kling/kling-v3-image-generation` 支持 1–9 张 | `2` |
| `watermark` | boolean | 可选。是否添加水印，默认 `true`。部分模型（如 `wan2.7-image-pro`）支持显式关闭 | `false` |
| `prompt_extend` | boolean | 可选。启用智能提示词扩展，返回优化后的 [prompt](../guides/prompt.md) 及推理过程（增加延迟） | `true` |
| `aspect_ratio` | string | 仅部分模型（如 `kling`）支持，指定输出宽高比 | `"1:1"` |

> **注意**：`size` 参数约束因模型而异：`wan2.6-t2i` 要求总像素在 `[1280*1280, 1440*1440]`；`qwen-image-3.0` 要求 `[512*512, 2048*2048]`；`z-image-turbo` 同样为 `[512*512, 2048*2048]`。跨范围将导致 `400 Bad Request`。

## 使用方式

### 地域与域名
- 所有模型必须与 API Key **地域一致**（北京、新加坡、弗吉尼亚等），跨地域调用将鉴权失败。
- **强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于公共域名 `dashscope.aliyuncs.com`。Workspace ID 在控制台「业务空间详情」中获取。

### 调用模式
- **同步调用**（推荐）：适用于 `wan2.6-t2i`、`qwen-image-3.0-pro`、`z-image-turbo`、`wan2.7-image-pro` 等模型，单次请求直接返回图像 Base64 或 URL。Endpoint 为 `/api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**（必需）：适用于涂鸦作画、局部重绘、虚拟模特、海报生成等耗时较长的模型。分两步：
  1. `POST /api/v1/services/.../generation` 创建任务，响应含 `task_id`；
  2. `GET /api/v1/tasks/{task_id}` 轮询状态，`SUCCEEDED` 后获取结果 URL（有效期 24 小时）。

### 认证与头信息
- `Authorization: Bearer $DASHSCOPE_API_KEY`（必填）
- `Content-Type: application/json`（必填）
- 异步接口必须携带 `X-DashScope-Async: enable`（缺失将报错 `"current user api does not support synchronous calls"`）

## 限制和注意事项

- **免费额度与计费**：所有模型均提供 500 张/90 天免费额度（主账号与 RAM 子账号共享），用尽后按单价计费（如 `wanx-style-repaint-v1` 0.12 元/张）。限时免费模型（如 `wanx-x-painting`）额度用尽即停用，不支持付费开通。
- **图片 URL 要求**：输入图像 URL 必须公网可访问、支持 HTTPS、无中文路径、大小 ≤10 MB（部分模型如 `shoemodel-v1` 要求 ≤5 MB）。内网或私有 OSS 地址需预签名或转为临时公网 URL。
- **错误处理**：常见报错 `BadRequest.InputDownloadFailed` 表示图片无法下载，需检查 URL 可达性与权限；`InvalidApiKey` 表示密钥无效或地域不匹配。
- **并发限制**：主账号与 RAM 子账号共用限流策略，典型为 QPS ≤2、同时处理任务数 ≤1（部分模型如 `image-out-painting` 为 5）。超出将返回 `429 Too Many Requests`。

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
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)


