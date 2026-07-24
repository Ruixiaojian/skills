# image generation

百炼平台提供丰富的图像生成与编辑能力，覆盖文生图（T2I）、图生图（I2I）、局部重绘、风格迁移、背景生成、扩图、擦除补全等核心场景。所有模型均通过统一的 HTTP API 或 DashScope SDK 调用，支持华北2（北京）、新加坡、美国（弗吉尼亚）等多地域部署，推荐使用业务空间专属域名以获得更高稳定性与性能。开发者需先开通对应模型服务并配置 API Key，部分模型处于邀测或免费体验阶段，详见各模型说明。

## 支持的模型/功能

百炼图像生成能力由多个专用模型支撑，按任务类型划分如下：

- **文生图（T2I）**：`qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo`、`kling/kling-v3-image-generation`、`vidu/vidu-image_reference2image` 等，支持自由指定分辨率（如 `1024*1024`、`2K`、`4K`）、宽高比（如 `1:1`、`16:9`）及输出张数（`n=1~9`）。其中 `qwen-image-3.0-pro` 同时支持 T2I 与 I2I，而 `z-image-turbo` 为轻量级快速模型 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **图生图/图像编辑（I2I）**：`qwen-image-2.0-pro`、`wan2.7-image-pro`、`wan2.5-i2i-preview`、`kling/kling-v3-omni-image-generation`（支持多图输入与分镜组图），支持基于 1–3 张参考图进行风格迁移、内容增删、主体动作修改等 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)。
- **专业工具类模型**：
  - 局部重绘：`wanx-x-painting`（免费体验，已停用付费）；
  - 虚拟模特：`virtualmodel-v2`（支持 2048px 输出与多宽高比）；
  - 鞋靴试穿：`shoemodel-v1`（免费体验）；
  - 图像擦除补全：`image-erase-completion`（免费体验）；
  - 人物实例分割：`image-instance-segmentation`（免费体验）；
  - 创意海报生成：`wanx-poster-generation-v1`（免费体验）；
  - 文字渲染与变形：`WordArt锦书`（支持汉字纹理与轮廓创意生成）[创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)。

> **注意**：`wanx-v1`（文生图V1）已被明确标记为“**推荐使用全面升级的文生图V2版模型**”，其能力与计费模式均已过时，不应作为新项目首选 [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)。

## 关键参数

所有图像模型共用以下核心参数结构，但具体取值范围与语义因模型而异：

- `model`：必填字符串，模型 ID（如 `"qwen-image-3.0-pro"`、`"wan2.7-image-pro"`），需与所选地域支持列表一致。
- `input`：必填对象，结构依任务类型变化：
  - 文生图：`{"messages": [{"role": "user", "content": [{"text": "提示词"}]}]}`（推荐）或旧式 `{"prompt": "..."}`（部分模型兼容）；
  - 图生图/编辑：`{"messages": [...]}` 中 `content` 可混合 `{"text": "指令"}` 与 `{"image": "url"}`；
  - 工具类（如局部重绘）：`{"base_image_url": "...", "mask_image_url": "...", "prompt": "..."}`。
- `parameters`：可选对象，常用字段包括：
  - `size`：分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）或预设值（`"1K"`、`"2K"`、`"4K"`）；部分模型（如 `qwen-image-3.0-pro`）允许总像素在 `512*512` 至 `2048*2048` 间自由设定；
  - `n`：生成张数，范围通常为 `1~9`（`wanx-style-repaint-v1` 固定为 `1`）；
  - `aspect_ratio`：宽高比（仅 `kling` 系列支持 `"16:9"`、`"9:16"`、`"1:1"`）；
  - `watermark`：布尔值，控制是否添加水印（默认 `true`）；
  - `prompt_extend`：布尔值，启用后返回优化提示词（如 `qwen-image-3.0-pro`、`z-image-turbo`）；
  - `thinking_mode`：布尔值，开启智能思考（`wan2.7-image-pro`）。

## 使用方式

### 调用协议与流程
- **同步调用**：适用于 `wan2.6-t2i`、`z-image-turbo`、`wan2.7-image-pro` 等模型，单次 HTTP 请求直接返回结果（含图片 URL），推荐大多数场景使用。
- **异步调用**：适用于耗时较长的模型（如 `wanx-v1`、`wanx-x-painting`、`image-out-painting`），需两步操作：
  1. 发起 `POST /api/v1/services/.../generation` 创建任务，获取 `task_id`；
  2. 轮询 `GET /api/v1/tasks/{task_id}` 查询状态，`task_status == "SUCCEEDED"` 时返回图片 URL（有效期 24 小时）。

### 地域与域名
- 华北2（北京）、新加坡、美国（弗吉尼亚）地域拥有独立 API Key 与请求地址，**不可混用**。
- 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），替代旧域名 `https://dashscope.aliyuncs.com`，以提升性能与稳定性。`{WorkspaceId}` 在百炼控制台“业务空间详情”中获取。

### 认证与请求头
- 必填 `Authorization: Bearer $DASHSCOPE_API_KEY`；
- 同步调用：`Content-Type: application/json`；
- 异步调用：**必须**添加 `X-DashScope-Async: enable`，否则报错。

## 限制和注意事项

- **免费额度与计费**：多数模型提供 500 张/90 天免费额度（主账号与 RAM 子账号共享），额度用尽后按单价计费（如 `wanx2.1-imageedit` 0.14 元/张）。`wanx-x-painting`、`shoemodel-v1`、`image-erase-completion` 等模型**仅限免费体验，额度用尽即不可调用，且不支持付费**，文档明确建议迁移到 `qwen-image-edit` 或 `wanx2.1-imageedit` [图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。
- **图片 URL 要求**：所有输入图片 URL 必须为公网可访问、支持 HTTP/HTTPS 协议，且不含中文字符；推荐上传至 OSS 获取临时公网 URL。
- **分辨率与格式**：
  - PNG 为最常见输出格式（`qwen`、`wan`、`kling` 系列）；
  - JPG 仅用于 `qwen-mt-image`（图像翻译）；
  - 输入图像分辨率通常要求 `512×512` 至 `4096×4096`，单边长度 `[512, 4096]` 像素，大小 ≤10MB。
- **错误处理**：常见错误如 `"BadRequest.InputDownloadFailed"` 表明图片 URL 不可达，需检查链接有效性与访问权限；`"InvalidApiKey"` 表示认证失败，应核对 API Key 是否正确配置。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
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


