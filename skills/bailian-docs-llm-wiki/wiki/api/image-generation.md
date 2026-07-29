# image generation

百炼平台提供丰富的图像生成与编辑能力，涵盖文生图（T2I）、图生图（I2I）、局部重绘、背景生成、风格迁移等全栈场景。所有模型均通过统一的 HTTP API 接口调用，支持同步与异步两种模式，并已全面接入业务空间专属域名以提升稳定性与性能。开发者需配置地域匹配的 API Key 并遵循各模型的输入约束。

## 支持的模型/功能

百炼平台当前提供三类核心图像能力：**通用文生图/图生图模型**（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo`）、**垂直领域专用模型**（如虚拟模特、鞋靴模特、AI试衣、FaceChain 人像写真）、**创意工具类模型**（如文字渲染 WordArt、海报生成、图像擦除补全）。其中，千问系列（Qwen）和万相系列（WanX）为主力通用模型，Vidu 和可灵（Kling）支持高精度参考生图与分镜组图；而 `wanx-x-painting`（图像局部重绘）、`wanx-virtualmodel`（虚拟模特）、`shoemodel-v1`（鞋靴模特）、`wanx-poster-generation-v1`（创意海报）等均明确标注为“免费体验”，额度用尽后不可调用且不支持付费 [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。此外，`qwen-mt-image`（图像翻译）仅限华北2（北京）地域使用，且必须使用该地域专属 API Key [原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

> **注意**：文档中对 `wan2.6-t2i` 的分辨率描述存在矛盾——[原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 声明其总像素在 `[1280*1280, 1440*1440]` 之间，而 `wan2.5-t2i-preview` 则明确支持 `768*2700` 等非正方形超长宽比；但 `wan2.7-image-pro` 在文生图场景支持 4K 输出，而图像编辑仅支持最高 2K [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。实际调用时应以具体模型文档的 `size` 参数说明为准。

## 关键参数

- **`model`**：必填字符串，指定模型名称（如 `"qwen-image-3.0-pro"`、`"wan2.7-image-pro"`），不同地域支持的模型列表不同，需查阅控制台或对应文档。
- **`input`**：必填对象，结构因任务类型而异：
  - 文生图：通常为 `{"messages": [{"role": "user", "content": [{"text": "..."}]}]}`；
  - 图生图/编辑：支持混合 `text` 与 `image` 元素，最多可传入 14 张参考图（Vidu）或 3 张（万相 2.6）；
  - 局部重绘/擦除：需提供 `base_image_url` 与 `mask_image_url`；
  - 虚拟模特：需 `base_image_url`、`mask_image_url` 及 `face_prompt`。
- **`parameters`**：可选对象，常用字段包括：
  - `size`：字符串，如 `"1024*1024"`、`"2K"`、`"4K"` 或 `"1:1"`（可灵）；部分模型（如 `qwen-image-3.0-pro`）默认自动推荐分辨率 [原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；
  - `n`：整数，生成图片张数（1–9，依模型而定）；
  - `aspect_ratio`（可灵）：`"16:9"` / `"9:16"` / `"1:1"`；
  - `watermark`：布尔值，控制是否添加水印（默认 `true`）；
  - `prompt_extend`：布尔值，启用智能提示词扩展（如 Z-Image）；
  - `thinking_mode`（万相 2.7）：启用推理过程返回。

## 使用方式

所有图像 API 均采用 **HTTP 调用**，推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代旧域名 `dashscope.aliyuncs.com`，以获得更高性能与稳定性。调用前需完成：
1. 在百炼控制台开通对应模型服务；
2. 获取并配置地域匹配的 API Key（华北2、新加坡、美国弗吉尼亚地域 Key 不互通）；
3. 将 `{WorkspaceId}` 替换为真实业务空间 ID。

**同步 vs 异步**：
- `multimodal-generation/generation`（如 Qwen 3.0、Z-Image、万相 2.7）支持**同步调用**，一次请求直接返回结果；
- `text2image/image-synthesis`、`image2image/image-synthesis`、`background-generation/generation` 等路径均为**异步调用**，需两步操作：① 创建任务获取 `task_id`；② 轮询 `task_id` 查询结果（有效期 24 小时）。异步接口**必须携带 `X-DashScope-Async: enable` 请求头**，否则报错 [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)。

## 限制和注意事项

- **地域与 Key 绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）地域拥有独立 API Key 与请求地址，跨地域调用将鉴权失败；
- **URL 访问性**：所有输入图片 URL 必须为公网可访问地址，OSS 或自建存储需确保外网可达，否则报错 `"Reference image download failed"` [原文标题](../../raw/model-api-reference/image-generation/image-faq.md)；
- **免费额度**：多数模型提供 500 张免费额度（90 天有效），仅成功生成的输出图片计费，失败或输入图片不计入；
- **图像格式与尺寸**：
  - 输入图：常见格式（JPG/PNG/WEBP），单边长度通常要求 `[512, 4096]` 像素，大小 ≤10 MB；
  - 输出图：主流为 PNG 格式，分辨率范围多为 `512*512` 至 `2048*2048`，4K 模型（如 `wan2.7-image-pro`、`vidu/vidu-image_reference2image`）需显式指定 `size`；
- **限流策略**：主账号与 RAM 子账号共享限流（如 QPS/RPS=2，同时处理任务数=1），超出将返回 `429 Too Many Requests`；
- **过期模型**：`wanx-v1`（文生图 V1）已明确推荐升级至 V2 版本 [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)，`wanx2.1-t2i-turbo` 等旧版模型虽仍可用，但功能与性能已被新模型覆盖。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)


