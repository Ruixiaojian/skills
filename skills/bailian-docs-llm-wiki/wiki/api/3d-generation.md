# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型，支持文生 3D、单图生 3D 和多图生 3D 三种输入模式，输出带 PBR 材质或无贴图的 GLB 格式模型及预览渲染图。该能力为异步任务，需通过 `task_id` 轮询获取结果，**仅在华北2（北京）地域可用**。详细接口规范与行为约束请参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，最高支持 200 万面，对应 Tripo 官方 API 版本 `v3.1-20260211`；
  - `Tripo/Tripo-P1.0`：专业级快速生成，最高 2 万面，对应版本 `P1-20260311`。
- **输入模式**（三者互斥）：
  - 文生 3D：通过 `prompt` 字段传入文本描述；
  - 单图生 3D：通过 `image` 字段传入单张公网 URL 图像；
  - 多图生 3D：通过 `images` 数组传入 4 张按「前、左、后、右」顺序排列的图像（空视角用 `{}` 占位），实际有效图数为 2–4 张。
- **输出类型**：
  - 默认返回 `pbr_model_url`（带 PBR 材质的 GLB）；
  - 若显式设置 `"texture": false, "pbr": false`，则返回 `base_model_url`（无贴图基础模型）；
  - 始终返回 `rendered_image_url`（单张预览图）。

> **注意**：文档中 `images` 数组长度固定为 4，但示例中存在传入 2 张图 + 2 个 `{}` 的写法，与“实际有效图数为 2~4 张”的说明一致；而部分旧文档曾误述为“必须填满 4 张”，此表述已过时，请以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的当前定义为准。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `model` | string | 必填 | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / string / array | 条件必填 | 三者仅选其一；`images` 数组长度恒为 4，空视角用 `{}` |
| `parameters.texture_quality` | string | 可选 | `standard`（默认）或 `detailed`；仅对带贴图输出生效 |
| `parameters.geometry_quality` | string | 可选 | 仅 `Tripo/Tripo-H3.1` 支持；`standard`（≤150 万面）或 `ultra`（≤200 万面） |
| `parameters.pbr` | boolean | 可选 | 默认 `true`；设为 `false` 时需同步设 `texture: false` 才能获得无贴图模型 |
| `parameters.texture` | boolean | 可选 | 默认 `true`；与 `pbr` 联动，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |

## 使用方式

1. **前置准备**：
   - 在[百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)开通 Tripo 服务；
   - 配置环境变量 `DASHSCOPE_API_KEY`（仅限北京地域 API Key）。

2. **创建任务**（POST）：
   - Endpoint：`https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - 请求头必须包含：`Content-Type: application/json`、`Authorization: Bearer <key>`、`X-DashScope-Async: enable`
   - 成功响应含 `task_id`（有效期 24 小时），**禁止重复提交相同任务**。

3. **轮询结果**（GET）：
   - Endpoint：`https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`
   - 建议间隔 ≥15 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；
   - `SUCCEEDED` 时 `output.results` 返回 `pbr_model_url`、`base_model_url`（按参数配置）和 `rendered_image_url`，所有 URL 有效期均为 2 小时。

## 限制和注意事项

- **地域限制**：API 仅支持华北2（北京）地域，跨地域调用将失败；
- **输入限制**：
  - `prompt` 最长 1024 字符；
  - 单图 `image` 或 `images[i].file_token` 必须为公网可访问的 HTTP/HTTPS URL，格式为 JPEG/PNG，分辨率 [20, 6000] 像素，单文件 ≤20MB；
- **任务生命周期**：
  - `task_id` 有效期严格为 24 小时，超时后查询返回 `task_status: UNKNOWN`；
  - 成功结果中的 URL（如 `pbr_model_url`）有效期仅 2 小时，需及时下载；
- **错误处理**：
  - 缺少 `X-DashScope-Async: enable` 头将报错 `current user api does not support synchronous calls`；
  - 错误码详情见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中引用的错误码文档。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


