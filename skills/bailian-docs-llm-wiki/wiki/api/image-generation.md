# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图、图生图、局部重绘、风格迁移、背景生成、AI试衣等数十种专业场景。所有模型均通过统一的 HTTP API 接口调用，支持同步与异步两种模式，并已适配 DashScope SDK（Python/Java）。开发者需先开通对应模型服务、获取 API Key 并配置业务空间专属域名以获得最佳性能。

## 支持的模型/功能

平台当前提供三大类图像能力：

- **通用文生图与编辑**：包括 `qwen-image-3.0-pro`（支持 T2I/I2I）、`wan2.6-t2i`、`wan2.7-image-pro`（支持 4K 文生图）、`z-image-turbo`（轻量快速）等主流模型；详见 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **垂直场景工具**：覆盖创意设计与电商需求，如 `wanx-background-generation-v2`（背景生成）、`image-out-painting`（画面扩展）、`wanx-style-repaint-v1`（人像风格重绘）、`shoemodel-v1`（鞋靴模特）、`image-erase-completion`（擦除补全）等。
- **专业增强与辅助模型**：如 `facechain`（人物写真训练与生成）、`wordart`（创意文字变形与纹理）、`outfitanyone`（AI试衣含基础版/Plus版/精修/分割）等，需组合调用实现端到端流程。

> **注意**：部分模型（如 `wanx-x-painting`、`wanx-poster-generation-v1`、`wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation`、`image-erase-completion`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确推荐迁移到 [千问-图像编辑](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md) 或 [万相2.1图像编辑](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md) 等替代方案。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | string | 必填。模型标识符，需与实际开通模型一致。不同地域支持模型列表不同，须查阅控制台确认。 | `"qwen-image-3.0-pro"`, `"wan2.6-t2i"`, `"kling/kling-v3-image-generation"` |
| `size` / `resolution` / `aspect_ratio` | string | 图像尺寸控制。各模型约束不同：<br>- `wan2.6-t2i`: 总像素 `[1280×1280, 1440×1440]`，宽高比 `[1:4, 4:1]`<br>- `qwen-image-2.0-pro`: 总像素 `512×512` 至 `2048×2048`<br>- `kling`: 支持 `"1k"`/`"2k"`/`"4k"` 及 `"16:9"`/`"9:16"`/`"1:1"`<br>- `vidu`: 支持 `"1024*1024"` 等自由格式 | `"1024*1024"`, `"2K"`, `"1:1"` |
| `n` | integer | 输出图像张数。多数模型支持 `1–6` 张，`kling` 支持 `1–9`，`vidu` 固定为 `1` 张。 | `2` |
| `prompt_extend` | boolean | 是否启用智能提示词扩展（如 `qwen-image-3.0-pro`、`z-image-turbo`）。开启后返回优化提示词，但增加延迟。 | `true` |
| `watermark` | boolean | 是否添加水印（默认 `true`）。部分模型（如 `wan2.7-image-pro`）支持设为 `false`。 | `false` |
| `X-DashScope-Async` | header | 异步调用必需头。**所有 HTTP 调用必须显式设置为 `"enable"`**，否则报错 `current user api does not support synchronous calls`（见 [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)）。 | `"enable"` |

## 使用方式

### 1. 域名与认证
- **强制使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但官方明确建议迁移以获得“卓越性能和更高稳定性”（见 [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)）。
- **API Key 配置**：通过环境变量 `$DASHSCOPE_API_KEY` 或请求头 `Authorization: Bearer <key>` 传递。

### 2. 同步 vs 异步
- **同步调用**：仅限 `wan2.6-t2i`、`qwen-image-3.0-pro`、`z-image-turbo`、`wan2.7-image-pro` 等新模型，单次请求直接返回结果（HTTP 200 + 图片 URL）。
- **异步调用**：其余模型（如 `wanx-v1`、`wanx-sketch-to-image-lite`、`image-out-painting`、`kling`、`vidu`）必须分两步：
  1. `POST /api/v1/services/.../generation` 创建任务，获取 `task_id`；
  2. 轮询 `GET /api/v1/tasks/{task_id}` 直至 `task_status == "SUCCEEDED"`，再提取 `output.results[0].url`。

### 3. 输入格式
- **文生图**：`input.messages[].content[].text`（推荐）或 `input.prompt`（兼容旧模型）。
- **图生图/编辑**：`input.messages[].content[].image` 数组传入 1–14 张参考图（`vidu` 支持最多 14 张；`qwen-image-3.0-pro` 支持 1–3 张）。
- **局部操作**（如重绘、擦除）：需额外提供 `mask_image_url` 或 `base_image_url` 等结构化输入。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key 与请求地址**完全独立，不可混用**，跨地域调用将导致鉴权失败（见 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)）。
- **图片 URL 要求**：所有输入图片 URL 必须为**公网可访问、无中文路径、支持 HTTP/HTTPS 协议**。内网或私有存储链接将报错 `Reference image download failed`（见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)）。
- **免费额度与计费**：免费额度（通常 500 张）按**成功生成的输出图片数量**计算，输入图或失败任务不计入。额度由主账号与 RAM 子账号共享，有效期 90 天。商业化模型（如 `wanx-v1` 0.16元/张）在额度用尽后自动转为付费（见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)）。
- **限流策略**：主账号与 RAM 子账号共用 QPS/RPS 限制（常见为 2），同时处理中任务数上限通常为 1（少数如 `image-out-painting` 为 5）。超出将返回 `429 Too Many Requests`。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)


