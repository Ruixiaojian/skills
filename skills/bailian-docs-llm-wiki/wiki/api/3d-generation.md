# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型，支持文生 3D、单图生 3D 和多图生 3D 三种输入模式，输出带 PBR 材质或无贴图的 GLB 格式模型及预览渲染图。该服务为异步 API，需通过任务 ID 轮询获取结果，仅在华北2（北京）地域可用。

## 支持的模型与功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，最高支持 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级生成，最高 2 万面，推理更快；对应 Tripo 官方 API 版本 `P1-20260311`。
  
- **输入模式**（三者互斥）：
  - 文生 3D：通过 `input.prompt` 描述目标模型（最大 1024 字符）；
  - 单图生 3D：通过 `input.image` 提供单张 JPEG/PNG 图像（分辨率 20–6000px，≤20MB）；
  - 多图生 3D：通过 `input.images` 提供长度为 4 的数组，顺序为前、左、后、右；缺失视角需填 `{}`，有效图数须 ≥2。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求 `images` 数组长度必须为 4，但示例中传入 2 张图 + 2 个 `{}` 的用法易被误读为“可变长”。实际必须严格传入 4 项，否则返回 `InvalidParameter` 错误。

## 关键参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `texture_quality` | string | 贴图质量，影响外观细节 | `"standard"`（标清）；可选 `"detailed"` |
| `geometry_quality` | string | 仅 `Tripo/Tripo-H3.1` 支持；控制面数上限 | `"standard"`（≤150 万面）；可选 `"ultra"`（≤200 万面） |
| `pbr` | boolean | 是否启用 PBR 材质（含法线、粗糙度等贴图） | `true`；设为 `false` 时需同步设 `texture: false` |
| `texture` | boolean | 是否生成基础贴图（Albedo） | `true`；禁用需同时设 `pbr: false` |

- **无贴图模型**：必须同时设置 `"texture": false, "pbr": false`，此时响应返回 `base_model_url`（GLB）而非 `pbr_model_url`。
- **图像 URL 要求**：公网可访问，支持 HTTP/HTTPS；`file_token` 字段名在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确为必需字段，不可省略。

## 使用方式

1. **开通与配置**：  
   - 在 [百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索并开通 “Tripo” 模型；  
   - 获取并配置 `DASHSCOPE_API_KEY` 环境变量（参见 [API Key 配置指南](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）。

2. **异步调用流程**：  
   - **步骤1（创建任务）**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`，必须携带请求头 `X-DashScope-Async: enable`，否则报错 `current user api does not support synchronous calls`；  
   - **步骤2（轮询结果）**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`，建议间隔 ≥15 秒；`task_id` 有效期为 24 小时。

3. **结果解析**：  
   - 成功时 `output.results[0]` 包含 `pbr_model_url`（PBR 模型）、`rendered_image_url`（预览图）；  
   - 无贴图时返回 `base_model_url`；所有 URL 有效期均为 2 小时，需及时下载。

详细请求体结构与示例见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域，其他地域调用将失败。
- **RPS 限制**：任务查询接口默认限流 20 RPS；高频轮询建议配置 [异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
- **任务生命周期**：`task_id` 24 小时后失效，查询返回 `task_status: "UNKNOWN"`。
- **输入校验**：`prompt`、`image`、`images` 三者严格互斥；`images` 数组长度必须为 4，空视角用 `{}` 占位。
- **错误处理**：失败时 `output.code` 和 `output.message` 提供具体原因，应结合 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 排查。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


