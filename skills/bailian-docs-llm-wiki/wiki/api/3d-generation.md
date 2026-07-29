# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式，输出 GLB 格式模型（含 PBR 材质或无贴图基础模型）及预览渲染图。所有调用均为[异步任务](../concepts/asynchronous-task.md)，需通过 `task_id` 轮询获取结果，且**仅限华北2（北京）地域可用**。开发者需提前开通服务并配置对应地域的 API Key。

## 支持的模型/功能

- **模型标识**：
  - `Tripo/Tripo-H3.1`：高精度生成，最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级生成，最高 2 万面，推理更快；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式（三者互斥）**：
  - 文生3D：通过 `input.prompt` 输入文本描述（≤1024 字符，支持中英文）；
  - 单图生3D：通过 `input.image` 传入单张公网 JPEG/PNG 图像（分辨率 [20, 6000] 像素，≤20MB）；
  - 多图生3D：通过 `input.images` 传入长度为 4 的数组，顺序固定为「前、左、后、右」；缺失视角需填空对象 `{}`；实际有效图数为 2–4 张。
- **输出类型**：
  - 默认返回带 PBR 材质的 GLB 模型（`pbr_model_url`）和预览图（`rendered_image_url`）；
  - 可通过设置 `"texture": false, "pbr": false` 获取无贴图基础模型（`base_model_url`），详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / object / array | ✅（三选一） | 仅允许一种输入方式；`images` 数组长度必须为 4，含空对象占位 |
| `parameters.texture_quality` | string | ❌ | `"standard"`（默认）或 `"detailed"`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | ❌ | 仅 `Tripo/Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | ❌ | 默认 `true`；设为 `false` 时将强制禁用贴图（需同时设 `texture: false`） |
| `parameters.texture` | boolean | ❌ | 默认 `true`；与 `pbr` 联动，二者同为 `false` 才返回 `base_model_url` |

> **注意**：原始文档中 `parameters.texture` 和 `parameters.pbr` 的联动逻辑明确要求“需同时设为 `false`”才生成无贴图模型，该规则在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中多次强调，务必遵守。

## 使用方式

1. **开通与认证**：
   - 在[百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索 “Tripo” 并开通服务；
   - 获取并配置该地域的 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)，确保环境变量 `DASHSCOPE_API_KEY` 已设置。

2. **创建任务（POST）**：
   - Endpoint（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - **必需请求头**：`Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`
   - 请求体示例（文生3D）：
     ```json
     {
       "model": "Tripo/Tripo-P1.0",
       "input": { "prompt": "一只可爱的猫" },
       "parameters": { "texture_quality": "standard" }
     }
     ```
   - 成功响应返回 `task_id`（有效期 24 小时），请妥善保存。

3. **轮询查询结果（GET）**：
   - Endpoint（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 仅需 `Authorization` 请求头；
   - 建议轮询间隔 ≥15 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；
   - 成功时 `output.results` 包含 `pbr_model_url`（或 `base_model_url`）、`rendered_image_url`，**所有 URL 有效期仅 2 小时**，需及时下载。

详细调用流程与错误处理可参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的完整示例与错误码说明。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 或 API Key 均不可用；
- **异步强制性**：`X-DashScope-Async: enable` 为必填请求头，缺失将报错 `current user api does not support synchronous calls`；
- **输入互斥性**：`prompt`、`image`、`images` 三者不可共存，否则返回 `InvalidParameter`；
- **多图格式要求**：`input.images` 必须为长度 4 的数组，顺序固定为「前、左、后、右」；传入非空对象时 `type` 必须为 `"jpeg"` 或 `"png"`，`file_token` 必须为公网可访问 HTTPS/HTTP URL；
- **资源时效性**：
  - `task_id` 查询有效期：24 小时；
  - 模型/渲染图下载 URL 有效期：2 小时；
- **RPS 限制**：任务查询接口默认 RPS 为 20，高频轮询建议配置[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)替代。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


