# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种输入模式。该服务采用异步 API 设计，需通过任务创建 + 轮询结果两步完成调用，适用于华北2（北京）地域。所有请求必须配置有效的 API Key 并显式声明 `X-DashScope-Async: enable` 头。

## 支持的模型/功能

- **模型名称**：  
  - `Tripo/Tripo-P1.0`：专业版，输出最高 2 万面，速度快，适用于快速原型与轻量级应用；  
  - `Tripo/Tripo-H3.1`：高精度版，输出最高 200 万面，支持 `geometry_quality: "ultra"`，适用于对几何细节要求高的场景。  
  详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 文档中“model”参数说明。

- **输入模式**（三者互斥）：  
  - 文生 3D：通过 `input.prompt` 提供文本描述；  
  - 单图生 3D：通过 `input.image` 提供单张公网可访问图像 URL；  
  - 多图生 3D：通过 `input.images` 提供长度为 4 的数组，按「前、左、后、右」顺序排列，空视角用 `{}` 占位。  
  具体示例见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中各 curl 示例。

- **输出类型**：  
  - 默认返回 PBR 材质模型（`pbr_model_url`，GLB 格式）及预览图（`rendered_image_url`）；  
  - 可通过设置 `"texture": false, "pbr": false` 获取无贴图基础模型（`base_model_url`）；  
  - 贴图质量由 `texture_quality` 控制（`standard` / `detailed`），仅对启用贴图的请求生效。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-P1.0` 或 `Tripo/Tripo-H3.1` |
| `input.prompt` | string | 条件必填 | 文生 3D 时使用，≤1024 字符，支持中英文 |
| `input.image` | string | 条件必填 | 单图生 3D 时使用，JPEG/PNG，20–6000px，≤20MB |
| `input.images` | array[object] | 条件必填 | 多图生 3D 时使用，固定长度 4，每项含 `type`（`jpeg`/`png`）和 `file_token`（公网 URL） |
| `parameters.texture_quality` | string | ❌ | `standard`（默认）或 `detailed`；仅当 `texture: true` 时生效 |
| `parameters.geometry_quality` | string | ❌ | 仅 `Tripo/Tripo-H3.1` 支持，`standard`（≤150 万面）或 `ultra`（≤200 万面） |
| `parameters.pbr` | boolean | ❌ | 默认 `true`；设为 `false` 时需同时设 `texture: false` 才返回 `base_model_url` |
| `parameters.texture` | boolean | ❌ | 默认 `true`；设为 `false` 且 `pbr: false` 时禁用贴图 |

> **注意**：`input` 中 `prompt`、`image`、`images` 严格互斥，同时传入多个将导致 `InvalidParameter` 错误 —— 此行为在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确强调，但部分旧版 SDK 示例存在误传风险，请以该文档为准。

## 使用方式

1. **开通与鉴权**：  
   - 仅限华北2（北京）地域，需在百炼控制台搜索并开通 Tripo 模型；  
   - 配置环境变量 `DASHSCOPE_API_KEY`，确保其对应北京地域的密钥。

2. **异步任务创建**（POST）：  
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   - Headers：`Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`（**缺一不可**）  
   - 成功响应返回 `task_id`（有效期 24 小时），用于后续轮询。

3. **轮询结果**（GET）：  
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - 建议间隔 ≥15 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；  
   - `SUCCEEDED` 响应中 `output.results` 包含 `pbr_model_url` 或 `base_model_url`（链接有效期 2 小时，需及时下载）。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京），其他地域 URL 不可用，且 API Key 必须为北京地域生成。
- **任务生命周期**：`task_id` 有效期 24 小时，超期后查询返回 `UNKNOWN`；结果 URL（如 `pbr_model_url`）有效期仅 2 小时。
- **RPS 限制**：任务查询接口默认限流 20 RPS，高频轮询建议改用[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
- **图像要求**：单图/多图输入均要求公网可访问、格式为 JPEG/PNG、边长 20–6000px、单图 ≤20MB；多图数组长度必须为 4，缺失视角需用 `{}` 显式占位。
- **错误处理**：常见错误码（如 `InvalidApiKey`、`InvalidParameter`）需结合 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 排查，具体字段校验逻辑以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 为准。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


