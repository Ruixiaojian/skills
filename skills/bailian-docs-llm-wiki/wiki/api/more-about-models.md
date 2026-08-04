# [more](more.md) about models

阿里云百炼平台提供多种模型调用机制与配套能力，涵盖同步/[异步任务](../concepts/asynchronous-task.md)处理、文件上传、连接优化及多业务空间隔离等场景。本文面向开发者，系统梳理核心能力、参数配置、使用方式及关键约束，帮助构建稳定、高效、安全的模型集成方案。

## 支持的模型/功能

百炼支持两类主要调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）：适用于文本生成、多模态理解等低延迟场景，直接返回结果；  
- **异步模型**（如 `wanx2.1-t2i-turbo`、`wanx2.1-kf2v-plus`、`paraformer-16k-1`）：适用于图像生成、视频合成、语音识别等耗时较长的任务，需通过任务 ID 轮询或事件通知获取结果 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  

此外，平台提供配套能力支撑多模态与高并发场景：  
- 本地文件上传获取临时 OSS URL，用于图像、视频、音频输入 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)；  
- 通过事件总线（EventBridge）配置 HTTP 回调或 RocketMQ 接收[异步任务](../concepts/asynchronous-task.md)完成通知，替代轮询，提升实时性与资源效率 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)；  
- 子业务空间（Workspace）隔离模型权限与计费，支持 RAM 用户管控与分账 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 6 中“DashScope 方式调用”示例代码被截断（末尾缺失），实际 Java SDK 示例应包含完整 `GenerationParam.builder()` 链式调用及 `gen.call(param)` 执行逻辑，请以 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 官方完整版为准。

## 关键参数

| 参数 | 说明 | 典型值/范围 | 注意事项 |
|------|------|-------------|----------|
| `expire_in_seconds`（临时 API Key） | 有效期 TTL | `[1, 1800]` 秒 | 默认 60 秒，不可手动删除，到期自动失效 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | [异步任务](../concepts/asynchronous-task.md)唯一标识 | UUID 格式字符串 | 必须用于查询、批量查询及取消操作；任务完成后保留约 24 小时 |
| `model_name`（文件上传） | 绑定模型名称 | 如 `qwen-vl-plus` | 文件与模型强绑定，跨模型调用将失败；上传时必须指定且与后续调用一致 |
| `X-DashScope-OssResourceResolve: enable` | 临时 URL 解析头 | 固定字符串 | 使用 `oss://` URL 时**必须显式添加**，否则模型调用报错 |
| `connectionPoolSize`（Java SDK） | 连接池最大连接数 | 默认 32，建议高并发下设为 256 | 需与 `maximumAsyncRequests` 协调，避免阻塞或服务端过载 |
| `limit_per_host`（Python aiohttp） | 单主机连接上限 | 默认 0（无限制），建议设为 30 | 防止单点请求压垮服务端 |

## 使用方式

### 1. 异步任务全流程
- **提交任务**：调用对应模型的异步接口（如文生图），获取 `task_id`；  
- **获取结果**：  
  - *轮询*：调用 `GET /api/v1/tasks/{task_id}`，QPS 限流 20；  
  - *事件通知*：在事件总线配置规则监听 `dashscope:System:AsyncTaskFinish` 事件，推送至 HTTP 或 RocketMQ [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)；  
- **状态管理**：支持 `PENDING` 状态任务取消（`POST /api/v1/tasks/{task_id}/cancel`），其他状态不可取消。

### 2. 多模态文件输入
- **上传文件**：调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取凭证，再 POST 至 OSS Host；  
- **构造请求**：将返回的 `oss://...` URL 作为输入字段（如 `input.image_url`），并在 Header 中添加 `X-DashScope-OssResourceResolve: enable`；  
- **时效控制**：URL 48 小时过期，生产环境**严禁使用**，应迁移到 OSS 等长期存储。

### 3. 连接复用优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 全局配置连接池参数（超时、大小等）；  
- **Python SDK**：  
  - 同步：复用 `requests.Session` 实例；  
  - 异步：传入自定义 `aiohttp.ClientSession` 并配置 `TCPConnector`；  
- **效果**：显著降低 TCP 握手开销，提升高并发吞吐量与稳定性。

### 4. 子业务空间调用
- **认证**：必须使用该 Workspace 的专属 API Key；  
- **Endpoint**：  
  - 北京地域：`https://dashscope.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容）或 `https://dashscope.aliyuncs.com/api/v1`（DashScope 原生）；  
  - 新加坡地域：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`；  
- **权限**：调用标准模型前需在 Workspace 内显式授权；调优部署模型则仅限本空间调用。

## 限制和注意事项

- **临时 API Key**：继承源 Key 的全部权限（含模型/知识库访问限制），且各地域 API Key **不互通**，需按地域分别申请 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)；  
- **文件上传**：  
  - 单文件 ≤ 1 GB；  
  - QPS 限流 100（按主账号+模型维度），**不可扩容**，禁止用于压测与生产高频场景；  
  - 文件仅限同主账号、同模型使用，无法跨账号/跨模型共享；  
- **异步任务**：  
  - 查询接口 QPS 限流 20（全账号共享）；  
  - 已结束任务约 24 小时后被自动清理，超时无法查询；  
- **连接复用**：Python 同步调用中若未正确关闭 `requests.Session`，可能导致连接泄漏；Java SDK 配置需确保 `maximumAsyncRequestsPerHost ≤ maximumAsyncRequests ≤ connectionPoolSize`；  
- **子空间调用**：OpenAI 兼容方式**不支持**调优部署模型，仅 DashScope 原生接口可用。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)


