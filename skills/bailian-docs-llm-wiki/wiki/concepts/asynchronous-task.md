# 异步任务

异步任务是百炼平台对耗时较长的模型推理请求（如图像生成、视频生成、3D建模等）所采用的标准执行模式：客户端发起请求后立即返回任务标识符（`task_id`），实际计算在服务端后台异步执行，结果需通过轮询或事件回调方式获取。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成**：`kling`、`vidu`、`wanx-v1` 等模型强制使用异步模式。调用 `POST /api/v1/services/aigc/multimodal-generation/generation` 创建任务，返回 `task_id`；再通过 `GET /api/v1/tasks/{task_id}` 轮询状态，直至 `task_status == "SUCCEEDED"` 后提取 `output.results[].url`（图片 URL 有效期 24 小时）。

- **视频生成**：全部模型统一启用异步调用，必须设置请求头 `X-DashScope-Async: enable`。创建任务后获得 `task_id`（有效期 24 小时），后续轮询 `/api/v1/tasks/{task_id}` 获取视频下载链接（URL 有效期通常为 2 小时）。

- **3D生成**：Tripo 模型仅支持异步，且**强约束地域为华北2（北京）**。请求需携带 `X-DashScope-Async: enable`，成功响应含 `task_id`；轮询间隔建议 ≥15 秒，结果中 `pbr_model_url` 或 `base_model_url` 有效期仅 2 小时，需及时下载。

- **模型微调与部署**：微调作业（`fine_tuning_jobs`）和部署操作本身即为异步任务。提交后返回 `job_id` 或 `deployment_id`，需轮询对应资源 endpoint（如 `GET /v1/fine_tuning_jobs/{job_id}`）确认完成状态，不可同步等待。

- **通用原则**：  
  - 所有异步任务均以 `task_id` 为唯一追踪凭证，格式为标准 UUID；  
  - 任务状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED` / `CANCELLED`；  
  - 避免高频轮询（推荐 ≥15 秒间隔），生产环境应优先配置 [EventBridge 回调](../../raw/model-api-reference/more-about-models/async-task-api.md) 接收 `dashscope:System:AsyncTaskFinish` 事件，实现低延迟、零限流的结果通知。

## 关键参数和配置

- `X-DashScope-Async: enable`：**必需请求头**，显式声明启用异步模式（部分 API 如视频生成强制要求，缺失将报错）；  
- `task_id`：字符串类型，由平台生成并返回，用于后续查询、取消或获取结果；  
- `expire_in_seconds`（可选）：部分异步管理接口支持指定任务保留时长（默认 24 小时），超期后任务记录与输出 URL 自动清理；  
- `X-DashScope-OssResourceResolve: enable`（文件类任务）：当输入含 OSS 临时 URL 时需添加，确保平台正确解析资源；  
- 回调配置（高级）：通过 EventBridge 绑定 HTTP Endpoint 或 RocketMQ Topic，接收结构化事件（含 `data.task_id`, `data.status`, `data.output`），替代轮询。

## 面向开发者，简洁实用

✅ **最佳实践**：  
- 始终检查响应状态码 `200` 和 `task_id` 字段，勿假设请求已立即完成；  
- 使用 SDK 的 `get_task_result(task_id)` 封装轮询逻辑（Python/Java SDK 均内置），避免手写重试；  
- 生产环境禁用裸轮询，务必配置 EventBridge 回调——单次事件触发 + 单次结果查询，性能与稳定性双优；  
- 所有异步输出 URL 均有时效性（2–24 小时不等），请在收到结果后立即下载或持久化存储；  
- `task_id` 是调试核心线索：日志中记录它，控制台中可通过「异步任务管理」页面直接检索全量状态与错误详情。

⚠️ **避坑提示**：  
- 不同模型/地域的 `task_id` 不互通，跨地域调用将失败；  
- 未配置 `X-DashScope-Async: enable` 却调用异步专属 endpoint（如 `/api/v1/tasks/xxx`），将返回 `400 Bad Request`；  
- 轮询频率超过 20 QPS 可能触发限流，导致 `429 Too Many Requests`；  
- 任务超时（如 24 小时未完成）后 `task_id` 失效，无法再查询，需重发请求。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)
- [model production](../api/model-production.md)


