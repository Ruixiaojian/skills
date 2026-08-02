# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果，且**仅限华北2（北京）地域可用**。调用前需在百炼控制台开通 Tripo 服务并配置对应地域的 API Key。详细说明请参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型与功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: ultra`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。

- **输入方式（三者互斥）**：
  - 文生3D：通过 `input.prompt` 提供文本描述（最大 1024 字符，支持中英文）。
  - 单图生3D：通过 `input.image` 提供单张公网可访问的 JPEG/PNG 图像（分辨率 20–6000px，≤20MB）。
  - 多图生3D：通过 `input.images` 提供长度为 4 的数组，按**前、左、后、右**顺序排列；缺失视角需填 `{}`，有效图片数须 ≥2。每张图格式需显式声明 `type: "jpeg"` 或 `"png"`，`file_token` 为公网 URL。

- **输出类型**：
  - 默认返回 PBR 材质模型（`pbr_model_url`，GLB 格式）及预览图（`rendered_image_url`）。
  - 无贴图模型需同时设置 `"texture": false, "pbr": false`，此时返回 `base_model_url`。

更多输入约束与示例详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / object / array | ✅（三选一） | 仅允许一种输入方式，混用将报错 |
| `parameters.texture_quality` | string | ❌ | 可选值：`"standard"`（默认）、`"detailed"`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | ❌ | 仅 `Tripo-H3.1` 支持；`"standard"`（≤150万面）或 `"ultra"`（≤200万面） |
| `parameters.pbr` | boolean | ❌ | 默认 `true`；设为 `false` 时需同步设 `texture: false` 才能生成无贴图模型 |
| `parameters.texture` | boolean | ❌ | 默认 `true`；与 `pbr` 联动，不可单独禁用贴图 |

> **注意**：文档中明确要求 `pbr` 和 `texture` **必须同时为 `false` 才能获得无贴图模型**，单独设置 `texture: false` 无效。该逻辑已在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中强调。

## 使用方式

1. **开通与认证**  
   - 在[百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)搜索 “Tripo” 并开通服务。  
   - 获取北京地域专用 API Key，并配置至环境变量 `DASHSCOPE_API_KEY`（参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的配置指引）。

2. **异步任务创建**  
   - 向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发起请求。  
   - **必需请求头**：`Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`（缺一则报错）。  
   - 成功响应返回 `task_id`（有效期 24 小时），**禁止重复提交相同任务**。

3. **轮询查询结果**  
   - 使用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态。  
   - 建议轮询间隔 ≥15 秒；RPS 限制为 20；超时（24 小时）后返回 `task_status: UNKNOWN`。  
   - 状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；成功时 `results` 中含 `pbr_model_url` 或 `base_model_url`（链接有效期 2 小时）。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须为该地域生成。
- **任务时效性**：`task_id` 有效期严格为 24 小时，超时无法查询；生成结果 URL 有效期为 2 小时，需及时下载。
- **输入校验**：`prompt`、`image`、`images` 三者互斥；`images` 数组长度必须为 4，空视角用 `{}` 占位。
- **资源限制**：单图分辨率需在 [20, 6000] 像素范围内，文件 ≤20MB；多图各图独立校验。
- **错误处理**：失败时 `output.code` 和 `output.message` 提供具体原因，应结合 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 排查。常见错误包括 `InvalidApiKey`、`InvalidParameter` 等。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


