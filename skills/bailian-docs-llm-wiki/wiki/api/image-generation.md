# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、背景生成、风格迁移等全栈式视觉生成任务。所有模型均通过统一的 HTTP API 接口调用，支持同步与异步两种模式，并已适配 DashScope SDK（Python/Java）。开发者需配置地域专属 API Key 与 Workspace ID 后即可集成。

## 支持的模型/功能

百炼图像生成能力由多个专用模型构成，按任务类型可分为三类：

- **通用文生图**：`wan2.6-t2i`、`qwen-image-2.0-pro`、`z-image-turbo`、`kling/kling-v3-image-generation`、`vidu/vidu-image_reference2image` 等，支持自由提示词输入与多分辨率输出；  
- **图像编辑与增强**：`qwen-image-3.0-pro`（T2I+I2I一体化）、`wan2.7-image-pro`（4K文生图+2K编辑）、`wan2.5-i2i-preview`（单图/多图融合）、`wanx-image-edit`（去水印、扩图、超分等）；  
- **垂直场景工具**：`wanx-sketch-to-image-lite`（涂鸦作画）、`wanx-x-painting`（局部重绘）、`wanx-style-repaint-v1`（人像风格重绘）、`shoemodel-v1`（鞋靴试穿）、`image-out-painting`（画面扩展）、`image-erase-completion`（擦除补全）等 [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)。

> **注意**：部分模型仅限华北2（北京）地域使用（如 `wanx-x-painting`、`shoemodel-v1`、`image-erase-completion`），且不支持付费续用，免费额度用尽后即不可调用，官方明确建议迁移到 [千问-图像编辑](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide) 或 [万相2.1图像编辑](https://help.aliyun.com/zh/model-studio/wanx-image-edit) [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | string | 必填，模型标识符，需与地域支持列表一致 | `"wan2.6-t2i"`, `"qwen-image-3.0-pro"` |
| `size` | string / object | 图像分辨率，格式为 `"宽*高"` 或预设值（如 `"1K"`、`"2K"`、`"4K"`）；部分模型（如 `wan2.7-image-pro`）支持 `"1024*1024"`，`qwen-image-3.0-pro` 默认自动推荐 | `"1024*1024"`, `"2K"` |
| `n` | integer | 生成图片数量，范围通常为 `1–9`（`wan2.6-t2i` 最高支持6张，`kling` 支持9张） | `2` |
| `watermark` | boolean | 是否添加水印，默认 `true`；部分模型（如 `wan2.7-image-pro`）可设为 `false` | `false` |
| `prompt_extend` | boolean | 是否启用智能提示词扩展（优化输入提示词并返回推理过程），增加响应延迟 | `true` |
| `aspect_ratio` | string | 宽高比，仅 `kling` 等部分模型支持显式指定 | `"1:1"`, `"16:9"` |

> **注意**：`size` 参数行为存在不一致——`wan2.5-i2i-preview` 未指定时默认 `1280*1280` 并保持输入图宽高比，而 `qwen-image-3.0-pro` 未指定时由模型自动推荐分辨率 [原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

## 使用方式

### 1. 基础前提
- 获取对应地域的 [API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并配置至环境变量 `DASHSCOPE_API_KEY`；
- 获取业务空间 ID（Workspace ID），用于构造请求 URL（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）；
- 所有模型均要求 `X-DashScope-Async: enable` 请求头（异步）或直接使用同步端点（仅 `wan2.6`、`qwen-image-3.0-pro`、`z-image-turbo` 等新协议模型支持）。

### 2. 调用模式
- **同步调用**（推荐多数场景）：适用于 `wan2.6-t2i`、`qwen-image-3.0-pro`、`z-image-turbo`，一次请求直接返回图像 Base64 或 URL；  
- **异步调用**（必需用于长耗时任务）：适用于 `wanx-v1`、`wanx-sketch-to-image-lite`、`wanx-x-painting` 等，需两步操作：  
  1. `POST /api/v1/services/.../generation` 创建任务，获取 `task_id`；  
  2. 轮询 `GET /api/v1/tasks/{task_id}` 查询状态，成功后返回图像 URL（有效期24小时）[原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)。

### 3. 输入结构
- 文生图：`input.messages[].content[].text`（推荐）或 `input.prompt`（旧版兼容）；  
- 图生图/编辑：`input.messages[].content[]` 混合 `text` 与 `image` 对象（支持最多14张参考图，如 `vidu` 模型）；  
- 局部操作（重绘/擦除）：需传入 `base_image_url` + `mask_image_url`（白色区域为待处理区域）。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key 与请求地址**不可混用**，跨地域调用将鉴权失败；  
- **URL 可访问性**：所有输入图片 URL 必须支持公网访问，内网或私有 OSS 链接需生成临时公网 URL；  
- **免费额度**：多数模型提供 500 张/90 天免费额度（如 `wanx-v1`、`wanx-sketch-to-image-lite`），额度用尽后部分模型（如 `wanx-x-painting`、`shoemodel-v1`）直接停用，不支持付费；  
- **图像限制**：输入图分辨率通常需在 `[512, 4096]` 像素范围内，单图大小 ≤10 MB，格式支持 JPG/PNG/WEBP/BMP；  
- **错误处理**：常见报错 `"BadRequest.InputDownloadFailed"` 表示图片 URL 不可达，需检查链接有效性及权限 [原文标题](../../raw/model-api-reference/image-generation/image-faq.md)。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)


