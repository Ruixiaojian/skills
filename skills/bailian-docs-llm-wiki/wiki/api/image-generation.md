# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图、图生图、局部重绘、风格迁移、背景生成、扩图、擦除补全等数十种场景。所有模型均通过统一的 HTTP API 接口调用，支持同步与异步两种模式，并已适配 DashScope SDK（Python/Java）。开发者需根据地域选择对应 API Key 与业务空间专属域名以确保稳定性和性能。

## 支持的模型/功能

平台当前支持以下主流图像模型及能力分类：

- **通用文生图（T2I）**：`qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo`、`qwen-image-max` 等，支持自由分辨率（如 `1024*1024`、`2K`、`4K`）、多张输出（`n=1~9`）及复杂文本渲染；其中 `qwen-image-3.0-pro` 同时支持 T2I 和图生图（I2I）[千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **图像编辑与融合**：`wan2.7-image-pro`（支持 4K 文生图与 2K 编辑）、`wan2.5-i2i-preview`（单/多图融合）、`qwen-image-2.0-pro`（文字精准添加、物体增删与风格迁移）；`qwen-image-edit` 系列明确区分生成与编辑能力，避免混淆 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)。
- **垂直场景专用模型**：
  - 局部重绘：`wanx-x-painting`（仅限北京地域，免费额度用尽后不可用）；
  - 虚拟模特：`virtualmodel-v2`（支持 2048 像素短边及多种宽高比）；
  - 鞋靴试穿：`shoemodel-v1`（多视角鞋图输入，免费体验）；
  - 创意海报：`wanx-poster-generation-v1`（结构化输入 title/sub_title/body_text，免费体验）；
  - 图像翻译：`qwen-mt-image`（中/英↔日/韩/西/法，仅北京地域）[千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。
- **辅助工具类**：`image-out-painting`（画面扩展）、`image-instance-segmentation`（人物实例分割）、`image-erase-completion`（擦除补全）、`wanx-background-generation-v2`（背景生成）等，均采用异步调用流程。

> **注意**：部分模型（如 `wanx-v1`、`wanx-sketch-to-image-lite`）在文档中被标注为“仅适用于华北2（北京）地域”，但其实际请求 URL 与 `qwen-image-3.0` 等模型一致，均要求使用 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 域名。跨地域混用 API Key 将导致鉴权失败，此限制在 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md) 中有明确说明，需严格遵循。

## 关键参数

所有图像 API 的核心参数结构统一，关键字段如下：

- **`model`**（必填）：模型标识符，如 `"wan2.6-t2i"`、`"qwen-image-3.0-pro"`。不同模型对 `input` 结构要求不同（见下文）。
- **`input`**（必填）：
  - 文生图：`{"prompt": "描述文本"}` 或 `{"messages": [{"role":"user","content":[{"text":"..."}]}]}`；
  - 图生图/编辑：`{"messages": [{"role":"user","content":[{"image":"url1"},{"image":"url2"},{"text":"指令"}]}]}`；
  - 工具类（如擦除）：`{"image_url": "...", "mask_url": "..."}`。
- **`parameters`**（可选）：
  - `size`：字符串格式，如 `"1024*1024"`、`"2K"`（对应 `2048*2048`），部分模型（如 `qwen-image-3.0-pro`）默认自动推荐；
  - `n`：生成图片数量，范围因模型而异（`qwen-image-max` 固定为 1，`kling` 支持 1~9）；
  - `watermark`：布尔值，控制是否添加水印（默认 `true`）；
  - `aspect_ratio`：字符串，如 `"1:1"`、`"16:9"`（`kling`、`vidu` 明确支持）；
  - `style_index` / `style_ref_url`：人像风格重绘专用参数；
  - `dilate_flag`：擦除补全中控制掩码膨胀。
- **请求头（Headers）**：
  - `Authorization: Bearer $DASHSCOPE_API_KEY`（必填）；
  - `Content-Type: application/json`（必填）；
  - `X-DashScope-Async: enable`（**异步模型必填**，如 `wanx-x-painting`、`image-out-painting`；同步模型如 `wan2.6-t2i` 不需此头）。

## 使用方式

### 调用模式选择
- **同步调用**：适用于 `wan2.6-t2i`、`z-image-turbo`、`qwen-image-3.0-pro` 等新版模型，一次请求直接返回结果（HTTP 200 + 图片 URL）。Endpoint 为 `/api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**：适用于耗时较长的模型（如局部重绘、虚拟模特、扩图），需两步操作：
  1. **创建任务**：POST 到对应服务路径（如 `/api/v1/services/aigc/image2image/image-synthesis`），获取 `task_id`；
  2. **轮询结果**：GET `/api/v1/tasks/{task_id}` 直至 `task_status == "SUCCEEDED"`，响应中含 `output.results[0].url`（有效期 24 小时）。

### 地域与域名配置
- 华北2（北京）：必须使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`（`{WorkspaceId}` 在控制台业务空间详情页获取）；
- 新加坡：使用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；
- 弗吉尼亚/法兰克福：仅支持旧域名 `https://dashscope-us.aliyuncs.com` 或 `https://dashscope-intl.aliyuncs.com`，且部分模型不支持（如 `wan2.6-t2i` 同步调用）。

### 示例（同步文生图）
```bash
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "qwen-image-3.0-pro",
    "input": {
        "messages": [{"role":"user","content":[{"text":"一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"}]}]
    },
    "parameters": {"size": "1024*1024", "n": 1}
}'
```

## 限制和注意事项

- **免费额度与计费**：多数模型提供 500 张/90 天免费额度（如 `wan2.6-t2i`、`wanx-style-repaint-v1`），额度用尽后按单价计费（如 `image-out-painting` 0.18 元/张）。所有计费项仅对**成功生成的输出图片**收费，失败或输入错误不扣费 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **图片 URL 要求**：所有输入图片 URL 必须公网可访问、支持 HTTPS、无中文路径，且建议小于 5MB（`shoemodel-v1` 明确要求 <5MB；`image-erase-completion` 支持 ≤10MB）。
- **异步任务管理**：`task_id` 有效期为 24 小时，禁止重复创建任务；轮询间隔建议 ≥2 秒，避免触发限流（主账号与 RAM 子账号共享 QPS 限制，通常为 2）。
- **模型兼容性**：`wan2.5` 及以下版本**不支持同步调用**，仅能通过异步接口使用；`qwen-image-edit` 模型**不支持指定分辨率**，而 `qwen-image-edit-plus` 支持自定义宽高，需注意区分 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)。
- **地域强约束**：`qwen-mt-image`、`wanx-x-painting`、`wanx-poster-generation-v1` 等模型文档明确声明“仅适用于华北2（北京）地域”，调用时若使用其他地域 API Key 将直接报错 `InvalidApiKey`。

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
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)


