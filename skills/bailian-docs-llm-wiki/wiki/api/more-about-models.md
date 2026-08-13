# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型服务的核心能力、关键配置项及使用约束。内容涵盖模型发现与权限管理、调用方式优化、异步任务处理、文件上传支持以及配额控制等关键环节，所有信息均基于当前平台最新接口规范整理。

## 支持的模型/功能

百炼平台提供丰富的模型生态，覆盖文本生成（TG）、视觉理解（VU）、图像生成（IG）、视频生成（VG）、语音识别（ASR）等十余种能力类型。开发者可通过 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 接口（`GET /api/v1/models`）按模态、供应商、能力、部署模式等维度动态检索可用模型，并获取其上下文长度、定价、输入/输出模态等元信息。模型权限需显式授予：对于标准模型（如 `qwen-plus`），必须通过 [查询模型权限](../../raw/model-api-reference/more-about-models/list-model-permissions.md) 和 [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md) 接口在子业务空间中完成推理（`inference`）授权；而调优后部署的私有模型则仅限其所在业务空间的 API Key 调用，无需额外授权。

部分计算密集型模型（如图像、视频生成）采用异步调用机制，需先创建任务获取 `task_id`，再轮询或订阅事件获取结果。平台提供统一的 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)，支持单任务查询、批量状态查询及任务取消。

> **注意**：文档 5 中提到“调用在阿里云百炼调优并部署的模型，无需模型调用授权”，但文档 9 的权限接口返回结构明确包含 `inference` 字段，且文档 11 的更新授权接口支持对任意模型设置 `inference: true/false`。这表明即使对调优模型，其推理权限仍受业务空间级管控，文档 5 的表述易引发误解，应以权限接口的实际行为为准。

## 关键参数

- **API Key 与地域绑定**：各地域（北京、新加坡、弗吉尼亚等）的 API Key 相互独立，不可混用。临时 API Key 继承其生成者 API Key 的全部权限与地域属性。
- **异步任务 TTL**：任务结果默认保留 24 小时，超时后数据被自动清理，查询将返回 `UNKNOWN` 状态。
- **文件上传约束**：上传时必须指定 `model_name`，且该名称须与后续模型调用时一致；临时 URL 有效期为 48 小时，过期即失效。
- **连接复用配置**：Java SDK 默认启用连接池，关键参数如 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）需根据并发量调整；Python SDK 需显式传入 `requests.Session` 或 `aiohttp.ClientSession` 实现复用。

## 使用方式

1. **模型调用**：推荐使用 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（`/compatible-mode/v1/chat/completions`）简化集成，但需注意子业务空间调用时必须使用该空间专属的 API Key，并正确配置 `base_url`（如北京地域为 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。
2. **异步任务通知**：为避免轮询限流（20 QPS），高并发场景应优先采用 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)，通过事件总线（EventBridge）主动推送 `dashscope:System:AsyncTaskFinish` 事件。
3. **文件上传**：调用[多模态](../concepts/multimodal.md)模型前，需先通过 `/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证，再将文件上传至 OSS 并获得 `oss://` 前缀的临时 URL；调用模型时，必须在请求 Header 中添加 `X-DashScope-OssResourceResolve: enable`。
4. **连接优化**：高并发应用应配置连接复用。Java SDK 通过 `Constants.connectionConfigurations` 设置，Python SDK 则需在 `Generation.call()` 或 `AioGeneration.call()` 中传入自定义 `session` 对象。

## 限制和注意事项

- **临时 API Key**：有效期最短 1 秒，最长 1800 秒（30 分钟），到期后自动失效，无法手动删除。
- **文件上传限流**：上传凭证接口按“主账号+模型”维度限流 100 QPS，且不支持扩容，**严禁用于生产环境或压测**；生产环境应使用阿里云 OSS 等稳定存储。
- **配额管理**：模型调用量受双重限制——账号级 `model_limit`（全局上限）和业务空间级 `workspace_limit`（可单独设置，但不能超过账号级上限）。可通过 [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md) 接口实时查看，并用 [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md) 接口动态调整。
- **地域 Endpoint 差异**：模型列表、限额、权限等管理类接口的 Endpoint 均需替换 `{WorkspaceId}`，且不同地域的域名结构不同（如北京为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://dashscope-intl.aliyuncs.com`），调用前务必核对。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)
- [查询模型权限](../../raw/model-api-reference/more-about-models/list-model-permissions.md)
- [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)
- [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)


