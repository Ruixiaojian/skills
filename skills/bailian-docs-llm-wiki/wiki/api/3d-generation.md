# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型提供文生3D、单图生3D 和多图生3D 三种模式，支持带贴图/PBR 材质或无贴图的基础模型输出。该能力为异步任务，需通过 `task_id` 轮询获取结果，适用于华北2（北京）地域。详细实现细节请参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **支持模型**：
  - `Tripo/Tripo-P1.0`：专业版，最高输出 2 万面，速度快，适用于快速原型与轻量级应用。
  - `Tripo/Tripo-H3.1`：高精度版，最高输出 200 万面，支持 `geometry_quality: "ultra"`，适用于对几何精度要求高的场景。
- **输入方式（互斥）**：
  - 文生3D：通过 `input.prompt` 输入文本描述（最大 1024 字符）。
  - 单图生3D：通过 `input.image` 提供单张 JPEG/PNG 图像（分辨率 20–6000px，≤20MB）。
  - 多图生3D：通过 `input.images` 提供长度为 4 的数组，按「前、左、后、右」顺序排列；缺失视角用 `{}` 占位，实际有效图数需 ≥2。
- **输出类型**：
  - 默认返回 PBR 材质模型（`pbr_model_url`，GLB 格式）及预览图（`rendered_image_url`）。
  - 无贴图模型需显式设置 `"texture": false, "pbr": false`，此时返回 `base_model_url`。
- 全部功能均在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中定义并验证。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✓ | 固定为 `Tripo/Tripo-P1.0` 或 `Tripo/Tripo-H3.1` |
| `input.prompt` / `input.image` / `input.images` | string / object / array | ✓（三选一） | 仅允许一种输入方式，同时传入将报错 |
| `parameters.texture_quality` | string | ✗ | `"standard"`（默认）或 `"detailed"`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | ✗ | 仅 `Tripo/Tripo-H3.1` 支持；`"standard"`（≤150万面）或 `"ultra"`（≤200万面） |
| `parameters.pbr` | boolean | ✗ | 默认 `true`；设为 `false` 时需同步设 `texture: false` 才能获得无贴图模型 |
| `parameters.texture` | boolean | ✗ | 默认 `true`；与 `pbr` 联动，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |

> **注意**：`pbr` 和 `texture` 的组合逻辑存在隐式依赖——当 `pbr=true` 时，系统强制启用贴图（即忽略 `texture=false`）。因此，**唯一生成无贴图模型的方式是同时设置 `"texture": false, "pbr": false`**。

## 使用方式

1. **开通与配置**  
   - 在[百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)搜索并开通 Tripo 模型。  
   - 配置环境变量 `DASHSCOPE_API_KEY`，确保使用北京地域的 API Key（参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)）。

2. **创建异步任务**  
   - `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   - 请求头必须包含：  
     - `Content-Type: application/json`  
     - `Authorization: Bearer $DASHSCOPE_API_KEY`  
     - `X-DashScope-Async: enable`（**缺失将报错**）  
   - 响应中提取 `task_id`（有效期 24 小时）。

3. **轮询查询结果**  
   - `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - 建议间隔 ≥15 秒轮询，状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`。  
   - 成功响应中 `output.results[0]` 包含 `pbr_model_url` 或 `base_model_url`（链接有效期 2 小时，需及时下载）。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域，其他地域 URL 不可用。
- **异步强制性**：所有调用必须启用 `X-DashScope-Async: enable`，不支持同步模式。
- **task_id 生命周期**：创建后 24 小时内有效，超时查询返回 `task_status: "UNKNOWN"`。
- **RPS 限制**：任务查询接口默认限流 20 QPS；高频轮询建议配置[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
- **图像约束**：单图/多图输入均要求公网可访问 URL（HTTP/HTTPS），格式为 JPEG/PNG，单图 ≤20MB，多图各图独立校验。
- **错误处理**：失败任务返回 `code` 和 `message`，需结合[统一错误码文档](https://help.aliyun.com/zh/model-studio/error-code)定位原因。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


