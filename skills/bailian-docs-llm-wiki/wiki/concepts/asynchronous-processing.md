# 异步处理

异步处理是百炼平台对长耗时、高资源消耗类 AI 任务（如 3D 生成、视频合成、大模型批量推理等）采用的标准执行模式：客户端发起请求后立即返回任务标识（`task_id`），服务端后台执行计算，结果通过轮询或事件回调方式获取，避免阻塞请求链路与连接超时。

## 在百炼平台的不同场景中，这个概念如何使用

- **3D 生成（`3d-generation`）**：所有文生3D、图生3D、多图生3D 请求均为强制异步。必须在请求头中显式设置 `X-DashScope-Async: enable`，否则报错；响应仅含 `task_id`，需调用 `/api/v1/tasks/{task_id}` 轮询状态（建议 ≥15 秒间隔），任务有效期严格为 **24 小时**。

- **视频生成（`video-generation-api`）**：全部视频类模型（T2V/I2V/R2V/编辑/动作迁移等）统一采用异步模式。同样依赖 `X-DashScope-Async: enable` 头，且要求模型、API Key、Endpoint 地域三者严格一致；支持 HTTP 回调或 RocketMQ 事件总线（`dashscope:System:AsyncTaskFinish`）接收完成通知，推荐替代轮询以规避 QPS 限流（20 次/秒）。

- **通用模型调用（`more-about-models`）**：图像生成、长文本生成、[多模态](multi-modal.md)批处理等耗时操作均归入异步任务体系。平台提供统一的异步任务管理 API（`GET /api/v1/tasks` 及 `GET /api/v1/tasks/{task_id}`），支持按状态、时间范围、模型名批量查询；任务元数据（如输入参数、错误码、耗时）均可通过任务 ID 获取。

- **实时 API（`realtime-api-user-guide`, `omni-realtime-api`）**：*不适用异步处理*。Realtime 系列接口（AOQ/WebSocket/WebRTC）面向低延迟交互场景，采用全双工流式通信，请求与响应实时交织，无 `task_id` 概念。其“异步”体现在事件驱动（如 `response.audio.delta`）和非阻塞 I/O，但不属于平台级异步任务范式。

> ✅ 关键区分：**异步任务（Async Task）是平台级任务调度机制，对应 `task_id` 生命周期；而 Realtime 的“异步通信”是传输层特性，不产生可轮询的任务实体。**

## 关键参数和配置

| 参数 / 配置项 | 说明 | 必填性 | 示例值 | 注意事项 |
|---------------|------|--------|--------|----------|
| `X-DashScope-Async` | 强制启用异步模式的请求头 | **必需** | `enable` | 缺失将导致 `400 Bad Request`：“current user api does not support synchronous calls” |
| `task_id` | 异步任务唯一标识符 | 返回值 | `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | 有效期 **24 小时**，超时后查询返回 `task_status: "UNKNOWN"`；禁止重复提交相同输入 |
| `X-DashScope-OssResourceResolve` | 含 `oss://` 文件 URL 的请求需启用此头 | 条件必需 | `enable` | 用于解析临时 OSS 资源（如上传的图片/视频），与异步任务常配合使用 |
| HTTP 回调地址（`callback_url`） | 任务完成时平台主动 POST 结果到指定 URL | 可选 | `https://your-domain.com/webhook` | 需支持 HTTPS，推荐用于生产环境替代轮询；回调体结构与 `GET /api/v1/tasks/{task_id}` 响应一致 |
| RocketMQ Topic | 订阅 `dashscope:System:AsyncTaskFinish` 事件 | 可选 | `dashscope-system-async-task-finish` | 需提前在控制台开通事件总线并授权，适合高并发、分布式系统 |

## 面向开发者，简洁实用

- **不要轮询，优先用回调**：高频轮询易触发限流（20 QPS），且增加客户端复杂度。生产环境务必配置 `callback_url` 或接入 RocketMQ。
- **`task_id` 是你的唯一凭证**：保存好它，所有后续操作（查状态、取结果、重试）都依赖它。建议与业务订单 ID 关联存储。
- **检查 `task_status` 再取结果**：轮询响应中先确认 `"task_status": "SUCCEEDED"`，再读取 `output` 字段；`"FAILED"` 时查看 `error_code` 和 `error_message` 排查（常见如 `INPUT_INVALID`, `QUOTA_EXCEEDED`, `MODEL_NOT_FOUND`）。
- **URL 有效期很短**：3D/视频等输出中的 `pbr_model_url`、`rendered_image_url`、`video_url` 等均为临时链接，**默认 2 小时过期**，收到后请立即下载或转存。
- **地域强绑定**：异步任务创建与查询必须使用同一地域 Endpoint（如北京：`cn-beijing.maas.aliyuncs.com`），跨地域调用必然失败。  
- **SDK 提示**：DashScope Python/Java SDK 已封装异步任务轮询与回调注册逻辑，直接调用 `generate_async()` + `get_task_result()` 即可，无需手动拼 URL。

## 关联主题页

- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [more about models](../api/more-about-models.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


