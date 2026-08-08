# [more](more.md) about models

阿里云百炼平台提供多样化的模型服务，涵盖大语言模型、多模态模型、语音与图像生成等。本文档面向开发者，系统梳理模型调用的核心能力、关键参数配置、使用方式及限制条件，帮助您高效、安全地集成百炼模型能力。所有功能均需配合有效的 API Key 使用，且部分能力（如异步任务、子业务空间）需满足特定前提条件。

## 支持的模型/功能

百炼平台支持按模态、能力、作者等多维度筛选和查询模型。通过 `GET /api/v1/models` 接口可获取实时模型列表，返回信息包括模型 ID、上下文长度、输入/输出模态、定价详情及支持的能力（如 `function-calling`、`structured-outputs`、`web-search` 等）[查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)。模型覆盖文本生成（TG）、视觉理解（VU）、图像生成（IG）、视频生成（VG）、语音识别（ASR）等多种能力，并支持全球、国际、中国大陆等不同部署模式。

对于需要精细化权限管控或分账的场景，可使用**子业务空间**调用模型：将 RAM 用户加入指定子空间，为其分配专属 API Key 和模型调用权限，实现资源隔离与费用独立核算 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。此外，平台支持为不可信前端环境（如浏览器、移动 App）生成**临时 API Key**，其有效期可设为 1–1800 秒，继承父 Key 的全部权限，有效规避永久密钥泄露风险 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

> **注意**：文档 7 中 `/api/v1/quotas` 接口的请求地址示例错误地复用了 `/api/v1/models` 的 Endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models`），实际应为 `/api/v1/quotas`。正确地址示例：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/quotas`。

## 关键参数

- **模型标识**：调用时必须指定 `model` 参数（模型 ID，如 `qwen3-max` 或 `wanx2.1-t2i-turbo`），该值需与上传文件时指定的 `model_name` 严格一致，否则文件无法解析。
- **异步任务控制**：对图像、视频等长耗时任务，需通过 `task_id` 轮询或事件通知获取结果；任务状态包括 `PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED` 等。
- **连接复用参数**：Java SDK 可配置 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）等连接池参数；Python SDK 支持传入 `aiohttp.ClientSession` 或 `requests.Session` 实现复用 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。
- **文件上传约束**：上传文件时必须携带 `model` 查询参数，且后续模型调用必须使用同一模型；临时 URL 有效期为 48 小时，调用时需在 Header 中显式添加 `X-DashScope-OssResourceResolve: enable`。

## 使用方式

1. **同步调用**：适用于低延迟文本类模型（如 `qwen-plus`），直接通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope 原生接口发起请求，返回结果即时可用。
2. **异步调用**：适用于图像生成、视频合成等长耗时任务。需先调用模型 API 获取 `task_id`，再通过 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 查询结果或取消任务（仅限 `PENDING` 状态）。为避免轮询限流（20 QPS），推荐配置事件总线接收 HTTP 回调或 RocketMQ 消息通知 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。
3. **文件上传**：调用多模态模型前，需先通过 `POST /api/v1/uploads?action=getPolicy` 获取上传凭证，再上传至 OSS 并获得 `oss://` 格式临时 URL；该 URL 必须在模型请求中作为输入参数传递。
4. **限额与配额管理**：通过 `GET /api/v1/quotas` 查询各模型的 QPS/RPM 和 TPM 用量限制，用于容量规划与异常诊断。

## 限制和注意事项

- **文件限制**：单文件上传上限为 1 GB；临时 URL 有效期 48 小时，**严禁用于生产环境**；上传限流为 100 QPS（按主账号+模型维度），不可扩容 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **异步任务限制**：任务结果保留 24 小时（具体以对应模型文档为准）；仅 `PENDING` 状态任务可取消；批量查询接口支持按时间范围、状态、模型名等条件过滤。
- **安全限制**：临时 API Key 不可手动删除，到期自动失效；子业务空间内调优部署的模型**仅支持 DashScope 原生调用，不兼容 OpenAI 接口**。
- **地域与 Endpoint**：子业务空间调用需使用对应地域的 Endpoint（如北京为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`），且 API Key 必须与业务空间所属地域匹配。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)


