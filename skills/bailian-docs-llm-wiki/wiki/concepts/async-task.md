# 异步任务

异步任务是百炼平台对长耗时 AI 模型调用（如图像生成、3D 建模、视频合成等）采用的标准交互模式：客户端发起请求后立即返回任务标识（`task_id`），模型服务在后台执行计算，开发者通过轮询或事件回调获取最终结果。该模式避免了 HTTP 连接长时间阻塞，保障高并发下的稳定性与资源利用率。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成（Image Generation）**：除 `wan2.6-t2i`、`qwen-image-3.0-pro` 等少数新模型支持同步调用外，绝大多数图像能力（如 `wanx-v1`、`kling/kling-v3-image-generation`、局部重绘、背景生成）均强制异步。需先 POST 到对应子路径（如 `/text2image/image-synthesis`）创建任务，再 GET `/api/v1/tasks/{task_id}` 查询状态。
  
- **3D 生成（3D Generation）**：Tripo 全系列模型（`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`）**仅支持异步调用**，且必须携带 `X-DashScope-Async: enable` 请求头；同步请求将直接报错。任务创建后需轮询至少 15 秒间隔，状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`。

- **视频生成（Video Generation）**：所有视频类 API（文生视频、图生视频、参考生视频、口型替换等）统一采用异步模式。无论模型厂商（Kling、PixVerse、Vidu、万相），均需通过 `/api/v1/services/aigc/video-generation/video-synthesis` 创建任务，并依赖 `task_id` 查询结果。

- **通用任务管理（More About Models）**：平台提供统一的异步任务生命周期管理能力，支持单查（`GET /api/v1/tasks/{task_id}`）、批量查询（`POST /api/v1/tasks/query`）、取消（`DELETE /api/v1/tasks/{task_id}`）。高并发场景下，推荐配置 EventBridge HTTP 回调或 RocketMQ 消息队列接收 `TASK_COMPLETED` 事件，替代轮询以规避 20 QPS 限流。

## 关键参数和配置

- **必需请求头**：
  - `X-DashScope-Async: enable`：显式启用异步模式，缺失将导致 400 错误（尤其在 3D、视频等强约束场景）。
  - `Authorization: Bearer $DASHSCOPE_API_KEY`：地域匹配的 API Key（北京、新加坡等地域 Key 不互通）。
  - `Content-Type: application/json`

- **核心响应字段**：
  - `task_id`：全局唯一字符串，有效期 24 小时，用于后续查询、取消或回调关联。
  - `status`：当前状态，典型值包括 `PENDING`（排队中）、`RUNNING`（执行中）、`SUCCEEDED`（成功）、`FAILED`（失败）、`UNKNOWN`（无效或过期）。
  - `output`：仅当 `status == "SUCCEEDED"` 时存在，结构因模型而异（如图像含 `url` 字段，3D 含 `pbr_model_url`，视频含 `video_url`）。

- **轮询建议**：
  - 初始延迟 ≥1 秒，后续间隔 ≥15 秒（3D 场景明确要求）；
  - 超时阈值建议设为 300 秒（5 分钟），部分复杂任务（如高精度 3D）可能耗时更长；
  - 避免高频轮询：单个 `task_id` 查询超过 20 次/分钟将触发限流。

- **生产级优化**：
  - 使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非公共域名；
  - 文件类输入（图像、视频、3D 参考图）优先上传至平台临时 OSS（返回 `oss://` URL），并添加 `X-DashScope-OssResourceResolve: enable` 头；
  - 高并发任务提交链路中，文件上传与任务创建应解耦，避免共享 100 QPS 上传限流通道。

> ⚠️ 注意：异步任务结果默认保留 24 小时，超时后 `output` 数据自动清理，不可恢复。关键业务请务必在 `SUCCEEDED` 后及时下载并持久化存储。

## 关联主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [more about models](../api/more-about-models.md)


