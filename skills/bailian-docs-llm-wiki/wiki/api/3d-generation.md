# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果，适用于华北2（北京）地域。该能力依赖 Tripo 官方模型服务，输出格式为 GLB（含 PBR 材质或基础网格），并附带预览渲染图。

## 支持的模型/功能

- **模型标识**：当前仅支持 `Tripo/Tripo-P1.0`（专业版，最高 2 万面，速度快）和 `Tripo/Tripo-H3.1`（高精度版，最高 200 万面）。二者在几何精度与输出质量上存在显著差异，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
- **生成模式**：
  - 文生3D：通过 `prompt` 字段传入文本描述；
  - 单图生3D：通过 `image` 字段传入单张公网可访问图像 URL；
  - 多图生3D：通过 `images` 数组传入 4 张按「前、左、后、右」顺序排列的图像对象（允许部分为空对象 `{}`）；
- **输出类型**：
  - 默认返回带 PBR 材质的 GLB 模型（`pbr_model_url`）及渲染图（`rendered_image_url`）；
  - 可显式禁用贴图与 PBR，获得无材质基础模型（`base_model_url`），需同时设置 `"texture": false, "pbr": false`。

> **注意**：原始文档中 `images` 数组长度被明确限定为 4，且顺序固定；但示例中“传入2张图”使用了 `[img1, {}, img3, {}]` 形式，实际有效图像数为 2。此设计与常见多视角建模逻辑一致，但开发者需严格按位置填充，不可省略或错序——该约束在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中有强制说明。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `model` | string | 是 | 固定为 `Tripo/Tripo-P1.0` 或 `Tripo/Tripo-H3.1` |
| `input.prompt` | string | 文生3D时必填 | 最长 1024 字符，支持中英文；[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求三者（`prompt`/`image`/`images`）互斥 |
| `input.image` | string | 单图生3D时必填 | 公网 HTTP/HTTPS URL，JPEG/PNG 格式，20–6000px 分辨率，≤20MB |
| `input.images` | array[object] | 多图生3D时必填 | 长度恒为 4，每项含 `type`（`jpeg`/`png`）和 `file_token`（URL）；空视角必须用 `{}` 占位 |
| `parameters.texture_quality` | string | 否 | `standard`（默认）或 `detailed`；仅对 `pbr=true` 有效 |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（≤150 万面）或 `ultra`（≤200 万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `false` 时将强制 `texture=false`，需配合 `texture=false` 才能获得 `base_model_url` |

## 使用方式

1. **前置准备**：
   - 在华北2（北京）地域开通 Tripo 服务：前往 [百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索并开通 “Tripo”；
   - 获取并配置 API Key（必须为北京地域）：参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的配置指引。

2. **创建任务（POST）**：
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - 必须携带请求头：`Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`
   - 请求体按模式选择 `input` 字段，`model` 和 `parameters` 按需设置。

3. **轮询查询结果（GET）**：
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 仅需 `Authorization` 请求头；
   - 建议轮询间隔 ≥15 秒，`task_id` 有效期为 24 小时；
   - 成功响应中 `output.results` 包含 `pbr_model_url`（或 `base_model_url`）、`rendered_image_url`，链接有效期 2 小时，需及时下载。

## 限制和注意事项

- **地域强绑定**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须在此地域生成；
- **异步强制性**：`X-DashScope-Async: enable` 为必填请求头，缺失将报错 “current user api does not support synchronous calls”；
- **输入互斥**：`prompt`、`image`、`images` 三者不可共存，否则返回 `InvalidParameter` 错误；
- **多图格式刚性**：`images` 数组长度必须为 4，顺序不可调整，空视角必须用 `{}` 占位（非 `null` 或省略）；
- **资源时效性**：
  - `task_id` 查询有效期：24 小时；
  - 模型/渲染图下载 URL 有效期：2 小时；
- **配额与限频**：任务提交无明确 RPS 限制，但查询接口默认 RPS 为 20；高频轮询建议改用 [异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


