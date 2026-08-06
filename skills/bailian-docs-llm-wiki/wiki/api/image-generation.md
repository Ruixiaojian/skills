# image generation

百炼平台提供多种图像生成与编辑能力，覆盖文生图、图生图、局部重绘、风格迁移、背景生成、扩图、擦除补全等核心场景。所有模型均通过统一的 HTTP API 或 DashScope SDK 调用，支持异步任务模式（主流）及部分模型的同步调用。开发者需按地域获取对应 API Key 并配置业务空间专属域名以获得最佳性能与稳定性。

## 支持的模型/功能

平台当前提供三类图像能力模型：

- **通用文生图/图生图模型**：包括 `wan2.6-t2i`、`wan2.7-image-pro`、`qwen-image-3.0-pro`、`z-image-turbo`、`kling/kling-v3-omni-image-generation` 等，支持自由尺寸、多宽高比、高分辨率（最高 4K）输出，适用于创意设计、内容生产等通用场景。其中 `wan2.6-t2i` 是文生图 V2 的主力推荐模型，而 `qwen-image-3.0-pro` 同时支持 T2I 和 I2I 一体化流程 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

- **专业编辑与工具类模型**：涵盖 `wanx2.1-imageedit`（全局/局部风格化、指令编辑、扩图、超分）、`wan2.5-i2i-preview`（单/多图融合）、`wanx-x-painting`（局部重绘）、`image-out-painting`（画面扩展）、`image-erase-completion`（擦除补全）等，面向精细化图像操作需求。需注意 `wanx-x-painting` 和 `image-erase-completion` 当前仅限免费体验，额度用尽后不可调用 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

- **垂直场景专用模型**：如 `wanx-style-repaint-v1`（人像风格重绘）、`virtualmodel-v2`（虚拟模特）、`shoemodel-v1`（鞋靴试穿）、`facechain`（人物写真）、`wordart`（创意文字）、`qwen-mt-image`（图像翻译）等，针对电商、营销、设计等特定业务优化。其中 `virtualmodel-v2` 支持自定义长宽比（2:1、16:9 等），而 `qwen-mt-image` 仅支持中/英文与其他语种互译，不支持非中/英语种直译 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

> **注意**：文档中存在模型命名与能力描述不一致的情况。例如，`wan2.6-image` 模型在 [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md) 中明确说明“如需纯文本生成图片（文生图），建议使用 `wan2.6-t2i` 模型”，但其文档标题仍称“图像生成与编辑”，易引发混淆。实际开发中应严格按模型名区分用途，避免误用。

## 关键参数

所有图像 API 均通过 `parameters` 字段控制生成行为，核心参数如下：

- `size`：指定输出分辨率。格式支持 `宽*高`（如 `"1024*1024"`）、预设档位（如 `"1K"`、`"2K"`、`"4K"`）或 `"auto"`。不同模型约束不同：`wan2.6-t2i` 要求总像素在 `[1280*1280, 1440*1440]`；`qwen-image-3.0-pro` 要求总像素在 `[512*512, 2048*2048]`；`vidu` 系列仅支持 `"1K"`/`"2K"`/`"4K"` 三档。

- `n`：生成图片张数。多数模型支持 `1-6` 张（如 `qwen-image-2.0-pro`），`kling` 系列支持 `1-9` 张，`z-image-turbo` 固定为 `1` 张。

- `watermark`：布尔值，控制是否添加水印。默认 `true`，生产环境建议显式设为 `false`。

- `aspect_ratio`：宽高比（仅 `kling` 等部分模型支持），可选 `"16:9"`、`"9:16"`、`"1:1"`。

- `prompt_extend`：布尔值，启用后返回优化后的提示词及推理过程（如 `z-image-turbo`），但增加响应延迟。

- 其他模型特有参数：`wanx-sketch-to-image-lite` 使用 `sketch_weight` 控制涂鸦权重；`virtualmodel-v2` 使用 `short_side_size` 指定短边；`qwen-mt-image` 使用 `source_lang`/`target_lang` 指定语种。

## 使用方式

### 调用协议
- **异步模式（主流）**：适用于所有图像生成与编辑模型（除明确标注支持同步的模型外）。流程为两步：
  1. **创建任务**：发送 POST 请求至 `/api/v1/services/aigc/{service}/generation`（或 `/image-synthesis` 等旧路径），携带 `X-DashScope-Async: enable` 头，获取 `task_id`。
  2. **轮询结果**：使用 `task_id` 调用查询接口（如 `/tasks/{task_id}`），直至 `task_status` 为 `"SUCCEEDED"`，返回含有效期（通常 24 小时）的图片 URL。
- **同步模式（少数）**：仅 `wan2.6` 及以上 `multimodal-generation/generation` 接口支持，一次请求直接返回结果，推荐用于低延迟要求场景。

### 地域与域名
- 所有模型均按地域隔离，**API Key、Endpoint URL、模型列表必须严格匹配同一地域**（北京、新加坡、弗吉尼亚、法兰克福、东京等）。
- 强烈推荐使用**业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非通用 `dashscope.aliyuncs.com`，以获得更高稳定性与性能。该要求在 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 等多份文档中被反复强调。

### 认证与环境
- 必须配置 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头。
- 开发者需提前在百炼控制台开通对应模型服务，并确保业务空间具备调用权限（尤其 RAM 子账号需显式填写 `X-DashScope-WorkSpace` 头）。

## 限制和注意事项

- **免费额度与计费**：所有模型均提供 500 张免费额度（90 天有效期），主账号与 RAM 子账号共享。超出后按模型单价计费（如 `wanx-v1` 0.16 元/张，`wanx-background-generation-v2` 0.08 元/张），仅对成功生成的图片收费。部分模型（如 `wanx-x-painting`、`shoemodel-v1`）明确标注“目前仅供免费体验”，额度用尽即不可用。

- **输入限制**：
  - 图片 URL 必须公网可访问、无中文路径、格式合规（JPG/PNG/WEBP 等），否则报错 `BadRequest.InputDownloadFailed` [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
  - 输入图片分辨率与大小有硬性约束（如 `image-instance-segmentation` 要求 `512×512` 至 `4096×4096`，单图 ≤10MB）。

- **地域强制约束**：跨地域调用（如用北京 Key 调用新加坡 Endpoint）必然失败，错误码多为鉴权失败或服务不可用。务必核对模型支持地域列表。

- **模型弃用提示**：`wanx-v1`（V1 版）文档明确提示“推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”，V1 已进入维护状态，新项目应优先选用 V2 或更新版本。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)


