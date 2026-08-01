# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果，适用于华北2（北京）地域。该能力依赖 Tripo 官方模型接口封装，具体行为与参数语义以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 文档为准。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
  
- **生成模式**（三者互斥，不可同时指定）：
  - 文生 3D：通过 `input.prompt` 指定文本描述；
  - 单图生 3D：通过 `input.image` 提供单张公网 URL 图像；
  - 多图生 3D：通过 `input.images` 提供长度为 4 的数组，按「前、左、后、右」顺序排列，空视角用 `{}` 占位。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求 `input` 中仅能选择一种输入方式（`prompt` / `image` / `images`），若同时传入多个字段，API 将返回 `InvalidParameter` 错误。

## 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | 条件必填（文生3D） | 最长 1024 字符，支持中英文；详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |
| `input.image` | string | 条件必填（单图生3D） | 公网 JPEG/PNG URL，宽高 ∈ [20, 6000] px，≤20MB |
| `input.images` | array[object] | 条件必填（多图生3D） | 长度固定为 4，每项含 `type`（`jpeg`/`png`）和 `file_token`（公网 URL）；空视角填 `{}` |
| `parameters.texture_quality` | string | ❌ | `standard`（默认）或 `detailed`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | ❌ | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（≤150 万面）或 `ultra`（≤200 万面） |
| `parameters.texture` | boolean | ❌ | 默认 `true`；设为 `false` 时需同时设 `pbr: false` 才生成无贴图模型 |
| `parameters.pbr` | boolean | ❌ | 默认 `true`；设为 `true` 时强制启用贴图，返回 `pbr_model_url` |

## 使用方式

1. **开通与配置**：  
   在百炼控制台（华北2 北京地域）搜索并开通 Tripo 模型服务；配置 `DASHSCOPE_API_KEY` 环境变量，确保使用北京地域的密钥。

2. **异步任务创建**（POST）：  
   请求 URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   **必需请求头**：  
   - `Content-Type: application/json`  
   - `Authorization: Bearer $DASHSCOPE_API_KEY`  
   - `X-DashScope-Async: enable`（缺失将报错 `current user api does not support synchronous calls`）

3. **轮询查询结果**（GET）：  
   请求 URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - `task_id` 有效期为 **24 小时**，超时返回 `task_status: "UNKNOWN"`；  
   - 建议轮询间隔 ≥15 秒，避免触发 RPS 限频（默认 20 QPS）；  
   - 成功响应中 `results` 数组包含 `pbr_model_url`（PBR 材质 GLB）、`base_model_url`（无贴图 GLB）或 `rendered_image_url`（预览图），链接有效期 **2 小时**，需及时下载。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域调用将失败；业务空间 ID 和 API Key 必须同地域。
- **输入互斥性**：`prompt`、`image`、`images` 三者严格互斥，违反将导致 `InvalidParameter` 错误。
- **图像规范**：单图/多图均要求公网可访问 URL，格式为 JPEG/PNG，单图文件 ≤20MB；多图数组必须为 4 项，缺失视角必须显式填 `{}`。
- **无贴图模型**：必须同时设置 `"texture": false, "pbr": false`，否则 `pbr: true` 会强制覆盖 `texture` 为 `true`。
- **任务管理**：不支持同步调用；取消任务需调用独立接口（见 [管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks)），未提供内联取消能力。
- **错误处理**：所有失败响应均含 `code` 和 `message` 字段，应结合 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 排查；常见错误如 `InvalidApiKey`、`InvalidParameter`、`TaskExpired` 等均在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确定义。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


