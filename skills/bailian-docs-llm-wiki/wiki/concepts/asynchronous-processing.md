# 异步处理

异步处理是百炼平台中用于执行耗时较长任务的核心机制，指调用方发起请求后立即返回任务标识（`task_id`），后台独立执行计算，结果通过轮询或事件回调方式获取，避免阻塞客户端连接与响应延迟。

## 在百炼平台的不同场景中，这个概念如何使用

- **应用调用（Application Call）**：通过设置 `background=true` 参数启用异步模式，适用于报告生成、多步骤工具链等长流程任务；返回 `task_id` 后需调用 `retrieve` 接口查询结果，**不支持[流式输出](streaming-output.md)**。
- **图像生成（Image Generation）**：局部重绘（`wanx-x-painting`）、背景生成（`wanx-background-generation-v2`）、擦除补全（`image-erase-completion`）等模型强制异步；需在请求头中添加 `X-DashScope-Async: enable`，再通过 `GET /api/v1/tasks/{task_id}` 轮询状态。
- **3D 生成（3D Generation）**：Tripo 模型（如 `Tripo/Tripo-H3.1`）**仅支持异步调用**，缺失 `X-DashScope-Async: enable` 头将直接报错；任务有效期严格为 24 小时，超时不可查。
- **视频生成（Video Generation）**：全部模型（文生视频、图生视频、动作迁移等）均采用异步模式；必须携带 `X-DashScope-Async: enable` 请求头，并依赖 `task_id` 查询结果或配置 HTTP 回调接收完成事件。
- **通用模型调用（More about Models）**：语音识别（`paraformer-16k-1`）、部分图像/视频旧版模型等被明确归类为“异步模型”；平台统一提供 `/api/v1/tasks/{task_id}` 查询接口，并支持批量管理、取消及事件驱动通知（EventBridge）。
- **模型生产（Model Production）**：微调训练（`fine-tune`）和部署（`deploy`）本身是异步任务——提交后返回 `job_id` 或 `deployment_id`，需轮询其状态（如 `SUCCEEDED`/`FAILED`），而非等待即时结果。

## 关键参数和配置

- **通用请求头**（所有异步模型必需）：
  - `X-DashScope-Async: enable` —— 缺失将导致同步调用失败或 400 错误。
  - `Authorization: Bearer $DASHSCOPE_API_KEY`
  - `Content-Type: application/json`

- **核心参数**：
  - `background: true`（仅 Application Call）：在请求体中显式开启异步模式。
  - `task_id`（返回值）：UUID 格式字符串，用于后续查询、取消或回调关联；有效期依服务而定（通常 24 小时）。
  - `model`（必填）：指定异步模型名（如 `Tripo/Tripo-H3.1`, `happyhorse-1.1-t2v`），决定路由与资源调度。

- **轮询与回调建议**：
  - 轮询间隔 ≥15 秒，避免触发 QPS 限流（默认 20 QPS）；
  - 生产环境推荐使用 [HTTP 回调或 RocketMQ 事件通知](https://help.aliyun.com/zh/model-studio/async-task-api)，减少主动轮询开销；
  - 状态流转典型路径：`PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED` / `CANCELLED`。

> ⚠️ 注意：异步任务不支持 `stream=true`；若需实时反馈，请选用同步模型或拆分任务粒度。

## 关联主题页

- [application call](../api/application-call.md)
- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [more about models](../api/more-about-models.md)
- [model production](../api/model-production.md)


