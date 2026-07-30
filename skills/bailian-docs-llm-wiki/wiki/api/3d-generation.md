# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。该服务采用异步任务机制，需通过创建任务 + 轮询结果两步完成调用，适用于华北2（北京）地域。所有调用均需配置有效的 API Key 并显式启用异步头 `X-DashScope-Async: enable`。

## 支持的模型/功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式**（三者互斥）：
  - 文生3D：通过 `input.prompt` 输入文本描述；
  - 单图生3D：通过 `input.image` 提供单张公网可访问图像 URL；
  - 多图生3D：通过 `input.images` 提供长度为 4 的数组，顺序固定为【前、左、后、右】，空视角用 `{}` 占位；
- **输出类型**：
  - 默认返回 PBR 材质模型（`pbr_model_url`，GLB 格式）及预览图（`rendered_image_url`）；
  - 无贴图模型需同时设置 `"texture": false, "pbr": false`，此时返回 `base_model_url`。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求仅支持华北2（北京）地域，且必须使用该地域的 API Key；其他地域 URL 不可用，此限制未在通用文档中说明，需严格遵循。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | 文生3D时必填 | 最长 1024 字符，支持中英文；详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |
| `input.image` | string | 单图生3D时必填 | 公网 HTTP/HTTPS 图像 URL；格式 JPEG/PNG；宽高 ∈ [20, 6000] px；≤ 20 MB |
| `input.images` | array[object] | 多图生3D时必填 | 长度恒为 4，每项含 `type`（`jpeg`/`png`）和 `file_token`（URL）；空视角填 `{}` |
| `parameters.texture_quality` | string | 否 | `"standard"`（默认）或 `"detailed"`；影响贴图分辨率 |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持；`"standard"`（≤150万面）或 `"ultra"`（≤200万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `false` 时需同步设 `texture: false` 才生效 |
| `parameters.texture` | boolean | 否 | 默认 `true`；与 `pbr` 联动控制是否生成贴图 |

## 使用方式

1. **前置准备**：
   - 在 [百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 开通 Tripo 服务；
   - [获取并配置北京地域的 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 到环境变量 `DASHSCOPE_API_KEY`；
2. **创建任务（POST）**：
   - 请求 URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - 必须携带请求头：`Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`
   - 请求体按输入模式选择 `prompt` / `image` / `images`，并合理设置 `parameters`
   - 成功响应返回 `task_id`（有效期 24 小时），**禁止重复提交同一任务**
3. **轮询结果（GET）**：
   - 请求 URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 建议间隔 ≥15 秒轮询，状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`
   - 成功时 `output.results` 包含 `pbr_model_url`（或 `base_model_url`）和 `rendered_image_url`，链接有效期 2 小时，需及时下载

完整调用流程示例见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中各 curl 示例。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，跨地域调用必然失败；
- **异步强制性**：HTTP 接口不支持同步调用，缺失 `X-DashScope-Async: enable` 头将报错 `current user api does not support synchronous calls`；
- **任务生命周期**：`task_id` 有效期严格为 24 小时，超时后查询返回 `task_status: "UNKNOWN"`；
- **RPS 限制**：任务结果查询接口默认限流 20 RPS，高频轮询建议改用 [异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)；
- **输入校验**：`prompt`、`image`、`images` 三者互斥，同时传入多个将直接报错 `InvalidParameter`；
- **图像要求**：单图/多图均需公网可直连，CDN 缓存需支持 CORS；多图场景下四视角分辨率不要求一致，但建议统一为 ≥256px 边长；
- **无贴图逻辑**：必须同时设置 `"texture": false` 和 `"pbr": false`，仅设其一无效。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


