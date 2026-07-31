# image generation

百炼平台的图像生成能力覆盖文生图、图生图、图像编辑、风格迁移、背景生成、扩图、擦除补全等全链路视觉创作场景，支持多模型协同与精细化控制。所有服务均基于统一 API 协议，但不同模型在调用方式（同步/异步）、输入结构（`input.messages` vs `input.prompt`）和参数约束上存在显著差异，开发者需按模型文档严格适配。

## 支持的模型/功能

百炼提供两类主流图像模型体系：**万相（WanX）系列**与**千问（Qwen）系列**，以及面向垂直场景的专用模型。

- **文生图（T2I）**：  
  - 万相：`wan2.6-t2i`、`wan2.7-image-pro`（支持4K）、`z-image-turbo`（轻量快速）；  
  - 千问：`qwen-image-2.0-pro`、`qwen-image-max`、`qwen-image-3.0-pro`（支持T2I+I2I）；  
  - 可灵：`kling/kling-v3-image-generation`（支持1k/2k/4k及分镜组图）；  
  - Vidu：`vidu/vidu-image_reference2image`（强文字渲染与UI还原）。  
  > **注意**：`wanx-v1` 已被明确标记为“推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”，其V1版文档 [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md) 中的 `wanx-v1` 模型已不建议新项目接入。

- **图像编辑与图生图（I2I）**：  
  - 通用编辑：`wan2.5-i2i-preview`（单/多图融合）、`wan2.7-image-pro`（图文混排）、`qwen-image-3.0-pro`（多图参考+精确编辑）；  
  - 局部操作：`wanx-x-painting`（局部重绘）、`image-erase-completion`（擦除补全）、`image-out-painting`（画面扩展）；  
  - 风格迁移：`wanx-style-repaint-v1`（人像风格重绘）、`wanx-sketch-to-image-lite`（涂鸦作画）。

- **垂直场景模型**：  
  - 商品展示：`wanx-virtualmodel`（虚拟模特）、`shoemodel-v1`（鞋靴试穿）、`aitryon-plus`（AI试衣）；  
  - 基础工具：`image-instance-segmentation`（人物实例分割）、`qwen-mt-image`（图像翻译）、`facechain-portrait-generation`（人物写真训练与生成）；  
  - 创意设计：`wanx-poster-generation-v1`（创意海报）、`wordart-quick-start`（创意文字纹理）。

所有模型均需通过 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md) 中所述的统一计费与限流规则管理，免费额度为500张/账号（主账号与RAM子账号共享），但部分模型如 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1` 等明确标注“目前仅供免费体验，免费额度用完后不可调用且不支持付费”。

## 关键参数

核心参数因模型类型而异，需严格区分：

- **尺寸控制**：  
  - `size`：字符串格式，如 `"1024*1024"`、`"2K"`、`"1k"`；部分模型（如 `wan2.6-t2i`）支持宽高比范围 `[1:4, 4:1]`，而 `qwen-image-3.0-pro` 要求总像素在 `512*512` 至 `2048*2048` 之间；  
  - `aspect_ratio`：仅 `kling` 系列支持显式设置（如 `"16:9"`）；  
  - `resolution`：`kling` 和 `vidu` 模型专用，值为 `"1k"`/`"2k"`/`"4k"`。

- **输出控制**：  
  - `n`：生成图片张数，多数模型支持 `1-6` 张，`kling` 支持 `1-9` 张，`vidu` 固定为 `1` 张；  
  - `watermark`：布尔值，控制是否添加水印（如 `wan2.7-image-pro` 默认 `false`）；  
  - `prompt_extend`：启用智能提示词优化（如 `z-image-turbo`），会增加响应时间。

- **输入结构**：  
  - 文生图模型（如 `wan2.6-t2i`、`qwen-image-3.0-pro`）使用 `input.messages` 数组，其中 `content` 为文本或图像对象；  
  - 旧版模型（如 `wanx-v1`、`wanx-background-generation-v2`）使用 `input.prompt` 字符串；  
  - 编辑类模型（如 `wan2.5-i2i-preview`）要求 `input.sketch_image_url` 或 `input.base_image_url` + `input.mask_image_url`。

- **其他关键参数**：  
  - `thinking_mode`（`z-image-turbo`）、`enable_interleave`（`wan2.6-image`）、`series_amount`（`kling/kling-v3-omni-image-generation` 分镜数量）等均为模型特有参数，不可跨模型复用。

## 使用方式

所有图像API均采用 **HTTP协议**，支持同步与异步两种调用模式，选择依据模型能力：

- **同步调用（推荐多数场景）**：  
  适用于 `wan2.6-t2i`、`wan2.7-image-pro`、`z-image-turbo`、`qwen-image-3.0-pro` 等支持新版 `multimodal-generation/generation` 接口的模型。一次请求即返回结果，Endpoint为：  
  `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（北京）或对应地域域名。  
  > 必须配置 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`，无需 `X-DashScope-Async` 头。

- **异步调用（必需场景）**：  
  适用于 `wanx-v1`、`wanx-x-painting`、`wanx-style-repaint-v1`、`image-out-painting` 等耗时较长的模型。流程为两步：  
  1. **创建任务**：向 `.../image-synthesis` 或 `.../generation` 端点发送请求，获取 `task_id`；  
  2. **轮询结果**：用 `task_id` 调用查询接口（如 `GET /api/v1/tasks/{task_id}`），直至 `task_status` 为 `SUCCEEDED`，返回图片URL（有效期24小时）。  
  所有异步请求必须携带 `X-DashScope-Async: enable` 请求头，否则报错“current user api does not support synchronous calls”——该限制在 [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md) 中被明确强调。

- **地域与认证**：  
  华北2（北京）、新加坡、美国（弗吉尼亚）地域拥有独立 API Key 与 Endpoint，**不可混用**；强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性，该建议在 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 等多篇文档中重复出现。

## 限制和注意事项

- **地域与模型绑定**：绝大多数模型（如 `wanx-v1`、`wanx-x-painting`、`wanx-style-repaint-v1`、`wanx-background-generation-v2`、`shoemodel-v1`、`image-instance-segmentation`、`image-erase-completion`）**仅支持华北2（北京）地域**，且必须使用该地域的 API Key；跨地域调用将直接失败。

- **图片URL要求**：所有涉及外部图片输入（`image_url`、`mask_url`、`ref_image_url` 等）的模型，均要求 URL **公网可访问、支持 HTTP/HTTPS、无中文字符、图片大小≤10MB**；若下载失败，错误码为 `BadRequest.InputDownloadFailed`，解决方案见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

- **免费额度与停用风险**：  
  - `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation`、`image-erase-completion`、`wanx-poster-generation-v1` 等模型明确标注“免费额度用完后不可调用且不支持付费”，无替代商业化路径；  
  - `wan2.6-t2i` 等商用模型则提供明确计费单价（如 `wanx-v1` 为 `0.16元/张`），需关注 [模型计费与限流](../../raw/model-api-reference/image-generation/image-faq.md) 中的详细说明。

- **输入格式陷阱**：  
  > **注意**：`wan2.6-image`（图文混排）与 `wan2.7-image-pro`（文生图）虽同属万相2.x系列，但前者仅支持[流式输出](../concepts/streaming-output.md)且 `enable_interleave` 参数需显式设置，而后者默认支持同步返回；二者 `input` 结构相同但 `parameters` 含义不同，混用将导致不可预期行为。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)


