# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果，且**仅限华北2（北京）地域可用**。调用前须在百炼控制台开通 Tripo 服务并配置对应地域的 API Key。

## 支持的模型与功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
  
- **核心功能**：
  - 文生 3D（`prompt` 输入）
  - 单图生 3D（`image` 输入）
  - 多图生 3D（`images` 数组输入，固定长度为 4，顺序为前/左/后/右；空视角用 `{}` 占位）
  - 可选生成带 PBR 材质的 GLB 模型（默认启用），或无贴图基础模型（需同时设置 `"texture": false, "pbr": false`）

详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的“适用范围”与“HTTP调用”章节。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | 条件必填 | 文生 3D 时使用，≤1024 字符，支持中英文 |
| `input.image` | string | 条件必填 | 单图 URL，格式 JPEG/PNG，宽高 ∈ [20, 6000] px，≤20 MB |
| `input.images` | array[object] | 条件必填 | 长度恒为 4 的数组，每项含 `type`（`jpeg`/`png`）和 `file_token`（公网 URL）；无效视角填 `{}` |
| `parameters.texture_quality` | string | ❌ | `"standard"`（默认）或 `"detailed"`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | ❌ | 仅 `Tripo/Tripo-H3.1` 支持，`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | ❌ | 默认 `true`；设为 `false` 时需同步设 `texture: false` 才可得无贴图模型 |
| `parameters.texture` | boolean | ❌ | 默认 `true`；与 `pbr` 联动，二者同为 `false` 时返回 `base_model_url` |

> **注意**：`input.prompt`、`input.image`、`input.images` 三者互斥，同时传入将报错。该约束在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的“请求体（Request Body）”部分明确说明。

## 使用方式

1. **开通与配置**  
   在 [百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索 “Tripo”，点击**立即开通**；获取并配置该地域的 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 到环境变量。

2. **创建[异步任务](../concepts/asynchronous-task.md)**  
   向 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送 `POST` 请求，**必须包含**以下请求头：
   - `Content-Type: application/json`
   - `Authorization: Bearer $DASHSCOPE_API_KEY`
   - `X-DashScope-Async: enable`（缺失将报错：“current user api does not support synchronous calls”）

3. **轮询查询结果**  
   使用返回的 `task_id`，向 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 发送 `GET` 请求（仅需 `Authorization` 头）。  
   - `task_id` 有效期 **24 小时**，超时返回 `task_status: "UNKNOWN"`  
   - 建议轮询间隔 ≥15 秒；RPS 限制为 20  
   - 成功响应中，`results` 数组包含 `pbr_model_url`（PBR GLB）、`base_model_url`（无贴图 GLB）或 `rendered_image_url`（预览图），**所有 URL 有效期均为 2 小时**

完整流程示例见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的“HTTP调用”部分。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须为该地域生成。
- **输入互斥性**：`prompt` / `image` / `images` 三者不可共存，违反将触发 `InvalidParameter` 错误。
- **多图格式要求**：`images` 数组长度必须为 4，顺序固定为【前、左、后、右】；少于 2 张有效图（即非 `{}` 项）将失败。
- **资源时效性**：`task_id` 24 小时后失效；生成结果 URL（如 `pbr_model_url`）2 小时后过期，需及时下载。
- **无贴图模型**：必须同时设置 `"texture": false` 和 `"pbr": false`，否则 `pbr: false` 会被忽略（因 `pbr=true` 强制启用贴图）。

> **注意**：文档中 `geometry_quality` 明确标注“仅支持模型：`Tripo/Tripo-H3.1`”，但示例请求体未体现该约束。实际调用 `Tripo/Tripo-P1.0` 时若传入 `geometry_quality`，将被静默忽略或报错——请以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“parameters”小节的模型兼容性说明为准。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


