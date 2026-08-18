# [more](more.md) about models

百炼平台提供丰富的模型调用能力与配套管理接口，涵盖模型发现、权限控制、限流配置、异步任务处理、文件上传、连接优化及安全凭证生成等核心场景。本文面向开发者，系统梳理关键能力、参数含义、使用方式及实践约束，帮助构建稳定、高效、可运维的模型服务集成。

## 支持的模型/功能

百炼平台支持多模态、文本、图像、视频、语音等全类型模型，并可通过标准 API 查询其元信息与能力特征。调用前需确认模型在当前业务空间中已获授权（见[查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md)），且符合地域与部署模式要求。

- **模型发现**：通过 `GET /api/v1/models` 接口可按模态（如 `TG` 文本生成、`IG` 图片生成）、能力（如 `function-calling`、`web-search`）、供应商（如 `qwen`、`zhipu-ai`）等维度筛选可用模型，并获取上下文长度、定价、输入/输出模态等关键元数据 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)。
- **模型授权管理**：子业务空间需显式授权方可调用标准模型（如 `qwen-plus`），调优后部署的模型则仅限其所在空间调用；授权状态可通过 `GET /api/v1/models/permissions` 查询，也可通过 `POST /api/v1/models/permissions` 批量更新 [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)。
- **异步任务支持**：图像生成、视频合成等长耗时模型强制采用异步模式，需先创建任务获取 `task_id`，再轮询或订阅事件获取结果。平台提供统一的异步任务管理接口，支持单查、批量查询及取消排队中任务 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

> **注意**：文档 3 中提到“任务完成后立即推送”HTTP 回调通知，但文档 2 明确指出“异步任务在完成后通常保留 24 小时”，而文档 4 要求临时文件“48 小时内完成模型调用”。三者有效期不一致，实际集成时应以具体任务类型文档为准，通用策略为：回调通知用于触发查询，查询动作必须在任务保留期内完成（≤24h），且所依赖的临时资源（如文件 URL）须仍在有效期内（≤48h）。

## 关键参数

以下参数在模型调用与管理中高频出现，直接影响行为与性能：

- **`model`（模型 ID）**：必需，用于指定目标模型（如 `qwen3-max`、`wan2.6-i2v-flash`），必须与上传文件时声明的模型一致（见[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)）。
- **`task_id`**：异步任务唯一标识，用于查询状态与结果，由任务创建接口返回。
- **`workspace_id`**：业务空间 ID，用于构造地域化 Endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），子空间调用必须使用其专属 API Key 与 Workspace ID。
- **限流参数**：
  - `request_limit` / `request_limit_period`：请求频率限制（如 `500` 次/秒 或 `2` 次/分钟）。
  - `usage_limit` / `usage_limit_field` / `usage_limit_period`：用量限制（如 `500000` tokens/6 秒）。
  - `async_user_queue_limit` / `async_user_concurrency_limit`：异步任务队列与并发上限。
  这些参数可通过 `GET /api/v1/models/limits` 查询，`POST /api/v1/models/limits` 更新 [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)。

## 使用方式

### 1. 凭证与环境
- 生产环境应使用长期有效的 API Key 并配置为 `DASHSCOPE_API_KEY` 环境变量。
- 在浏览器或移动 App 等不可信环境，**必须**通过后端服务生成临时 API Key（TTL 1–1800 秒），避免永久密钥泄露 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 2. 文件上传
- 多模态模型需传入文件 URL，可调用 `/api/v1/uploads?action=getPolicy&model={model}` 获取 OSS 上传凭证，再上传至临时存储，获得 `oss://` 前缀的 URL（有效期 48 小时）。
- **关键约束**：上传时指定的 `model` 必须与后续模型调用的 `model` 完全一致；调用时需在 Header 中添加 `X-DashScope-OssResourceResolve: enable`。

### 3. 异步任务通知
- 避免高频轮询（受限于 20 QPS），推荐配置事件总线（EventBridge）接收 `dashscope:System:AsyncTaskFinish` 事件，通过 HTTP 回调或 RocketMQ 主动推送任务完成通知 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 4. 连接复用
- 高并发场景下，应启用 SDK 连接池：
  - Java SDK：通过 `Constants.connectionConfigurations` 配置 `connectionPoolSize`、超时等参数。
  - Python SDK：传入自定义 `requests.Session`（同步）或 `aiohttp.ClientSession`（异步）实现复用 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 限制和注意事项

- **临时资源时效性**：临时 API Key 最长 1800 秒，临时文件 URL 有效期固定为 48 小时，均不可续期。生产环境严禁直接使用，应使用 OSS 等持久化存储。
- **地域与 Endpoint 绑定**：各地域（北京、新加坡、弗吉尼亚等）API Key 不互通，Endpoint 地址亦不同，调用前务必核对 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 中的地域说明。
- **限流维度**：文件上传凭证接口限流为 **100 QPS（按主账号+模型）**，异步任务查询接口为 **20 QPS（按主账号）**，模型调用限流则按 `model_limit` 和 `workspace_limit` 双层控制，超出将返回 `Throttling.RateQuota` 错误。
- **子空间调用约束**：调用子业务空间模型时，必须使用该空间生成的 API Key，且 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)的 `base_url` 需替换为对应 Workspace ID 的域名（如 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`）。
- **权限继承**：临时 API Key 继承生成它的永久 Key 的全部权限（含模型与知识库访问限制），无法做细粒度降权。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)


