# 异步任务

异步任务是百炼平台中用于处理耗时较长的 AI 接口调用的核心执行模型：客户端提交请求后立即返回任务标识（`task_id`），服务端在后台异步执行计算，开发者通过轮询 `GET /api/v1/tasks/{task_id}` 获取最终结果。该模型适用于图像生成、视频生成、3D 生成等资源密集型场景，兼顾系统稳定性与开发者可控性。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成（Image Generation）**：除 `wan2.6`、`qwen-image-3.0` 等新模型支持同步调用外，多数模型（如 `wanx-v1`、`wanx-x-painting`、`image-out-painting`）强制采用异步模式。调用 `POST /api/v1/services/aigc/multimodal-generation/image-synthesis` 创建任务，再轮询 `GET /api/v1/tasks/{task_id}` 获取图片 URL（有效期 24 小时）。

- **视频生成（Video Generation）**：**全部模型均强制异步**。必须携带 `X-DashScope-Async: enable` 头，调用 `POST /api/v1/services/aigc/video-generation/video-synthesis` 创建任务，再通过 `GET /api/v1/tasks/{task_id}` 查询状态；成功响应中 `output.results[].url` 指向 MP4 或 GIF 下载地址（有效期 24 小时）。

- **3D 生成（3D Generation）**：Tripo 系列（`Tripo/Tripo-H3.1` 等）**仅支持异步**，且地域强约束（华北2）。创建任务需 POST 到 `/api/v1/services/aigc/video-generation/3d-generation`（注意路径含 `video-generation`），轮询返回 `pbr_model_url`（PBR GLB）、`base_model_url`（无贴图 GLB）或 `rendered_image_url`（预览图），所有结果 URL 有效期为 2 小时。

- **实时 API（Realtime & Omni Realtime）**：**不适用异步任务模型**。此类接口基于 WebSocket/AOQ/WebRTC 实现流式事件通信，采用会话生命周期管理（`session.create` → `input.audio.commit` → `response.text.delta` 等事件流），无需 `task_id` 轮询。若误传 `X-DashScope-Async: enable` 将导致鉴权失败或协议错误。

> ⚠️ 注意：异步任务是**能力层面的执行范式**，而非统一 API 设计。各领域 Endpoint 路径、参数结构、结果字段均独立定义，不可跨服务复用 `task_id` 或轮询逻辑。

## 关键参数和配置

- **必需请求头**：  
  `X-DashScope-Async: enable` —— 所有异步任务调用必须显式声明，缺失将报错 `"current user api does not support synchronous calls"`。

- **任务标识**：  
  `task_id` —— 创建任务成功后返回的唯一字符串（如 `"task-abc123xyz"`），用于后续轮询。**有效期统一为 24 小时**，超时后 `GET /api/v1/tasks/{task_id}` 返回 `task_status: "UNKNOWN"`。

- **轮询建议**：  
  - 初始间隔 ≥15 秒（避免高频无效请求）；  
  - 可结合 `task_status` 字段（`"QUEUED"` → `"RUNNING"` → `"SUCCESS"`/`"FAILED"`）动态调整间隔；  
  - RPS 限制为 20（全局限频，非单任务）。

- **结果获取**：  
  轮询响应中关键字段因服务而异：  
  - 图像：`output.results[].url`（图片直链）；  
  - 视频：`output.results[].url`（MP4/GIF 直链）；  
  - 3D：`output.results[].pbr_model_url` / `base_model_url` / `rendered_image_url`（GLB 或 PNG 链接）；  
  所有结果 URL 均为临时链接，**务必及时下载并持久化存储**。

- **地域与域名**：  
  异步任务必须使用**业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 仅作兼容，性能与稳定性不保障；跨地域调用（如北京模型配上海 API Key）将直接鉴权失败。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


