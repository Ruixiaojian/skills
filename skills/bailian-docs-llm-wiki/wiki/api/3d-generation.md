# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果。该能力当前仅在华北2（北京）地域可用，且依赖 Tripo 官方模型服务集成。

## 支持的模型/功能

- **支持模型**：`Tripo/Tripo-P1.0`（专业版，最高2万面，速度快）和 `Tripo/Tripo-H3.1`（高精度版，最高200万面）。二者参数支持略有差异，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
- **输入模式**：
  - 文生3D：通过 `prompt` 字段传入文本描述；
  - 单图生3D：通过 `image` 字段传入单张公网可访问图像 URL；
  - 多图生3D：通过 `images` 数组传入4张按“前、左、后、右”顺序排列的图像（缺位用 `{}` 占位），实际有效图数为 2–4 张。
- **输出类型**：
  - 默认返回 PBR 材质模型（GLB 格式，含贴图与物理渲染属性），URL 字段为 `pbr_model_url`；
  - 可显式禁用贴图与 PBR（即 `texture: false` 且 `pbr: false`），此时返回无贴图基础模型，URL 字段为 `base_model_url`；
  - 始终返回一张预览渲染图（`rendered_image_url`）。

> **注意**：文档中 `images` 数组长度固定为 4，但示例同时展示了传入 4 张图和仅传入 2 张图（其余为 `{}`）的用法；[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求数组长度必须为 4，否则将报错，开发者需严格遵守。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `model` | string | 是 | 固定为 `Tripo/Tripo-P1.0` 或 `Tripo/Tripo-H3.1` |
| `input.prompt` | string | 文生3D时必填 | 中英文均可，最大 1024 字符 |
| `input.image` | string | 单图生3D时必填 | 公网 JPEG/PNG URL，宽高 ∈ [20, 6000] px，≤20 MB |
| `input.images` | array[object] | 多图生3D时必填 | 长度恒为 4 的数组，每项含 `type`（`jpeg`/`png`）和 `file_token`（公网 URL），空视角填 `{}` |
| `parameters.texture_quality` | string | 否 | `standard`（默认）或 `detailed`；仅对 `pbr: true` 有效 |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（150万面）或 `ultra`（200万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `false` 时需同步设 `texture: false` 才能获得无贴图模型 |
| `parameters.texture` | boolean | 否 | 默认 `true`；与 `pbr` 联动，单独设 `false` 无效 |

完整参数定义与约束请参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 使用方式

1. **开通与配置**：
   - 在[百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)搜索并开通 Tripo 模型；
   - 获取北京地域专用 API Key，并配置至环境变量 `DASHSCOPE_API_KEY`。

2. **异步调用流程**（两步）：
   - **步骤1：创建任务**  
     `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
     请求头必须包含：`Content-Type: application/json`、`Authorization: Bearer <API_KEY>`、`X-DashScope-Async: enable`。  
     成功响应返回 `task_id`（有效期 24 小时）。
   - **步骤2：轮询结果**  
     `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
     建议间隔 ≥15 秒轮询，状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`；`UNKNOWN` 表示 task_id 过期或不存在。

详细请求体结构与示例见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域，其他地域 URL 不可用。
- **异步强制性**：`X-DashScope-Async: enable` 为必需请求头，同步调用会报错 `"current user api does not support synchronous calls"`。
- **输入互斥**：`prompt`、`image`、`images` 三者不可共存，同时传入将导致 `InvalidParameter` 错误。
- **图片规范**：单图/多图均要求公网可访问、格式为 JPEG/PNG、单图 ≤20 MB；多图 `images` 数组长度必须为 4，否则请求失败。
- **结果时效性**：`pbr_model_url`、`base_model_url`、`rendered_image_url` 链接有效期均为 **2 小时**，需及时下载。
- **RPS 限制**：任务查询接口默认限流 20 RPS；高频轮询建议改用[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


