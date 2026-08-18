# 3d generation

百炼平台的 3d generation 能力基于 Tripo 模型提供文生3D、单图生3D 和多图生3D 三种生成模式，支持带贴图（PBR）与无贴图两种输出类型。所有调用均为异步任务，需通过 `task_id` 轮询获取结果，且**仅在华北2（北京）地域可用**。开发者需提前开通服务并配置对应地域的 API Key。

## 支持的模型/功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入方式（三者互斥）**：
  - 文生3D：通过 `input.prompt` 指定中文/英文提示词（≤1024 字符）；
  - 单图生3D：通过 `input.image` 传入单张 JPEG/PNG 公网 URL（分辨率 20–6000px，≤20MB）；
  - 多图生3D：通过 `input.images` 传入长度为 4 的数组，按**前、左、后、右**顺序排列，空视角用 `{}` 占位（实际有效图数为 2–4 张）。
- **输出类型**：
  - 默认生成 PBR 材质模型（含贴图），返回 `pbr_model_url`；
  - 无贴图模型需**同时设置 `"texture": false` 和 `"pbr": false`**，返回 `base_model_url`。

> **注意**：原始文档中 `input.images` 示例使用了 `file_token` 字段名，但实际应为 `url` 或 `file_token`？经核对 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中所有 curl 示例均使用 `file_token`，且未提及其他字段名，故以该文档为准。后续如官方 SDK 或新文档变更字段名，需同步更新。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / string / array | 条件必填 | 三者仅可选其一；`images` 数组长度恒为 4，空视角填 `{}` |
| `parameters.texture_quality` | string | 否 | `"standard"`（默认）或 `"detailed"`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `false` 时将强制禁用贴图（除非同时设 `texture: false`） |
| `parameters.texture` | boolean | 否 | 默认 `true`；设为 `false` 且 `pbr: false` 时输出无贴图模型 |

所有请求**必须包含**以下 Header：
- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（缺此头将报错：“current user api does not support synchronous calls”）

## 使用方式

1. **开通与配置**：  
   在[阿里云百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索 “Tripo”，点击**立即开通**；再[获取并配置北京地域的 API Key](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

2. **创建任务（POST）**：  
   请求地址（北京地域）：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   成功响应含 `task_id`（有效期 24 小时），**禁止重复提交相同请求**。

3. **轮询查询结果（GET）**：  
   请求地址：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   建议间隔 ≥15 秒轮询；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；`UNKNOWN` 表示 `task_id` 过期或无效。

4. **结果解析**：  
   `SUCCEEDED` 响应中：
   - `output.results[0].pbr_model_url`：PBR 模型 GLB 下载链接（2 小时有效）；
   - `output.results[0].base_model_url`：无贴图基础模型 GLB（仅当 `texture: false && pbr: false` 时存在）；
   - `output.results[0].rendered_image_url`：预览渲染图 WebP 链接（2 小时有效）；
   - `usage.3d_task_type` 标识任务类型（`text-to-3d`/`image-to-3d`/`multi-image-to-3d`）。

详细请求/响应结构及错误码，请参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 或 API Key 均不可用；调用前务必确认 WorkspaceId 与地域匹配。
- **异步强制性**：所有请求必须携带 `X-DashScope-Async: enable`，同步调用不被支持。
- **task_id 生命周期**：创建后 24 小时内有效，超时后查询返回 `task_status: "UNKNOWN"`，无法恢复。
- **图片规范**：单图/多图均要求公网可访问、格式为 JPEG/PNG、单文件 ≤20MB、边长 ∈ [20, 6000] px；多图视角顺序严格为 `[前, 左, 后, 右]`，缺失视角必须用 `{}` 占位。
- **无贴图逻辑**：仅当 `texture: false` **且** `pbr: false` 同时成立时，才返回 `base_model_url`；若仅设 `texture: false`，`pbr` 仍为 `true`，系统将忽略 `texture` 设置。
- **RPS 限制**：任务查询接口默认限流 20 RPS；高频轮询建议改用[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)机制。
- **错误排查**：失败响应中的 `code` 和 `message` 需结合 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 分析；常见错误包括 `InvalidApiKey`、`InvalidParameter` 等。完整错误处理指南见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


