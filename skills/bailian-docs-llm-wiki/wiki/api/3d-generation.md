# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果。该能力当前**仅限华北2（北京）地域**可用，且依赖已开通的 Tripo 服务与正确配置的 API Key。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。

- **输入模式**（三者互斥）：
  - 文生 3D：通过 `input.prompt` 指定中文或英文提示词（≤1024 字符）；
  - 单图生 3D：通过 `input.image` 提供单张 JPEG/PNG 图像 URL（宽高 ∈ [20, 6000] 像素，≤20MB）；
  - 多图生 3D：通过 `input.images` 提供长度为 4 的数组，按顺序表示前、左、后、右视角；缺失视角需填空对象 `{}`（实际有效图数为 2–4 张）。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求 `images` 数组**必须固定为 4 项**，即使部分视角为空；若传入非 4 项数组，将触发 `InvalidParameter` 错误。

## 关键参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `texture_quality` | string | 贴图质量，影响外观细节 | `"standard"`（可选 `"detailed"`） |
| `geometry_quality` | string | 仅 `Tripo-H3.1` 支持；控制面数上限 | `"standard"`（`"ultra"` → 最高 200 万面） |
| `pbr` | boolean | 是否启用 PBR 材质（含物理光照响应） | `true`（设为 `false` 时需同步设 `texture: false`） |
| `texture` | boolean | 是否生成贴图（含 UV 和基础纹理） | `true`（无贴图需 `texture: false` + `pbr: false`） |

- `pbr: true` 会**强制启用贴图**（即忽略 `texture: false`），返回 `pbr_model_url`；
- 无贴图模型仅在 `texture: false` 且 `pbr: false` 时生成，返回 `base_model_url`；
- 更多参数说明详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 使用方式

1. **前置准备**：
   - 在 [百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索并开通 “Tripo” 服务；
   - 配置环境变量 `DASHSCOPE_API_KEY`，确保使用北京地域的 API Key（参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)）。

2. **异步任务创建**（POST）：
   - Endpoint（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - 必须携带请求头：`X-DashScope-Async: enable`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`
   - 成功响应返回 `task_id`（有效期 24 小时），**禁止重复提交相同任务**。

3. **轮询查询结果**（GET）：
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 建议轮询间隔 ≥15 秒；RPS 限制为 20；
   - 状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`/`CANCELED`/`UNKNOWN`；
   - 成功时 `output.results` 包含 `pbr_model_url`（PBR 模型）、`base_model_url`（无贴图模型）或 `rendered_image_url`（预览图），所有 URL 有效期 **2 小时**。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域调用将失败；
- **异步强制性**：同步调用不被支持，缺失 `X-DashScope-Async: enable` 头将报错 `current user api does not support synchronous calls`；
- **task_id 生命周期**：创建后 24 小时内有效，超时查询返回 `task_status: "UNKNOWN"`；
- **输入校验**：`prompt`/`image`/`images` 三者严格互斥；`images` 数组长度必须为 4（含空对象）；
- **资源限制**：单张图像 ≤20MB，分辨率 ∈ [20, 6000] 像素；多图各视角可分辨率不一致；
- **产物下载**：所有生成 URL（GLB/WebP）有效期仅 2 小时，需及时持久化存储。

> **注意**：文档中未提及对 `prompt` 内容安全过滤机制，但实际生产环境应自行校验输入合规性；建议参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的错误码章节排查常见失败原因（如 `InvalidParameter`、`InvalidApiKey`）。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


