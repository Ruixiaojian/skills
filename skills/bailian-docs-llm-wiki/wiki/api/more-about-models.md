# [more](more.md) about models

百炼平台提供多种模型调用机制与配套能力，覆盖同步/异步任务、多模态文件处理、子空间隔离、连接优化等核心场景。本文面向开发者，系统梳理模型服务的关键能力、参数配置、使用方式及限制，帮助构建稳定、高效、安全的 AI 应用。

## 支持的模型/功能

百炼支持两类主要模型调用路径：  
- **标准模型**（如 `qwen-plus`、`wanx2.1-t2i-turbo`）：需在业务空间中显式授权调用权限，支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope 原生接口；  
- **调优后部署的私有模型**：仅限其所属业务空间的 API Key 调用，无需额外授权，但不支持 OpenAI 兼容方式 [原文标题](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  

关键功能包括：  
- **异步任务处理**：适用于图像生成、视频合成、长文本语音识别等耗时操作，需通过 `task_id` 查询结果或取消任务；  
- **临时文件托管**：上传本地图片/音频/视频获取 `oss://` 格式临时 URL（有效期 48 小时），调用时必须携带请求头 `X-DashScope-OssResourceResolve: enable`；  
- **事件驱动通知**：通过事件总线（EventBridge）配置 HTTP 回调或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，替代轮询 [原文标题](../../raw/model-api-reference/more-about-models/async-task-api.md)；  
- **子业务空间隔离**：按业务/团队划分独立空间，实现模型权限管控与费用分账，调用时必须使用对应空间的 API Key。

> **注意**：文档 4 中“DashScope 方式调用子业务空间模型”的示例代码在 Java 部分被截断（末尾缺失 `}` 和异常处理），实际使用请以 [原文标题](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 完整代码为准。

## 关键参数

| 参数 | 说明 | 取值范围/默认值 | 注意事项 |
|------|------|----------------|----------|
| `expire_in_seconds`（临时 API Key） | 有效期（TTL） | `[1, 1800]` 秒，默认 60 秒 | 临时 Key 继承生成者全部权限，到期自动失效，不可手动删除 [原文标题](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 字符串 | 用于查询状态、批量检索或取消（仅 `PENDING` 状态可取消） |
| `model_name`（文件上传） | 指定文件用途的模型名 | 如 `qwen-vl-plus` | 文件与模型强绑定，跨模型调用将失败；且必须与后续模型调用一致 |
| 连接池参数（Java SDK） | `connectionPoolSize`、`maximumAsyncRequests` 等 | 默认 `32` | 高并发场景需按业务负载调优，`maximumAsyncRequestsPerHost` ≤ `maximumAsyncRequests` ≤ `connectionPoolSize` |
| `limit` / `limit_per_host`（Python async） | `aiohttp.TCPConnector` 连接数限制 | 默认 `100` / `0` | 避免对单一 endpoint 过载，建议设 `limit_per_host=30` |

## 使用方式

### 1. 异步任务全流程
- **提交任务**：调用对应模型的异步接口（如文生图），获取 `task_id`；  
- **查询结果**：`GET /api/v1/tasks/{task_id}`，支持单查或批量查（`GET /api/v1/tasks/`）；  
- **取消任务**：`POST /api/v1/tasks/{task_id}/cancel`（仅限 `PENDING` 状态）；  
- **接收通知（推荐）**：在事件总线配置规则，监听 `dashscope:System:AsyncTaskFinish` 事件，解析 `data.task_id` 后单次查询结果，避免轮询限流（20 QPS）。

### 2. 多模态文件处理
- **上传文件**：调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取凭证，再 POST 至 OSS；  
- **构造请求**：在模型调用请求体中传入 `oss://` URL，并在 Header 中添加 `X-DashScope-OssResourceResolve: enable`；  
- **时效管理**：URL 48 小时过期，生产环境应使用 OSS 等长期存储。

### 3. 子业务空间调用
- **API Key 隔离**：必须使用目标子空间创建的 API Key；  
- **Endpoint 区分**：北京地域用 `https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡地域需替换 `{WorkspaceId}`，如 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`；  
- **SDK 配置**：Python/Java 等 SDK 需显式设置 `base_url` 或 `base_http_api_url`。

### 4. 连接复用优化
- **Java**：通过 `Constants.connectionConfigurations` 设置超时与连接池大小；  
- **Python 同步**：复用 `requests.Session()` 实例；  
- **Python 异步**：传入 `aiohttp.ClientSession(connector=TCPConnector(...))` 到 `AioGeneration.call()`。

## 限制和注意事项

- **临时 API Key**：继承源 Key 全部权限，包括知识库访问限制；各地域 Key 不互通，调用时需匹配对应 Endpoint；  
- **异步任务保留期**：成功/失败任务数据默认保留 24 小时，超时后自动清理，无法恢复；  
- **文件上传限流**：按“主账号+模型”维度限 100 QPS，超出即失败，**严禁用于生产压测**；  
- **临时 URL 安全性**：`oss://` URL 无鉴权，48 小时后失效，**禁止用于生产环境**，应迁移到自有 OSS 并配置签名 URL；  
- **子空间模型调用**：调优模型仅支持 DashScope 原生接口，不兼容 OpenAI 协议；  
- **连接复用**：Python 同步调用中若未显式关闭 `Session`，可能导致连接泄漏；Java SDK 的 `maximumAsyncRequestsPerHost` 必须 ≤ `maximumAsyncRequests`，否则请求可能阻塞。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


