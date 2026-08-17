# image generation

百炼平台提供丰富的图像生成与编辑能力，覆盖文生图（T2I）、图生图（I2I）、局部编辑、背景生成、风格迁移等全链路场景。所有模型均通过统一的 HTTP API 或 DashScope SDK 调用，支持同步与异步两种模式，适用于从快速原型验证到高并发生产部署的各类开发者需求。

## 支持的模型/功能

平台当前提供多类图像模型，按能力可分为：

- **通用文生图**：`qwen-image-3.0-pro`（推荐）、`wan2.6-t2i`、`z-image-turbo`、`qwen-image-max`，支持中英文提示词、复杂文本渲染及多样化艺术风格 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **图像编辑与融合**：`wan2.7-image-pro`（支持4K文生图与2K编辑）、`qwen-image-2.0-pro`（文字渲染与语义遵循更强）、`wan2.5-i2i-preview`（单图编辑/多图融合） [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。
- **专业工具型模型**：  
  - 局部重绘：`wanx-x-painting`（免费体验，需涂抹掩码图）；  
  - 虚拟模特/鞋靴试穿：`virtualmodel-v2`、`shoemodel-v1`（均限北京地域，免费额度用尽后不可调用）；  
  - 图像擦除补全：`image-erase-completion`（免费体验，推荐替代方案见[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)） [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)；  
  - 创意海报、背景生成、人物实例分割等均属轻量级垂直工具模型，全部限定华北2（北京）地域调用。

> **注意**：部分模型存在地域与协议不一致问题。例如，`wanx-v1`（V1版）仅支持北京地域异步调用，而 `wan2.6-t2i` 及以上版本支持北京/新加坡/弗吉尼亚三地，并新增同步调用能力；`qwen-image-3.0-pro` 的 endpoint 与 `qwen-image-2.0-pro` 不同，前者使用 `/multimodal-generation/generation`，后者仍沿用 `/text2image/image-synthesis`，开发者需严格按文档选择对应 URL 和参数结构。

## 关键参数

核心参数在不同模型间存在共性与差异：

- **`model`**：必填字符串，如 `"qwen-image-3.0-pro"`、`"wan2.6-t2i"`，需与所选 endpoint 和地域匹配。
- **`size`**：控制输出分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）或预设值（如 `"1K"`、`"2K"`、`"4K"`）。`qwen-image-3.0-pro` 要求总像素在 `512*512` 至 `2048*2048` 之间；`wan2.6-t2i` 支持 `[1280*1280, 1440*1440]`；`z-image-turbo` 支持 `[512*512, 2048*2048]`。
- **`n`**：生成图片张数。`qwen-image-2.0-pro` 支持 `1–6` 张；`kling/kling-v3-image-generation` 支持 `1–9`；多数免费模型（如 `wanx-x-painting`）固定为 `1`。
- **`watermark`**：布尔值，控制是否添加水印，默认 `true`，可设为 `false` 去除。
- **`prompt_extend`**：`z-image-turbo` 等模型支持，开启后返回优化提示词及推理过程，但增加延迟。
- **异步必需头**：所有 HTTP 异步调用必须包含 `X-DashScope-Async: enable`，缺失将报错 `"current user api does not support synchronous calls"` [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)。

## 使用方式

### 调用前提
- 获取对应地域的 [API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，并配置至环境变量 `DASHSCOPE_API_KEY`；
- 获取业务空间 ID（Workspace ID），用于构造专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），**强烈推荐迁移至新域名以获得更高稳定性**；
- 所有模型均要求 API Key、endpoint、模型三者地域一致，跨地域调用必然失败。

### 同步 vs 异步
- **同步调用**（推荐多数场景）：适用于 `wan2.6-t2i`、`qwen-image-3.0-pro`、`z-image-turbo`、`wan2.7-image-pro` 等新版模型，一次请求直接返回结果，endpoint 为 `/multimodal-generation/generation`。
- **异步调用**（必需长耗时任务）：适用于 `wanx-v1`、`wanx-x-painting`、`image-out-painting`、`wanx-background-generation-v2` 等，流程为：  
  1. `POST /.../generation` 创建任务，获取 `task_id`；  
  2. 定期 `GET /.../result?task_id=xxx` 轮询，直至 `task_status == "SUCCEEDED"`，返回含 `url` 的结果（有效期 24 小时）。

### 请求示例（同步）
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

- **地域绑定**：除 `z-image-turbo`、`wan2.6-t2i` 等少数模型外，绝大多数图像模型（如 `wanx-v1`、`wanx-x-painting`、`shoemodel-v1`、`image-instance-segmentation`）**仅支持华北2（北京）地域**，且必须使用该地域 API Key 与专属域名。
- **免费额度与计费**：所有模型均提供 500 张免费额度（90 天有效期），用尽后部分模型（如 `wanx-v1`、`wan2.6-t2i`）转为付费（单价 0.02–0.18 元/张），而 `wanx-x-painting`、`shoemodel-v1` 等明确标注“免费体验，用尽后不可调用” [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **图片 URL 要求**：输入图片 URL 必须公网可访问、无中文路径、支持 HTTP/HTTPS；若下载失败，错误码为 `BadRequest.InputDownloadFailed`，需检查链接有效性或上传至 OSS [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **输入限制**：`image-erase-completion` 要求 `image_url` 与 `mask_url` 分辨率均在 `[512, 4096]` 像素且大小 ≤10MB；`shoemodel-v1` 要求模板图与鞋图长宽比在 `[2:3, 3:2]` 内；`kling` 模型 `aspect_ratio` 仅支持 `"16:9"`、`"9:16"`、`"1:1"`。
- **模型弃用风险**：`qwen-image-2.0` 系列已标注“当前能力与 `-2026-03-03` 版本相同”，建议优先选用 `qwen-image-3.0-pro` 或 `qwen-image-2.0-pro-2026-06-22` 等明确标注为 `推荐` 的最新子版本。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)


