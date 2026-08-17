# [more](more.md) about models

百炼平台提供丰富的模型管理与调用能力，涵盖模型发现、权限控制、限流配置、异步任务处理、文件上传、连接优化及安全凭证管理等核心场景。本文面向开发者，系统梳理关键能力、参数含义、使用方式及实践约束，帮助构建稳定、高效、可运维的模型服务集成方案。

## 支持的模型/功能

百炼平台支持[多模态](../concepts/multi-modal.md)、文本、语音、图像、视频、3D 等全类型模型，可通过统一接口查询和管理。  
- **模型发现**：调用 `GET /api/v1/models` 可按作者（`providers`）、能力（`capabilities`，如 `TG` 文本生成、`IG` 图片生成）、部署模式（`service_site`）等维度筛选，并获取上下文长度、定价、输入/输出模态等元信息 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)。  
- **模型授权控制**：子业务空间需显式授权方可调用标准模型（如 `qwen-plus`），而调优后部署的模型仅限其所在空间调用，无需额外授权 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  
- **异步任务支持**：图像生成、视频合成等长耗时任务采用异步模式，需先创建任务再轮询或订阅事件获取结果 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **文件上传与引用**：[多模态](../concepts/multi-modal.md)模型（如 `qwen-vl-plus`）需传入文件 URL；平台提供免费临时 OSS 存储，上传后返回 `oss://` 格式 URL（有效期 48 小时），调用时须在 Header 中添加 `X-DashScope-OssResourceResolve: enable` [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 4 明确指出“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但文档 9 和 10 的权限接口均将 `inference` 权限作为独立可配置项。实践中，调优模型虽不依赖该权限字段，但仍需确保调用方 API Key 所属空间与模型部署空间一致，权限接口返回的 `inference: true` 仅反映空间级访问许可状态，非强制校验条件。

## 关键参数

| 参数 | 说明 | 典型值 | 来源 |
|------|------|--------|------|
| `model` | 模型 ID，用于所有模型调用及管理接口 | `qwen-plus`, `wanx2.1-kf2v-plus` | [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) |
| `task_id` | 异步任务唯一标识，用于查询状态或接收回调通知 | `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `expire_in_seconds` | 临时 API Key 有效期（秒） | `1800`（30 分钟） | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `request_limit` / `usage_limit` | 模型限流配额（QPM / TPM） | `60`, `100000` | [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md) |
| `X-DashScope-OssResourceResolve` | 调用含 `oss://` URL 的[多模态](../concepts/multi-modal.md)模型时必需的 Header | `enable` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |

## 使用方式

- **模型调用**：  
  - 标准模型支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`base_url=https://dashscope.aliyuncs.com/compatible-mode/v1`）和 DashScope 原生 SDK；  
  - 子业务空间必须使用该空间专属 API Key，并确认已授予对应模型的 `inference` 权限；  
  - 多模态输入需先上传文件获取 `oss://` URL，再在请求中引用。  

- **异步任务处理**：  
  - 推荐使用 **HTTP 回调或 RocketMQ** 接收事件总线推送的任务完成通知（`dashscope:System:AsyncTaskFinish`），避免轮询限流（20 QPS） [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)；  
  - 若必须轮询，应使用 `GET /api/v1/tasks/{task_id}` 查询单任务，或 `GET /api/v1/tasks/` 批量查询，注意任务保留期通常为 24 小时。  

- **连接与性能优化**：  
  - Java SDK 默认启用连接池，可配置 `connectionPoolSize`（默认 32）、`maximumAsyncRequests` 等参数；  
  - Python SDK 支持传入 `requests.Session`（同步）或 `aiohttp.ClientSession`（异步）实现连接复用 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。  

- **权限与配额管理**：  
  - 查询当前空间已授权模型：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED`；  
  - 设置模型限流：`POST /api/v1/models/limits`（覆盖）或 `GET /api/v1/models/limits`（查询）；  
  - 临时凭证生成：`POST /api/v1/tokens?expire_in_seconds=1800`，适用于前端直连等不可信环境 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

## 限制和注意事项

- **临时资源时效性**：临时 API Key 默认 60 秒，最长 1800 秒；临时文件 URL 有效期严格为 48 小时，超时即失效，**禁止用于生产环境**；生产环境应使用 OSS 等长期存储 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)、[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **限流与配额**：  
  - 文件上传凭证接口限流为 100 QPS（按主账号+模型维度），不可扩容；  
  - 异步任务查询接口限流为 20 QPS（按账号维度）；  
  - 模型限流支持账号级（`model_limit`）与业务空间级（`workspace_limit`）两级配置，后者不能突破前者 [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)。  
- **地域与 Endpoint 差异**：北京、新加坡等地域的 API Key 不通用，Endpoint URL 也不同（如新加坡需带 `WorkspaceId` 和 `ap-southeast-1`）；临时 API Key 生成接口的 URL 需匹配地域 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **安全性**：临时 API Key 继承生成它的永久 Key 的全部权限（含知识库访问限制），且无法手动删除，仅能等待自动过期。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)


