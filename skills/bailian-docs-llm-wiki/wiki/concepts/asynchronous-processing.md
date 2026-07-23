# 异步处理

异步处理是百炼平台中用于应对长耗时任务（如图像生成、视频合成、3D建模、语音识别等）的核心执行模式：调用方发起请求后立即返回任务 ID，不阻塞等待结果；实际计算在后台异步执行，结果通过轮询或事件通知方式获取。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成**：`wanx-v1`、`wan2.5-i2i-preview`、`wanx-style-repaint-v1` 等模型强制异步调用；需设置请求头 `X-DashScope-Async: enable`，创建任务后通过 `task_id` 查询状态与结果 URL（如 `pbr_model_url` 或图片链接），结果链接默认有效期 2 小时。
  
- **视频生成**：所有视频类模型（`wan2.7-t2v-*`、`pixverse/*t2v`、`kling/*`、`vidu/*` 等）均仅支持异步模式，必须携带 `X-DashScope-Async: enable` 请求头；任务状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`，成功后返回视频下载地址。

- **3D 生成**：Tripo 模型（`Tripo/Tripo-P1.0`、`Tripo/Tripo-H3.1`）全程异步，输入支持文/图/多图，输出为 GLB 文件；同样依赖 `X-DashScope-Async: enable`，且仅在北京地域可用。

- **语音与多模态识别**：`paraformer-8k-v1` 等语音识别模型采用异步流程，适用于长音频（>60 秒）处理，避免 HTTP 连接超时。

- **文件预处理**：文件上传后若需解析（如 PDF 文本提取），状态可能为 `"processing"`，属隐式异步过程，需轮询 `/v1/files/{file_id}` 直至 `status == "uploaded"` 才可用于知识库等下游任务。

> ✅ 共性特征：所有显式异步调用均返回 `task_id`；任务默认保留 24 小时；结果资源（图片、视频、3D 模型、文本等）URL 有短期有效期（2–24 小时），务必及时下载或持久化。

## 关键参数和配置

| 参数/配置 | 说明 | 必填性 | 注意事项 |
|-----------|------|--------|----------|
| `X-DashScope-Async: enable` | HTTP 请求头，标识本次调用为异步模式 | ✅ 所有显式异步模型必需 | 缺失将报错 `"current user api does not support synchronous calls"` |
| `task_id` | 任务唯一标识符，由平台生成并返回于创建响应中 | ✅ 后续查询/取消操作必需 | 需安全存储（如数据库或内存缓存），不可丢失；有效期 24 小时 |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` 临时 URL 作为输入时必需 | ⚠️ 条件必填（仅当输入含 `oss://` 资源时） | 常见于图像/视频/3D 模型调用前的文件引用环节 |
| 轮询间隔 | 查询 `/api/v1/tasks/{task_id}` 的时间间隔 | ❌ 推荐配置 | 建议 ≥15 秒（3D）、≥5 秒（图像）、≥30 秒（视频）；QPS 限流为 20，高频轮询易触发限流 |
| 事件回调（EventBridge） | 替代轮询的推荐方案：配置 HTTP 回调或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件 | ❌ 可选但强烈推荐 | 规避轮询限流，适合高并发、大规模任务场景；事件中含 `task_id`，仍需主动调用一次 `/api/v1/tasks/{task_id}` 获取最终结果 |

## 面向开发者，简洁实用

- **不要同步等待**：异步任务无实时响应体，切勿在主线程中循环阻塞等待；使用定时器、协程或消息队列解耦。
- **务必校验状态**：查询任务返回的 `task_status` 字段，仅当值为 `"SUCCEEDED"` 时才读取 `output.results`；`"FAILED"` 需检查 `output.error.code` 和 `message`。
- **及时下载结果**：所有生成的资源 URL（图片、视频、GLB、音频等）均为临时链接，过期即失效。建议在收到结果后立即 `GET` 下载并存入自有存储。
- **善用事件驱动**：生产环境优先配置 EventBridge 回调，降低轮询开销与服务端压力；回调 URL 需可公网访问且响应迅速（建议 <3s）。
- **错误重试策略**：对 `5xx` 或网络超时可重试（带指数退避），但 `4xx` 错误（如 `InvalidParameter`、`TaskNotFound`）应修正请求再发，而非盲目重试。
- **清理与监控**：记录 `task_id` 生命周期，对超 24 小时未完成的任务标记为超时；结合云监控配置异步任务失败率、平均耗时等告警指标。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [file management api](../api/file-management-api.md)


