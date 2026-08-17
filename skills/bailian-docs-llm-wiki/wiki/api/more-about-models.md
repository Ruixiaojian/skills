# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型服务的高级能力与关键配置项，涵盖模型发现、权限管理、调用优化及[异步任务](../concepts/asynchronous-task.md)处理等核心场景。所有功能均需配合有效的 API Key 使用，建议通过子业务空间进行权限隔离与成本分账。

## 支持的模型/功能

百炼平台提供丰富的模型生态，支持文本生成（TG）、视觉理解（VU）、图像生成（IG）、视频生成（VG）、语音识别（ASR）等多种模态能力。可通过 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 接口动态获取当前可用模型，支持按作者（如 `qwen`、`zhipu-ai`）、能力（如 `Reasoning`、`Multimodal-Omni`）、部署模式（如 `global`、`asia-pacific-china`）等多维度筛选，并返回上下文长度、定价、输入/输出模态等关键元信息。

对于子业务空间用户，需显式配置模型调用权限：标准模型（如 `qwen-plus`）需通过 [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md) 接口授权；而调优后部署的模型仅限其所在空间调用，无需额外授权。此外，[查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md) 接口可实时查看当前空间已授权模型及其 `inference`、`fine_tune` 等权限状态。

> **注意**：文档 3 中提到“调用在阿里云百炼调优并部署的模型，无需模型调用授权”，但文档 9 和 10 的权限接口明确支持对 `fine_tune` 和 `deploy` 权限的细粒度控制。实际生产中，调优模型虽默认不可跨空间调用，但其训练与部署权限仍需通过权限接口显式管理，二者不矛盾，而是作用于不同生命周期阶段。

## 关键参数

- **临时凭证有效期**：生成临时 API Key 时，`expire_in_seconds` 参数范围为 `[1, 1800]` 秒，默认 60 秒，超时后自动失效且不可手动删除 —— 详见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **文件有效期**：上传本地文件获取的 `oss://` 临时 URL 有效期固定为 48 小时，且必须与后续模型调用使用同一主账号和模型名称，调用时需在 Header 中添加 `X-DashScope-OssResourceResolve: enable`。
- **[异步任务](../concepts/asynchronous-task.md)保留期**：任务完成后数据通常保留 24 小时（具体以对应任务文档为准），超时后系统自动清理，批量查询接口亦受此限制。
- **连接复用参数**：Java SDK 默认启用连接池，关键参数包括 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）；Python SDK 需传入自定义 `aiohttp.ClientSession` 或 `requests.Session` 实现复用 —— 参见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 使用方式

- **模型调用**：推荐使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-mode/v1/chat/completions`）或原生 DashScope SDK。子业务空间调用必须使用该空间专属 API Key，并正确配置 `base_url`（北京地域为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡地域需嵌入 `WorkspaceId`）。
- **文件上传**：多模态模型（如 `qwen-vl-plus`）需先调用 `/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略，再直传至 OSS，最终获得 `oss://` URL。该 URL 仅限同模型、同主账号调用。
- **[异步任务](../concepts/asynchronous-task.md)管理**：图像/视频类模型需两步调用：先创建任务获取 `task_id`，再通过 `/api/v1/tasks/{task_id}` 查询结果。为避免轮询限流（20 QPS），强烈推荐使用 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)，由事件总线主动推送 `dashscope:System:AsyncTaskFinish` 事件。
- **限额与权限管理**：通过 `/api/v1/models/limits` 查询各模型的 QPM/TPM 限额；通过 `/api/v1/models/permissions` 查看/更新推理、微调等权限。更新操作支持逐模型配置或一键授权（`access_all_entities=OPEN`）。

## 限制和注意事项

- **地域与 Endpoint 绑定严格**：各 API（模型列表、限额、权限等）的 Endpoint 均与地域强绑定，北京、新加坡、弗吉尼亚等地域的 URL 格式不同，且 API Key 不通用。调用前务必确认地域并替换 `{WorkspaceId}`。
- **生产环境规避临时机制**：临时 API Key 和临时文件 URL 均不适用于生产环境。前者因 TTL 过短易导致请求中断；后者因 48 小时有效期、100 QPS 上传限流及不可下载等限制，官方明确建议生产环境使用阿里云 OSS 等长期稳定存储。
- **权限继承风险**：临时 API Key 完全继承其生成所用永久 API Key 的全部权限（含模型/知识库访问限制），请勿在不可信环境直接暴露永久 Key —— 此点已在 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 文档中强调。
- **异步任务状态语义**：`output.task_status` 为 `SUCCEEDED` 仅表示任务调度成功，不代表所有子任务成功；需检查 `output.task_metrics` 中 `SUCCEEDED`/`FAILED` 计数及 `results` 数组中的具体错误项（如 `DataInspectionFailed`）。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)


