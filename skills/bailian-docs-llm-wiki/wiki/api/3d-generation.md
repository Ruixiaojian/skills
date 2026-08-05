# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。所有任务均采用异步调用方式，需通过 `task_id` 轮询获取结果。该能力当前仅在华北2（北京）地域可用，且依赖 Tripo 官方模型服务 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **生成模式**（互斥，仅可选其一）：
  - 文生3D：通过 `input.prompt` 输入文本描述；
  - 单图生3D：通过 `input.image` 提供单张公网可访问图像 URL；
  - 多图生3D：通过 `input.images` 提供长度为 4 的数组，顺序为前、左、后、右；空视角用 `{}` 占位，有效图片数需 ≥2。
- **输出类型**：
  - 默认返回 PBR 材质模型（GLB，含贴图），URL 字段为 `pbr_model_url`；
  - 无贴图模型需显式设置 `"texture": false, "pbr": false`，返回 `base_model_url`；
  - 均附带预览图 `rendered_image_url`。

> **注意**：原始文档中 `input.images` 数组长度明确要求为 4，但示例中传入 2 张图时仍使用 4 元素数组（含 `{}` 占位），而非动态长度数组。此设计已在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确定义，其他文档若声称支持变长数组则属过时信息。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | 条件必填（文生3D） | 最大 1024 字符，支持中英文 |
| `input.image` | string | 条件必填（单图） | JPEG/PNG，宽高 [20, 6000]px，≤20MB，公网 HTTPS/HTTP URL |
| `input.images` | array[object] | 条件必填（多图） | 长度恒为 4；每个元素含 `type`（`jpeg`/`png`）和 `file_token`（URL）；无效位置填 `{}` |
| `parameters.texture_quality` | string | ❌ | 可选值：`"standard"`（默认）、`"detailed"` |
| `parameters.geometry_quality` | string | ❌ | 仅 `Tripo/Tripo-H3.1` 支持；`"standard"`（≤150 万面）、`"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | ❌ | 默认 `true`；设为 `false` 时需同时设 `texture: false` 才生效 |
| `parameters.texture` | boolean | ❌ | 默认 `true`；与 `pbr` 联动控制贴图生成 |

请求头必须包含：
- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（**缺失将报错**：“current user api does not support synchronous calls”）

## 使用方式

1. **开通与配置**  
   在百炼控制台（[华北2（北京）地域](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)）搜索并开通 Tripo 模型；按 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 指引配置 API Key 到环境变量。

2. **创建异步任务**  
   向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送请求，获取 `task_id`（有效期 24 小时）。

3. **轮询查询结果**  
   定期调用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`，建议间隔 ≥15 秒。状态流转为：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`。成功响应中 `results` 数组包含 `pbr_model_url` 或 `base_model_url`（链接有效期 2 小时，需及时下载）。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域，其他地域 URL 不可用。
- **任务时效**：`task_id` 有效期严格为 24 小时，超时后查询返回 `task_status: "UNKNOWN"`。
- **RPS 限制**：任务查询接口默认限流 20 QPS；高频轮询或需事件通知时，应配置 [异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
- **输入校验**：`prompt`/`image`/`images` 三者互斥，同时传入将直接报错；`images` 数组长度必须为 4，否则触发参数校验失败。
- **资源约束**：单图/多图输入的图像分辨率、格式、大小限制详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)，超出将返回 `InvalidParameter` 错误。
- **错误处理**：所有失败响应均含 `code` 和 `message` 字段，需结合 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 排查。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


