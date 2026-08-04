# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图（T2I）、图生图（I2I）、局部重绘、风格迁移、背景生成、人物写真、创意文字等数十种细分场景。所有服务均通过统一的 HTTP API 或 DashScope SDK 调用，支持同步与异步两种模式，并按实际成功生成图片计费。开发者需根据地域选择对应 API Key 与业务空间专属域名以确保稳定调用。

## 支持的模型/功能

平台当前提供三大类图像能力模型：

- **通用文生图与编辑模型**：包括 `qwen-image-3.0-pro`（支持 T2I/I2I 双模态）、`wan2.7-image-pro`（4K 文生图）、`z-image-turbo`（轻量快速生图）等。其中千问系列模型强调复杂文本渲染与语义遵循，万相系列侧重艺术风格多样性与电商适配性 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
  
- **垂直场景专用模型**：覆盖特定需求，如 `wanx-sketch-to-image-lite`（涂鸦作画）、`wanx-style-repaint-v1`（人像风格重绘）、`image-out-painting`（图像画面扩展）、`vidu/vidu-image_reference2image`（高精度 UI/图表渲染）等。部分模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`image-erase-completion`）当前仅限免费体验，额度用尽后不可调用 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

- **创意工具与辅助模型**：如 `FaceChain`（基于 2 张图训练专属人像）、`WordArt锦书`（汉字创意变形与纹理生成）、`OutfitAnyone`（AI 试衣流水线，含基础版 `aitryon` 与精修版 `aitryon-refiner`）等，适用于内容创作与电商增强场景 [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)。

> **注意**：文档中提及的 `wanx-v1`（V1 版）已明确标注“推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”；而 `wan2.6-t2i` 等 V2 模型在分辨率支持（如 `768*2700`）、同步调用能力等方面显著优于 V1，实际开发应优先选用 V2 及以上版本。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | string | 必填，指定调用模型名，需与地域支持列表一致 | `"qwen-image-3.0-pro"`, `"wan2.7-image-pro"` |
| `size` / `resolution` / `aspect_ratio` | string | 控制输出分辨率或宽高比。不同模型约束不同：<br>- `qwen-image-3.0-pro`：总像素需在 `512*512` 至 `2048*2048` 之间<br>- `wan2.6-t2i`：宽高比范围 `[1:4, 4:1]`，总像素 `[1280*1280, 1440*1440]`<br>- `kling/kling-v3-*`：支持 `"1k"`/`"2k"`/`"4k"` 及 `"16:9"`/`"1:1"` 等 | `"1024*1024"`, `"2K"`, `"1:1"` |
| `n` | integer | 生成图片张数（若模型支持多图输出） | `1`（默认）, `2`, `6` |
| `prompt` / `messages.content.text` | string | 主提示词，描述目标图像内容。千问/万相新模型统一采用 `messages` 结构 | `"一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"` |
| `negative_prompt` | string | （部分模型支持）反向提示词，用于排除不期望元素 | `"不要使用红色元素"` |
| `watermark` | boolean | 是否添加平台水印 | `false`（推荐生产环境关闭） |
| `X-DashScope-Async` | header | 异步调用必填请求头，值必须为 `"enable"` | `"enable"` |

> **注意**：`size` 参数在不同模型间含义不一致——`wan2.5-i2i-preview` 中为 `"宽*高"` 像素值，`kling` 模型中为 `"1k"` 字符串标识，`z-image-turbo` 则要求总像素在 `[512*512, 2048*2048]` 区间。务必查阅对应模型文档确认格式。

## 使用方式

### 1. 基础准备
- 获取并配置 API Key：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
- 确认地域与 Workspace ID：华北2（北京）、新加坡、美国（弗吉尼亚）地域拥有独立 API Key 与域名，**不可混用**；强烈建议迁移到业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

### 2. 调用模式选择
- **同步调用**：适用于 `wan2.6`、`qwen-image-3.0`、`z-image-turbo` 等支持模型，一次请求返回结果，URL 为 `/api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**：适用于耗时较长任务（如局部重绘、虚拟模特、背景生成），流程为：
  1. `POST /api/v1/services/.../generation` 创建任务，获取 `task_id`；
  2. 定期 `GET /api/v1/tasks/{task_id}` 查询状态，直至 `task_status == "SUCCEEDED"`，返回图片 URL（有效期 24 小时）。

### 3. 示例（同步文生图）
```bash
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{
    "model": "qwen-image-3.0-pro",
    "input": {
      "messages": [{"role":"user","content":[{"text":"一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"}]}]
    },
    "parameters": {"size": "1024*1024", "n": 1}
  }'
```

## 限制和注意事项

- **地域与域名绑定**：所有模型均严格绑定地域。例如 `qwen-mt-image` 仅支持华北2（北京）；`kling` 和 `Vidu` 模型也仅限北京地域；跨地域调用将导致鉴权失败或服务报错。
- **图片 URL 要求**：输入图片 URL 必须公网可访问、无中文路径、支持 HTTP/HTTPS 协议。若下载失败，错误码为 `BadRequest.InputDownloadFailed`，需检查链接有效性或上传至 OSS 等云存储 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **免费额度与计费**：多数模型提供 500 张免费额度（90 天有效），额度用尽后按单价计费（如 `wanx2.1-t2i-plus` 为 0.16 元/张）。**仅对模型成功生成的输出图片收费**，失败或输入图片不计入费用。
- **限流策略**：主账号与 RAM 子账号共享限流，典型为 QPS ≤ 2、并发任务数 ≤ 1。高并发场景需申请配额提升。
- **输入格式限制**：图像文件大小通常 ≤ 10MB，格式支持 JPG/PNG/WEBP/BMP；分辨率下限 512×512，上限依模型而定（如 `image-instance-segmentation` 最高支持 4096×4096）。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)


