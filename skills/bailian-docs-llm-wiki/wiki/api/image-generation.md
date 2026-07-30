# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图、图生图、局部重绘、风格迁移、背景生成、AI试衣等20+类模型。所有服务均通过统一的HTTP API或DashScope SDK调用，支持同步/异步模式，并按实际成功生成图片计费。开发者需根据地域选择对应API Key与业务空间专属域名以保障稳定性与性能。

## 支持的模型/功能

百炼平台图像能力分为通用生成、专业编辑与创意工具三大类：

- **通用生成模型**：包括 `wan2.6-t2i`（万相V2文生图）、`qwen-image-3.0-pro`（千问3.0[多模态](../concepts/multi-modal.md)生成）、`z-image-turbo`（轻量级快速生图）和 `kling/kling-v3-omni-image-generation`（可灵分镜组图）。其中 `qwen-image-3.0-pro` 同时支持文生图（T2I）与图生图（I2I），且输出总像素需在512×512至2048×2048之间 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；`wan2.6-t2i` 支持自由选尺寸，总像素范围为[1280×1280, 1440×1440] [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

- **专业编辑模型**：覆盖 `wan2.7-image-pro`（万相2.7图文混排与4K编辑）、`qwen-image-edit`（千问图像编辑，支持多图输入/输出及文字渲染增强）和 `vidu/vidu-image_reference2image`（Vidu参考生图，支持最多14张参考图）。

- **创意工具模型**：包括 `wanx-x-painting`（图像局部重绘）、`wanx-style-repaint-v1`（人像风格重绘）、`image-out-painting`（画面扩展）、`shoemodel-v1`（鞋靴模特）、`facechain`（人物写真训练与生成）及 `wordart`（创意文字变形与纹理生成）等垂直场景专用模型。部分模型如 `wanx-x-painting` 和 `shoemodel-v1` 当前仅提供免费体验，额度用尽后不可调用 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

> **注意**：文档中 `wanx-v1`（万相V1）明确标注“推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”；而 `wan2.6-t2i` 文档指出其支持HTTP同步调用，但 `wan2.5` 及以下版本仅支持异步调用——二者能力存在代际差异，V2应为当前主力推荐版本。

## 关键参数

各模型共性参数如下，具体取值因模型而异：

- `model`：必填字符串，指定模型ID（如 `"wan2.6-t2i"`、`"qwen-image-3.0-pro"`）。
- `input.prompt` 或 `input.messages`：文本提示词，`qwen-image-3.0-pro` 等新模型要求使用 `messages` 格式（含 `role` 和 `content` 数组）。
- `parameters.size`：图像分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）或语义化值（如 `"1K"`、`"2K"`、`"4K"`）。`wan2.5-i2i-preview` 默认生成 `1280*1280` 图像并保持输入图宽高比 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。
- `parameters.n`：生成图片数量，范围通常为 `1–9`（`qwen-image-2.0-pro` 支持 `1–6` 张）。
- `parameters.watermark`：布尔值，控制是否添加水印（默认 `true`）。
- `X-DashScope-Async`：请求头必填项，异步调用必须设为 `"enable"`；同步调用（如 `wan2.6`）则不包含此头。

## 使用方式

### 域名与认证
- **必须使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。旧域名 `dashscope.aliyuncs.com` 仍可用但不推荐 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)。
- **API Key配置**：需提前获取并设为环境变量 `DASHSCOPE_API_KEY`，请求头中使用 `Authorization: Bearer $DASHSCOPE_API_KEY`。

### 调用模式
- **同步调用**：适用于 `wan2.6-t2i`、`z-image-turbo` 等低延迟模型，单次请求返回结果。Endpoint为 `/api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**：适用于耗时较长的模型（如局部重绘、虚拟模特），流程为两步：
  1. `POST /api/v1/services/.../generation` 创建任务，获取 `task_id`；
  2. 轮询 `GET /api/v1/tasks/{task_id}` 查询状态，成功后返回图片URL（有效期24小时）。

### 示例命令
```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan2.6-t2i",
    "input": {"prompt": "一间花店，木质门，摆放花朵"},
    "parameters": {"size": "1024*1024", "n": 1}
  }'
```

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的API Key与Endpoint不可混用，跨地域调用将鉴权失败。
- **图片URL要求**：所有输入图片URL必须公网可访问、无中文路径、支持HTTP/HTTPS协议；OSS等云存储需配置公开读权限。
- **免费额度与计费**：多数模型提供500张免费额度（90天有效），额度用尽后按单价计费（如 `wanx-v1` 为0.16元/张）。计费仅针对**成功生成的输出图片**，失败或输入图片不计入 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **文件限制**：输入图像格式限于 JPG/PNG/WEBP/BMP/AVIF；分辨率通常要求 ≥512×512 且 ≤4096×4096；单图大小 ≤10MB。
- **模型弃用风险**：`wanx-v1`、`wanx-x-painting`、`shoemodel-v1` 等模型明确标注“仅免费体验”或“推荐替代方案”，长期项目应优先选用 `qwen-image-3.0-pro` 或 `wan2.7-image-pro` 等持续维护的主力模型。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)




