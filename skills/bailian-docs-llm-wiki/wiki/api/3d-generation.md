# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。所有任务均为异步执行，需通过 `task_id` 轮询获取结果。当前服务仅在华北2（北京）地域可用，且依赖已开通的 Tripo 模型权限与正确配置的 API Key。

## 支持的模型/功能

- **支持模型**：  
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。  
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。  
  两者均支持文生3D、单图生3D 和多图生3D，但 `geometry_quality` 仅对 `Tripo-H3.1` 生效。

- **输入方式（互斥）**：  
  - `prompt`：文本描述（最大 1024 字符），用于文生3D；详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。  
  - `image`：单张公网可访问图像（JPEG/PNG，20–6000px，≤20MB）。  
  - `images`：固定长度为 4 的数组，按 `[前, 左, 后, 右]` 顺序传入图像对象（缺失视角填 `{}`），实际有效图数为 2–4 张。

- **输出类型**：  
  - 默认返回 PBR 材质模型（`pbr_model_url`，GLB 格式）及预览图（`rendered_image_url`，WebP）。  
  - 无贴图模型需显式设置 `"texture": false, "pbr": false`，此时返回 `base_model_url`。  
  所有 URL 链接有效期均为 **2 小时**，需及时下载。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `model` | string | 是 | 必须为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / string / array | 条件必填 | 三者互斥，仅选其一；`images` 数组长度恒为 4，空视角用 `{}` 占位 |
| `parameters.texture_quality` | string | 否 | `"standard"`（默认）或 `"detailed"`；仅影响贴图分辨率 |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo-H3.1` 支持：`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `false` 时将强制禁用贴图（需同时设 `texture: false`） |
| `parameters.texture` | boolean | 否 | 默认 `true`；与 `pbr` 联动，二者同为 `false` 时返回无贴图模型 |

> **注意**：文档中明确要求 `pbr` 和 `texture` 必须**同时为 `false`** 才能生成无贴图模型，单独设置任一参数为 `false` 不生效。该逻辑与部分旧版 SDK 示例存在不一致，以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 为准。

## 使用方式

1. **前置准备**：  
   - 在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)开通 Tripo 模型服务；  
   - 获取并配置北京地域的 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)，确保环境变量 `DASHSCOPE_API_KEY` 已设置；  
   - 获取业务空间 ID（`WorkspaceId`），用于构造请求 URL。

2. **异步任务创建（POST）**：  
   - 请求地址（北京地域）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   - **必需请求头**：  
     - `Content-Type: application/json`  
     - `Authorization: Bearer $DASHSCOPE_API_KEY`  
     - `X-DashScope-Async: enable`（缺此头将报错：“current user api does not support synchronous calls”）  
   - 成功响应返回 `task_id`（有效期 24 小时），**禁止重复提交相同任务**。

3. **轮询查询结果（GET）**：  
   - 请求地址：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - 建议轮询间隔 ≥15 秒；状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`；  
   - 查询接口 RPS 限制为 20，高频轮询请改用[异步回调](https://help.aliyun.com/zh/model-studio/async-task-api)；  
   - 详细响应结构与错误处理参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域，其他地域 URL 不可用；  
- **任务时效性**：`task_id` 有效期严格为 **24 小时**，超时后查询返回 `task_status: "UNKNOWN"`；  
- **输入约束**：  
  - `prompt` 最长 1024 字符（含中文、英文等）；  
  - 图像 URL 必须为公网可直连 HTTP/HTTPS 地址，CDN 或私有存储需开放匿名访问；  
  - `images` 数组必须为长度 4，不可省略或截断；  
- **资源限制**：单次调用仅生成 1 个 3D 模型（`usage.count` 恒为 1）；  
- **安全提示**：API Key 严禁硬编码或泄露至前端；生产环境建议使用临时凭证或服务端代理；  
- **调试建议**：新手可参考 [Postman 快速上手指南](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api) 验证请求格式。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


