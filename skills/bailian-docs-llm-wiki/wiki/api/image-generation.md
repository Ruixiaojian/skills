# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图、图生图、局部重绘、风格迁移、背景生成、AI试衣等20余种专业场景。所有模型均通过统一的HTTP API或DashScope SDK调用，支持同步与异步两种模式，适用于从快速原型验证到高并发生产环境的各类需求。

## 支持的模型/功能

平台当前提供三大类图像模型能力：

- **通用文生图与编辑**：包括千问系列（`qwen-image-*`、`qwen-image-edit-*`）、万相系列（`wan2.7-image-*`、`wan2.6-t2i`、`wanx2.1-t2i-*`）、Z-Image（`z-image-turbo`）和可灵（`kling/kling-v3-*`）。其中 `qwen-image-2.0-pro` 和 `wan2.7-image-pro` 为当前推荐主力模型，分别在文字渲染精度与4K高清输出上具备优势 [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)。
  
- **垂直场景专用模型**：覆盖电商与设计工作流，如虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）、创意海报生成（`wanx-poster-generation-v1`）、图像背景生成（`wanx-background-generation-v2`）、人物实例分割（`image-instance-segmentation`）及图像擦除补全（`image-erase-completion`）。这些模型多为地域限定（仅华北2北京），且部分处于免费体验阶段 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

- **创意工具与辅助能力**：包括涂鸦作画（`wanx-sketch-to-image-lite`）、人像风格重绘（`wanx-style-repaint-v1`）、AI试衣（`aitryon-plus`）、FaceChain人物写真、WordArt锦书文字艺术等。其中 FaceChain 需先完成人物形象训练再生成写真，而 WordArt 锦书则专注于汉字纹理与变形 [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)。

> **注意**：文档中存在模型命名与能力描述不一致的情况。例如，`wan2.6-t2i` 在 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 中明确标注为“支持HTTP同步调用”，但同系列 `wan2.5-t2i-preview` 及更早版本则“不支持HTTP同步调用”；而 `wan2.7-image-pro` 在 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md) 中声明“仅文生图场景支持4K分辨率”，但未说明组图生成的最高分辨率限制。开发者应以实际调用返回的 `400 Bad Request` 错误码及官方控制台模型详情页为准。

## 关键参数

所有图像API均通过 `parameters` 对象传递核心控制参数，常见字段如下：

- `size` / `resolution` / `aspect_ratio`：控制输出尺寸。格式多样，如 `"1024*1024"`（万相V1/V2）、`"2K"`（万相2.7）、`"1k"`（可灵、Vidu）、`"1:1"`（可灵、Vidu）。总像素范围普遍为 `512×512` 至 `2048×2048`，`wan2.7-image-pro` 文生图支持 `4K`（`3840×2160`）[万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。
- `n`：生成图片张数，取值范围因模型而异：`1–6`（千问系列）、`1–9`（可灵）、`1–4`（创意海报、鞋靴模特）。
- `watermark`：布尔值，控制是否添加平台水印，默认 `true`，部分模型（如 `wan2.7-image-pro`）支持设为 `false`。
- `prompt_extend`：启用智能提示词扩展，返回优化后的提示词及推理过程，会增加响应时间（Z-Image、万相2.6等支持）。
- `style_index` / `style_ref_url`：用于人像风格重绘，前者指定预置风格索引，后者传入自定义风格参考图。
- `X-DashScope-Async`：**必选请求头**，异步调用必须设为 `"enable"`；缺失将报错 `"current user api does not support synchronous calls"`。

## 使用方式

### 调用模式
- **同步调用**：适用于耗时较短（通常 < 15s）的模型，如 `z-image-turbo`、`wan2.6-t2i`、`qwen-image-*`（Pro/Plus系列默认同步）。一次HTTP POST即可返回结果，无需轮询。
- **异步调用**：适用于耗时较长（1–2分钟）的模型，如万相V1、局部重绘、虚拟模特、背景生成等。流程分两步：
  1. `POST /api/v1/services/.../generation` 创建任务，获取 `task_id`；
  2. `GET /api/v1/tasks/{task_id}` 轮询状态，直至 `task_status == "SUCCEEDED"` 后获取 `output.results[].url`。

### 地域与域名
- 华北2（北京）、新加坡、美国（弗吉尼亚）地域拥有独立API Key与请求地址，**不可混用**。
- 强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性；旧域名（`dashscope.aliyuncs.com`）仍兼容但非最优 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)。

### 认证与环境
- 必须配置 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头。
- 推荐通过环境变量管理API Key，并使用DashScope SDK（Python/Java）简化调用逻辑。

## 限制和注意事项

- **免费额度与计费**：所有模型均提供500张免费额度（有效期90天），主账号与RAM子账号共享。超出后按模型单价计费（如 `wanx-v1`: 0.16元/张，`wanx-style-repaint-v1`: 0.12元/张），仅对**成功生成的输出图片**收费 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **图片URL要求**：输入图片URL必须公网可访问、无中文路径、支持HTTP/HTTPS。若下载失败，错误码为 `BadRequest.InputDownloadFailed`，需检查链接有效性或上传至OSS等云存储 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **限流策略**：主账号与RAM子账号共用QPS/RPS限制（常见为2 QPS），同时处理中任务数上限为1–5个，超限将返回 `429 Too Many Requests`。
- **模型可用性**：部分模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`）当前仅限免费体验，额度用尽后不可调用且不支持付费，文档已明确提示替代方案 [图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)


