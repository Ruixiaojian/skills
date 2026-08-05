# [more](more.md) about models

阿里云百炼平台支持多种模型调用方式与配套能力，涵盖同步/异步任务处理、多业务空间隔离、文件上传、连接复用及安全凭证管理等核心场景。本文面向开发者，系统梳理关键能力、参数约束、使用路径及注意事项，帮助构建稳定、高效、安全的模型集成方案。

## 支持的模型与功能

百炼平台支持两类主要模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）：适用于文本生成、多模态理解等低延迟场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音识别 `paraformer-16k-1`）：因处理耗时长，需通过任务 ID 轮询或事件通知获取结果。异步任务管理能力详见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  

此外，平台支持在**子业务空间**中调用标准模型（如 `qwen-plus`）或专属调优模型，实现权限隔离与费用分账，具体请参考 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  

> **注意**：文档 3 中明确指出，“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但该模型**仅能由其所在业务空间的 API Key 调用**；而调用标准模型（如 `qwen-plus`）则必须提前为子空间[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)。此权限逻辑在不同文档中表述一致，无矛盾。

## 关键参数

| 参数 | 说明 | 典型值/范围 | 来源 |
|------|------|-------------|------|
| `task_id` | 异步任务唯一标识，用于查询、取消任务 | UUID 格式字符串 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 模型名称，用于文件上传绑定、权限校验、地域路由 | `qwen-plus`, `wanx2.1-t2i-turbo`, `paraformer-8k-v1` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)、[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) |
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒（默认 60 秒） | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 固定字符串 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` / `limit_per_host` | Java/Python SDK 连接池参数，影响高并发性能 | Java 默认 32；Python `aiohttp.TCPConnector` 默认 `limit=100`, `limit_per_host=0` | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 异步任务处理
- **轮询模式**：调用 `/api/v1/tasks/{task_id}` 查询状态（限流 20 QPS），适用于简单集成；  
- **事件驱动模式**：通过 [事件总线 EventBridge](https://help.aliyun.com/zh/eventbridge/product-overview/what-is-eventbridge) 配置 HTTP 回调或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，避免轮询限流与资源浪费 —— 详见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)；  
- **任务管理**：支持批量查询（`GET /api/v1/tasks/`）、取消 PENDING 状态任务（`POST /api/v1/tasks/{task_id}/cancel`）。

### 2. 多业务空间调用
- 子空间模型调用**必须使用该空间的 API Key**；  
- OpenAI 兼容方式：`base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"`；  
- DashScope 原生方式：北京地域使用 `https://dashscope.aliyuncs.com/api/v1`，新加坡地域需替换为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`。

### 3. 文件上传与引用
- 上传前需指定 `model_name`，生成 `oss://` 开头的临时 URL（有效期 48 小时）；  
- 在模型请求中传入该 URL 时，**必须添加请求头 `X-DashScope-OssResourceResolve: enable`**；  
- 生产环境强烈建议使用 OSS 等长期存储，而非临时 URL —— 参见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

### 4. 连接优化
- Java SDK：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize`, `readTimeout`）；  
- Python SDK：同步调用使用 `requests.Session`，异步调用使用 `aiohttp.ClientSession` + `TCPConnector`，显式传入 `session` 参数。

### 5. 安全凭证
- 不可信端（如浏览器、App）应通过后端服务调用 `/api/v1/tokens` 接口生成临时 API Key（TTL 可设 1–1800 秒），避免永久密钥泄露 —— 详见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

## 限制和注意事项

- **异步任务保留期**：任务完成后通常保留 24 小时，超时后自动清理，查询接口将返回 `UNKNOWN` 状态；  
- **临时文件限制**：单文件 ≤ 1 GB；上传限流为 **100 QPS（按主账号+模型维度）**；`oss://` URL 仅限同主账号、同模型使用，且不可下载/修改；  
- **临时 API Key**：无法手动删除，到期自动失效；继承父 Key 全部权限（含模型/知识库访问控制）；  
- **连接复用警告**：Python 同步调用中若未正确关闭 `requests.Session`，可能导致连接泄漏；Java SDK 中 `maximumAsyncRequests` 应 ≤ `connectionPoolSize`，否则可能阻塞；  
- **地域与 Endpoint 绑定**：北京、新加坡等地域的 API Key 与 Endpoint 严格对应，混用将导致鉴权失败；  
- **生产环境规避项**：临时 URL、文件上传接口、未配置连接池的高并发调用均**不适用于生产环境**，文档中已多次强调（如 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 中“请勿用于生产环境”）。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)


