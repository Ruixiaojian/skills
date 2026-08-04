# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果。该能力当前**仅限华北2（北京）地域**可用，且依赖 Tripo 官方 API 接口封装，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型与功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。

- **输入模式**（三者互斥）：
  - 文生 3D：通过 `input.prompt` 指定文本描述；
  - 单图生 3D：通过 `input.image` 提供单张公网可访问图像 URL；
  - 多图生 3D：通过 `input.images` 提供长度为 4 的数组，按「前、左、后、右」顺序排列，空视角用 `{}` 占位。

- **输出类型**：
  - 默认返回 PBR 材质模型（GLB 格式，含贴图），URL 字段为 `pbr_model_url`；
  - 可显式禁用贴图（需同时设置 `"texture": false, "pbr": false`），此时返回无贴图基础模型，URL 字段为 `base_model_url`；
  - 所有成功响应均包含预览图 `rendered_image_url`。

详细参数与输入约束请参考原始文档：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | ⚠️（文生 3D 时必填） | 最长 1024 字符，支持中英文 |
| `input.image` | string | ⚠️（单图生 3D 时必填） | 公网 HTTP/HTTPS URL，JPEG/PNG，20–6000px，≤20MB |
| `input.images` | array[object] | ⚠️（多图生 3D 时必填） | 长度固定为 4，每个元素含 `type`（`jpeg`/`png`）和 `file_token`（URL） |
| `parameters.texture_quality` | string | ❌（默认 `standard`） | 可选 `standard` / `detailed`；仅对含贴图任务生效 |
| `parameters.geometry_quality` | string | ❌（仅 `Tripo/Tripo-H3.1` 支持） | 可选 `standard`（≤150 万面） / `ultra`（≤200 万面） |
| `parameters.pbr` | boolean | ❌（默认 `true`） | 设为 `false` 时需同步设 `texture: false` 才能输出无贴图模型 |
| `parameters.texture` | boolean | ❌（默认 `true`） | 与 `pbr` 联动，二者同为 `false` 时启用无贴图模式 |

> **注意**：`parameters.texture` 和 `parameters.pbr` 的组合逻辑在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确定义——仅当两者均为 `false` 时才返回 `base_model_url`；若仅设 `texture: false` 而 `pbr: true`，系统将强制启用贴图。

## 使用方式

1. **开通与配置**  
   - 在百炼控制台（华北2 北京地域）搜索并开通 **Tripo** 模型服务；  
   - 获取并配置 `DASHSCOPE_API_KEY` 到环境变量（参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的配置指引）。

2. **[异步任务](../concepts/asynchronous-task.md)提交**  
   - 向 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送 `POST` 请求；  
   - **必须**携带请求头：`X-DashScope-Async: enable`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`；  
   - 成功响应返回 `task_id`（有效期 24 小时），**禁止重复创建任务**。

3. **轮询查询结果**  
   - 向 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 发送 `GET` 请求（仅需 `Authorization` 头）；  
   - 建议轮询间隔 ≥15 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；  
   - 成功时 `output.results[0]` 包含 `pbr_model_url` 或 `base_model_url`（2 小时有效），务必及时下载。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域，其他地域 URL 不可用；
- **API Key 绑定**：必须使用北京地域生成的 API Key，跨地域调用将失败；
- **任务时效性**：
  - `task_id` 查询有效期为 **24 小时**，超时返回 `task_status: "UNKNOWN"`；
  - 模型下载 URL（`pbr_model_url`/`base_model_url`/`rendered_image_url`）有效期为 **2 小时**；
- **RPS 限制**：任务查询接口默认限流 20 QPS，高频轮询建议配置[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)；
- **输入校验**：`prompt`、`image`、`images` 三者严格互斥，同时传入将返回 `InvalidParameter` 错误；
- **图像要求**：单图/多图均需公网可访问、格式合规（JPEG/PNG）、尺寸在 [20, 6000] px 范围内；
- **错误排查**：所有错误码及含义详见官方[错误码文档](https://help.aliyun.com/zh/model-studio/error-code)，原始文档亦有引用说明：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


