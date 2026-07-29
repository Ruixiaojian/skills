# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种输入模式。所有任务均采用异步调用流程（创建任务 → 轮询结果），适用于华北2（北京）地域，需配置对应地域的 API Key。详细实现细节请参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型与功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式**（三者互斥）：
  - 文生 3D：通过 `input.prompt` 输入文本描述；
  - 单图生 3D：通过 `input.image` 提供单张公网可访问图像 URL；
  - 多图生 3D：通过 `input.images` 提供长度为 4 的数组，按「前、左、后、右」顺序排列，缺失视角可用空对象 `{}` 占位。
- **输出类型**：
  - 默认返回 PBR 材质模型（GLB，含贴图），URL 字段为 `pbr_model_url`；
  - 无贴图模型需显式设置 `"texture": false, "pbr": false`，返回 `base_model_url`；
  - 所有成功响应均附带 `rendered_image_url`（预览图，WebP 格式）。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求仅支持华北2（北京）地域，且必须使用该地域的 API Key；跨地域调用将失败，此限制未在其他文档中被覆盖或修订。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✓ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | 条件必填 | 文生 3D 时使用，≤1024 字符，支持中英文 |
| `input.image` | string | 条件必填 | 单图生 3D 时使用，JPEG/PNG，宽高 ∈ [20, 6000] px，≤20 MB |
| `input.images` | array[object] | 条件必填 | 多图生 3D 时使用，固定长度 4，每项含 `type`（jpeg/png）和 `file_token`（公网 URL） |
| `parameters.texture_quality` | string | ✗ | 可选：`"standard"`（默认）、`"detailed"` |
| `parameters.geometry_quality` | string | ✗ | 仅 `Tripo/Tripo-H3.1` 支持：`"standard"`（≤150 万面）、`"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | ✗ | 默认 `true`；设为 `false` 时需同时设 `texture: false` 才生成无贴图模型 |
| `parameters.texture` | boolean | ✗ | 默认 `true`；与 `pbr` 联动，共同控制贴图生成 |

## 使用方式

1. **开通与配置**  
   在 [百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索并开通 Tripo 模型；获取北京地域的 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)，并配置至环境变量 `DASHSCOPE_API_KEY`。

2. **发起[异步任务](../concepts/asynchronous-task.md)**  
   向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送请求，**必须包含**以下请求头：
   - `Content-Type: application/json`
   - `Authorization: Bearer $DASHSCOPE_API_KEY`
   - `X-DashScope-Async: enable`（缺则报错）

3. **轮询结果**  
   使用返回的 `task_id`，以 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态。建议间隔 ≥15 秒轮询；`task_id` 有效期为 24 小时。更多操作详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的“管理[异步任务](../concepts/asynchronous-task.md)”指引。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，URL、API Key、控制台入口均需匹配该地域；其他地域调用将失败。
- **异步强制性**：不支持同步调用，`X-DashScope-Async: enable` 为必需头，否则返回 `current user api does not support synchronous calls` 错误。
- **输入互斥性**：`prompt`、`image`、`images` 三者不可共存，同时传入将导致 `InvalidParameter` 错误。
- **多图格式要求**：`input.images` 数组长度必须为 4，即使部分视角为空也需保留位置（用 `{}` 占位）；实际有效图片数应为 2–4 张。
- **资源时效性**：`pbr_model_url`、`base_model_url`、`rendered_image_url` 均仅有效 2 小时，需及时下载；`task_id` 查询有效期为 24 小时，超时返回 `UNKNOWN` 状态。
- **RPS 限制**：任务查询接口默认限流 20 QPS；高频轮询或需事件驱动，请配置 [异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


