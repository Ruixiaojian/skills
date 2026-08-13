# 3d generation

百炼平台的 3d generation 能力基于 Tripo 模型提供文生3D、单图生3D 和多图生3D 三种生成模式，支持带贴图（PBR）与无贴图两种输出形式。该能力为异步任务型 API，需通过“创建任务 → 轮询查询”两步完成，适用于华北2（北京）地域。所有调用均需配置对应地域的 API Key 并启用 `X-DashScope-Async: enable` 请求头。

## 支持的模型/功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
  
- **输入方式（三者互斥）**：
  - 文生3D：通过 `input.prompt` 指定中文或英文提示词（≤1024 字符）；
  - 单图生3D：通过 `input.image` 传入单张公网 JPEG/PNG 图像（20–6000 像素边长，≤20MB）；
  - 多图生3D：通过 `input.images` 传入长度为 4 的数组，按 `[前, 左, 后, 右]` 顺序填充，空视角用 `{}` 占位（实际有效图数为 2–4 张）。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求 `input` 中 `prompt`、`image`、`images` 三者仅能选其一，同时传入将直接报错；该约束在 SDK 封装中必须严格校验，避免静默忽略。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `texture_quality` | string | 贴图质量，仅对带贴图任务生效 | `"standard"`（可选 `"detailed"`） |
| `geometry_quality` | string | 仅 `Tripo/Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） | `"standard"` |
| `pbr` | boolean | 是否生成 PBR 材质模型；设为 `true` 时自动启用贴图 | `true` |
| `texture` | boolean | 是否生成贴图；设为 `false` 且 `pbr=false` 时返回无贴图模型（`base_model_url`） | `true` |

> **注意**：无贴图模型必须**同时设置 `texture: false` 和 `pbr: false`**，否则 `pbr=true` 会强制覆盖 `texture` 设置。详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“无贴图生成”示例。

## 使用方式

1. **前置准备**：
   - 在 [百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 开通 Tripo 模型服务；
   - 配置对应地域的 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 到环境变量（如 `DASHSCOPE_API_KEY`）。

2. **创建任务（POST）**：
   - Endpoint（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - 必须 Header：`Content-Type: application/json`、`Authorization: Bearer <key>`、`X-DashScope-Async: enable`
   - Body 示例（文生3D）：
     ```json
     {
       "model": "Tripo/Tripo-P1.0",
       "input": { "prompt": "一只可爱的猫" },
       "parameters": { "texture_quality": "standard" }
     }
     ```
   - 成功响应含 `task_id`（有效期 24 小时），**禁止重复提交相同请求**。

3. **轮询查询结果（GET）**：
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 建议轮询间隔 ≥15 秒；RPS 限制为 20，高频场景请配置 [异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
   - 成功响应中 `output.results` 包含：
     - `pbr_model_url`（GLB，含材质贴图，有效期 2 小时）；
     - `base_model_url`（GLB，无贴图，仅当 `texture=false && pbr=false` 时返回）；
     - `rendered_image_url`（预览图，WebP 格式）。

完整流程与各模式调用示例详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强绑定**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须为该地域颁发。
- **任务生命周期**：`task_id` 有效期严格为 24 小时，超时后查询返回 `task_status: "UNKNOWN"`，无法恢复。
- **图像规范**：单图/多图输入均要求公网可访问 HTTPS/HTTP URL；多图数组长度固定为 4，缺失视角必须显式填 `{}`，不可省略或缩短数组。
- **错误处理**：常见失败原因包括 `InvalidParameter`（如 `images` 数组长度≠4）、`InvalidApiKey`（Header 缺失或 Key 错误）、`Forbidden`（未开通服务）。详细错误码请参考官方 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


