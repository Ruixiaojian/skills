# [more](more.md) about models

百炼平台提供丰富的模型能力与配套基础设施，涵盖同步/异步调用、文件上传、权限隔离、连接优化及配额管理等关键环节。本文面向开发者，系统梳理模型使用的核心路径与约束条件，帮助您高效、安全地集成模型服务。

## 支持的模型与功能

百炼支持多模态、文本生成、语音识别、图像/视频生成等全栈模型，可通过 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 接口按作者（如 `qwen`、`deepseek`）、能力（如 `TG`、`IG`、`VG`）、部署模式等维度筛选，并获取上下文长度、定价及输入/输出模态等元信息。部分模型（如图像生成、视频生成）采用异步调用机制，需通过 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 创建任务、轮询或取消任务；同时支持通过事件总线配置 HTTP 回调或 RocketMQ 接收任务完成通知，避免高频轮询。

> **注意**：文档 7 和文档 8 中的 Endpoint 地址存在不一致——文档 7 的“北京地域”Endpoint 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models`，而文档 8 的“北京地域”Endpoint 错误地写为相同路径（应为 `/api/v1/quotas`）。实际调用时请以接口路径为准：模型列表用 `/api/v1/models`，限额查询用 `/api/v1/quotas`。

## 关键参数

- **临时 API Key**：用于不可信环境（如浏览器、App），通过 `POST /api/v1/tokens?expire_in_seconds=1800` 生成，TTL 范围为 `[1, 1800]` 秒，继承源 Key 全部权限。详见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **临时文件 URL**：上传文件需指定 `model_name`，生成 `oss://` 前缀 URL，有效期 48 小时；调用时必须在 Header 中添加 `X-DashScope-OssResourceResolve: enable`。
- **[异步任务](../concepts/asynchronous-task.md)状态**：`task_status` 取值包括 `PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`、`CANCELED`、`UNKNOWN`；仅 `PENDING` 状态可取消。
- **连接复用参数**：Java SDK 可配置 `connectionPoolSize`、`maximumAsyncRequests` 等；Python SDK 支持传入 `aiohttp.ClientSession` 或 `requests.Session` 复用连接。

## 使用方式

- **模型调用**：支持 DashScope 原生协议与 OpenAI 兼容协议。子业务空间调用需使用该空间专属 API Key，并配置对应地域的 `base_url`（如北京为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡需替换 `{WorkspaceId}`）。
- **文件上传**：先调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证，再直传至 OSS；上传后 URL 仅限同模型、同主账号调用。
- **异步结果获取**：通过 `GET /api/v1/tasks/{task_id}` 查询单任务，或 `GET /api/v1/tasks/` 批量查询（支持按 `model_name`、`status`、时间范围等过滤）。
- **连接优化**：高并发场景下，Java SDK 默认启用连接池，建议根据 QPS 调整 `connectionPoolSize`；Python SDK 推荐使用 `with requests.Session()` 或 `aiohttp.ClientSession` 显式管理连接生命周期。

## 限制和注意事项

- **临时资源时效性**：临时 API Key 最长 30 分钟；临时文件 URL 仅 48 小时有效，**严禁用于生产环境**；生产环境应使用阿里云 OSS 等持久化存储。
- **配额与限流**：
  - 文件上传凭证接口限流为 **100 QPS（按主账号+模型维度）**，超限即失败；
  - [异步任务](../concepts/asynchronous-task.md)查询接口限流为 **20 QPS（按主账号）**；
  - 各模型具体 QPS/RPM、TPM 限额可通过 [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md) 接口获取。
- **权限与隔离**：子业务空间的模型调用需单独授权（标准模型）或仅限本空间 API Key 调用（调优模型）；临时 API Key 权限继承自源 Key，无细粒度控制。
- **地域与 Endpoint**：各地域 API Key 不互通；调用前务必确认 Endpoint 与密钥地域匹配（如北京密钥不可用于新加坡 Endpoint）。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)


