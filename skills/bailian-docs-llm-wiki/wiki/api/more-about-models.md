# [more](more.md) about models

百炼平台提供丰富的模型调用能力，涵盖标准大模型、[多模态](../concepts/multimodal.md)模型、图像/视频生成模型及领域专用模型。本文档面向开发者，系统梳理模型服务的核心能力、关键参数、调用方式及使用约束，帮助您高效、安全地集成模型能力。

## 支持的模型与功能

百炼平台支持多种模型类型和能力，可通过统一接口查询和管理：

- **模型发现**：调用 `GET /api/v1/models` 接口可按作者（如 `qwen`, `deepseek`）、模态（如 `TG` 文本生成、`VU` 视觉理解）、能力（如 `function-calling`, `web-search`）等维度筛选可用模型，并获取上下文长度、定价等元信息 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)。
- **模型限额**：通过 `GET /api/v1/quotas` 可实时查询当前 API Key 下各模型的 QPS/RPM 请求限流及 TPM 用量限制，用于容量规划和异常排查 [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)。
- **异步任务支持**：图像生成、视频生成等长耗时模型采用异步机制，需先创建任务再轮询或接收通知。平台提供统一的异步任务管理 API，支持查询单个/批量任务状态及取消排队中的任务 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **事件驱动通知**：为避免轮询开销，推荐通过事件总线配置 HTTP 回调 URL 或 RocketMQ 消息队列，接收 `dashscope:System:AsyncTaskFinish` 事件，实现任务完成后的即时响应 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

> **注意**：文档 6 中列出的 `/api/v1/quotas` 请求地址存在错误——其“请求地址”表格中误将 `/api/v1/quotas` 的 Endpoint 写为 `/api/v1/models`（与文档 5 的模型列表接口相同）。正确地址应为 `/api/v1/quotas`，例如北京地域为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/quotas`。请以实际接口文档为准。

## 关键参数

模型调用涉及多个核心参数，需根据场景合理配置：

- **身份认证**：
  - 永久 API Key：用于服务端可信环境，需在控制台创建并配置为 `DASHSCOPE_API_KEY` 环境变量。
  - 临时 API Key：适用于浏览器、App 等不可信前端，通过后端调用 `/api/v1/tokens` 生成，有效期 1–1800 秒，继承源 Key 全部权限 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **地域与端点**：不同地域（北京、新加坡、弗吉尼亚等）Endpoint 不同，且 API Key 不互通。子业务空间调用需使用该空间专属 API Key，并匹配对应地域的 base_url（如新加坡需带 `{WorkspaceId}`）。
- **连接复用**：高并发场景下，Java SDK 默认启用连接池，Python SDK 支持传入 `requests.Session` 或 `aiohttp.ClientSession` 复用连接，显著降低资源消耗 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。
- **文件上传**：[多模态](../concepts/multimodal.md)模型需传入文件 URL。平台提供免费临时 OSS 存储，上传时必须指定 `model_name`（如 `qwen-vl-plus`），且文件仅对该模型有效，有效期 48 小时 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

## 使用方式

模型调用支持多种协议和 SDK：

- **[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**：适用于 `qwen-plus` 等标准模型，兼容主流 OpenAI SDK。需设置 `base_url`（北京为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`），并确保使用目标业务空间的 API Key。
- **DashScope 原生接口**：适用于所有模型（包括调优部署模型），调用路径更短（如文本生成为 `/api/v1/services/aigc/text-generation/generation`）。子业务空间调用需显式配置 `base_url` 或使用 WorkspaceId 构建 Endpoint。
- **异步调用流程**：
  1. 调用模型创建异步任务，获取 `task_id`；
  2. 通过 `GET /api/v1/tasks/{task_id}` 查询结果，或配置事件总线接收推送；
  3. 对于 PENDING 任务，可调用 `POST /api/v1/tasks/{task_id}/cancel` 主动取消。

## 限制和注意事项

- **临时文件与模型绑定**：上传文件时指定的 `model_name` 必须与后续模型调用一致，跨模型无法共享；文件与主账号强绑定，不可跨账号访问；48 小时后自动清理，**严禁用于生产环境**，生产环境应使用阿里云 OSS [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **临时 API Key 无手动删除**：其生命周期由 TTL 决定，到期自动失效，无法提前撤销。
- **子业务空间权限隔离**：调用标准模型（如 `qwen-plus`）需在子空间中单独授权；而调优部署的模型仅能被其所在业务空间的 API Key 调用，且不支持 OpenAI 兼容方式。
- **限流与配额**：文件上传凭证接口限流 100 QPS（按主账号+模型维度），异步任务查询接口限流 20 QPS，均不支持扩容。务必在代码中实现重试退避逻辑。
- **地域一致性**：API Key、Endpoint、临时文件上传地址、异步任务查询地址必须属于同一地域，混用将导致认证失败或资源不可达。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)


