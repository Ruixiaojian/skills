# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图、图生图、局部重绘、风格迁移、背景生成、AI试衣等20余种专业场景模型。所有服务均基于统一的API协议，支持HTTP异步/同步调用及DashScope SDK集成，适用于电商、设计、内容创作等开发者场景。

## 支持的模型/功能

平台当前提供三类核心能力：**通用图像生成**（如文生图）、**图像编辑与增强**（如局部重绘、扩图）、**垂直领域工具**（如虚拟模特、AI试衣）。主要模型包括：

- **万相系列**：`wan2.6-t2i`（推荐V2文生图）、`wan2.5-i2i-preview`（通用图像编辑）、`wanx-style-repaint-v1`（人像风格重绘）、`wanx-background-generation-v2`（背景生成）[原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)  
- **千问系列**：`qwen-image-3.0-pro`（T2I+I2I一体化）、`qwen-image-edit-max`（高精度图像编辑）、`qwen-mt-image`（图像翻译）[原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)  
- **轻量与专用模型**：`z-image-turbo`（快速文生图）、`kling/kling-v3-omni-image-generation`（分镜组图）、`shoemodel-v1`（鞋靴试穿）、`facechain`（人物写真训练与生成）  
- **免费体验模型**：`wanx-x-painting`（图像局部重绘）、`wanx-virtualmodel`（虚拟模特）、`image-erase-completion`（擦除补全）等均处于免费体验阶段，额度用尽后不可调用且不支持付费 [原文标题](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)

> **注意**：文档中多次提及 `wanx-v1`（V1文生图）已明确标注“推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”；同时 `wan2.6-t2i` 明确支持HTTP同步调用，而 `wan2.5` 及以下版本仅支持异步调用——这与部分旧文档未明确区分调用方式存在潜在矛盾，开发者应以[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)为准。

## 关键参数

不同模型共性参数如下，具体支持情况需查阅对应模型文档：

- `model`：必填，指定模型名称（如 `"wan2.6-t2i"`、`"qwen-image-3.0-pro"`）
- `input.prompt` 或 `input.messages`：文本提示词，V2及以后模型普遍采用 `messages` 数组格式（含 `text` 和可选 `image` 元素）
- `parameters.size`：输出分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）或语义值（如 `"1K"`），各模型约束不同：
  - `wan2.6-t2i`：总像素在 `[1280*1280, 1440*1440]`，宽高比 `[1:4, 4:1]`
  - `qwen-image-3.0-pro`：总像素 `[512*512, 2048*2048]`
  - `kling` 系列：仅支持 `"1k"`/`"2k"`/`"4k"` 等预设值
- `parameters.n`：生成张数，范围通常为 `1–9`，部分模型（如 `qwen-image-max`）固定为 `1`
- `parameters.aspect_ratio`（Kling）或 `parameters.resolution`（Vidu）：控制宽高比与分辨率组合
- `X-DashScope-Async: enable`：**所有HTTP异步调用必需**，缺失将报错 `"current user api does not support synchronous calls"`  
- `X-DashScope-Sse: enable` + `parameters.stream: true`：图文混排（`enable_interleave=true`）时必需的流式配置

## 使用方式

### 调用前提
- 获取并配置 API Key（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)），注意**华北2（北京）、新加坡、美国（弗吉尼亚）地域的API Key与请求地址独立，不可混用**  
- 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代旧域名（`dashscope.aliyuncs.com`），以获得更高性能与稳定性  

### 调用模式
- **同步调用**：适用于 `wan2.6-t2i`、`z-image-turbo`、`qwen-image-2.0-pro` 等支持模型，单次请求直接返回结果（含图片URL），响应更快  
- **异步调用**：适用于绝大多数图像模型（如 `wanx-v1`、`wan2.5-i2i-preview`、`image-out-painting`），流程为：  
  1. `POST /api/v1/services/.../generation` 创建任务，获取 `task_id`  
  2. 轮询 `GET /api/v1/tasks/{task_id}` 查询状态，`task_status == "SUCCEEDED"` 时返回图片URL（有效期24小时）  

### 示例命令
```bash
# 同步调用 wan2.6-t2i（北京地域）
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan2.6-t2i",
    "input": {"messages": [{"role":"user","content":[{"text":"一间花店"}]}]},
    "parameters": {"size": "1024*1024"}
  }'

# 异步调用 wan2.5-i2i-preview（单图编辑）
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis \
  -H "X-DashScope-Async: enable" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan2.5-i2i-preview",
    "input": {
      "prompt": "将连衣裙换成复古蕾丝长裙",
      "images": ["https://example.com/input.jpg"]
    }
  }'
```

## 限制和注意事项

- **地域与域名绑定**：所有模型均严格按地域隔离，跨地域调用将导致鉴权失败；务必使用对应地域的 Workspace ID 构造请求 URL  
- **图片URL要求**：输入图片必须为**公网可访问的HTTPS/HTTP链接**，OSS等云存储需开启公共读权限；URL中禁止含中文字符  
- **免费额度**：多数模型提供500张免费额度（如 `wanx-v1`、`wanx-style-repaint-v1`），仅对**成功生成的输出图片**计数，失败/输入图片不计入；额度90天有效，主账号与RAM子账号共享  
- **限流策略**：主账号与RAM子账号共用QPS/RPS限制（常见为2 QPS），同时处理中任务数上限通常为1（少数如 `image-out-painting` 为5）  
- **错误处理**：  
  - `BadRequest.InputDownloadFailed`：检查图片URL是否可公网访问、是否被防盗链拦截  
  - `InvalidApiKey`：确认API Key正确且地域匹配  
  - `current user api does not support synchronous calls`：异步模型未设置 `X-DashScope-Async: enable` 头  
- **模型弃用风险**：`wanx-v1`、`wanx-x-painting` 等模型已明确标注“推荐使用V2版”或“免费体验”，长期项目应避免依赖

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)


