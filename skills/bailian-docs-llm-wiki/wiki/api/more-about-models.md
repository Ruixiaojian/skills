# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型服务的核心能力与使用规范，涵盖模型调用方式、关键参数配置、资源管理机制及常见限制。内容基于官方 API 行为与 SDK 实现，不包含营销性描述，所有技术细节均以可验证的接口契约为准。

## 支持的模型与功能

百炼平台支持两类模型调用路径：**标准模型**（如 `qwen-plus`、`qwen-vl-plus`）和**用户调优后部署的私有模型**。标准模型需在业务空间中显式授权方可调用；而调优模型仅限其所属业务空间的 API Key 访问，且**不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，必须通过 DashScope 原生接口调用 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

多模态任务（图像、视频、音频生成等）普遍采用**异步模式**：先提交任务获取 `task_id`，再轮询或通过事件总线接收完成通知。异步任务支持查询单个结果、批量状态检索及取消（仅限 `PENDING` 状态）[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

对于文件输入场景（如 VL 模型），需先将本地文件上传至百炼临时存储，获取 `oss://` 开头的临时 URL（有效期 48 小时），并在后续模型请求中通过 `X-DashScope-OssResourceResolve: enable` 请求头启用解析 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 2 中称“调用在阿里云百炼调优并部署的模型，无需模型调用授权”，但文档 2 同时明确要求“使用该子业务空间的 API Key”。这与权限模型逻辑一致——调优模型的访问控制粒度是业务空间级而非模型级，因此“无需额外授权”指无需在权限中心单独勾选模型，但业务空间绑定仍是强制前提。

## 关键参数

- **临时 API Key**：通过 `POST /api/v1/tokens` 接口生成，`expire_in_seconds` 参数控制 TTL（1–1800 秒），默认 60 秒。临时 Key 继承父 Key 的全部权限（含模型/[知识库](../concepts/knowledge-base.md)访问限制）[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **异步任务 ID**：所有异步接口（创建、查询、取消）均以 `task_id` 为唯一标识，该 ID 由任务创建响应返回，不可自定义。
- **连接复用参数**：
  - Java SDK：通过 `Constants.connectionConfigurations` 配置 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）等，需确保后者 ≤ 前者；
  - Python SDK：同步调用传入 `requests.Session`，异步调用传入 `aiohttp.ClientSession` 并配置 `TCPConnector` 的 `limit` 和 `limit_per_host`。

## 使用方式

### 调用入口
- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：适用于标准模型，Base URL 因地域而异：
  - 北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **DashScope 原生接口**：适用于所有模型（含调优模型），Base URL 同样按地域区分，且新加坡地域需显式配置 `WorkspaceId`。

### 文件处理流程
1. 调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证；
2. 使用凭证将文件 POST 至 OSS Host，获得 `oss://...` URL；
3. 在模型请求中传入该 URL，并在 Header 中添加 `X-DashScope-OssResourceResolve: enable`。

### 异步通知机制
为避免轮询限流（20 QPS），推荐通过 **事件总线 EventBridge** 接收 `dashscope:System:AsyncTaskFinish` 事件。支持两种目标：
- HTTP 回调：需公网/VPC 可达，事件 Body 包含 `task_id` 和 `task_status`；
- RocketMQ：提供消息可靠性保障，适合金融等高一致性场景。

## 限制和注意事项

- **临时文件**：上传与模型强绑定（`model_name` 必须一致），且仅限同一主账号下使用；48 小时过期，**严禁用于生产环境**；上传接口限流 100 QPS（按“主账号+模型”维度），超限直接失败。
- **临时 API Key**：无法手动删除，到期自动失效；各地域 API Key 不互通，调用时需匹配对应地域 Endpoint。
- **异步任务**：任务结果保留 24 小时（具体以模型文档为准）；`CANCEL` 接口仅对 `PENDING` 状态有效，其他状态返回 `UnsupportedOperation` 错误码。
- **连接复用**：Python 同步调用中若复用 `requests.Session`，需显式调用 `session.close()` 或使用 `with` 语句；Java SDK 连接池参数需协同调整，例如 `maximumAsyncRequestsPerHost` 应 ≤ `maximumAsyncRequests`。

> **注意**：文档 5 多次强调“临时 URL 请勿用于生产环境”，而文档 6 的连接复用示例代码中，Python 异步示例使用了硬编码的北京地域 URL（`dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'`）。该写法在跨地域部署时会导致请求失败，实际应根据 WorkspaceId 动态构造 URL，参考文档 2 中新加坡地域的配置方式。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


