# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型提供文生 3D、单图生 3D 和多图生 3D 三种模式，支持带贴图（PBR/Standard/Detailed）和无贴图两种输出形式。所有调用均为异步任务，需通过 `task_id` 轮询获取结果，且**仅限华北2（北京）地域可用**。详细接口规范与行为约束请参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型与功能

- **支持模型**：
  - `Tripo/Tripo-P1.0`：专业版，最高 2 万面，生成速度快；
  - `Tripo/Tripo-H3.1`：高精度版，最高 200 万面，支持 `geometry_quality: ultra`（仅该模型可用）。
- **输入方式（三者互斥）**：
  - 文生 3D：通过 `input.prompt` 提供文本描述；
  - 单图生 3D：通过 `input.image` 提供单张 JPEG/PNG 图像 URL；
  - 多图生 3D：通过 `input.images` 提供长度为 4 的数组，按「前、左、后、右」顺序排列，空视角用 `{}` 占位。
- **输出类型**：
  - 默认返回 PBR 材质模型（`pbr_model_url`）及渲染图（`rendered_image_url`）；
  - 无贴图模型需显式设置 `"texture": false, "pbr": false`，此时返回 `base_model_url`。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求 `X-DashScope-Async: enable` 请求头，缺失将直接报错“current user api does not support synchronous calls”；同步调用在当前版本**完全不支持**，此限制未在其他文档中被覆盖或弱化。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✓ | 固定为 `Tripo/Tripo-P1.0` 或 `Tripo/Tripo-H3.1` |
| `input.prompt` / `input.image` / `input.images` | string / object / array | ✓（三选一） | 输入内容，详见上节；`images` 数组长度必须为 4 |
| `parameters.texture_quality` | string | ✗ | 可选值：`standard`（默认）、`detailed`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | ✗ | 仅 `Tripo-H3.1` 支持，可选 `standard`（≤150 万面）或 `ultra`（≤200 万面） |
| `parameters.pbr` | boolean | ✗ | 默认 `true`；设为 `false` 时需同时设 `texture: false` 才能获得无贴图模型 |
| `parameters.texture` | boolean | ✗ | 默认 `true`；与 `pbr` 联动，单独设 `false` 无效 |

图像输入限制（适用于 `image` 和 `images` 中每个元素）：
- 格式：JPEG/PNG；
- 分辨率：宽高均 ∈ [20, 6000] 像素，建议 ≥256px；
- 文件大小：≤20 MB；
- URL 协议：仅支持公网 HTTP/HTTPS。

## 使用方式

1. **开通与配置**：  
   在[百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)搜索并开通 Tripo 模型；配置 `DASHSCOPE_API_KEY` 环境变量（参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的配置指引）。

2. **创建任务（POST）**：  
   请求 URL（北京地域）：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   必须携带请求头：`Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`。  
   成功响应含 `task_id`（有效期 24 小时），**禁止重复提交相同任务**。

3. **轮询结果（GET）**：  
   请求 URL：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   建议间隔 ≥15 秒轮询；状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`；超时（24h）返回 `task_status: UNKNOWN`。  
   成功时 `output.results` 包含 `pbr_model_url`（或 `base_model_url`）和 `rendered_image_url`，**所有 URL 有效期仅 2 小时，需及时下载**。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须在此地域下生成 —— 此限制在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中被多次强调，无例外说明。
- **异步强制性**：所有 3D 生成请求必须启用异步（`X-DashScope-Async: enable`），同步调用不可用。
- **输入互斥性**：`prompt`、`image`、`images` 三者不可共存，否则返回 `InvalidParameter` 错误。
- **多图格式刚性**：`input.images` 必须为长度 4 的数组，即使只传 2 张图，也需补 `{}` 占位，顺序不可乱。
- **资源时效性**：`task_id` 有效期 24 小时；结果 URL（`pbr_model_url` 等）有效期 2 小时；过期后需重新提交任务。
- **RPS 限制**：任务查询接口默认限流 20 RPS，高频轮询建议改用[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


