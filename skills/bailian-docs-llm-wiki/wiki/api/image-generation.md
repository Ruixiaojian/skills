# image generation

百炼平台提供丰富的图像生成与编辑能力，覆盖文生图（T2I）、图生图（I2I）、局部重绘、背景生成、风格迁移、AI试衣等15+类专业场景。所有模型均通过统一的HTTP API或DashScope SDK调用，支持异步任务模式与部分模型的同步直出，并已全面适配业务空间专属域名以提升稳定性与性能。

## 支持的模型/功能

百炼平台当前提供以下主流图像生成与编辑模型，按能力分类如下：

- **文生图（T2I）**：`wan2.6-t2i`（推荐）、`qwen-image-3.0-pro`、`z-image-turbo`、`kling/kling-v3-image-generation`、`vidu/vidu-image_reference2image`  
- **图生图/图像编辑（I2I）**：`qwen-image-3.0-pro`（支持1–3张参考图）、`wan2.7-image-pro`（支持4K文生图与2K编辑）、`wan2.5-i2i-preview`（单图编辑/多图融合）、`qwen-image-edit-max`（工业级几何推理与角色一致性）  
- **专用工具类**：  
  - 局部重绘：`wanx-x-painting`（免费体验，[原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)）  
  - 涂鸦作画：`wanx-sketch-to-image-lite`（支持手绘草图+文本引导）  
  - 图像擦除补全：`image-erase-completion`（免费体验，[原文标题](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)）  
  - 虚拟模特：`virtualmodel-v2`（支持2048短边、多长宽比及背景权重控制）  
  - 鞋靴模特：`shoemodel-v1`（免费体验，需多视角鞋图与模板图）  
  - 人物实例分割：`image-instance-segmentation`（免费体验，输出像素级mask）  
  - 创意海报生成：`wanx-poster-generation-v1`（免费体验，[原文标题](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)）  
  - 图像翻译：`qwen-mt-image`（仅北京地域，支持中/英↔日/韩/法/西互译）  

> **注意**：`wanx-v1`（V1版文生图）已明确标注为“推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”；同时，`wanx-x-painting`、`shoemodel-v1`、`wanx-poster-generation-v1` 等多个模型在各自文档中均声明“目前仅供免费体验，免费额度用完后不可调用且不支持付费”，与通用计费模型存在显著策略差异。

## 关键参数

| 参数名 | 类型 | 说明 | 示例值 | 文档依据 |
|--------|------|------|--------|----------|
| `model` | string | 必填，指定调用模型名称 | `"wan2.6-t2i"`、`"qwen-image-3.0-pro"` | 所有API文档均要求 |
| `size` | string | 输出分辨率，格式为`宽*高`或预设值（如`1K`/`2K`/`4K`） | `"1024*1024"`、`"2K"` | [万相V2 API](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)、[Vidu API](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md) |
| `n` | integer | 生成图片张数（部分模型固定为1） | `1`–`9`（`kling`支持最高9张） | [可灵API](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md) |
| `prompt` / `input.messages` | string / array | 提示词输入方式：V1/V2模型用`prompt`字段；Qwen/Kling/Vidu等新模型统一采用`messages`数组结构 | `{"text": "一间花店..."}` | [千问3.0 API](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)、[万相V2 API](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) |
| `X-DashScope-Async` | header | 异步调用必需头，值必须为`enable` | `"enable"` | 所有异步模型均强制要求，见[涂鸦作画API](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md) |
| `watermark` | boolean | 控制是否添加水印（部分模型默认开启） | `false` | [万相2.7 API](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md) |

> **注意**：`prompt_extend` 参数在 `z-image-turbo` 和 `wan2.7-image-pro` 中用于启用智能提示词优化，但其行为（返回推理过程）与 `qwen-image-3.0-pro` 的隐式扩展逻辑不同，开发者需按模型文档单独验证。

## 使用方式

### 1. 基础准备
- 获取并配置 API Key：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，[配置环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)  
- **强烈建议使用业务空间专属域名**（非旧版 `dashscope.aliyuncs.com`），华北2（北京）和新加坡地域均需替换为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，其中 `{WorkspaceId}` 在控制台业务空间详情页获取。该迁移已在[千问3.0 API](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)、[万相V2](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)等20+文档中被反复强调为“推荐”或“重要”。

### 2. 调用模式
- **同步调用**（推荐多数场景）：适用于 `wan2.6-t2i`、`z-image-turbo`、`wan2.7-image-pro` 等模型，一次请求直接返回结果（HTTP 200 + 图片URL）。  
- **异步调用**（必需）：适用于 `wanx-v1`、`wan2.5-i2i-preview`、`wanx-x-painting` 等耗时较长的模型，流程为：  
  1. `POST /api/v1/services/.../generation` 创建任务 → 获取 `task_id`  
  2. `GET /api/v1/tasks/{task_id}` 轮询状态 → 直至 `task_status == "SUCCEEDED"` 返回图片URL（有效期24小时）  

### 3. 输入格式示例（文生图）
```bash
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{
    "model": "wan2.6-t2i",
    "input": {
      "messages": [{"role": "user", "content": [{"text": "一间有着精致窗户的花店"}]}]
    },
    "parameters": {"size": "1024*1024", "n": 1}
  }'
```

## 限制和注意事项

- **地域与密钥绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key 与请求地址**严格隔离**，混用将导致鉴权失败。例如，`qwen-mt-image` 明确限定“仅在华北2（北京）地域可用”，而 `wan2.6-t2i` 在弗吉尼亚地域也支持（见[万相V2文档](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)）。
- **图片URL要求**：所有涉及 `image_url` 的接口（如图生图、局部重绘、背景生成）均要求 URL **公网可访问、无中文路径、支持HTTP/HTTPS**；若使用私有OSS，需生成临时公网URL（见[图像擦除补全API](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)）。
- **免费额度与限流**：  
  - 免费额度为“成功生成的输出图片数量”，失败/输入图不计入；  
  - 主账号与RAM子账号**共享额度与QPS/RPS限制**（如 `wanx-v1` 限流为2 QPS，`image-out-painting` 为2 QPS）；  
  - 多个模型（如 `wanx-x-painting`、`shoemodel-v1`）明确标注“免费额度用完后不可调用且不支持付费”，无替代付费通道。
- **错误处理**：常见报错 `BadRequest.InputDownloadFailed` 表明图片URL不可达，需检查链接有效性及CORS权限；`current user api does not support synchronous calls` 错误则表明遗漏了 `X-DashScope-Async: enable` 头（见[涂鸦作画API](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)）。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)


