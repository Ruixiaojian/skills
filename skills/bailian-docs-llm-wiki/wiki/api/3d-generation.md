# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果，且**仅限华北2（北京）地域可用**。调用前需在百炼控制台开通 Tripo 服务并配置对应地域的 API Key。

## 支持的模型/功能

- **支持模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
  
- **输入模式**（三者互斥）：
  - 文生3D：通过 `input.prompt` 描述目标模型（最大 1024 字符，支持中英文）。
  - 单图生3D：通过 `input.image` 提供单张 JPEG/PNG 图像（分辨率 [20, 6000] 像素，≤20MB）。
  - 多图生3D：通过 `input.images` 提供长度为 4 的数组，顺序固定为【前、左、后、右】；空视角用 `{}` 占位，实际有效图数需 ≥2。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求 `images` 数组长度必须为 4，但示例中传入 2 张图时仍使用 4 元素数组（含 `{}`），开发者需严格遵守该结构，不可缩短数组长度。

## 关键参数

| 参数 | 类型 | 说明 | 默认值 | 备注 |
|------|------|------|--------|------|
| `texture_quality` | string | 贴图质量 | `"standard"` | 可选 `"standard"` / `"detailed"`；仅对带贴图任务生效 |
| `geometry_quality` | string | 几何精度 | `"standard"` | **仅 `Tripo/Tripo-H3.1` 支持**；`"ultra"` 输出最高 200 万面 |
| `pbr` | boolean | 是否启用 PBR 材质 | `true` | 设为 `true` 时强制启用贴图（即 `texture` 自动为 `true`），返回 `pbr_model_url` |
| `texture` | boolean | 是否生成贴图 | `true` | 如需无贴图模型，**必须同时设 `texture: false` 且 `pbr: false`**，返回 `base_model_url` |

详细参数定义与约束请参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的“请求体（Request Body）”章节。

## 使用方式

1. **开通与配置**：  
   在 [百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索 “Tripo”，开通服务；按 [API Key 配置指南](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables) 设置环境变量。

2. **[异步任务](../concepts/asynchronous-task.md)创建**（POST）：  
   请求 URL（北京地域）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   **必需请求头**：`Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`  
   成功响应返回 `task_id`（24 小时内有效），**禁止重复提交相同任务**。

3. **轮询查询结果**（GET）：  
   请求 URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   建议轮询间隔 ≥15 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；超时（24h）返回 `task_status: "UNKNOWN"`。  
   成功响应中：
   - `pbr_model_url`：PBR 材质 GLB 模型（`pbr: true` 时返回，链接有效期 2 小时）
   - `base_model_url`：无贴图基础 GLB 模型（`texture: false && pbr: false` 时返回）
   - `rendered_image_url`：预览渲染图（WebP 格式）

完整调用流程与各模式示例详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用，且 API Key 必须为该地域生成。
- **异步强制性**：所有请求必须携带 `X-DashScope-Async: enable`，否则报错 `current user api does not support synchronous calls`。
- **输入互斥性**：`prompt`、`image`、`images` 三者不可共存，同时传入将导致 `InvalidParameter` 错误。
- **多图格式**：`images` 数组长度必须为 4，缺失视角必须用 `{}` 占位；图像 URL 需为公网可访问的 HTTP/HTTPS 地址，格式为 `jpeg` 或 `png`。
- **资源时效性**：`task_id` 有效期 24 小时；生成结果 URL（`pbr_model_url` 等）有效期仅 2 小时，需及时下载。
- **错误处理**：失败响应中 `code` 和 `message` 字段指向统一 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)，调试时应优先查阅该文档。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


