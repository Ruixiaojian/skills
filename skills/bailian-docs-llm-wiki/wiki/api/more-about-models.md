# [more](more.md) about models

百炼平台提供丰富的模型调用能力，涵盖同步/异步任务处理、多业务空间隔离、连接复用优化、文件临时存储及安全凭证管理等核心场景。本文档面向开发者，系统梳理关键能力、参数配置、使用方式及限制条件，帮助构建稳定高效的模型服务集成。

## 支持的模型/功能

百炼支持标准大模型（如 `qwen-plus`）、[多模态](../concepts/multi-modal.md)模型（如 `qwen-vl-plus`）、语音识别（如 `paraformer-8k-v1`）、文生图（`wanx2.1-t2i-turbo`）、文生视频（`wanx2.1-kf2v-plus`）等全栈模型。模型调用可基于默认业务空间或子业务空间进行隔离部署，适用于权限管控与费用分账场景 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。对于长耗时任务（如图像/视频生成），平台统一采用异步机制，并提供完整的任务生命周期管理能力，包括创建、状态查询、批量轮询与取消 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

> **注意**：文档 2 中提到“部分任务（如文生图、文生视频）提供了SDK，SDK已实现轮询”，但文档 6 明确指出异步任务需主动调用 `/api/v1/tasks/{task_id}` 查询结果，且轮询存在 20 QPS 限流。实际开发中应优先采用事件总线回调方案以规避限流风险，而非依赖 SDK 内置轮询逻辑。

## 关键参数

- **临时API Key有效期**：通过 `expire_in_seconds` 参数控制，范围为 `[1, 1800]` 秒，默认 60 秒 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **文件临时URL有效期**：固定为 48 小时，超时后自动清理，不可续期。  
- **连接池参数（Java SDK）**：`connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）、`connectTimeout`（默认 120 秒）等需按并发量调优。  
- **异步任务查询限流**：单账号维度 20 QPS，适用于 `/api/v1/tasks/{task_id}`、`/api/v1/tasks/` 和 `/api/v1/tasks/{task_id}/cancel` 三个接口。  
- **文件上传限流**：按“主账号+模型”维度 100 QPS，不可扩容。

## 使用方式

- **子空间模型调用**：必须使用该子空间生成的 API Key，并显式配置对应地域的 `base_url`（北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`）。  
- **异步任务通知**：推荐通过事件总线配置 HTTP 回调 URL 或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，避免轮询 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。  
- **连接复用**：Java SDK 默认启用连接池，可通过 `Constants.connectionConfigurations` 配置；Python SDK 需传入自定义 `requests.Session`（同步）或 `aiohttp.ClientSession`（异步）。  
- **本地文件上传**：调用 `/api/v1/uploads?action=getPolicy&model={model_name}` 获取凭证，再上传至 OSS，返回 `oss://...` URL；**模型调用时必须在请求头添加 `X-DashScope-OssResourceResolve: enable`**。  

## 限制和注意事项

- **临时API Key**：继承源 API Key 的全部权限，无法手动删除，到期自动失效；各地域 API Key 不互通。  
- **文件上传绑定性**：上传时指定的 `model_name` 必须与后续模型调用的模型完全一致，且文件仅限同一主账号下使用；生产环境严禁使用该临时存储，应迁移到阿里云 OSS。  
- **异步任务数据保留**：任务完成后通常保留 24 小时，超时后自动清理，`/api/v1/tasks/` 接口无法查询历史数据。  
- **取消任务限制**：仅支持取消 `PENDING` 状态任务，`RUNNING` 或已完成任务不可取消。  
- **地域一致性**：北京、新加坡、弗吉尼亚等不同地域的 API Key、Endpoint、WorkspaceId 均不通用，需严格匹配。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)


