# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果，适用于华北2（北京）地域。该能力依赖 Tripo 官方模型服务，输出格式为 GLB（含 PBR 材质或基础网格），并附带预览渲染图。

## 支持的模型/功能

- **模型标识**：当前仅支持 `Tripo/Tripo-P1.0`（专业版，最高 2 万面，速度快）和 `Tripo/Tripo-H3.1`（高精度版，最高 200 万面）。二者在几何精度与输出质量上存在显著差异，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
- **输入模式**：
  - 文生3D：通过 `prompt` 字段传入文本描述（最大 1024 字符，支持中英文）；
  - 单图生3D：通过 `image` 字段传入单张公网可访问的 JPEG/PNG 图像（分辨率 20–6000 像素，≤20MB）；
  - 多图生3D：通过 `images` 数组传入 4 张图像（顺序固定为前/左/后/右），允许部分位置填空对象 `{}`，实际有效图数为 2–4 张。
- **输出类型**：
  - 默认返回 `pbr_model_url`（含 PBR 材质的 GLB）和 `rendered_image_url`（预览图）；
  - 可通过设置 `"texture": false, "pbr": false` 获取无贴图的 `base_model_url`。

> **注意**：文档中 `images` 数组明确要求长度为 4，且顺序不可变；但示例中“传入2张图”使用了 `[img1, {}, img3, {}]` 形式，与“仅支持前/左/后/右四视角”的说明一致。请勿尝试非标准索引或长度 ≠ 4 的数组，否则将触发 `InvalidParameter` 错误 —— 此行为已在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中严格定义。

## 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `Tripo/Tripo-P1.0` 或 `Tripo/Tripo-H3.1` |
| `input.prompt` / `input.image` / `input.images` | string / string / array[object] | 条件必填 | 三者互斥，仅可选其一；`images` 必须为长度 4 的数组 |
| `parameters.texture_quality` | string | 否 | `standard`（默认）或 `detailed`；仅对含贴图任务生效 |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（≤150 万面）或 `ultra`（≤200 万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `false` 时需同步设 `texture: false` 才能获得 `base_model_url` |
| `parameters.texture` | boolean | 否 | 默认 `true`；与 `pbr` 联动控制贴图生成，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |

## 使用方式

1. **前置准备**：
   - 在华北2（北京）地域开通 Tripo 服务（[控制台链接](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)）；
   - 配置 `DASHSCOPE_API_KEY` 环境变量，并确保请求头包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `X-DashScope-Async: enable`。

2. **创建任务（POST）**：
   - 请求地址：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - 必须携带 `X-DashScope-Async: enable`，否则报错 `current user api does not support synchronous calls`。

3. **轮询结果（GET）**：
   - 地址：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - `task_id` 有效期为 24 小时，建议轮询间隔 ≥15 秒；
   - 成功响应中 `output.results` 包含 `pbr_model_url`（或 `base_model_url`）、`rendered_image_url`，所有 URL 有效期仅 2 小时，需及时下载。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须在该地域下生成。
- **异步强制性**：不支持同步调用，`X-DashScope-Async: enable` 为硬性请求头，缺失即失败。
- **输入互斥性**：`prompt`、`image`、`images` 三者不可共存，同时传入将返回 `InvalidParameter`。
- **多图格式刚性**：`images` 数组长度必须为 4，缺失视角必须用 `{}` 占位，不可省略或缩短数组。
- **资源时效性**：`task_id` 24 小时后失效；生成结果 URL（如 `pbr_model_url`）2 小时后过期，需在有效期内完成下载。
- **错误处理**：任务失败时 `output.code` 和 `output.message` 提供具体原因，应优先查阅 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)，而非重试无效请求。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


