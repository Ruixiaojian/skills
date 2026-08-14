# 3d generation

百炼平台的 3d generation 能力基于 Tripo 模型提供文生3D、单图生3D 和多图生3D 三种生成模式，支持带贴图（PBR）与无贴图两种输出形式。该能力为[异步任务](../concepts/async-task.md)型 API，需通过“创建任务 → 轮询查询”两步完成调用，适用于华北2（北京）地域。所有请求必须配置 `X-DashScope-Async: enable` 请求头，同步调用不被支持。

## 支持的模型/功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级生成，最高 2 万面，推理更快；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式（三者互斥）**：
  - 文生3D：通过 `input.prompt` 指定中文或英文提示词（≤1024 字符）；
  - 单图生3D：通过 `input.image` 传入单张公网 JPEG/PNG 图像（20–6000px，≤20MB）；
  - 多图生3D：通过 `input.images` 传入长度为 4 的数组，按**前、左、后、右**顺序排列，缺失视角可用空对象 `{}` 占位（实际有效图数需 ≥2）。
- **输出类型**：
  - 默认返回 PBR 材质模型（`pbr_model_url`，GLB 格式）及预览图（`rendered_image_url`）；
  - 无贴图模型需**同时设置 `"texture": false` 和 `"pbr": false`**，此时返回 `base_model_url`。

> **注意**：原始文档中 `multi-image-to-3d` 示例代码使用了 `file_token` 字段名，但实际应为 `url` 或 `file_token`？经核对 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中所有 curl 示例均使用 `file_token`，且字段说明明确要求其为“图像的公网URL”，故以该文档为准，无需修正。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / string / array | 条件必填 | 三者仅可选其一；`images` 数组长度恒为 4，空视角填 `{}` |
| `parameters.texture_quality` | string | 否 | `"standard"`（默认）或 `"detailed"`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `false` 时将强制禁用贴图（除非同时设 `texture: false`） |
| `parameters.texture` | boolean | 否 | 默认 `true`；与 `pbr: false` **必须同时为 `false`** 才能获得无贴图模型 |

所有请求必须携带以下 Header：
- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确强调：缺少此头将报错 `"current user api does not support synchronous calls"`）

## 使用方式

1. **开通与配置**  
   在[百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)搜索并开通 “Tripo” 模型；获取并配置北京地域专用 API Key（[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 强调“本文档仅适用于华北2（北京）地域”）。

2. **创建任务（POST）**  
   请求 URL（北京地域）：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   成功响应含 `task_id`（有效期 24 小时），**禁止重复提交相同请求**。

3. **轮询查询结果（GET）**  
   请求 URL：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   建议轮询间隔 ≥15 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；`UNKNOWN` 表示 task_id 过期或无效。

4. **结果解析**  
   `output.results` 为数组（当前固定返回 1 项），包含：
   - `pbr_model_url`（PBR 模型，GLB，2 小时有效）
   - `base_model_url`（无贴图模型，GLB，2 小时有效，仅当 `texture` & `pbr` 均为 `false` 时存在）
   - `rendered_image_url`（预览图，WebP，2 小时有效）

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，API Key 也必须为北京地域生成。
- **异步强制性**：所有请求必须设置 `X-DashScope-Async: enable`，同步调用直接报错。
- **task_id 生命周期**：创建后 24 小时内有效，超时查询返回 `task_status: "UNKNOWN"`，无法恢复。
- **图片规范**：单图/多图均要求 JPEG/PNG 格式、20–6000px 边长、≤20MB；多图 `images` 数组长度严格为 4，顺序不可变。
- **无贴图逻辑**：必须同时设置 `"texture": false` 和 `"pbr": false`，任一为 `true` 均会启用贴图生成。
- **RPS 限制**：任务查询接口默认限流 20 RPS；高频轮询建议改用[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)机制。
- **错误处理**：失败响应含 `code` 和 `message`，需结合[错误码文档](https://help.aliyun.com/zh/model-studio/error-code)定位；常见错误如 `InvalidApiKey`、`InvalidParameter` 等均在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的“错误码”章节有指引。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


