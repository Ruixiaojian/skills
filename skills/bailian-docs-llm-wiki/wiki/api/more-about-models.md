# [more](more.md) about models

百炼平台提供丰富的模型调用能力与配套管理接口，涵盖模型发现、权限控制、限流配置、异步任务处理、文件上传、连接优化及安全凭证管理等核心场景。本文面向开发者，系统梳理关键能力、参数含义、使用方式及约束条件，帮助高效、稳定地集成模型服务。

## 支持的模型与功能

百炼平台支持[多模态](../concepts/multi-modal.md)、文本、语音、图像、视频等全类型模型，可通过标准 API 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用。所有可用模型可通过 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 接口动态获取，支持按能力（如 `TG` 文本生成、`IG` 图片生成）、供应商（如 `qwen`、`zhipu-ai`）、部署模式（`global`、`asia-pacific-china`）等多维度筛选，并返回上下文长度、定价、输入/输出模态等关键元信息。

模型调用需明确归属业务空间：默认业务空间的 API Key 可调用全部标准模型；若需精细化管控（如分账、权限隔离），应使用 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 方式——必须使用该子空间专属 API Key，并为标准模型显式配置调用权限（调优后部署的模型则自动授权且仅限本空间调用）。

对于[多模态](../concepts/multi-modal.md)模型（如 `qwen-vl-plus`），输入文件需先上传至百炼临时存储并获取 `oss://` URL。该 URL 有效期 48 小时，且**必须与目标模型绑定**（上传时指定 `model_name`），调用时还需在请求头中添加 `X-DashScope-OssResourceResolve: enable`。详细流程见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 5 明确指出“文件上传与模型调用所使用的 API Key 必须属于同一个阿里云主账号”，而文档 4 中子业务空间调用示例未强调此约束。实际开发中，子空间上传文件与调用模型的 API Key 必须同属一个主账号，否则将失败。

## 关键参数

- **限流参数（QPM/TPM）**：模型调用受请求频率（QPM）和用量（TPM）双重限制。可通过 [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md) 查看当前配额，通过 [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md) 动态调整。注意：设置 TPM 前必须已设置 QPM，否则会返回 `InvalidParameter` 错误。
- **异步任务参数**：图像/视频生成等长耗时任务采用异步模式，需通过 `task_id` 轮询或事件通知获取结果。轮询接口 `/api/v1/tasks/{task_id}` 有 20 QPS 限流；批量查询 `/api/v1/tasks/` 同样受限，且任务数据保留期通常为 24 小时（以具体模型文档为准）。
- **连接复用参数**：高并发场景下，Java SDK 默认启用连接池，可配置 `connectionPoolSize`、`readTimeout` 等；Python SDK 需传入自定义 `requests.Session` 或 `aiohttp.ClientSession` 实现复用，显著降低资源消耗。

## 使用方式

- **认证**：所有 API 均需在 `Authorization` Header 中携带 `Bearer {API_KEY}`。生产环境推荐使用 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 机制，在不可信客户端（如浏览器）中规避永久密钥泄露风险。临时 Key TTL 范围为 1–1800 秒，到期自动失效，不可手动删除。
- **异步任务结果获取**：除轮询外，推荐通过 [事件总线接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)，配置 HTTP 回调或 RocketMQ，避免轮询限流与资源浪费。回调事件中 `data.task_status` 和 `data.task_id` 是关键字段。
- **权限与限额管理**：模型调用前，需确认权限状态——[查询模型权限](../../raw/model-api-reference/more-about-models/list-model-permissions.md) 返回 `inference: true` 才可调用；限额不足时，需调用 [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md) 或 [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md) 接口调整。

## 限制和注意事项

- **临时文件限制**：上传接口限流为 100 QPS（按主账号+模型维度），且不支持扩容；文件大小上限 1 GB；48 小时后自动清理。**严禁用于生产环境或压测**，生产环境应使用 OSS 等持久化存储。
- **地域与 Endpoint 差异**：北京、新加坡等地域的 API Key 不通用；子业务空间调用需使用对应地域的 Endpoint（如新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`），且需替换 `{WorkspaceId}`。
- **异步任务生命周期**：任务完成后保留约 24 小时，超时后无法查询。轮询时需结合 `task_status`（`PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED`）判断状态，避免无效请求。
- **SDK 连接配置**：Java SDK 连接池默认参数（如 `connectionPoolSize=32`）在高并发场景下易成为瓶颈，建议根据实际负载调大 `connectionPoolSize` 和 `maximumAsyncRequests`；Python 同步调用务必复用 `requests.Session` 实例，否则每次调用新建连接开销巨大。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)
- [查询模型权限](../../raw/model-api-reference/more-about-models/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)


