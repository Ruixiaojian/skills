# [more](more.md) about models

阿里云百炼平台提供丰富的模型能力与配套管理接口，涵盖模型发现、权限控制、调用优化、异步任务处理及安全凭证管理等核心场景。本文面向开发者，系统梳理关键能力、参数含义、使用方式及实践约束，帮助您高效、稳定地集成模型服务。

## 支持的模型/功能

百炼平台支持多模态、文本、图像、视频、语音等全栈模型，可通过标准 API 查询可用模型列表及其元信息（如模态类型、上下文长度、定价、部署地域等）。调用 `GET /api/v1/models` 接口可按 `capabilities`（如 `TG` 文本生成、`IG` 图片生成）、`providers`（如 `qwen`、`kling`）、`service_site` 等维度筛选，并获取实时价格与规格详情 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)。

模型权限与限额需独立管理：  
- **权限**：子业务空间中调用标准模型（如 `qwen-plus`）前，必须通过 `GET /api/v1/models/permissions` 查询并确认已授权 `inference` 权限；而调优后部署的模型则无需额外授权，仅限其所在空间的 API Key 调用 [查询模型权限](../../raw/model-api-reference/more-about-models/list-model-permissions.md)。  
- **限额**：各模型的请求频率（QPS/RPM）与用量（TPM）配额可通过 `GET /api/v1/models/limits` 查看，不同模型差异显著（例如 `wan2.6-i2v-flash` 限流为 5 QPS，`qwen-image-max` 为 2 RPM）[查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)。

> **注意**：文档 3 中指出“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但文档 9 的权限接口返回示例中明确包含 `qwen3-max` 的 `fine_tune: true` 字段，表明微调权限与推理权限是正交配置项。二者无矛盾，但需注意：**调优模型本身不依赖权限接口授权，而对标准模型执行微调操作则需 `finetune: true` 权限**。

## 关键参数

- **异步任务 ID (`task_id`)**：图像/视频生成等长耗时任务的核心标识，用于后续轮询或回调通知中的结果查询。任务状态包括 `PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED` 等 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **临时文件 URL (`oss://...`)**：上传本地文件后获得的 48 小时有效 URL，**必须**在模型调用请求头中显式添加 `X-DashScope-OssResourceResolve: enable` 才能被服务端解析 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **连接复用配置**：Java SDK 默认启用连接池，关键参数包括 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）；Python SDK 需传入自定义 `requests.Session` 或 `aiohttp.ClientSession` 实现复用 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。  
- **临时 API Key TTL**：通过 `POST /api/v1/tokens?expire_in_seconds=1800` 生成，有效期范围为 1–1800 秒，过期后自动失效且不可手动删除 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

## 使用方式

- **异步任务**：优先采用事件总线（EventBridge）接收 HTTP 回调或 RocketMQ 通知，避免轮询限流（20 QPS）。任务完成事件类型为 `dashscope:System:AsyncTaskFinish`，携带 `task_id` 和 `task_status`，收到后仅需一次 `GET /api/v1/tasks/{task_id}` 即可获取结果 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。  
- **子空间调用**：使用子业务空间的专属 API Key，并指定对应 `base_url`（北京地域为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡需带 `WorkspaceId`）；调优模型仅支持 DashScope 原生接口，不兼容 OpenAI 格式 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  
- **文件上传**：先调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取 OSS 上传凭证，再直传至 OSS，最后将 `oss://` URL 作为输入参数传给模型。注意文件与模型名称强绑定，且主账号隔离 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **权限与限额管理**：通过 `POST /api/v1/models/permissions` 更新模型授权（支持逐模型或一键 `OPEN` 全部推理模型），通过 `POST /api/v1/models/limits` 设置 QPM/TPM 配额（支持 `OVERLAY` 合并覆盖或 `DELETE` 清除） [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)、[更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)。

## 限制和注意事项

- **临时文件存储**：`oss://` URL 有效期严格为 48 小时，超时即不可用；上传限流为 100 QPS（按“主账号+模型”维度），**禁止用于生产环境或压测**；生产环境务必使用阿里云 OSS 等长期稳定存储 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **异步任务保留期**：任务完成后数据通常保留 24 小时，超时后系统自动清理，查询接口将返回 `UNKNOWN` 状态 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **连接复用配置风险**：Java SDK 中 `connectionPoolSize` 过高可能导致服务端负载过大，过低则引发请求阻塞；Python 异步调用中 `limit_per_host` 若设为 0（无限制），可能对单一主机造成冲击 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。  
- **临时 API Key 安全边界**：其权限完全继承自生成它的永久 API Key，若后者拥有全域模型访问权，则临时 Key 同样具备——因此应在后端严格管控生成逻辑，避免前端直接暴露调用入口 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)
- [查询模型权限](../../raw/model-api-reference/more-about-models/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)


