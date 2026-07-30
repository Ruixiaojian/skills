# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果，且**仅限华北2（北京）地域可用**。调用前需在百炼控制台开通 Tripo 服务并配置对应地域的 API Key。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **生成模式**（三者互斥）：
  - 文生 3D：通过 `input.prompt` 输入文本描述；
  - 单图生 3D：通过 `input.image` 提供单张公网可访问图像 URL；
  - 多图生 3D：通过 `input.images` 提供长度为 4 的数组，顺序固定为【前、左、后、右】，缺失视角填 `{}` 即可（实际有效图数需 ≥2）。
- **输出类型**：
  - 默认返回 PBR 材质模型（`pbr_model_url`，GLB 格式）及预览图（`rendered_image_url`）；
  - 可显式禁用贴图与 PBR（需同时设 `"texture": false, "pbr": false`），此时返回无贴图基础模型（`base_model_url`）。

> **注意**：原始文档中 `Tripo/Tripo-H3.1` 的 `geometry_quality` 参数仅对该模型生效，但 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中未明确标注其对 `Tripo-P1.0` 不可用——实际调用将被忽略，开发者应避免在 `P1.0` 请求中传入该参数。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | ⚠️（文生3D时必填） | 最长 1024 字符，支持中英文等多语言 |
| `input.image` | string | ⚠️（单图生3D时必填） | 公网 HTTP/HTTPS URL；格式 JPEG/PNG；宽高 ∈ [20, 6000]px；≤20MB |
| `input.images` | array[object] | ⚠️（多图生3D时必填） | 长度必须为 4；每项含 `type`（`jpeg`/`png`）和 `file_token`（URL）；空视角填 `{}` |
| `parameters.texture_quality` | string | ❌（默认 `standard`） | 可选 `standard` / `detailed`；影响贴图分辨率 |
| `parameters.geometry_quality` | string | ❌（仅 `H3.1` 有效） | 可选 `standard`（≤150 万面） / `ultra`（≤200 万面） |
| `parameters.pbr` | boolean | ❌（默认 `true`） | 设为 `true` 时强制启用贴图；设为 `false` 时需同步设 `texture: false` 才得无贴图模型 |
| `parameters.texture` | boolean | ❌（默认 `true`） | 与 `pbr` 联动；二者同为 `false` 时返回 `base_model_url` |

所有请求**必须包含**以下 Header：
- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（缺此头将报错：“current user api does not support synchronous calls”）

详情参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的请求头与请求体定义。

## 使用方式

1. **开通与配置**  
   在 [百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all) 搜索 “Tripo”，开通服务；按 [API Key 配置指南](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables) 设置环境变量。

2. **创建任务（POST）**  
   向 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送异步请求，获取 `task_id`（有效期 24 小时）。  
   示例（文生3D）：
   ```json
   {
     "model": "Tripo/Tripo-P1.0",
     "input": { "prompt": "一只可爱的猫" },
     "parameters": { "texture_quality": "standard" }
   }
   ```

3. **轮询结果（GET）**  
   定期（建议 ≥15 秒间隔）调用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态。  
   状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；`UNKNOWN` 表示 `task_id` 过期或无效。  
   成功响应中 `output.results[0].pbr_model_url`（或 `base_model_url`）即为模型下载地址，**链接有效期仅 2 小时**，需及时保存。

完整流程与各模式示例详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 无法调用，且 API Key 必须为该地域生成。
- **异步强制性**：不支持同步调用；`X-DashScope-Async: enable` 为硬性要求。
- **任务生命周期**：
  - `task_id` 有效期：24 小时（创建后起算）；
  - 模型下载 URL 有效期：2 小时（结果返回后起算）；
  - 查询接口 RPS 限制：默认 20，高频轮询建议配置 [异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
- **输入校验**：
  - `input.prompt`、`input.image`、`input.images` 三者严格互斥，同时存在将返回 `InvalidParameter` 错误；
  - `input.images` 数组长度必须为 4，否则报错；
  - 图像 URL 需公网可访问，且服务端能成功拉取（超时或 4xx/5xx 均失败）。
- **资源消耗**：`H3.1` 模型生成耗时显著长于 `P1.0`，且 `ultra` 模式可能进一步延长处理时间，生产环境建议优先评估 `P1.0` 是否满足需求。

如遇错误，请依据响应中的 `code` 和 `message` 字段查阅 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)，具体字段说明亦见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)




