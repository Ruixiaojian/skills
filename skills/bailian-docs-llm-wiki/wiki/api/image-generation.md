# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图（T2I）、图生图（I2I）、局部重绘、风格迁移、背景生成、AI试衣等数十种专业场景。所有模型均通过统一的HTTP API或DashScope SDK调用，支持同步/异步模式，并按实际成功生成图片计费。开发者需根据地域选择对应API Key与业务空间专属域名以确保服务稳定性。

## 支持的模型/功能

平台当前提供三大类图像模型：

- **通用文生图/编辑模型**：包括千问系列（`qwen-image-3.0-pro`、`qwen-image-2.0-pro`、`qwen-image-edit-max`）、万相系列（`wan2.6-t2i`、`wan2.7-image-pro`、`wan2.5-i2i-preview`）、Z-Image（`z-image-turbo`）及Vidu（`vidu/vidu-image_reference2image`）、可灵（`kling/kling-v3-omni-image-generation`）。其中千问-图像生成与编辑3.0模型同时支持T2I与I2I，详见[千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；万相2.7专业版在文生图场景下支持4K输出，而组图生成仅支持2K [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。

- **垂直领域工具模型**：覆盖创意设计与电商应用，如涂鸦作画（`wanx-sketch-to-image-lite`）、图像局部重绘（`wanx-x-painting`）、虚拟模特（`wanx-virtualmodel`）、鞋靴模特（`shoemodel-v1`）、创意海报生成（`wanx-poster-generation-v1`）、图像擦除补全（`image-erase-completion`）、人物实例分割（`image-instance-segmentation`）、图像背景生成（`wanx-background-generation-v2`）等。多数工具模型当前仅提供免费体验，额度用尽后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)替代 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

- **特色增强模型**：如AI试衣OutfitAnyone（含`aitryon-plus`、`aitryon-refiner`等子模型）、人物写真FaceChain、创意文字WordArt锦书等，面向特定业务流深度优化。

> **注意**：部分模型存在地域限制。例如，`qwen-mt-image`（图像翻译）仅支持华北2（北京）地域；`wanx-v1`、`wanx-style-repaint-v1`、`wanx-poster-generation-v1`等均明确限定为北京地域使用。跨地域混用API Key将导致鉴权失败，详见各文档“前提条件”章节。

## 关键参数

核心参数因模型类型而异，但共性较强：

- **`model`**：必填字符串，指定模型ID（如`wan2.6-t2i`、`qwen-image-3.0-pro`），各地域支持列表需查阅控制台模型市场。
- **`size`**：控制输出分辨率。格式支持`宽*高`（如`1024*1024`）、预设值（如`1K`、`2K`、`4K`）或比例约束（如`16:9`）。不同模型范围不同：`qwen-image-3.0-pro`要求总像素512×512至2048×2048；`wan2.6-t2i`限定总像素在[1280×1280, 1440×1440]；`z-image-turbo`支持512×512至2048×2048。
- **`n`**：生成图片张数。`qwen-image-2.0-pro`支持1–6张；`kling/kling-v3-omni-image-generation`在组图模式下通过`series_amount`指定2–9张；多数工具模型（如`wanx-sketch-to-image-lite`）固定为1张。
- **`prompt` / `input.messages`**：文本提示词。千问、万相2.6+、Vidu、可灵等新模型采用`messages`数组结构（含`role`和`content`），兼容[多模态](../concepts/multi-modal.md)输入（text + image）；旧模型（如`wanx-v1`）仍使用扁平化`prompt`字段。
- **`parameters`**：扩展配置。常用项包括：
  - `watermark`: 布尔值，控制是否添加水印（默认`true`）；
  - `prompt_extend`: 布尔值，启用智能提示词扩展（如Z-Image）；
  - `aspect_ratio` / `resolution`: 可灵模型专用宽高比与分辨率控制；
  - `style_index` / `style_ref_url`: 人像风格重绘模型用于指定预置风格或自定义风格图。

## 使用方式

所有图像API均需先获取API Key并配置环境变量（`DASHSCOPE_API_KEY`），强烈建议迁移至业务空间专属域名以获得更高性能与稳定性：

- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

调用模式分为两类：

- **同步调用**：适用于`wan2.6-t2i`、`wan2.7-image-pro`、`z-image-turbo`、`qwen-image-3.0-pro`等新模型，单次请求直接返回结果（HTTP 200 + 图片base64或URL）。示例见[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

- **异步调用**：适用于绝大多数模型（如`wanx-v1`、`wanx-sketch-to-image-lite`、`image-out-painting`、`wanx-background-generation-v2`等），流程为两步：
  1. 发起`POST`创建任务，必须携带`X-DashScope-Async: enable`请求头，返回`task_id`；
  2. 轮询`GET /api/v1/tasks/{task_id}`获取状态，直至`task_status`为`SUCCEEDED`，响应中包含图片URL（有效期24小时）。

> **注意**：`X-DashScope-Async: enable`是异步调用的强制请求头，缺失将报错“current user api does not [support](../guides/support.md) synchronous calls”，该约束在[万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)中有明确强调。

## 限制和注意事项

- **地域与Key隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的API Key与请求地址完全独立，不可混用。跨地域调用将导致鉴权失败或服务报错，此规则适用于所有模型，包括千问、万相、Vidu等。
- **免费额度与计费**：多数模型提供500张免费额度（90天有效），额度用尽后按单价计费（如`wanx-v1` 0.16元/张，`image-out-painting` 0.18元/张）。计费仅针对**成功生成的输出图片**，失败任务不扣费。详情参见[常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **图片URL要求**：输入图片URL必须公网可访问、无中文路径、支持HTTP/HTTPS协议，且建议上传至OSS等云存储以保障稳定性。若下载失败，将返回`BadRequest.InputDownloadFailed`错误。
- **模型时效性**：部分模型（如`wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`）明确标注“目前仅供免费体验”，额度用尽后不可调用且不支持付费，文档已给出替代方案指引。
- **输入规范**：图像尺寸、格式、大小均有严格限制（如`image-instance-segmentation`要求512×512至4096×4096像素，≤10MB），超出将触发校验失败。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)


