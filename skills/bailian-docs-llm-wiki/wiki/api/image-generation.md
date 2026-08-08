# image generation

百炼平台提供多种图像生成与编辑能力，覆盖文生图、图生图、局部编辑、风格迁移、背景生成等核心场景。所有模型均通过统一的 HTTP API 或 DashScope SDK 调用，支持华北2（北京）、新加坡、美国（弗吉尼亚）等多地域部署，推荐使用业务空间专属域名以获得更高稳定性与性能。开发者需按地域获取对应 API Key，并严格遵循异步或同步调用协议。

## 支持的模型/功能

百炼平台图像生成能力分为通用生成、专业编辑与创意工具三大类：

- **通用文生图/图生图模型**：  
  - `wan2.6-t2i`、`wan2.7-image-pro`（万相系列，支持自由尺寸、4K输出、图文混排）  
  - `qwen-image-3.0-pro`、`qwen-image-2.0-pro`（千问系列，强文本渲染与语义一致性）  
  - `z-image-turbo`（轻量级快速生图，适合低延迟场景）  
  - `kling/kling-v3-omni-image-generation`（支持分镜组图与角色连续性）  
  - `vidu/vidu-image_reference2image`（高精度UI/图表渲染与像素级还原）

- **专业图像编辑模型**：  
  - `wan2.5-i2i-preview`（通用图生图，支持单图编辑与多图融合）  
  - `wan2.7-image-pro`（支持图像编辑、文生组图、图生组图）  
  - `qwen-image-edit-max`（工业设计、几何推理、角色一致性强化）  
  - `wanx2.1-imageedit`（扩图、去水印、线稿生图、局部重绘等全栈编辑）

- **垂直场景创意工具**：  
  - `wanx-sketch-to-image-lite`（涂鸦作画）、`wanx-x-painting`（局部重绘）、`wanx-style-repaint-v1`（人像风格重绘）  
  - `image-out-painting`（画面扩展）、`image-erase-completion`（擦除补全）、`image-instance-segmentation`（人物实例分割）  
  - `virtualmodel-v2`（虚拟模特）、`shoemodel-v1`（鞋靴试穿）、`facechain`（人物写真训练与生成）  
  - `wordart`（创意文字变形与纹理生成）、`qwen-mt-image`（图像文字翻译）  

> **注意**：部分模型如 `wanx-x-painting`、`wanx-virtualmodel`、`image-erase-completion` 等当前仅提供免费体验，额度用尽后不可调用且不支持付费，替代方案请参考 [图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide) 或 [图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit) —— 此信息来自 [常见问题 (raw/model-api-reference/image-generation/image-faq.md)](../../raw/model-api-reference/image-generation/image-faq.md)。

## 关键参数

所有模型共用基础参数结构，但具体支持项因模型而异：

- **`model`**（必选）：模型标识符，如 `"wan2.6-t2i"`、`"qwen-image-3.0-pro"`。各地域支持模型列表需查阅 [模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。
- **`input`**（必选）：输入内容，格式取决于任务类型：
  - 文生图：`{"text": "prompt"}`（`qwen`/`wan2.7` 等新协议）或 `{"prompt": "..."}`（旧协议如 `wanx-v1`）  
  - 图生图：`{"messages": [...]}` 中包含 `text` + `image` 对象（如 [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md) 所示）  
  - 局部编辑：需提供 `base_image_url` 与 `mask_image_url`（如 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)）
- **`parameters`**（可选）：控制生成行为：
  - `size`：分辨率，支持 `"1024*1024"`、`"1K"`、`"2K"`、`"4K"` 或宽高比约束（如 `"16:9"`）。`wan2.6-t2i` 要求总像素在 `[1280*1280, 1440*1440]`，`qwen-image-3.0` 要求 `[512*512, 2048*2048]`。
  - `n`：生成张数，范围通常为 `1–9`（`qwen-image-max` 固定为 `1`）。
  - `watermark`：是否添加水印（`true`/`false`），默认 `true`。
  - `prompt_extend`：启用提示词智能扩展（如 `z-image-turbo`）。
  - `aspect_ratio` / `resolution`：用于 `kling` 等模型指定构图与清晰度。
- **请求头**（HTTP 必选）：
  - `Authorization: Bearer $DASHSCOPE_API_KEY`
  - `Content-Type: application/json`
  - 异步模型必须含 `X-DashScope-Async: enable`；同步模型（如 `wan2.6-t2i`）**不得设置该头**。

> **注意**：`size` 参数在不同文档中存在矛盾：`wan2.5-i2i-preview` 文档称“未指定时默认 `1280*1280`”，而 `qwen-image-2.0-pro` 文档称“默认总像素接近 `1024*1024`”。实际行为以模型实际响应为准，建议显式指定。

## 使用方式

### 调用协议选择
- **同步调用**（推荐多数场景）：适用于 `wan2.6-t2i`、`z-image-turbo`、`wan2.7-image-pro` 等模型，一次请求返回结果。Endpoint 为 `/api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**（必需长耗时任务）：适用于 `wanx-v1`、`wan2.5-i2i-preview`、`qwen-mt-image` 等模型，需两步操作：
  1. `POST /.../generation` 创建任务，获取 `task_id`；
  2. `GET /.../result?task_id=xxx` 轮询结果（有效期 24 小时）。

### 地域与域名
- **必须匹配**：API Key、Endpoint、模型三者所属地域须一致（北京/新加坡/弗吉尼亚/法兰克福/东京），跨地域调用将鉴权失败。
- **推荐域名**：优先使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于通用域名 `https://dashscope.aliyuncs.com` —— 此建议在 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 等多篇文档中反复强调。

### 开发准备
- 获取并配置 API Key（[获取指南](https://help.aliyun.com/zh/model-studio/get-api-key)）。
- 安装 DashScope SDK（Python/Java 支持）或直接构造 HTTP 请求。
- 图片 URL 必须公网可访问（OSS 或自建存储），禁止内网地址或含中文路径。

## 限制和注意事项

- **免费额度与计费**：所有模型均提供 500 张免费额度（90 天有效期），主账号与 RAM 子账号共享。超出后按单价计费（如 `wanx-v1` 0.16 元/张，`wanx-sketch-to-image-lite` 0.06 元/张），详情见 [模型计费与限流](https://help.aliyun.com/zh/model-studio/image-faq#3436cf2280fnh) —— 此说明在 [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md) 等文档中明确引用。
- **限流规则**：主账号与子账号共用 QPS/RPS 限制（常见为 2 QPS），同时处理中任务数上限为 1–5（如 `image-out-painting` 为 5）。
- **图片要求**：
  - URL 必须支持 HTTP/HTTPS 且无中文字符；
  - 分辨率通常要求 `[512, 4096]` 像素单边长度，大小 ≤10 MB；
  - 下载失败报错 `"Reference image download failed"` 时，需检查链接可达性与权限（见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)）。
- **模型弃用**：`wanx-v1` 已被明确标注为“推荐使用全面升级的文生图V2版模型”，旧版仅限兼容场景。
- **地域特例**：`qwen-mt-image`、`facechain`、`wordart` 等模型**仅支持华北2（北京）地域**，调用前务必确认。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)


