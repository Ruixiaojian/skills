# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。该能力采用异步 API 设计，需先创建任务获取 `task_id`，再轮询查询结果。所有调用必须在华北2（北京）地域进行，并使用对应地域的 API Key [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式**（三者互斥）：
  - 文生3D：通过 `input.prompt` 输入文本描述；
  - 单图生3D：通过 `input.image` 传入单张公网可访问图像 URL；
  - 多图生3D：通过 `input.images` 传入长度为 4 的数组，按 `[前, 左, 后, 右]` 顺序排列，空视角用 `{}` 占位。
- **输出类型**：
  - 默认返回 PBR 材质模型（GLB），含 `pbr_model_url`；
  - 无贴图模型需显式设置 `"texture": false, "pbr": false`，返回 `base_model_url`；
  - 均附带一张预览渲染图 `rendered_image_url`。

> **注意**：文档中明确要求“`prompt`、`image`、`images` 三者互斥”，但部分示例未强调此约束。实际调用时若同时传入多个，将返回 `InvalidParameter` 错误 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | ⚠️（文生3D必填） | 中英文提示词，≤1024 字符 |
| `input.image` | string | ⚠️（单图生3D必填） | JPEG/PNG 公网 URL，宽高 ∈ [20, 6000] px，≤20 MB |
| `input.images` | array[object] | ⚠️（多图生3D必填） | 长度为 4 的数组，每项含 `type`（`jpeg`/`png`）和 `file_token`（URL）；无效项填 `{}` |
| `parameters.texture_quality` | string | ❌（默认 `standard`） | `standard`（标清）或 `detailed`（高清） |
| `parameters.geometry_quality` | string | ❌（仅 `Tripo-H3.1` 支持） | `standard`（≤150 万面）或 `ultra`（≤200 万面） |
| `parameters.pbr` | boolean | ❌（默认 `true`） | `true` 时强制启用贴图，返回 `pbr_model_url`；设为 `false` 时需同步设 `texture: false` |
| `parameters.texture` | boolean | ❌（默认 `true`） | 控制是否生成贴图；与 `pbr` 联动，二者同为 `false` 才返回 `base_model_url` |

所有请求必须携带 `X-DashScope-Async: enable` 请求头，否则报错：“current user api does not [support](../guides/support.md) synchronous calls” [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 使用方式

1. **开通与配置**：
   - 在百炼控制台（华北2 北京）搜索并开通 `Tripo` 模型；
   - 获取并配置该地域的 API Key 到环境变量 `DASHSCOPE_API_KEY`。

2. **创建任务（POST）**：
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - 必须设置 `Content-Type: application/json` 和 `Authorization: Bearer $DASHSCOPE_API_KEY`
   - 成功响应返回 `task_id`（有效期 24 小时），**禁止重复提交相同任务**。

3. **轮询查询结果（GET）**：
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 建议轮询间隔 ≥15 秒；RPS 限制为 20；
   - 状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`/`CANCELED`/`UNKNOWN`；
   - `SUCCEEDED` 响应中 `results` 数组包含 `pbr_model_url`、`rendered_image_url` 或 `base_model_url`（视参数而定），所有 URL 有效期 2 小时。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须匹配该地域。
- **任务生命周期**：
  - `task_id` 有效期严格为 24 小时，超时后查询返回 `task_status: "UNKNOWN"`；
  - 输出 URL（如 `pbr_model_url`）有效期仅 2 小时，需及时下载。
- **输入校验**：
  - 图像 URL 必须可公开访问（HTTP/HTTPS），CDN 或 OSS 直链均可；
  - 多图模式下 `images` 数组长度必须为 4，即使部分为空对象 `{}`。
- **错误处理**：
  - 常见错误码参考官方 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)；
  - `InvalidParameter` 多因 `prompt`/`image`/`images` 混用或格式不合规导致。
- **资源消耗**：
  - `Tripo-H3.1` 任务耗时显著长于 `Tripo-P1.0`，建议根据精度需求与延迟容忍度选型。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


