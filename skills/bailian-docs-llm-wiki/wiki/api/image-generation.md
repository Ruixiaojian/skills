# image generation

百炼平台的图像生成能力覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、背景生成、扩图、擦除补全等十余类任务，支持千问、万相、可灵、Vidu、Z-Image 等多系列模型。所有接口均基于统一的[异步任务](../concepts/async-task.md)模型设计（部分新模型支持同步调用），需通过业务空间专属域名调用以获得最佳性能与稳定性。开发者需按地域独立配置 API Key 并严格匹配 endpoint。

## 支持的模型/功能

平台提供两类核心能力：**通用图像生成模型**（如 `qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo`）和**垂直场景专用模型**（如 `wanx-style-repaint-v1`、`shoemodel-v1`、`image-out-painting`）。前者支持多模态输入（文本+图像）、灵活分辨率与风格控制；后者聚焦特定任务，例如人像风格迁移、鞋靴AI试穿、海报自动生成等。值得注意的是，部分模型（如 `wanx-x-painting`、`shoemodel-v1`、`wanx-poster-generation-v1`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，详见 [常见问题 (raw/model-api-reference/image-generation/image-faq.md)](../../raw/model-api-reference/image-generation/image-faq.md)。此外，[千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 明确指出其同时支持 T2I 与 I2I，而旧版 `qwen-image-edit` 模型则明确不支持分辨率指定，存在能力差异。

> **注意**：文档中关于 `wan2.6-t2i` 的支持范围存在矛盾。[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 声明该模型支持 HTTP 同步调用，但 [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md) 却将其归类为“图像编辑”模型，并提示“如需纯文本生成图片（文生图），建议使用 `wan2.6-t2i` 模型”，暗示其非主推文生图能力。实际开发应以 `wan2.6-t2i` 作为文生图首选，`wan2.6-image` 用于编辑任务。

## 关键参数

- **`model`**：必填，指定模型名称（如 `qwen-image-3.0-pro`, `wan2.7-image-pro`, `vidu/vidu-image_reference2image`），不同地域支持的模型列表不同。
- **`size` / `resolution` / `aspect_ratio`**：控制输出规格。`size` 格式为 `"宽*高"`（如 `"1024*1024"`）或预设值（如 `"1K"`、`"2K"`、`"4K"`）；`aspect_ratio` 用于指定宽高比（如 `"16:9"`、`"1:1"`）。各模型约束不同：`qwen-image-3.0-pro` 要求总像素在 `512*512` 至 `2048*2048` 之间；`wan2.6-t2i` 要求总像素在 `[1280*1280, 1440*1440]` 之间；`z-image-turbo` 同样要求总像素在此区间。
- **`n`**：生成图片张数，范围因模型而异：`qwen-image-2.0-pro` 支持 `1-6` 张；`kling/kling-v3-image-generation` 支持 `1-9` 张；多数专用模型（如 `wanx-style-repaint-v1`）固定为 `1` 张。
- **`input`**：核心输入结构。文生图通常为 `{"text": "prompt"}`；图生图/编辑则为 `{"messages": [...]}` 数组，其中 `content` 可包含 `text` 和 `image` 对象；局部重绘等任务则需 `base_image_url` 与 `mask_image_url`。
- **`parameters`**：扩展控制项。常用参数包括 `watermark`（布尔值，控制是否添加水印）、`prompt_extend`（布尔值，启用智能提示词优化）、`thinking_mode`（布尔值，返回推理过程）等。

## 使用方式

所有图像 API 均采用 **HTTP 调用**，推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）而非旧域名 `https://dashscope.aliyuncs.com`，以获得更高性能与稳定性。调用流程分为两类：

- **同步调用**（推荐用于 `wan2.6-t2i`、`qwen-image-3.0-pro`、`z-image-turbo` 等新模型）：单次 POST 请求即可返回结果，Endpoint 为 `/api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**（适用于绝大多数模型，如 `wanx-v1`、`wan2.5-i2i-preview`、`kling/kling-v3-image-generation`）：分两步——先 `POST` 创建任务获取 `task_id`，再轮询 `/api/v1/tasks/{task_id}` 查询状态直至 `SUCCEEDED`。创建任务的 Endpoint 因模型类型而异，例如文生图用 `/text2image/image-synthesis`，图生图用 `/image2image/image-synthesis`，背景生成用 `/background-generation/generation`。

无论哪种方式，请求头均需包含 `Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`，异步调用还必须设置 `X-DashScope-Async: enable`。[千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md) 特别强调此请求头为必选，缺失将直接报错。

## 限制和注意事项

- **地域与密钥绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立的 API Key 与请求地址，**绝对不可混用**，跨地域调用将导致鉴权失败或服务报错。
- **URL 访问性**：所有输入图片 URL 必须为公网可访问地址。若使用私有存储（如 OSS），需确保 Bucket 权限允许公网读取，否则会返回 `BadRequest.InputDownloadFailed` 错误，详见 [常见问题 (raw/model-api-reference/image-generation/image-faq.md)](../../raw/model-api-reference/image-generation/image-faq.md)。
- **免费额度与计费**：免费额度（通常为 500 张）仅对**成功生成的输出图片**计数，输入图片及失败任务不计入。额度由主账号与其 RAM 子账号共享，有效期 90 天。商业化模型（如 `wanx-v1` 单价 0.16 元/张）在额度用尽后需付费，而部分模型（如 `wanx-x-painting`）则为限时免费，额度用尽即不可用。
- **并发与速率限制**：主账号与 RAM 子账号共用限流策略，典型限制为任务下发接口 QPS 2、同时处理中任务数 1。高并发场景需自行实现排队与重试逻辑。

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
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)


