# image generation

百炼平台的图像生成能力覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、背景生成、扩图、文字渲染与翻译等全链路场景，支持多模型并行调用与灵活参数配置。所有服务均基于统一的[异步任务](../concepts/asynchronous-task.md)模型（部分新模型支持同步调用），需通过业务空间专属域名接入以获得最佳性能。

## 支持的模型/功能

百炼提供两类核心图像能力：**通用生成模型**（如 `qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo`）和**垂直场景模型**（如虚拟模特、鞋靴试穿、创意海报、FaceChain人像训练等）。通用模型普遍支持文生图与图生图，其中：
- `qwen-image-3.0-pro` 和 `qwen-image-2.0-pro` 系列在文本渲染、语义遵循与真实质感上表现突出，详见 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；
- `wan2.7-image-pro` 支持文生图场景下的4K高清输出，而图像编辑与组图生成最高支持2K分辨率；
- `z-image-turbo` 为轻量级模型，适合对响应速度敏感的低延迟场景；
- 垂直模型如 `wanx-virtualmodel`、`shoemodel-v1`、`wanx-poster-generation-v1` 等均聚焦特定任务，但多数当前仅限免费体验，额度用尽后不可调用（参见 [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)）。

> **注意**：文档中 `wanx-v1`（V1版）与 `wan2.6-t2i`（V2版）存在能力代际差异：V1版仅支持华北2（北京）地域且不支持HTTP同步调用；V2版已扩展至新加坡、弗吉尼亚等地域，并新增同步调用协议。开发者应优先选用V2及以上版本。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | string | 必选。模型标识符，需与所选地域支持的模型列表一致 | `"qwen-image-3.0-pro"`, `"wan2.6-t2i"` |
| `size` | string | 可选。输出分辨率，格式为 `"宽*高"` 或预设值（如 `"1K"`、`"2K"`、`"4K"`）。不同模型约束不同：<br>- `qwen-image-*`：总像素需在 `512×512` 至 `2048×2048` 之间；<br>- `wan2.6-t2i`：宽高比范围 `[1:4, 4:1]`，总像素 `[1280×1280, 1440×1440]`；<br>- `vidu/*`：仅支持 `"1K"`、`"2K"`、`"4K"` 预设 | `"1024*1024"`, `"2K"` |
| `n` | integer | 可选。生成图片张数（部分模型固定为1）。`qwen-image-*` 支持 `1–6` 张；`kling/*` 支持 `1–9` 张；`wan2.7-image-pro` 在文生图模式下支持 `1–6` 张 | `1`, `4` |
| `prompt_extend` | boolean | 可选。启用“智能思考”能力，返回优化后的提示词及推理过程（增加响应时间）。适用于 `z-image-turbo`、`wan2.7-image-pro` 等模型 | `true` |
| `watermark` | boolean | 可选。是否添加水印，默认 `true`。部分模型（如 `wan2.7-image-pro`）建议设为 `false` 以获取纯净输出 | `false` |
| `aspect_ratio` | string | 可选。宽高比，仅 `kling/*` 模型明确支持 `"16:9"`、`"9:16"`、`"1:1"` | `"1:1"` |

## 使用方式

所有图像API均采用标准HTTP调用，**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`。调用前需完成三步准备：
1. 在百炼控制台开通对应模型服务；
2. 获取并配置该地域的API Key（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）；
3. 获取业务空间ID（Workspace ID），用于构造Endpoint URL。

**调用模式分两类**：
- **同步调用**（推荐）：适用于 `wan2.6-t2i`、`qwen-image-3.0-pro`、`wan2.7-image-pro` 等新模型，一次请求即返回结果。示例见 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)；
- **异步调用**（兼容旧模型）：适用于 `wanx-v1`、`wanx-x-painting`、`image-out-painting` 等，需两步操作：① 创建任务获取 `task_id`；② 轮询 `task_id` 查询结果。所有异步接口**必须携带 `X-DashScope-Async: enable` 请求头**，否则报错。

> **注意**：文档 1 中的 `curl` 示例使用旧域名 `dashscope.aliyuncs.com`，而文档 2、3、4、6 等均明确要求迁移至业务空间专属域名。若混用旧域名与新模型（如 `qwen-image-3.0-pro`），将导致鉴权失败或服务不可用。

## 限制和注意事项

- **地域与密钥绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的API Key与Endpoint严格隔离，跨地域调用必然失败。例如，新加坡地域的Key不可用于北京Endpoint。
- **图片URL要求**：所有输入图片URL必须为公网可访问地址（HTTP/HTTPS），且不含中文字符；OSS等云存储链接需确保Bucket权限开放。若下载失败，错误码为 `BadRequest.InputDownloadFailed`（参见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)）。
- **免费额度与计费**：多数模型提供500张免费额度（有效期90天），额度用尽后按单价计费（如 `wanx-style-repaint-v1` 为0.12元/张）。**注意**：免费额度仅统计成功生成的图片，失败、超时或无效请求不计入。
- **输入限制**：图像类任务（如擦除补全、实例分割）对输入图有严格要求：分辨率 `512×512` 至 `4096×4096`，单边长度 `[512, 4096]`，文件大小 ≤10MB；文本提示词长度建议 ≤512字符，避免冗余描述影响效果。
- **模型弃用提示**：`wanx-v1`、`wanx-sketch-to-image-lite`、`wanx-x-painting` 等模型已在文档中明确标注“推荐使用替代方案”，其功能已被 `qwen-image-edit` 或 `wan2.5-i2i-preview` 等新模型覆盖，新项目不应依赖。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)


