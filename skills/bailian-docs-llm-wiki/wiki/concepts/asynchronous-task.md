# 异步任务

异步任务是百炼平台中用于处理耗时较长模型调用的执行模式，其核心特征是**请求立即返回任务标识（`task_id`），结果通过后续轮询或事件通知方式获取**，避免客户端长时间阻塞。该模式适用于图像生成、视频生成、3D建模、长文本报告生成等计算密集型或I/O延迟高的场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成**：旧版模型（如 `wanx-v1`、`image-out-painting`）强制异步；调用时需携带 `X-DashScope-Async: enable` 请求头，创建任务后通过 `task_id` 轮询 `/api/v1/tasks/{task_id}` 获取结果。
- **视频生成**：**全部模型均采用异步模式**，无同步选项；必须设置 `X-DashScope-Async: enable`，任务 ID 有效期为 24 小时，状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`。
- **3D生成（Tripo）**：全量异步，仅支持华北2（北京）地域；请求必须含 `X-DashScope-Async: enable`，响应返回 `task_id`，轮询间隔建议 ≥15 秒。
- **应用调用（Application Call）**：通过 `background=true` 参数显式启用异步模式，适用于长流程智能体或工作流（如多步骤报告生成）；成功响应直接返回 `task_id`，不等待执行完成。
- **通用模型服务（如语音识别、部分[多模态](multi-modal.md)模型）**：`paraformer-16k-1`、`wanx2.1-kf2v-plus` 等明确归类为“异步模型”，需统一通过[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 查询状态、取消任务或批量管理。

> ✅ 统一要求：所有异步调用**必须携带 `X-DashScope-Async: enable` 请求头**，否则将返回错误 `current user api does not support synchronous calls`。

## 关键参数和配置

| 参数/配置 | 说明 | 注意事项 |
|-----------|------|----------|
| `task_id` | 异步任务唯一标识符，UUID 格式字符串，由创建接口返回 | 有效期因场景而异：视频/3D任务为 24 小时；通用异步任务默认 7 天（以实际 API 响应为准）；需妥善存储并用于后续查询或取消操作 |
| `X-DashScope-Async: enable` | **强制请求头**，标识本次调用为异步模式 | 缺失将导致鉴权失败或 400 错误；不可省略，与模型类型无关 |
| `background=true` | 应用调用场景下的布尔参数，启用异步执行 | 仅作用于 `application call` 接口；设为 `true` 后响应体结构变为 `{ "task_id": "...", "status": "PENDING" }` |
| 轮询频率 | 建议 ≥15 秒一次（3D）、≥30 秒一次（视频）；通用任务避免高频轮询 | 轮询接口有 QPS 限制（默认 20 QPS），超限将触发限流；生产环境**强烈推荐使用 HTTP 回调或 MQ 通知替代轮询** |
| 回调配置 | 通过 `callback_url`（HTTP）或 `mq_endpoint`（消息队列）注册完成通知 | 需确保服务可公网访问（HTTP）或已配置阿里云 RocketMQ 权限；回调内容包含 `task_id` 和 `result`，无需轮询 |

## 面向开发者，简洁实用

- ✅ **第一步：确认模型是否支持异步** —— 查阅对应模型文档，若标注为“异步模型”或要求 `X-DashScope-Async: enable`，则必须走异步流程。
- ✅ **第二步：发起异步请求** —— 添加必要头信息（`Authorization`, `Content-Type`, `X-DashScope-Async: enable`），发送 POST 请求，提取响应中的 `task_id`。
- ✅ **第三步：获取结果**  
  - *开发调试*：用 `GET /api/v1/tasks/{task_id}` 轮询，检查 `task_status` 字段（`SUCCEEDED`/`FAILED`）；  
  - *生产部署*：配置 `callback_url`，在服务端接收 JSON 格式回调（含 `task_id`, `result`, `end_time`），实现零轮询实时交付。
- ⚠️ **避坑提示**：  
  - 时间字段兼容性：`start_time`/`end_time` 在响应中可能为字符串（如 `"2023-12-20 21:36:45.913"`）或毫秒时间戳（`Long`），建议优先按字符串解析，再 fallback 到时间戳；  
  - URL 域名必须匹配：异步任务 Endpoint 必须使用业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），禁用 `dashscope.aliyuncs.com`；  
  - 文件输入需预处理：图像/视频/3D 输入必须先上传至 OSS 获取 `oss://` URL，并在请求头中添加 `X-DashScope-OssResourceResolve: enable`。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [application call](../api/application-call.md)


