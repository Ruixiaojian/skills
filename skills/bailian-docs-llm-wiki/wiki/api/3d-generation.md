# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果，且**仅限华北2（北京）地域可用**。调用前需在百炼控制台开通 Tripo 服务并配置对应地域的 API Key。

## 支持的模型/功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
  
- **输入模式**（三者互斥）：
  - 文生3D：通过 `input.prompt` 描述目标模型（最大 1024 字符，支持中英文）。
  - 单图生3D：通过 `input.image` 提供单张 JPEG/PNG 图像 URL（分辨率 20–6000px，≤20MB）。
  - 多图生3D：通过 `input.images` 提供长度为 4 的数组，按顺序对应**前、左、后、右**视角；缺失视角需填 `{}`，有效图片数须为 2–4 张。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求 `images` 数组长度固定为 4，但示例中传入 2 张图时仍使用 4 元素数组（含空对象），开发者需严格遵守该结构，不可缩短数组长度。

## 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input` | object | ✅ | 仅可含 `prompt` / `image` / `images` 之一 |
| `parameters.texture_quality` | string | ❌ | 可选值：`"standard"`（默认）、`"detailed"`；仅对带贴图任务生效 |
| `parameters.geometry_quality` | string | ❌ | 仅 `Tripo/Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | ❌ | 默认 `true`；设为 `false` 时需同时设 `texture: false` 才能生成无贴图模型 |
| `parameters.texture` | boolean | ❌ | 默认 `true`；与 `pbr` 联动，二者同为 `false` 时返回 `base_model_url` |

详细参数定义与约束请参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的“请求体（Request Body）”章节。

## 使用方式

1. **开通与配置**：  
   在 [百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索 “Tripo” 并开通服务；[获取并配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 到环境变量（如 `DASHSCOPE_API_KEY`）。

2. **创建任务（POST）**：  
   请求 URL（北京地域）：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   **必需请求头**：  
   - `Content-Type: application/json`  
   - `Authorization: Bearer $DASHSCOPE_API_KEY`  
   - `X-DashScope-Async: enable`（缺此头将报错）  

3. **轮询结果（GET）**：  
   使用上一步返回的 `task_id` 查询：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - 建议轮询间隔 ≥15 秒；  
   - `task_id` 有效期为 **24 小时**；  
   - 成功响应中 `output.results` 包含 `pbr_model_url`（PBR 材质 GLB）、`base_model_url`（无贴图 GLB）或 `rendered_image_url`（预览图），所有 URL 有效期 **2 小时**。

完整调用流程与各模式示例见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须为该地域生成。
- **异步强制性**：不支持同步调用；`X-DashScope-Async: enable` 为硬性要求。
- **输入互斥**：`prompt`、`image`、`images` 三者不可共存，否则返回 `InvalidParameter` 错误。
- **多图格式**：`images` 数组必须为长度 4，视角顺序固定为 `[前, 左, 后, 右]`；空视角必须显式填 `{}`，不可省略或缩短数组。
- **资源时效性**：`task_id` 24 小时后失效；生成结果 URL（如 `pbr_model_url`）2 小时后过期，需及时下载。
- **错误处理**：失败时 `output.task_status` 为 `FAILED`，并附带 `code` 和 `message`；常见错误码详见官方 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


