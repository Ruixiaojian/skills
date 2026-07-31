# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果，且**仅限华北2（北京）地域可用**。调用前需在百炼控制台开通 Tripo 服务并配置对应地域的 API Key。

## 支持的模型与功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
  
- **核心功能**：
  - 文生 3D（`prompt` 输入）
  - 单图生 3D（`image` 输入）
  - 多图生 3D（`images` 数组输入，固定长度为 4，顺序为前/左/后/右；空视角用 `{}` 占位）
  - 可选生成带 PBR 材质的 GLB（`pbr: true`，默认启用）、标准贴图（`texture_quality: "standard"` 或 `"detailed"`）或无贴图基础模型（需同时设置 `texture: false` 与 `pbr: false`）

详细参数与行为说明见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | 条件必填 | 文生 3D 时使用，≤1024 字符，支持中英文 |
| `input.image` | string | 条件必填 | 单图 URL，格式为 JPEG/PNG，宽高 ∈ [20, 6000] px，≤20 MB |
| `input.images` | array[object] | 条件必填 | 长度恒为 4 的数组，每项含 `type`（`jpeg`/`png`）和 `file_token`（公网 URL）；缺失视角填 `{}` |
| `parameters.texture_quality` | string | ❌ | `"standard"`（默认）或 `"detailed"`，仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | ❌ | 仅 `Tripo/Tripo-H3.1` 支持，`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | ❌ | 默认 `true`；设为 `false` 时需同步设 `texture: false` 才能生成无贴图模型 |
| `parameters.texture` | boolean | ❌ | 默认 `true`；与 `pbr` 联动，二者同为 `false` 时返回 `base_model_url` |

> **注意**：`input` 中 `prompt`、`image`、`images` 三者**互斥**，同时传入将报错；该约束在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确要求。

## 使用方式

1. **开通与配置**  
   在 [百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索 “Tripo” 并开通服务；获取并配置该地域专属的 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

2. **创建任务（POST）**  
   请求地址（北京地域）：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   **必需请求头**：  
   - `Content-Type: application/json`  
   - `Authorization: Bearer $DASHSCOPE_API_KEY`  
   - `X-DashScope-Async: enable`（缺此头将报错）  

   成功响应返回 `task_id`（有效期 24 小时），**禁止重复提交相同任务**。

3. **轮询查询结果（GET）**  
   请求地址：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   建议轮询间隔 ≥15 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；超时（24h）返回 `task_status: "UNKNOWN"`。  
   成功时 `output.results` 包含 `pbr_model_url`（PBR GLB）、`rendered_image_url`（预览图）或 `base_model_url`（无贴图 GLB）。所有 URL 有效期均为 **2 小时**，需及时下载。

完整调用示例与错误处理详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须与该地域绑定。
- **异步强制性**：不支持同步调用；`X-DashScope-Async: enable` 为硬性要求。
- **输入校验**：
  - `images` 数组长度必须为 4，即使部分视角为空（`{}`）；
  - 图像 URL 必须可公开访问（HTTP/HTTPS），CDN 或 OSS 直链均可，但内网地址无效。
- **资源时效性**：
  - `task_id` 有效期：24 小时；
  - 结果 URL（`pbr_model_url` 等）有效期：2 小时；
  - 查询接口 RPS 限制为 20，高频轮询建议改用 [异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
- **模型面数限制**：`Tripo/Tripo-P1.0` 最高输出 2 万面，`Tripo/Tripo-H3.1` 在 `ultra` 模式下可达 200 万面，超出将被截断。

> **注意**：文档中未提及 `Tripo/Tripo-H3.1` 对 `texture_quality` 的支持情况，但根据参数定义逻辑及实际行为，该参数对其有效；如有疑问，请以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 实际运行结果为准。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


