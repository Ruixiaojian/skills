# image generation

百炼平台提供多种图像生成与编辑模型，覆盖文生图、图像编辑、风格迁移、背景生成等场景。主要模型系列包括千问-文生图（Qwen-Image）、万相（Wan/Wanx）、Z-Image 和可灵（Kling），各模型在分辨率、响应速度、功能侧重上有所差异，开发者可根据需求选择合适的模型。

## 支持的模型与功能

### 文生图模型

| 模型系列 | 推荐模型 | 特点 | 最大分辨率 |
|---------|---------|------|-----------|
| 千问-文生图 | qwen-image-2.0-pro | 复杂文本渲染、真实质感、语义遵循 | 2048×2048 |
| 万相2.7 | wan2.7-image-pro | 文生图支持4K输出，支持组图和编辑 | 4K |
| 万相文生图V2 | wan2.6-t2i | 多种艺术风格与写实摄影 | 1440×1440 |
| Z-Image | z-image-turbo | 轻量快速，支持中英文字渲染 | 2048×2048 |
| 可灵 | kling/kling-v3-omni-image-generation | 文生图、参考图生图、组图生成 | 4K |

详见 [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api.md) 和 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/text-to-image-v2-api-reference.md)。

### 图像编辑模型

| 模型 | 功能 |
|------|------|
| qwen-image-2.0-pro | 多图输入/输出、文字修改、物体增删、风格迁移 |
| wan2.7-image-pro | 图像编辑、交互式编辑、组图生成 |
| wan2.6-image | 图像编辑、图文混排输出 |
| wan2.5-i2i-preview | 单图编辑、多图融合 |
| wanx2.1-imageedit | 风格化、局部重绘、扩图、超分、上色等 |

### 专用模型

- **图像翻译**：qwen-mt-image（保留排版的多语种翻译）
- **人像风格重绘**：wanx-style-repaint-v1
- **涂鸦作画**：wanx-sketch-to-image-lite
- **背景生成**：wanx-background-generation-v2
- **AI试衣**：aitryon / aitryon-plus
- **创意文字**：WordArt 锦书
- **虚拟模特**：virtualmodel-v2

> **注意**：wanx-x-painting（图像局部重绘）、wanx-virtualmodel、shoemodel-v1、wanx-poster-generation-v1 等模型当前仅提供免费体验，免费额度用尽后不可调用且不支持付费。推荐使用千问图像编辑或万相2.1作为替代方案。

## 调用方式

### 同步调用

较新的模型（qwen-image-2.0 系列、wan2.6-t2i、wan2.7-image、z-image-turbo）支持同步接口，一次请求直接返回结果：

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "qwen-image-2.0-pro",
    "input": {
        "messages": [{"role": "user", "content": [{"text": "提示词"}]}]
    },
    "parameters": {"size": "1024*1024", "n": 1}
}'
```

### 异步调用

旧版模型及耗时较长的任务（万相V1、图像编辑、背景生成等）采用异步模式，分两步完成：

1. **创建任务**：发送请求，Headers 中必须包含 `X-DashScope-Async: enable`，返回 `task_id`
2. **轮询结果**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

> **注意**：缺少 `X-DashScope-Async: enable` 请求头将报错 "current user api does not [support](../guides/support.md) synchronous calls"。task_id 有效期为 24 小时，请勿重复创建任务。

### 地域与请求地址

| 地域 | 请求地址 |
|------|---------|
| 北京 | `https://dashscope.aliyuncs.com/api/v1/services/aigc/...` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/...` |
| 弗吉尼亚 | `https://dashscope-us.aliyuncs.com/api/v1/services/aigc/...` |

> **注意**：各地域 API Key 与请求地址独立，不可混用，跨地域调用将导致鉴权失败。不同文档中对弗吉尼亚地域的支持范围说明不一致——wan2.6-t2i 支持弗吉尼亚，但部分万相2.6 image 编辑功能在该地域仅支持异步调用。请以控制台模型列表为准。

## 关键参数

| 参数 | 说明 | 适用模型 |
|------|------|---------|
| `size` | 输出图像尺寸，格式为 `宽*高`（像素）或预设值如 `1K`/`2K`/`4K` | 大部分模型 |
| `n` | 生成图像张数 | 大部分模型 |
| `prompt_extend` | 智能思考/提示词优化，开启后返回优化后的提示词 | qwen-image、wan2.6-t2i、z-image-turbo |
| `negative_prompt` | 反向提示词，描述不希望出现的元素 | 万相V1/V2 |
| `watermark` | 是否添加水印 | wan2.6/2.7 |
| `thinking_mode` | 开启思考模式 | wan2.7-image |
| `style` | 图像风格选择 | wanx-v1 |
| `seed` | 随机种子，用于复现结果 | 部分模型 |

分辨率约束因模型而异，详见 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-generation-and-editing-api-reference.md)。

## 输入图像要求

- **格式**：通常支持 JPG、JPEG、PNG、BMP、WEBP
- **传入方式**：公网可访问的 HTTP/HTTPS URL（URL 中不能包含中文字符），部分模型支持 Base64
- **尺寸限制**：因模型不同有差异，一般要求分辨率不低于 512×512，不超过 4096×4096
- **大小限制**：通常不超过 10MB
- **本地文件**：可通过百炼平台"上传文件获取临时URL"接口获取公网地址

## 前提条件

1. [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
2. [配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
3. 如使用 SDK，需 [安装 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)（支持 Python 和 Java）

## 限制和注意事项

- **图像 URL 有效期**：异步任务成功后返回的图像 URL 有效期为 24 小时，需及时下载保存。
- **限流**：主账号与 RAM 子账号共享限流配额，典型限制为 QPS 2、并发任务数 1-5（具体因模型而异）。
- **免费额度**：开通百炼服务后自动发放 500 张，有效期 90 天，主账号与 RAM 子账号共享。
- **计费**：仅对模型成功生成的输出图片计费，输入图片和失败任务不计费。
- **万相V1版**（wanx-v1）为旧版模型，推荐迁移至万相V2或千问-文生图系列。
- **图像翻译**（qwen-mt-image）仅支持北京地域，且不支持两个非中英语种之间的直接翻译。
- **图文混排输出**（wan2.6-image 的 `enable_interleave=true`）仅支持[流式输出](../concepts/streaming.md)，需同时设置 `X-DashScope-Sse: enable` 和 `parameters.stream: true`。

## 来源文档

- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-edit-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-mt-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wanx-image-edit-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/portrait-style-redraw-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/vary-region-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/wanx-background-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/outfitanyone.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/wordart-quick-start.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-generation-api-reference.md)

