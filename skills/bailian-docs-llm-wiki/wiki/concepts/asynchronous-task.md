# 异步任务

异步任务是百炼平台对耗时较长、无法即时返回结果的模型推理操作所采用的标准执行模式。调用方提交请求后，平台立即返回一个唯一的 `task_id`，后续通过该 ID 轮询或接收回调获取最终结果，避免长连接阻塞与超时风险。

## 在百炼平台的不同场景中，这个概念如何使用

- **3D 生成（`3d-generation`）**：所有文生3D、单图生3D、多图生3D 请求均为强制异步。必须在请求头中携带 `X-DashScope-Async: enable`，否则直接报错；成功响应仅含 `task_id`，需轮询 `/api/v1/tasks/{task_id}` 获取 GLB 模型与渲染图 URL（有效期 2 小时）。

- **视频生成（`video-generation-api`）**：全部视频类能力（文生视频、图生视频、数字人、编辑等）统一采用异步流程。创建任务后获得 `task_id`（有效期 24 小时），轮询接口返回结构化结果（如 `video_url`、`thumbnail_url`），状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`。

- **实时 API（`omni-realtime-api` 和 `realtime-api-user-guide`）**：虽以 WebSocket/AOQ 等低延迟协议为主，但**部分配套操作仍属异步任务**——例如：上传大尺寸音频/图像文件后生成的 `oss://` 临时 URL、调用工具（Function Calling）后等待客户端回传结果再触发最终响应、启用联网搜索（`enable_search`）时后台发起的独立检索请求等。这些子过程不阻塞主会话流，但有独立生命周期和状态。

- **通用模型调用（`more-about-models`）**：图像理解（VU）、多图输入类视觉模型等非流式高开销任务，也遵循“提交→轮询”范式。平台建议通过 HTTP 回调或 MQ 订阅 `dashscope:System:AsyncTaskFinish` 事件替代高频轮询，提升系统稳定性。

> ✅ 共同特征：  
> - 所有异步任务均返回 `task_id`，用于唯一标识与状态追踪；  
> - `task_id` 默认有效期为 **24 小时**，超时后无法查询；  
> - 最终输出（如模型 URL、视频地址、结构化 JSON）通常带有 **2 小时有效期**，需及时下载或持久化；  
> - 轮询接口默认限流 **20 QPS**，生产环境强烈推荐使用回调机制。

## 关键参数和配置

| 参数 / 配置 | 说明 | 是否必填 | 备注 |
|-------------|------|----------|------|
| `X-DashScope-Async: enable` | HTTP 请求头，显式声明启用异步模式 | 是（3D/视频等强约束场景） | 缺失将返回 `current user api does not support synchronous calls` 错误 |
| `task_id` | 任务唯一标识符，字符串类型 | — | 创建任务成功后返回，用于轮询或回调上下文；24 小时内有效 |
| `X-DashScope-OssResourceResolve: enable` | 当输入含 `oss://` URL 时需携带 | 是（若使用临时文件） | 确保平台能解析并访问跨服务资源 |
| `callback_url`（可选） | 创建任务时指定的 HTTP 回调地址 | 否 | 推荐用于生产环境，避免轮询；需支持 POST，接收 `application/json` 格式事件 |
| `polling_interval` | 轮询间隔建议值 | 否（开发者控制） | 3D 生成建议 ≥15 秒；视频生成建议 ≥5 秒；避免触发 QPS 限流 |

> ⚠️ 注意：  
> - 异步任务**不支持同步返回结果**，即使请求体中包含 `stream: false` 或类似字段也无效；  
> - `task_id` 查询接口 `/api/v1/tasks/{task_id}` 返回的 `output.task_status` 为 `SUCCEEDED` 仅表示主任务完成，**需检查 `results` 数组内容及各子项 `status` 字段**（如 `DataInspectionFailed` 表示某张输入图解析失败）；  
> - 所有异步任务均受地域强约束：`task_id`、API Key、Endpoint 必须属于同一地域（如华北2），跨地域查询将失败。

## 面向开发者：最佳实践

- **不要轮询，优先用回调**：在创建任务请求体中添加 `"callback_url": "https://your-domain.com/webhook"`，平台将在任务完成时推送标准事件（含 `task_id`, `status`, `results`, `error`）。  
- **及时处理结果 URL**：`pbr_model_url`、`video_url` 等链接仅 2 小时有效，建议收到后立即 `HEAD` 校验 + `GET` 下载至自有存储。  
- **幂等性设计**：`task_id` 可重复查询，响应不变；回调可能重复投递，请基于 `task_id` 做去重处理。  
- **错误兜底**：轮询超时（如 10 分钟无 `SUCCEEDED`）或回调失败时，主动调用 `/api/v1/tasks/{task_id}` 获取最终状态，并根据 `output.error.code`（如 `InvalidParameter`, `ResourceNotReady`）做针对性重试或告警。  
- **监控关键指标**：关注 `task_id` 创建成功率、平均轮询次数、回调送达率，结合云监控配置异步任务失败率 > 1% 的告警。

## 关联主题页

- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [more about models](../api/more-about-models.md)


