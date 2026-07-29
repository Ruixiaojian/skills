# [more](more.md) about models

阿里云百炼平台支持多种模型调用方式与配套能力，涵盖同步/异步任务处理、多业务空间隔离、文件上传、连接优化等核心场景。本文面向开发者，系统梳理模型使用的关键路径、参数配置、限制条件及最佳实践，帮助快速构建稳定高效的 AI 应用。

## 支持的模型与功能

百炼支持文本生成（如 `qwen-plus`）、多模态理解（如 `qwen-vl-plus`）、文生图（如 `wanx2.1-t2i-turbo`）、文生视频（如 `wanx2.1-kf2v-plus`）、语音识别（如 `paraformer-8k-v1`）等模型。其中，**图像生成、视频生成、长音频处理等耗时型任务统一采用异步调用机制**，需通过任务 ID 轮询或事件通知获取结果 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
> **注意**：文档 4 中提到“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，无需模型调用授权”，但该描述与权限管控逻辑存在潜在冲突——实际中，子业务空间内调优模型仍需在该空间内完成模型授权绑定，否则调用将返回 `Forbidden` 错误。请以控制台「模型权限管理」页面配置为准。

除标准模型外，百炼还支持在**子业务空间（Sub-workspace）** 中独立部署和调用模型，实现权限隔离与费用分账。子空间模型调用必须使用该空间专属的 API Key，并严格匹配地域 Endpoint（如北京为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`）[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

## 关键参数

| 参数 | 说明 | 典型值 | 注意事项 |
|------|------|--------|----------|
| `task_id` | 异步任务唯一标识符 | `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | 必须用于查询或取消任务；仅对 `PENDING` 状态任务支持取消 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 模型名称（区分大小写） | `qwen-plus`, `wanx2.1-t2i-turbo` | 文件上传时必须指定且与后续调用模型一致；不同模型间文件 URL 不互通 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | HTTP 请求头 | `enable` | 使用 `oss://` 类型临时 URL 时**必须显式添加**，否则模型服务无法解析资源 |
| `expire_in_seconds` | 临时 API Key 有效期 | `60`–`1800`（秒） | 默认 60 秒，最大 30 分钟；过期后自动失效，不可手动删除 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |

## 使用方式

### 异步任务结果获取
推荐两种方式：
- **轮询查询**：调用 `GET /api/v1/tasks/{task_id}` 获取单任务状态，或 `GET /api/v1/tasks/` 批量查询。QPS 限流为 **20**，超限将返回 `Throttling.RateQuota` 错误。
- **事件驱动通知**：通过事件总线（EventBridge）配置 HTTP 回调或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，避免轮询开销 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 文件上传与引用
调用多模态模型前，需先上传本地文件获取 `oss://` 临时 URL：
- 上传接口 `/api/v1/uploads?action=getPolicy&model={model_name}` 限流 **100 QPS**（按主账号+模型维度）；
- 文件有效期 **48 小时**，过期后 URL 失效；
- 调用模型时，除传入 URL 外，**必须在 Header 中设置 `X-DashScope-OssResourceResolve: enable`**。

### 连接复用优化
高并发场景下建议启用连接复用：
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize=256`, `connectTimeout=10s`）；
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession(connector=TCPConnector(...))`。

## 限制和注意事项

- **临时 URL 严禁用于生产环境**：48 小时有效期、100 QPS 限流、不支持扩容，[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 明确建议生产环境使用 OSS 等长期存储方案。
- **API Key 绑定关系严格**：子业务空间的 API Key 仅能调用该空间内已授权的模型；临时 API Key 继承源 Key 的全部权限，包括模型访问范围。
- **地域隔离**：北京、新加坡、弗吉尼亚等地域的 API Key 和 Endpoint **完全独立**，不可混用；新加坡地域需替换 `{WorkspaceId}` 占位符。
- **异步任务数据保留策略**：任务完成后通常保留 **24 小时**，超时后系统自动清理，批量查询接口无法返回已清理任务记录 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


