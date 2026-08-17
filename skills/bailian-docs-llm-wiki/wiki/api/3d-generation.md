# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果，适用于华北2（北京）地域。该能力依赖 Tripo 官方模型服务，输出格式为 GLB（含 PBR 材质或基础网格），并附带预览渲染图。

## 支持的模型/功能

- **模型标识**：当前仅支持 `Tripo/Tripo-P1.0`（专业版，最高 2 万面，速度快）和 `Tripo/Tripo-H3.1`（高精度版，最高 200 万面）。二者在几何精度与输出质量上存在显著差异，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
- **生成模式**：
  - 文生3D：通过 `prompt` 字段传入文本描述；
  - 单图生3D：通过 `image` 字段传入单张公网可访问图像 URL；
  - 多图生3D：通过 `images` 数组传入 4 张按“前、左、后、右”顺序排列的图像（空视角可用 `{}` 占位），实际有效图像数为 2~4 张。
- **输出类型**：
  - 默认返回 PBR 材质模型（`pbr_model_url`）及渲染图（`rendered_image_url`）；
  - 可显式禁用贴图与 PBR，仅返回无材质基础模型（`base_model_url`），需同时设置 `"texture": false, "pbr": false` —— 此行为在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确定义。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `Tripo/Tripo-P1.0` 或 `Tripo/Tripo-H3.1` |
| `input.prompt` | string | 条件必填 | 文生3D时使用，最大 1024 字符，支持中英文 |
| `input.image` | string | 条件必填 | 单图生3D时使用，JPEG/PNG，20–6000px，≤20MB |
| `input.images` | array[object] | 条件必填 | 多图生3D时使用，长度固定为 4，每项含 `type`（`jpeg`/`png`）和 `file_token`（公网 URL） |
| `parameters.texture_quality` | string | 否 | `standard`（默认）或 `detailed`；仅对 `Tripo/Tripo-P1.0` 有效 |
| `parameters.geometry_quality` | string | 否 | `standard`（默认）或 `ultra`；**仅 `Tripo/Tripo-H3.1` 支持**，见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |
| `parameters.pbr` / `parameters.texture` | boolean | 否 | 均默认 `true`；若需无贴图模型，**必须同时设为 `false`** |

> **注意**：文档中 `geometry_quality` 明确标注仅适用于 `Tripo-H3.1`，但部分旧示例未强调此限制，开发者应以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的参数说明为准。

## 使用方式

1. **前置准备**：
   - 在华北2（北京）地域开通 Tripo 服务（控制台搜索 “Tripo” → 立即开通）；
   - 配置 `DASHSCOPE_API_KEY` 环境变量，并确保请求头包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `X-DashScope-Async: enable`。

2. **创建任务（POST）**：
   - Endpoint（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - `input` 中三者（`prompt`/`image`/`images`）**严格互斥**，不可共存；
   - 成功响应返回 `task_id`（有效期 24 小时），用于后续轮询。

3. **轮询结果（GET）**：
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 建议轮询间隔 ≥15 秒；
   - 状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；
   - `SUCCEEDED` 响应中 `results` 数组包含 `pbr_model_url`、`rendered_image_url` 或 `base_model_url`（取决于参数配置），所有 URL 有效期 **2 小时**，需及时下载。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须在该地域生成。
- **异步强制要求**：`X-DashScope-Async: enable` 为必填请求头，缺失将报错 `current user api does not support synchronous calls`。
- **输入互斥性**：`prompt`、`image`、`images` 三者不可同时存在，否则返回 `InvalidParameter` 错误。
- **多图格式**：`images` 数组长度必须为 4，缺失视角须用 `{}` 占位，不可省略或缩短数组。
- **资源时效性**：
  - `task_id` 查询有效期：24 小时；
  - 成果 URL（`pbr_model_url` 等）有效期：2 小时；
- **RPS 限制**：任务查询接口默认限流 20 QPS，高频轮询建议配置[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)替代。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


