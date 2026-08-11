# 3d generation

3D generation 是百炼平台提供的异步3D模型生成能力，支持文本、单图、多图三种输入方式生成带贴图或无贴图的GLB格式3D模型。该能力基于 Tripo 模型实现，需在华北2（北京）地域调用，且必须配置对应地域的 API Key。整个流程采用“创建任务 → 轮询查询”两阶段模式，不支持同步调用。

## 支持的模型/功能

- **支持模型**：`Tripo/Tripo-P1.0`（专业版，最高2万面，速度快）和 `Tripo/Tripo-H3.1`（高精度版，最高200万面）。详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
- **输入方式**：
  - 文生3D（`prompt` 字段）
  - 单图生3D（`image` 字段，公网 JPEG/PNG URL）
  - 多图生3D（`images` 字段，固定长度为4的数组，顺序为前/左/后/右；空视角用 `{}` 占位）
- **输出类型**：
  - 默认返回 PBR 材质模型（`pbr_model_url`，含贴图与物理渲染属性）
  - 可通过设置 `"texture": false, "pbr": false` 获取无贴图基础模型（`base_model_url`）
  - 同时返回预览渲染图（`rendered_image_url`）

> **注意**：文档中明确要求 `input` 中 `prompt`、`image`、`images` 三者互斥，但部分旧示例未严格校验——实际调用时若同时传入多个将直接报错 `InvalidParameter`，请严格遵循 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的参数约束。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-P1.0` 或 `Tripo/Tripo-H3.1` |
| `input.prompt` | string | ⚠️（文生3D必填） | 最长1024字符，支持中英文；仅文生3D场景使用 |
| `input.image` | string | ⚠️（单图生3D必填） | 公网 JPEG/PNG URL；宽高 ∈ [20, 6000] px，≤20MB |
| `input.images` | array[object] | ⚠️（多图生3D必填） | 长度恒为4；每项含 `type`（`jpeg`/`png`）和 `file_token`（URL）；无效项填 `{}` |
| `parameters.texture_quality` | string | ❌（默认 `standard`） | 可选 `standard` / `detailed`；仅对 `pbr: true` 有效 |
| `parameters.geometry_quality` | string | ❌（仅 `Tripo/Tripo-H3.1` 支持） | 可选 `standard`（≤150万面） / `ultra`（≤200万面） |
| `parameters.pbr` | boolean | ❌（默认 `true`） | 设为 `false` 时需同时设 `texture: false` 才能获得无贴图模型 |
| `parameters.texture` | boolean | ❌（默认 `true`） | 控制是否生成贴图；与 `pbr` 联动，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |

## 使用方式

1. **开通与配置**  
   在百炼控制台（华北2地域）搜索并开通 Tripo 模型服务，获取该地域专属 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`。

2. **创建任务（POST）**  
   请求地址（北京地域）：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   **必需请求头**：  
   - `Content-Type: application/json`  
   - `Authorization: Bearer $DASHSCOPE_API_KEY`  
   - `X-DashScope-Async: enable`（缺失将报错 `current user api does not support synchronous calls`）

3. **轮询结果（GET）**  
   使用上一步返回的 `task_id` 查询：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - 建议轮询间隔 ≥15 秒  
   - `task_id` 有效期 24 小时  
   - 成功响应中 `output.results` 包含 `pbr_model_url` 或 `base_model_url`（链接有效期 2 小时，需及时下载）

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须与该地域绑定。
- **异步强制性**：所有调用必须启用 `X-DashScope-Async: enable`，同步调用会被拒绝。
- **输入互斥性**：`prompt` / `image` / `images` 三者不可共存，否则返回 `InvalidParameter` 错误。
- **图片规范**：单图/多图均要求公网可访问 URL；多图 `images` 数组长度必须为 4，缺失视角需显式填 `{}`。
- **资源时效性**：`task_id` 24 小时后失效；生成结果 URL（如 `pbr_model_url`）2 小时后过期，需及时持久化存储。
- **错误处理**：失败任务返回 `task_status: FAILED` 及 `code`/`message`，应依据 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 定位问题，而非重试无效请求。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


