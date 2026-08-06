# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果，适用于华北2（北京）地域。该能力面向开发者提供标准化 API 接口，输出 GLB 格式模型及预览图。

## 支持的模型/功能

- **模型标识**：当前仅支持 `Tripo/Tripo-P1.0`（专业版，最高 2 万面，速度快）和 `Tripo/Tripo-H3.1`（高精度版，最高 200 万面）。二者在 `geometry_quality` 参数支持上存在差异，详见下文。
- **生成模式**：
  - 文生 3D：通过 `input.prompt` 输入文本描述；
  - 单图生 3D：通过 `input.image` 提供单张公网可访问图像 URL；
  - 多图生 3D：通过 `input.images` 提供长度为 4 的数组，顺序固定为「前、左、后、右」，空视角用 `{}` 占位；
- **输出类型**：
  - 默认返回 PBR 材质模型（`pbr_model_url`）和渲染预览图（`rendered_image_url`）；
  - 可显式禁用贴图与 PBR，获得无材质基础模型（`base_model_url`），需同时设置 `"texture": false, "pbr": false`。

> **注意**：原始文档中 `Tripo/Tripo-H3.1` 明确支持 `geometry_quality: ultra`，但 `Tripo/Tripo-P1.0` 未声明支持该参数；若对后者传入 `geometry_quality`，将被忽略。请以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“parameters”章节的模型兼容性说明为准。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `model` | string | 必填 | 固定为 `Tripo/Tripo-P1.0` 或 `Tripo/Tripo-H3.1` |
| `input.prompt` | string | 文生 3D 时必填 | 最长 1024 字符，支持中英文 |
| `input.image` | string | 单图生 3D 时必填 | 公网 HTTP/HTTPS URL，JPEG/PNG，20–6000px，≤20MB |
| `input.images` | array[object] | 多图生 3D 时必填 | 长度为 4 的数组，每项含 `type`（`jpeg`/`png`）和 `file_token`（URL） |
| `parameters.texture_quality` | string | 可选 | `standard`（默认）或 `detailed`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | 可选 | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（150 万面）或 `ultra`（200 万面） |
| `parameters.pbr` | boolean | 可选 | 默认 `true`；设为 `false` 时需同步设 `texture: false` 才返回 `base_model_url` |
| `parameters.texture` | boolean | 可选 | 默认 `true`；与 `pbr` 联动控制贴图生成 |

## 使用方式

1. **开通与配置**：  
   在 [百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索并开通 Tripo 模型服务；配置地域匹配的 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 至环境变量（如 `DASHSCOPE_API_KEY`）。

2. **创建异步任务**（POST）：  
   请求 URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   **必需请求头**：  
   - `Content-Type: application/json`  
   - `Authorization: Bearer $DASHSCOPE_API_KEY`  
   - `X-DashScope-Async: enable`（**不可省略**，否则报错 `current user api does not support synchronous calls`）  

   成功响应返回 `task_id`（有效期 24 小时），用于后续轮询。

3. **轮询查询结果**（GET）：  
   请求 URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   建议轮询间隔 ≥15 秒；状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`；超时（24h）返回 `UNKNOWN`。  
   成功响应中，`output.results` 包含 `pbr_model_url`（默认）、`base_model_url`（无贴图时）或 `rendered_image_url`。所有 URL 有效期均为 **2 小时**，需及时下载。

详细调用示例（含文生、单图、多图、无贴图等场景）见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须在此地域下生成。
- **输入互斥性**：`input.prompt`、`input.image`、`input.images` 三者**严格互斥**，同时传入多个将导致 `InvalidParameter` 错误。
- **多图格式要求**：`input.images` 数组长度必须为 4；缺失视角必须用 `{}` 占位，不可省略或缩短数组。
- **资源时效性**：`task_id` 有效期 24 小时；模型/图片下载 URL 有效期 2 小时；过期后需重新提交任务。
- **RPS 限制**：任务查询接口默认限流 20 QPS；高频轮询建议改用 [异步回调](https://help.aliyun.com/zh/model-studio/async-task-api) 机制。
- **错误处理**：所有失败响应均含 `code` 和 `message` 字段，应结合 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 排查；常见错误包括 `InvalidApiKey`、`InvalidParameter`、`UNKNOWN`（task_id 过期）等。

更多操作（如批量查询、取消任务）请参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“管理异步任务”相关指引。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


