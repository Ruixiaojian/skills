# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。该能力采用异步 API 调用方式，需通过任务 ID 轮询获取结果，适用于华北2（北京）地域。所有调用均需配置有效的 API Key 并显式启用异步头 `X-DashScope-Async: enable`。

## 支持的模型/功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级生成，输出模型最高 2 万面，响应更快；对应 Tripo 官方 API 版本 `P1-20260311`。
- **生成模式**（三者互斥）：
  - 文生3D：通过 `input.prompt` 指定文本描述（最大 1024 字符）；
  - 单图生3D：通过 `input.image` 提供单张公网 URL 图像（JPEG/PNG，20–6000px，≤20MB）；
  - 多图生3D：通过 `input.images` 提供长度为 4 的数组，顺序为前、左、后、右；空视角用 `{}` 占位，实际有效图数为 2–4 张。
- **输出类型**：
  - 默认返回 PBR 材质模型（`pbr_model_url`，GLB 格式）及预览图（`rendered_image_url`）；
  - 无贴图模型需同时设置 `"texture": false, "pbr": false`，返回 `base_model_url`。

详细参数与行为说明见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / object / array | ✅（三选一） | 输入源，不可共存；`images` 数组必须为长度 4，含空对象占位 |
| `parameters.texture_quality` | string | ❌ | `"standard"`（默认）或 `"detailed"`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | ❌ | 仅 `Tripo/Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | ❌ | 默认 `true`；设为 `false` 时需同步设 `texture: false` 才能获得无贴图模型 |
| `parameters.texture` | boolean | ❌ | 默认 `true`；与 `pbr` 联动，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |

> **注意**：文档中 `parameters.texture` 和 `parameters.pbr` 的联动逻辑存在隐式约束——当 `pbr=true` 时会强制启用贴图（即忽略 `texture=false`），该行为在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确说明，开发者须按此组合配置。

## 使用方式

1. **开通与鉴权**：
   - 仅限华北2（北京）地域，需在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)搜索并开通 Tripo 模型；
   - 配置地域匹配的 API Key 到环境变量 `DASHSCOPE_API_KEY`（参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)）。

2. **异步任务提交**（POST）：
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - 必须携带请求头：`Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`
   - 成功响应含 `task_id`（有效期 24 小时），**禁止重复创建任务**。

3. **轮询查询结果**（GET）：
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 建议轮询间隔 ≥15 秒；RPS 限制为 20；
   - 状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；`UNKNOWN` 表示 task_id 过期或无效。

完整调用示例（含文生3D、单图、多图、无贴图）见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强约束**：API 仅支持华北2（北京）地域，其他地域 URL 不可用；
- **异步强制要求**：同步调用被明确拒绝，缺失 `X-DashScope-Async: enable` 头将报错 `"current user api does not support synchronous calls"`；
- **输入互斥性**：`prompt`、`image`、`images` 三者不可同时存在，否则返回 `InvalidParameter`；
- **多图格式**：`input.images` 必须为长度 4 的数组，即使部分视角为空也需保留 `{}` 占位；
- **URL 时效性**：`pbr_model_url`、`base_model_url`、`rendered_image_url` 有效期均为 **2 小时**，需及时下载；
- **任务生命周期**：`task_id` 有效期为 **24 小时**，超时后查询返回 `task_status: "UNKNOWN"`；
- **错误处理**：失败时响应含 `code` 和 `message`，应结合 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 排查，而非重试无效请求。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


