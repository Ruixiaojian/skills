# 3d generation

3D generation 是百炼平台提供的异步 3D 模型生成能力，支持文本、单图、多图三种输入方式，输出 GLB 格式的 3D 模型（含 PBR 材质或无贴图基础模型）。该能力基于 Tripo 模型实现，当前仅在华北2（北京）地域可用，且必须配置对应地域的 API Key。完整流程为“创建任务 → 轮询查询结果”，任务 ID 有效期为 24 小时。

## 支持的模型/功能

- **支持模型**：`Tripo/Tripo-P1.0`（专业版，最高 2 万面，速度快）和 `Tripo/Tripo-H3.1`（高精度版，最高 200 万面）。二者参数支持存在差异，详见 [原文标题](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
- **输入方式**（三者互斥）：
  - 文生3D：通过 `prompt` 字段传入中文/英文提示词（≤1024 字符）；
  - 单图生3D：通过 `image` 字段传入单张 JPEG/PNG 公网 URL（分辨率 20–6000px，≤20MB）；
  - 多图生3D：通过 `images` 数组传入 4 张图像（顺序为前/左/后/右），空视角用 `{}` 占位，实际有效图数为 2–4 张。
- **输出类型**：
  - 默认返回带 PBR 材质的 `pbr_model_url`（GLB）及预览图 `rendered_image_url`；
  - 无贴图模型需显式设置 `"texture": false, "pbr": false`，此时返回 `base_model_url`。

> **注意**：文档中 `images` 数组长度固定为 4 且顺序严格定义为“前、左、后、右”，但示例中传入 2 张图时未明确是否允许跳过中间索引（如 `[img1, {}, img3, {}]`）。请以 [原文标题](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“多图生3D模型（传入2张图）”小节为准，该写法是官方支持的合法形式。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `Tripo/Tripo-P1.0` 或 `Tripo/Tripo-H3.1` |
| `input.prompt` / `input.image` / `input.images` | string / string / array | 条件必填 | 三者仅选其一；`images` 数组长度必须为 4，每项含 `type`（`jpeg`/`png`）和 `file_token`（公网 URL） |
| `parameters.texture_quality` | string | 否 | 可选 `standard`（默认）、`detailed`；仅对 `Tripo/Tripo-P1.0` 和 `Tripo/Tripo-H3.1` 均生效 |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（≤150 万面）、`ultra`（≤200 万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `false` 时需同时设 `texture: false` 才能获得无贴图模型 |
| `parameters.texture` | boolean | 否 | 默认 `true`；与 `pbr` 联动，详见 [原文标题](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |

## 使用方式

1. **开通与配置**：在百炼控制台（华北2 北京地域）搜索并开通 Tripo 模型服务，[获取并配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 到环境变量。
2. **创建异步任务**（POST）：
   - URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - 请求头：`Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`（**必须**，否则报错）
   - 请求体：按输入类型构造 `input`，并可选配置 `parameters`
3. **轮询查询结果**（GET）：
   - URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 建议间隔 ≥15 秒；`task_id` 有效期 24 小时；成功响应中 `output.results` 包含 `pbr_model_url` 或 `base_model_url`（链接有效期 2 小时，需及时下载）

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，API Key 也必须为该地域生成。
- **异步强制性**：所有调用必须启用 `X-DashScope-Async: enable`，同步调用不被支持。
- **输入互斥性**：`prompt`、`image`、`images` 不能共存，否则返回 `InvalidParameter` 错误。
- **图片要求**：单图/多图均需公网可访问 URL，格式为 JPEG/PNG，单图大小 ≤20MB，分辨率边长 ∈ [20, 6000]。
- **任务管理**：任务状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`；`UNKNOWN` 状态表示 task_id 过期或不存在；RPS 查询上限为 20，高频轮询建议配置[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
- **资源时效性**：生成结果 URL（`pbr_model_url`/`base_model_url`/`rendered_image_url`）有效期仅 2 小时，务必及时下载保存。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


