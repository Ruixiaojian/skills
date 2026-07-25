# 3d generation

3D generation 是百炼平台提供的异步3D模型生成能力，支持文本、单图及多图输入方式，输出 GLB 格式的 3D 模型（含 PBR 材质或无贴图版本）。该能力基于 Tripo 模型实现，当前仅在华北2（北京）地域可用，且必须配置对应地域的 API Key。完整调用流程为“创建任务 → 轮询查询结果”，不支持同步调用。

## 支持的模型/功能

- **支持的模型**：  
  - `Tripo/Tripo-H3.1`：高精度生成，最高支持 200 万面，支持 `geometry_quality: "ultra"`；  
  - `Tripo/Tripo-P1.0`：专业级生成，最高 2 万面，推理更快，适合对速度敏感的场景。  
  两模型均支持文生3D、单图生3D、多图生3D 三种输入模式，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

- **核心功能**：  
  - 文生3D（`prompt` 输入）  
  - 单图生3D（`image` 输入，需公网可访问 URL）  
  - 多图生3D（`images` 数组，固定长度为4，顺序为前/左/后/右；空视角用 `{}` 占位）  
  - 可选输出：带 PBR 材质的 GLB（默认）、无贴图基础模型（需显式设置 `"texture": false, "pbr": false`）  

> **注意**：文档中明确要求 `images` 数组长度必须为 4，但示例中传入 2 张图时仍使用 `[img1, {}, img3, {}]` 形式——这与“实际有效图片数量为 2~4 张”的说明一致，**非 bug，而是设计约束**。请严格按此格式构造请求体，否则将返回 `InvalidParameter` 错误。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | 条件必填（仅文生3D） | 最长 1024 字符，支持中英文；[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确限定为字符计数（含汉字） |
| `input.image` | string | 条件必填（仅单图） | 公网 HTTP/HTTPS URL；格式 JPEG/PNG；宽高 ∈ [20, 6000] px；≤20 MB |
| `input.images` | array[object] | 条件必填（仅多图） | 长度恒为 4；每项含 `type`（`jpeg`/`png`）和 `file_token`（URL）；无效项填 `{}` |
| `parameters.texture_quality` | string | ❌ | 可选值：`"standard"`（默认）、`"detailed"`；仅对 `pbr: true` 生效 |
| `parameters.geometry_quality` | string | ❌ | 仅 `Tripo/Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | ❌ | 默认 `true`；设为 `false` 时需同时设 `texture: false` 才能获得无贴图模型 |
| `parameters.texture` | boolean | ❌ | 默认 `true`；与 `pbr` 联动，二者同为 `false` 时返回 `base_model_url` |

所有请求**必须**携带 `X-DashScope-Async: enable` 请求头，否则报错 `current user api does not support synchronous calls` —— 此限制在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的“重要”提示中已强调。

## 使用方式

1. **前置准备**  
   - 在华北2（北京）地域开通 Tripo 模型服务：前往 [百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索 “Tripo” 并开通；  
   - 获取并配置该地域的 API Key 到环境变量 `DASHSCOPE_API_KEY`（参见 [配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）。

2. **创建任务（POST）**  
   - Endpoint（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   - 必须 Header：`Content-Type: application/json`, `Authorization: Bearer $DASHSCOPE_API_KEY`, `X-DashScope-Async: enable`  
   - Body 示例（文生3D）：
     ```json
     {
       "model": "Tripo/Tripo-P1.0",
       "input": { "prompt": "一只可爱的猫" },
       "parameters": { "texture_quality": "standard" }
     }
     ```
   - 成功响应含 `task_id`（有效期 24 小时），**禁止重复提交相同任务**。

3. **轮询查询结果（GET）**  
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - 建议轮询间隔 ≥15 秒；RPS 限制为 20；超时（24h）返回 `task_status: "UNKNOWN"`；  
   - 成功时 `output.results` 包含 `pbr_model_url`（PBR GLB）、`rendered_image_url`（预览图）或 `base_model_url`（无贴图 GLB）。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须为该地域生成。  
- **异步强制性**：所有调用必须启用 `X-DashScope-Async: enable`，同步调用直接拒绝。  
- **输入互斥**：`prompt` / `image` / `images` 三者**只能且必须指定其一**，混合传入将返回 `InvalidParameter`。  
- **多图格式刚性**：`images` 数组长度必须为 4，即使只提供 2 张图也需补 `{}` 占位，否则报错。  
- **资源时效性**：`task_id` 有效期 24 小时；生成结果 URL（如 `pbr_model_url`）有效期仅 2 小时，需及时下载。  
- **错误处理**：失败时 `output.code` 和 `output.message` 提供具体原因，应结合 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 排查；常见错误包括 `InvalidApiKey`、`InvalidParameter`、`ResourceNotFound` 等。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


