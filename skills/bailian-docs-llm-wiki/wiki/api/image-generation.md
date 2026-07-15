# image generation

百炼平台提供多种图像生成与编辑能力，覆盖文生图、图生图、局部编辑、背景生成、风格迁移等核心场景。所有模型均通过统一的 HTTP API 接口调用，支持同步与异步两种模式，开发者可根据任务耗时和业务需求灵活选择。模型能力按功能域组织，部分模型已升级为多模态统一接口（如 `multimodal-generation/generation`），而历史模型仍沿用独立路径（如 `text2image/image-synthesis`）。

## 支持的模型/功能

平台当前提供三类主流图像能力：

- **通用文生图模型**：包括千问系列（`qwen-image-*`）、万相V2/V2.6/V2.7（`wan2.6-t2i`、`wan2.7-image-pro`）、Z-Image（`z-image-turbo`）及Vidu、可灵等专业模型。其中 `qwen-image-2.0-pro` 和 `wan2.7-image-pro` 为当前推荐主力模型，分别在文字渲染精度与4K高清输出上具备优势 [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)。
  
- **图像编辑与增强模型**：涵盖千问图像编辑（`qwen-image-edit-*`）、万相通用编辑（`wan2.5-i2i-preview`、`wanx2.1-imageedit`）、局部重绘（`wanx-x-painting`）、虚拟模特（`virtualmodel-v2`）、鞋靴试穿（`shoemodel-v1`）等。需注意 `wanx-x-painting` 和 `wanx-virtualmodel` 等部分模型仅限免费体验，额度用尽后不可调用 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

- **创意工具与垂直模型**：包括图像画面扩展（`image-out-painting`）、背景生成（`wanx-background-generation-v2`）、人物实例分割（`image-instance-segmentation`）、图像擦除补全（`image-erase-completion`）、AI试衣（`aitryon-plus`）、FaceChain人像写真、WordArt锦书文字艺术等。这些模型多采用异步调用，且普遍限定于华北2（北京）地域 [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)。

> **注意**：文档中存在模型命名不一致问题。例如 `wan2.6-t2i`（文生图专用）与 `wan2.6-image`（支持图文混排）属不同能力栈，但文档未明确区分其适用边界；另 `wan2.7-image-pro` 在文生图场景支持4K，但在图像编辑场景仅支持2K，该限制未在所有相关文档中同步说明。

## 关键参数

所有图像API均通过 `parameters` 对象控制输出行为，核心参数如下：

- `size`：指定输出分辨率。格式支持 `宽*高`（如 `"1024*1024"`）、预设档位（如 `"1K"`、`"2K"`、`"4K"`）或比例（如 `"4:3"`）。不同模型支持范围不同：`qwen-image-*` 要求总像素在 `512×512` 至 `2048×2048` 之间；`wan2.6-t2i` 限定总像素在 `[1280×1280, 1440×1440]`；`vidu` 系列支持 `1K/2K/4K` 档位。未指定时，各模型按默认规则推导（如 `qwen-image-edit` 默认总像素接近 `1024×1024`，宽高比继承最后一张输入图）。

- `n`：生成图像张数。`qwen-image-max` 固定为 1 张；`qwen-image-2.0-pro`、`wan2.5-i2i-preview` 等支持 `1–6`；`kling/kling-v3-omni-image-generation` 在组图模式下通过 `series_amount` 指定 `2–9` 张。

- `watermark`：布尔值，控制是否添加平台水印。多数模型默认 `true`，生产环境建议显式设为 `false`。

- `prompt_extend`：仅 `z-image-turbo` 等部分模型支持，启用后返回优化提示词及推理过程，但增加响应延迟。

- 其他功能型参数：`aspect_ratio`（`kling` 系列）、`resolution`（`kling`）、`ref_prompt_weight`（背景生成）、`dilate_flag`（擦除补全）、`thinking_mode`（`wan2.7-image-pro`）等，需按具体模型文档使用。

## 使用方式

### 调用模式
- **同步调用**：适用于响应快（通常 < 10s）的模型，如 `qwen-image-2.0-pro`（北京/新加坡地域）、`wan2.6-t2i`（仅 `wan2.6`）、`z-image-turbo`（北京地域）、`wan2.7-image-pro`。请求地址统一为 `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`，需配置 `X-DashScope-Sse: enable` + `parameters.stream: true` 才支持流式图文混排输出。
  
- **异步调用**：适用于耗时较长（1–2分钟）的模型，如 `wanx-v1`、`wanx-x-painting`、`image-out-painting`、`wanx-background-generation-v2` 等。流程分两步：
  1. 创建任务：`POST {endpoint}`，返回 `task_id`；
  2. 轮询结果：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`（部分模型如 `image-instance-segmentation` 明确要求此路径）。

### 必要配置
- **API Key 与地域绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）地域各自独立管理 API Key 与请求域名，跨地域调用将鉴权失败。强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)。
- **请求头强制项**：异步调用必须包含 `X-DashScope-Async: enable`；同步调用需 `Content-Type: application/json` 和 `Authorization: Bearer $DASHSCOPE_API_KEY`。
- **输入格式**：文生图使用 `input.prompt` 或 `input.messages`；图生图/编辑类模型使用 `input.messages` 数组，内含 `{"text": "..."}` 和 `{"image": "url"}` 对象；部分旧模型（如 `wanx-v1`）仍用 `input.ref_image` 字段。

## 限制和注意事项

- **地域与模型可用性**：`qwen-mt-image`、`vidu`、`kling`、`virtualmodel-v2`、`shoemodel-v1`、`wanx-poster-generation-v1` 等全部限定于华北2（北京）地域；`z-image-turbo` 新加坡地域仅支持专属域名调用；`wan2.6-t2i` 在美国（弗吉尼亚）支持同步调用，但 `wan2.5` 及以下版本不支持。
  
- **免费额度与计费**：所有模型均提供 500 张免费额度（有效期 90 天），主账号与 RAM 子账号共享。`wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`wanx-poster-generation-v1`、`image-instance-segmentation`、`image-erase-completion` 等模型无计费单价，免费额度用尽即停用；其余模型如 `wanx-v1`（0.16元/张）、`wanx-style-repaint-v1`（0.12元/张）按成功生成图片计费。

- **输入约束**：
  - 图片 URL 必须公网可访问、无中文路径、支持 HTTP/HTTPS；
  - 图像尺寸：多数模型要求单边 ≥ 512px 且 ≤ 4096px，文件大小 ≤ 10MB；
  - 局部编辑类模型（如 `wanx-x-painting`）需提供 `mask_image_url`，且涂抹区域需为非零像素；
  - `image-erase-completion` 的 `mask_url` 必须与原图同尺寸，非零区域为擦除目标。

- **错误处理**：常见报错 `BadRequest.InputDownloadFailed` 表示图片 URL 不可达，需检查网络权限与 OSS/Bucket ACL 配置；缺失 `X-DashScope-Async` 头将直接返回“不支持同步调用”错误。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)


