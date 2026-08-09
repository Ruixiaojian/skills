# [more](more.md) about models

百炼平台提供丰富的模型调用能力，涵盖同步/异步接口、多地域支持、子空间隔离、文件上传、限额管理及连接优化等核心功能。本文面向开发者，系统梳理模型服务的关键能力、参数配置、使用方式及限制条件，帮助您高效、安全地集成大模型能力。

## 支持的模型/功能

百炼平台支持多种模态和能力的模型，包括文本生成（TG）、视觉理解（VU）、图像生成（IG）、视频生成（VG）、语音识别（ASR）等。可通过 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 接口按作者（如 `qwen`、`wan`）、能力（如 `function-calling`、`web-search`）、上下文长度或部署模式筛选可用模型，并获取其定价、输入/输出模态及 `context_window` 等元信息。部分模型（如图像、视频生成类）采用异步调用机制，需通过任务 ID 查询结果或取消任务；异步任务状态支持 PENDING、RUNNING、SUCCEEDED、FAILED 等完整生命周期管理。此外，[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 支持权限隔离与分账，适用于多租户或精细化管控场景。

> **注意**：文档 4 中提到“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，无需模型调用授权”，但该描述与权限模型实际逻辑存在偏差——调优模型仍需在子空间中显式授权方可调用，否则会返回 `Forbidden` 错误。请以控制台实际权限配置为准。

## 关键参数

- **API Key 与地域绑定**：各地域（北京、新加坡、弗吉尼亚等）API Key 相互独立，不可混用；调用时必须匹配对应地域的 Endpoint（如北京为 `https://dashscope.aliyuncs.com/api/v1/...`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/...`）。  
- **异步任务 TTL**：临时 API Key 默认有效期 60 秒，可通过 `expire_in_seconds` 参数设置，范围为 `[1, 1800]` 秒，详见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **文件上传约束**：上传文件时必须指定 `model_name`，且后续调用必须使用同一模型；临时 URL 有效期固定为 48 小时，且调用时必须在 Header 中添加 `X-DashScope-OssResourceResolve: enable`。  
- **连接复用参数**：Java SDK 默认启用连接池，关键参数包括 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）；Python SDK 需手动传入 `requests.Session` 或 `aiohttp.ClientSession` 实现复用。

## 使用方式

- **同步调用**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-mode/v1/chat/completions`）或 DashScope 原生接口（如 `/api/v1/services/aigc/text-generation/generation`），需配置 `base_url` 和 `Authorization` Header。  
- **异步调用**：先提交任务获取 `task_id`，再通过 [查询异步任务结果接口](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 轮询，或更优地配置 [HTTP回调URL或MQ接收通知](../../raw/model-api-reference/more-about-models/async-task-api.md) 避免轮询限流。  
- **文件上传**：调用 `/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证，再 POST 至 OSS Host，最终获得 `oss://...` 格式 URL。  
- **限额与模型发现**：通过 `/api/v1/quotas` 查询各模型 QPS/RPM 及 TPM 用量限制；通过 `/api/v1/models` 动态获取模型列表及能力详情，支撑运行时模型选型。

## 限制和注意事项

- **临时资源时效性**：临时 API Key 和文件 URL 均为短期凭证，**严禁用于生产环境长期服务**；生产环境应使用稳定存储（如 OSS）和永久 API Key。  
- **限流严格**：文件上传凭证接口限流 100 QPS（按主账号+模型维度），异步任务查询/取消接口限流 20 QPS（按主账号维度），超限将直接失败。  
- **权限与归属约束**：上传文件与调用 API 的 API Key 必须属于同一阿里云主账号；子业务空间的模型调用仅限该空间 API Key，且标准模型需单独授权。  
- **连接复用实践**：Java SDK 连接池大小建议根据并发量调整（如高并发场景设为 256），但 `maximumAsyncRequestsPerHost` 不得超过 `connectionPoolSize`；Python 同步调用推荐使用 `with requests.Session()` 确保资源释放。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


