# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图、图生图、局部重绘、风格迁移、背景生成、AI试衣等20余种专业模型。所有服务均通过统一的HTTP API或DashScope SDK调用，支持异步与同步两种模式，适用于电商、设计、内容创作等多类场景。

## 支持的模型/功能

百炼平台当前提供三大类图像能力：**基础生成类**（如文生图）、**编辑增强类**（如局部重绘、扩图、擦除补全）、**垂直场景类**（如虚拟模特、鞋靴试穿、创意海报）。核心模型包括：

- **万相系列**：`wan2.7-image-pro`（4K文生图）、`wan2.6-t2i`（推荐V2版文生图）、`wanx-sketch-to-image-lite`（涂鸦作画）、`wanx-style-repaint-v1`（人像风格重绘）[原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)  
- **千问系列**：`qwen-image-3.0-pro`（T2I/I2I一体化）、`qwen-image-2.0-pro`（强文本渲染）、`qwen-mt-image`（图像翻译）[原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)  
- **轻量与专用模型**：`z-image-turbo`（快速生图）、`kling/kling-v3-omni-image-generation`（分镜组图）、`vidu/vidu-image_reference2image`（UI/图表精准还原）、`facechain`（人物写真训练与生成）  
- **免费体验模型**：`wanx-x-painting`（图像局部重绘）、`wanx-virtualmodel`（虚拟模特）、`image-erase-completion`（图像擦除补全）等均标注为“仅免费体验”，额度用尽后不可调用且不支持付费 [原文标题](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)

> **注意**：文档中多次出现“推荐使用V2版”与“V1版已过时”的表述（如[万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)），但部分V1模型（如`wanx-v1`）仍在计费列表中。实际开发中应优先选用V2及更高版本（如`wan2.6-t2i`、`wan2.7-image-pro`），V1模型已不建议新项目接入。

## 关键参数

不同模型共用部分通用参数，但关键行为由模型类型决定：

- **`model`**：必填字符串，指定具体模型名（如`wan2.7-image-pro`、`qwen-image-3.0-pro`），各地域支持模型不同，需查阅[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)确认。
- **`size` / `resolution` / `aspect_ratio`**：分辨率控制参数，语义因模型而异：
  - `wan2.7-image-pro` 支持 `"2K"`、`"4K"` 等字符串值；
  - `qwen-image-*` 系列要求总像素在 `512*512` 至 `2048*2048` 之间；
  - `kling` 系列使用 `resolution: "1k"` + `aspect_ratio: "16:9"` 组合；
  - `vidu` 系列支持 `"1K"`、`"2K"`、`"4K"`。
- **`n`**：生成图片张数，多数模型支持 `1–9`，`qwen-image-*` 支持 `1–6` 张。
- **`prompt` / `input.messages`**：提示词输入方式分化明显：
  - V1/V2文生图模型（如`wanx-v1`, `wan2.6-t2i`）使用 `input.prompt` 字符串；
  - 多模态统一接口（如`wan2.7-image-pro`, `qwen-image-3.0-pro`, `z-image-turbo`）使用 `input.messages` 数组，其中 `content` 为文本或图像对象混合列表。
- **`watermark`**：布尔值，控制是否添加水印（默认 `true`），`wan2.7-image-pro`、`vidu` 等模型明确支持设为 `false`。
- **异步必需头**：所有异步调用必须包含 `X-DashScope-Async: enable`，缺失将报错 `current user api does not support synchronous calls` [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)。

## 使用方式

### 基础流程
1. **开通与鉴权**：在百炼控制台开通对应模型服务，获取地域专属API Key并配置至环境变量 `$DASHSCOPE_API_KEY`。
2. **选择域名**：强烈推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于公共域名 `https://dashscope.aliyuncs.com`。
3. **构造请求**：根据模型文档选择同步或异步调用路径：
   - **同步调用**（推荐多数场景）：仅限 `wan2.6` 及以上、`wan2.7`、`qwen-image-3.0-pro`、`z-image-turbo` 等模型，单次请求直接返回结果（含图像URL）。
   - **异步调用**（传统模式）：适用于 `wanx-v1`、`wanx-sketch-to-image-lite`、`wanx-x-painting` 等，需两步：① `POST /generation` 创建任务获 `task_id`；② 轮询 `/tasks/{task_id}` 查询状态，成功后返回图像URL（有效期24小时）。

### 示例：同步文生图（wan2.7-image-pro）
```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan2.7-image-pro",
    "input": {
      "messages": [{"role":"user","content":[{"text":"一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"}]}]
    },
    "parameters": {"size": "2K", "n": 1, "watermark": false}
  }'
```

### 示例：异步局部重绘（wanx-x-painting）
```bash
# 步骤1：创建任务
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis \
  -H "X-DashScope-Async: enable" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wanx-x-painting",
    "input": {
      "prompt": "一只狗戴着红色眼镜",
      "base_image_url": "https://example.com/base.jpg",
      "mask_image_url": "https://example.com/mask.png"
    }
  }'
```

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域拥有独立API Key与请求地址，**不可混用**，跨地域调用将导致鉴权失败 [原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **URL要求**：所有输入图片URL必须为公网可访问、支持HTTP/HTTPS协议的地址，且URL中**不能含中文字符**；推荐上传至OSS获取临时公网URL。
- **免费额度**：所有模型均提供500张免费额度（有效期90天），仅对**成功生成的输出图片**计费，失败或输入图片不计入额度。
- **限流规则**：主账号与RAM子账号共享限流，典型限制为“任务下发接口QPS=2，同时处理中任务数=1”，高并发场景需自行实现队列控制。
- **图像格式与尺寸**：
  - 输出格式：绝大多数模型为 `PNG`，仅 `qwen-mt-image` 输出 `JPG`；
  - 输入尺寸：`image-instance-segmentation` 要求图像分辨率 `512×512` 至 `4096×4096`，单边长度 `[512, 4096]`，大小 ≤10MB；
  - 图片链接：若遇 `BadRequest.InputDownloadFailed` 错误，请检查URL可访问性及下载权限 [原文标题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **模型弃用提示**：`wanx-v1` 文档明确标注“推荐使用全面升级的文生图V2版模型”，`wanx-x-painting`、`wanx-virtualmodel` 等免费模型已声明“额度用尽后不可调用且不支持付费”，生产环境应规避依赖。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)


