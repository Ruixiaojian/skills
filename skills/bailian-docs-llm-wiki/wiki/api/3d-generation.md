# 3d generation

百炼平台的 3d generation 能力基于 Tripo 模型提供文生3D、单图生3D 和多图生3D 三种生成模式，支持带贴图（PBR）和无贴图两种输出格式。所有调用均为异步任务，需通过 `task_id` 轮询获取结果，且**仅限华北2（北京）地域可用**。该能力需在百炼控制台开通 Tripo 服务并配置对应地域的 API Key [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级生成，最高 2 万面，推理更快；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入方式（三者互斥）**：
  - 文生3D：通过 `input.prompt` 输入文本描述（最大 1024 字符）；
  - 单图生3D：通过 `input.image` 传入单张公网 JPEG/PNG 图像（分辨率 20–6000px，≤20MB）；
  - 多图生3D：通过 `input.images` 传入长度为 4 的数组，顺序固定为【前、左、后、右】；缺失视角需填 `{}`，实际有效图数为 2–4 张。
- **输出格式**：
  - 默认返回 PBR 材质模型（`pbr_model_url`，GLB 格式）及预览图（`rendered_image_url`）；
  - 无贴图模型需显式设置 `"texture": false, "pbr": false`，此时返回 `base_model_url`。

> **注意**：原始文档中 `input.images` 示例使用了 `file_token` 字段名，但实际应为 `url` 或 `file_token`？经核对 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中所有 curl 示例均使用 `file_token`，且未提及其他字段名，故以该文档为准。后续如 SDK 或新文档出现不一致，需以最新 API 文档为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / object / array | 条件必填 | 三者仅可选其一；`images` 数组长度必须为 4，空视角用 `{}` 占位 |
| `parameters.texture_quality` | string | 否 | `"standard"`（默认）或 `"detailed"`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `false` 时需同时设 `texture: false` 才能获得无贴图模型 |
| `parameters.texture` | boolean | 否 | 默认 `true`；与 `pbr` 联动，二者同为 `false` 时返回 `base_model_url` |

## 使用方式

1. **开通与配置**：  
   在[百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)搜索 “Tripo” 并开通服务；获取并配置该地域的 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

2. **创建任务（POST）**：  
   请求 URL（北京地域）：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   **必需请求头**：  
   - `Content-Type: application/json`  
   - `Authorization: Bearer $DASHSCOPE_API_KEY`  
   - `X-DashScope-Async: enable`（缺此头将报错）  

3. **轮询查询（GET）**：  
   使用上一步返回的 `task_id` 查询：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - 建议轮询间隔 ≥15 秒；  
   - `task_id` 有效期为 24 小时；  
   - 成功响应中 `output.results` 包含 `pbr_model_url`（或 `base_model_url`）和 `rendered_image_url`，**链接有效期仅 2 小时，须及时下载**。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须为该地域生成。
- **异步强制性**：不支持同步调用；`X-DashScope-Async: enable` 为硬性要求。
- **输入互斥**：`prompt`、`image`、`images` 不可共存，否则返回 `InvalidParameter` 错误。
- **多图格式**：`input.images` 必须为长度 4 的数组，顺序不可变；无效项必须为 `{}`，不可省略或传 `null`。
- **资源时效性**：  
  - `task_id` 24 小时后失效（状态变为 `UNKNOWN`）；  
  - 成果 URL（`pbr_model_url` 等）2 小时后过期，需立即下载或持久化存储。
- **RPS 限制**：任务查询接口默认 RPS=20，高频轮询建议改用[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)机制。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


