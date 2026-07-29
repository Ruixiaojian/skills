# image generation

百炼平台提供多种图像生成与编辑能力，覆盖文生图、图生图、局部编辑、风格迁移、背景生成、人物写真等全链路场景。所有模型均通过统一的 HTTP API 或 DashScope SDK 调用，支持[异步任务](../concepts/asynchronous-task.md)模式（主流）及部分模型的同步直出模式。开发者需按地域配置独立 API Key 与业务空间专属域名以确保稳定性和性能。

## 支持的模型/功能

平台当前提供三大类图像能力模型：

- **通用文生图/图生图模型**：包括 `qwen-image-3.0-pro`（[千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)）、`wan2.7-image-pro`、`z-image-turbo`、`kling/kling-v3-omni-image-generation` 和 `vidu/vidu-image_reference2image`，支持自由分辨率设置、多张输出、图文混排及分镜组图生成。
- **垂直场景专用模型**：如 `wanx-sketch-to-image-lite`（涂鸦作画）、`wanx-x-painting`（局部重绘）、`wanx-style-repaint-v1`（人像风格重绘）、`image-out-painting`（画面扩展）、`image-erase-completion`（擦除补全）等，聚焦特定任务，参数精简、效果可控。
- **创意工具与行业模型**：涵盖 `facechain-portrait-generation`（人物写真）、`outfitanyone`（AI试衣）、`wordart-quick-start`（创意文字）、`virtualmodel-v2`（虚拟模特）及 `shoemodel-v1`（鞋靴模特），需组合调用辅助模型实现端到端流程。

> **注意**：部分模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确推荐迁移到 [千问-图像编辑](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md) 或 [万相2.1图像编辑](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md) 等替代方案。

## 关键参数

| 参数名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `model` | string | 必填，指定模型名称，需与地域支持列表一致 | `"qwen-image-3.0-pro"`, `"wan2.7-image-pro"` |
| `size` / `resolution` / `aspect_ratio` | string | 控制输出分辨率与宽高比。不同模型约束不同：<br>- `qwen-image-*`：支持 `512*512` 至 `2048*2048` 总像素；<br>- `wan2.6-t2i`：宽高比 `[1:4, 4:1]`，总像素 `[1280*1280, 1440*1440]`；<br>- `kling`：固定 `1k`/`2k`/`4k` 及 `16:9`/`9:16`/`1:1`；<br>- `vidu`：支持 `1K`/`2K`/`4K` | `"1024*1024"`, `"2K"`, `"16:9"` |
| `n` | integer | 生成图片数量（1–9），部分模型（如 `qwen-image-max`）固定为 1 张 | `2` |
| `prompt` / `input.messages[].content[].text` | string | 主提示词，支持中英文及复杂描述。`qwen-image-3.0-pro` 等新模型推荐使用 `messages` 结构 | `"一间有着精致窗户的花店..."` |
| `input.messages[].content[].image` | string | [多模态输入](../concepts/multi-modal-input.md)，用于图生图或编辑任务，最多支持 14 张参考图（Vidu） | `{"image": "https://xxx.png"}` |
| `watermark` | boolean | 是否添加水印，默认 `true`，部分模型（如 `wan2.7-image-pro`）可设为 `false` | `false` |

## 使用方式

所有图像 API 均采用 **HTTP 调用**，核心流程如下：

1. **准备环境**：获取对应地域的 [API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，配置至环境变量 `$DASHSCOPE_API_KEY`；确认业务空间 ID（Workspace ID），并优先使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），详见 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。
2. **选择调用模式**：
   - **同步直出**（推荐）：适用于 `wan2.6` 及以上、`qwen-image-3.0-pro`、`z-image-turbo` 等模型，单次 POST 请求直接返回图片 URL（含 `Content-Type: image/png`）。示例 endpoint：`POST /api/v1/services/aigc/multimodal-generation/generation`。
   - **异步轮询**（兼容性广）：适用于 `wanx-v1`、`wan2.5-i2i-preview`、`kling`、`vidu` 等模型，需两步操作：<br>① 创建任务：`POST /api/v1/services/aigc/xxx/generation`，返回 `task_id`；<br>② 轮询结果：`GET /api/v1/tasks/{task_id}`，直至 `task_status == "SUCCEEDED"`，获取 `output.results[].url`（有效期 24 小时）。
3. **构造请求**：严格设置请求头 `Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`；异步调用必须包含 `X-DashScope-Async: enable`。

## 限制和注意事项

- **地域与密钥隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key 与请求地址**完全独立**，混用将导致鉴权失败。务必在控制台对应地域下获取 Key 并替换 URL 中的 `{WorkspaceId}`。
- **图片 URL 要求**：所有输入图片 URL 必须为**公网可访问 HTTPS 地址**，且无中文路径；OSS 等云存储需开启公共读权限。常见报错 `"Reference image download failed"` 即源于此 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **免费额度与计费**：多数模型提供 500 张/90 天免费额度（主账号与 RAM 子账号共享），额度用尽后按单价计费（如 `wanx-v1`: 0.16 元/张）。限时免费模型（如 `wanx-x-painting`）额度耗尽即停用，不支持续费。
- **输入限制**：图像尺寸需符合模型要求（如 `image-instance-segmentation` 要求 512×512 至 4096×4096 像素）；文本 [prompt](../guides/prompt.md) 长度建议 ≤ 512 token；多图输入时注意各模型支持的最大张数（Vidu 支持 14 张，OutfitAnyone 基础版限 2 张）。
- **错误处理**：HTTP 状态码非 200 时检查 `code` 字段（如 `BadRequest.InputDownloadFailed`），响应体中 `request_id` 是排查问题的关键凭证。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)


