# 3d generation

百炼平台的 3d generation 能力基于 Tripo 模型提供文生3D、单图生3D 和多图生3D 三种生成模式，支持带贴图（PBR）与无贴图两种输出形式。所有调用均为异步任务，需通过 `task_id` 轮询获取结果，且**仅限华北2（北京）地域可用**。开发者需提前开通服务并配置对应地域的 API Key。

## 支持的模型/功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级生成，最高 2 万面，推理更快；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入方式（互斥）**：
  - 文生3D：通过 `input.prompt` 指定中文或英文提示词（≤1024 字符）；
  - 单图生3D：通过 `input.image` 传入单张 JPEG/PNG 公网 URL（分辨率 [20, 6000] 像素，≤20MB）；
  - 多图生3D：通过 `input.images` 传入长度为 4 的数组，顺序固定为【前、左、后、右】，空视角用 `{}` 占位（实际有效图数 2–4 张）。
- **输出类型**：
  - 默认返回 PBR 材质模型（`pbr_model_url`，GLB 格式）及预览图（`rendered_image_url`）；
  - 无贴图模型需**同时设置 `"texture": false` 和 `"pbr": false`**，此时返回 `base_model_url`。

> **注意**：原始文档中 `multi-image-to-3d` 示例代码里 `images` 数组元素使用了 `"file_token"` 字段名，但请求体定义中明确要求字段名为 `"file_token"` —— 实际调用以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的示例为准，该字段名正确，无需修改。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `model` | string | 是 | 必须为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / string / array | 条件必填 | 三者互斥，仅可选其一 |
| `parameters.texture_quality` | string | 否 | `"standard"`（默认）或 `"detailed"`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `false` 时将强制禁用贴图（需同步设 `texture: false`） |
| `parameters.texture` | boolean | 否 | 默认 `true`；设为 `false` 且 `pbr: false` 时输出无贴图模型 |

详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“请求体（Request Body）”章节的完整定义。

## 使用方式

1. **前置准备**：
   - 在[百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索并开通 “Tripo” 模型；
   - 获取并配置北京地域专用的 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)，确保环境变量 `DASHSCOPE_API_KEY` 已设置。

2. **创建异步任务**（POST）：
   - Endpoint（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - **必需请求头**：`Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`
   - 成功响应含 `task_id`（有效期 24 小时），**禁止重复提交相同请求**。

3. **轮询查询结果**（GET）：
   - Endpoint（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 建议轮询间隔 ≥15 秒；RPS 限制为 20；超时（24h）后状态返回 `UNKNOWN`。
   - 成功时 `output.results` 包含 `pbr_model_url`（或 `base_model_url`）和 `rendered_image_url`，链接有效期 2 小时，需及时下载。

完整调用流程与各模式示例见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须为该地域生成。
- **异步强制性**：`X-DashScope-Async: enable` 为必填请求头，缺失将报错 `current user api does not support synchronous calls`。
- **输入互斥**：`prompt`、`image`、`images` 不可共存，否则返回 `InvalidParameter` 错误。
- **多图格式**：`images` 数组长度必须为 4，缺失视角必须用 `{}` 占位，不可省略或缩短数组。
- **资源时效性**：
  - `task_id` 查询有效期：24 小时；
  - 成果 URL（`pbr_model_url` 等）有效期：2 小时；
- **错误处理**：失败任务返回 `task_status: "FAILED"` 及 `code`/`message`，需结合 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 排查；常见错误如 `InvalidApiKey`、`InvalidParameter` 等均在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的“错误码”章节有说明。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


