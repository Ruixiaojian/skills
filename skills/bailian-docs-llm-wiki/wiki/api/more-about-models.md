# [more](more.md) about models

百炼平台提供丰富的模型调用能力，涵盖同步/异步调用、多地域支持、子[业务空间隔离](../concepts/workspace-isolation.md)、连接复用优化及资源限额管理等核心能力。本文档面向开发者，系统梳理模型使用的关键路径与约束条件，帮助您高效、安全地集成百炼模型服务。

## 支持的模型/功能

百炼平台支持多种模态和能力的模型，包括文本生成（TG）、深度推理（Reasoning）、视觉理解（VU）、图像/视频生成（IG/VG）、语音识别（ASR）等。可通过 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 接口按 `providers`、`capabilities`、`features` 等维度筛选，并获取上下文长度、定价、输入/输出模态等元信息。所有标准模型均需在对应业务空间中显式授权后方可调用；而用户在百炼平台调优并部署的私有模型，则**仅限其所在业务空间的 API Key 调用**，且无需额外授权 [原文标题](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

部分计算密集型模型（如图像生成、视频生成）采用异步调用机制，需先创建任务获取 `task_id`，再通过 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 查询结果或取消任务。异步任务默认保留 24 小时（具体以各模型文档为准），超时后自动清理。

> **注意**：文档 8 中 `/api/v1/quotas` 的请求地址示例错误地复用了 `/api/v1/models` 的 Endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models`），实际应为 `/api/v1/quotas`。正确地址格式为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/quotas` —— 请以 [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md) 文档的接口定义为准。

## 关键参数

- **API Key 管理**：生产环境推荐使用临时 API Key 避免密钥泄露。临时 Key 继承生成者的全部权限，有效期 TTL 可设为 1–1800 秒，通过 `POST /api/v1/tokens?expire_in_seconds=1800` 获取 [原文标题](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **文件上传**：调用[多模态](../concepts/multi-modal.md)模型需上传本地文件获取临时 URL（`oss://...`），该 URL 有效期固定为 48 小时，且必须在请求头中显式添加 `X-DashScope-OssResourceResolve: enable` 才能被解析。
- **地域与 Endpoint**：不同地域使用独立 Endpoint（如北京、新加坡、弗吉尼亚），子业务空间调用需替换 `{WorkspaceId}`；OpenAI 兼容模式在北京地域使用 `https://dashscope.aliyuncs.com/compatible-mode/v1`，在新加坡地域则需使用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`。
- **连接复用**：高并发场景下，Java SDK 默认启用连接池，可配置 `connectionPoolSize`、`maximumAsyncRequests` 等参数；Python SDK 支持传入 `requests.Session`（同步）或 `aiohttp.ClientSession`（异步）实现复用 [原文标题](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 使用方式

1. **模型调用**：  
   - 标准模型调用需确保 API Key 已获对应模型权限（子业务空间需单独授权）；  
   - 子业务空间模型必须使用该空间的 API Key，并按地域选择正确 Endpoint；  
   - [多模态](../concepts/multi-modal.md)输入需先调用 `/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证，再上传至 OSS 并构造 `oss://` URL。

2. **异步任务处理**：  
   - 创建任务后，可通过 `GET /api/v1/tasks/{task_id}` 单查，或 `GET /api/v1/tasks/` 批量查询；  
   - 为避免轮询限流（20 QPS），推荐通过 [事件总线 EventBridge](../../raw/model-api-reference/more-about-models/async-task-api.md) 配置 HTTP 回调或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，再按需查询结果。

3. **限额与监控**：  
   - 调用 `GET /api/v1/quotas` 可实时查看各模型的 QPS/RPM 和 TPM 用量限制；  
   - 异步任务的 `async_user_queue_limit` 和 `async_user_concurrency_limit` 字段直接反映排队与并发上限。

## 限制和注意事项

- **临时文件存储**：`oss://` URL 仅限 48 小时，且绑定模型与主账号，不可跨模型/跨账号复用；上传接口限流为 100 QPS（按“主账号+模型”维度），**严禁用于生产环境或压测**，生产环境应使用阿里云 OSS [原文标题](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **临时 API Key**：无法手动删除，到期自动失效；其权限完全继承自生成者，务必谨慎控制生成 Key 的权限范围。
- **异步任务取消**：仅支持取消 `PENDING` 状态的任务，`RUNNING` 或已完成状态不可取消。
- **连接复用最佳实践**：Java SDK 中 `maximumAsyncRequests` 不应超过 `connectionPoolSize`；Python 同步调用建议用 `with requests.Session()` 确保资源释放。
- **地域一致性**：API Key、Endpoint、文件上传凭证、异步任务查询均需严格匹配同一地域（北京/新加坡/弗吉尼亚等），跨地域调用将失败。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)


