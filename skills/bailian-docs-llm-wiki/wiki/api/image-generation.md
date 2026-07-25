# image generation

百炼平台的图像生成能力覆盖文生图、图生图、图像编辑、风格迁移、创意设计等全场景，支持多模型协同与精细化控制。所有服务均需通过 API Key 鉴权，推荐使用业务空间专属域名以获得更高稳定性与性能。开发者应优先选用新版同步协议模型（如 `wan2.7-image-pro`、`qwen-image-3.0-pro`），并在调用前确认地域、模型可用性及计费状态。

## 支持的模型/功能

百炼提供两类核心图像能力：**通用生成模型**（如万相、千问、Z-Image、Vidu、可灵）和**垂直场景工具模型**（如虚拟模特、鞋靴试穿、海报生成、FaceChain 写真等）。模型能力持续演进，部分旧版模型（如 `wanx-v1`）已明确标注为“推荐升级至 V2 版本” [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)；而部分工具类模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`）当前仅限免费体验，额度用尽后不可调用且不支持付费 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

- **主流通用模型**：
  - `wan2.7-image-pro`：支持文生图（4K）、图像编辑、图文混排，推荐用于高质量生产场景 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。
  - `qwen-image-3.0-pro`：同时支持文生图（T2I）与图生图（I2I），总像素约束为 512×512 至 2048×2048，处于邀测阶段。
  - `z-image-turbo`：轻量级模型，响应快，适用于快速原型验证。
  - `vidu/vidu-image_reference2image`：强项为中英文字渲染与 UI/图表像素级还原，支持 1K/2K/4K 输出。
  - `kling/kling-v3-omni-image-generation`：支持分镜组图生成，保持角色/场景连续性。

- **垂直工具模型**：
  - `image-out-painting`（画面扩展）、`image-erase-completion`（擦除补全）、`wanx-style-repaint-v1`（人像风格重绘）等均采用异步工作流。
  - `facechain-portrait-generation` 需先完成人物形象训练，再批量生成写真。
  - `wordart-quick-start` 专用于汉字创意变形与纹理生成，分“文字变形”与“文字纹理生成”两类接口。

> **注意**：文档间存在模型命名与能力描述不一致问题。例如，`wan2.6-image` 文档称其“如需纯文生图，建议使用 `wan2.6-t2i` 模型”，但 `wan2.6-t2i` 实际属于文生图专用模型族（见 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)），二者定位不同，不可混用。

## 关键参数

所有图像 API 均通过 `parameters` 字段控制输出行为，核心参数如下：

- `size`：指定分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）或语义化值（如 `"1K"`、`"2K"`、`"4K"`）。各模型约束不同：`wan2.7-image-pro` 文生图支持 `"2K"`，图像编辑仅支持最高 `"2K"`；`qwen-image-3.0-pro` 要求总像素在 `[512×512, 2048×2048]` 区间；`z-image-turbo` 同样适用该范围。
- `n`：生成图片张数，多数模型支持 `1–6` 张（如 `qwen-image-2.0-pro`），`kling` 模型支持 `1–9` 张，`vidu` 系列固定为 `1` 张。
- `watermark`：布尔值，默认 `true`，设为 `false` 可关闭水印（如 `wan2.7-image-pro`、`vidu`）。
- `prompt_extend`：启用智能提示词优化（如 `z-image-turbo`、`wan2.7-image-pro`），返回增强后的 [prompt](../guides/prompt.md)，但增加延迟。
- `aspect_ratio` / `resolution`：`kling` 模型使用 `aspect_ratio`（如 `"1:1"`）与 `resolution`（如 `"1k"`）组合控制输出比例与尺寸。
- `style_index` / `style_ref_url`：`wanx-style-repaint-v1` 支持预置风格索引或自定义风格图参考。
- `dilate_flag`：`image-erase-completion` 中用于控制掩码膨胀，影响擦除边缘平滑度。

## 使用方式

所有图像 API 均支持 HTTP 调用，**强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代旧域名 `https://dashscope.aliyuncs.com`，以获得更优性能与稳定性。调用流程分为两类：

- **同步调用（推荐）**：适用于 `wan2.6` 及以上、`qwen-image-3.0-pro`、`z-image-turbo`、`wan2.7-image-pro` 等模型。单次请求直接返回结果（含图片 URL 或 base64 数据），无需轮询。示例 endpoint：  
  `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

- **异步调用（必需）**：适用于 `wanx-v1`、`wan2.5-i2i-preview`、`wanx-sketch-to-image-lite`、`wanx-x-painting`、`virtualmodel-v2` 等模型。流程为两步：  
  1. **创建任务**：发送 POST 请求至对应 endpoint（如 `/api/v1/services/aigc/text2image/image-synthesis`），获取 `task_id`；  
  2. **轮询结果**：使用 `task_id` 定期调用查询接口（如 `/api/v1/tasks/{task_id}`），直至 `task_status` 为 `"SUCCEEDED"`，返回图片 URL（有效期 24 小时）。  
  所有异步请求必须携带 `X-DashScope-Async: enable` 请求头，缺失将报错。

> **注意**：`image-erase-completion` 文档中 endpoint 仍为旧域名 `https://dashscope.aliyuncs.com/...`，而其他同类模型（如 `image-out-painting`、`wanx-background-generation-v2`）均已迁移到 `maas.aliyuncs.com` 域名。开发者应统一使用新域名，避免鉴权失败。

## 限制和注意事项

- **地域与密钥隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域拥有独立 API Key 与请求地址，**不可混用**。跨地域调用将导致鉴权失败或服务报错。
- **URL 访问要求**：所有输入图片 URL 必须为公网可访问、支持 HTTP/HTTPS 协议的地址。内网地址、本地文件路径或含中文字符的 URL 均会触发 `BadRequest.InputDownloadFailed` 错误 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **免费额度与计费**：多数模型提供 500 张免费额度（90 天有效），主账号与 RAM 子账号共享。计费按成功生成图片数量计算，失败或超时任务不计费。`wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1` 等模型明确标注“免费额度用完后不可调用且不支持付费”，无替代付费通道。
- **图像格式与大小**：输出格式以 PNG 为主（`qwen-mt-image` 为 JPG）；输入图像通常要求格式为 JPG/PNG/WEBP，分辨率不低于 512×512 且不超过 4096×4096，单图大小 ≤10MB。
- **并发与限流**：主账号与 RAM 子账号共用限流策略，典型配置为任务下发接口 QPS 限制 `2`，同时处理中任务数 `1`（部分模型如 `image-out-painting` 为 `5`）。超出限流将返回 `429 Too Many Requests`。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)


