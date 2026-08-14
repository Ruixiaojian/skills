# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的核心能力与约束。涵盖模型发现与权限管理、[异步任务](../concepts/async-task.md)处理、文件上传、连接优化等关键环节，所有内容均基于平台当前 API 行为，不包含营销性描述。

## 支持的模型/功能

百炼平台提供多模态、文本、语音、图像、视频等全栈模型服务，支持标准模型调用、子业务空间隔离、模型权限精细化管控及限额配置。可通过 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 接口（`GET /api/v1/models`）按能力（如 `TG` 文本生成、`IG` 图片生成）、供应商（如 `qwen`、`kling`）、部署模式等维度动态发现可用模型，并获取上下文长度、定价等元信息。模型权限需显式授予：子业务空间中调用标准模型前，必须通过 [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md) 或控制台完成推理权限配置；而调优后部署的模型则仅限其所在空间的 API Key 调用，无需额外授权。

> **注意**：文档 4 明确指出“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但文档 9 的接口说明和示例中均未体现此例外逻辑，实际调用时应以运行时行为为准，建议优先参考控制台权限配置状态。

[异步任务](../concepts/async-task.md)是图像生成、视频合成等长耗时模型的标准交互模式，平台提供统一的[异步任务](../concepts/async-task.md)管理 API，支持创建、单查、批量查询及取消任务。此外，为降低轮询开销，平台支持通过事件总线（EventBridge）主动推送任务完成通知，可配置 HTTP 回调或 RocketMQ 消息队列接收事件，详见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

## 关键参数

- **临时 API Key**：用于不可信环境（如浏览器、App），通过 `POST /api/v1/tokens` 生成，默认 TTL 60 秒，最大 1800 秒（30 分钟），继承源 API Key 全部权限。
- **异步任务 ID**：所有异步任务返回唯一 `task_id`，后续查询或取消操作均以此为标识。
- **文件 URL**：调用多模态模型需传入文件 URL，平台提供免费临时 OSS 存储，上传后返回 `oss://` 格式 URL，有效期 48 小时，且**必须**在请求头中添加 `X-DashScope-OssResourceResolve: enable` 才能被模型服务解析。
- **连接复用参数**：Java SDK 默认启用连接池，关键参数包括 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）；Python SDK 需手动传入 `requests.Session` 或 `aiohttp.ClientSession`，推荐配置 `limit_per_host` 避免对单一域名压测。

## 使用方式

1. **模型调用**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)时，Base URL 因地域和业务空间而异。北京地域默认空间为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡地域子空间需替换为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`。务必使用目标空间的 API Key。
2. **异步任务**：先调用对应模型的创建接口（如文生图），获取 `task_id`；再通过 `GET /api/v1/tasks/{task_id}` 查询结果。高并发场景下，应优先采用事件总线回调方案，避免轮询触发 20 QPS 限流。
3. **文件上传**：调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证，再将文件 POST 至凭证中的 `upload_host`。上传与模型调用必须使用同一主账号的 API Key，且 `model_name` 必须严格一致。
4. **权限与限额管理**：
   - 查询当前空间已授权模型：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED`
   - 查询各模型实时限额：`GET /api/v1/models/limits`
   - 更新单个或多个模型的 QPM/TPM：`POST /api/v1/models/limits`，支持 `OVERLAY`（覆盖）和 `DELETE`（清空）操作。

## 限制和注意事项

- **临时文件存储**：`oss://` URL 仅限 48 小时，且上传接口限流为 100 QPS（按主账号+模型维度），**严禁用于生产环境或压测**。生产环境请使用阿里云 OSS 等持久化存储。
- **异步任务保留期**：任务完成后数据默认保留 24 小时，超时后自动清理，无法查询。
- **API Key 地域隔离**：北京、新加坡、弗吉尼亚等地域的 API Key 互不通用，调用前需确认 Endpoint 与 API Key 匹配。
- **子空间模型调用**：必须使用该子空间生成的 API Key，且标准模型需提前授权；调优模型仅限本空间调用。
- **连接复用**：Java SDK 连接池参数 `maximumAsyncRequestsPerHost` 必须 ≤ `maximumAsyncRequests`，否则可能引发请求阻塞；Python 同步调用中，`requests.Session` 应复用而非每次新建。

> **注意**：文档 5 明确警告“文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景**”，而文档 2 中异步任务查询接口的限流为 20 QPS，两者量级差异显著，在设计高并发文件上传+任务提交链路时，必须将文件上传作为前置批处理步骤，避免与任务查询共享同一限流通道。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)
- [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)
- [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)
- [查询模型权限](../../raw/model-api-reference/more-about-models/list-model-permissions.md)


