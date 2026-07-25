# [more](more.md) about models

阿里云百炼平台提供多种模型调用方式与配套能力，涵盖标准模型、子业务空间隔离、多模态文件处理、连接复用优化及异步任务管理等核心场景。本文面向开发者，系统梳理模型服务的关键能力、参数配置、使用路径及约束条件，帮助构建稳定、高效、可扩展的 AI 应用。

## 支持的模型与功能

百炼支持调用两类模型：**标准模型**（如 `qwen-plus`、`qwen-vl-plus`）和**在百炼平台调优并部署的私有模型**。标准模型需通过 API Key 显式授权后方可调用；而调优模型仅限其所属业务空间的 API Key 调用，且不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  
多模态模型（如图像、视频、音频生成）依赖外部文件输入，需先通过临时存储服务上传本地文件并获取 `oss://` 格式 URL，该 URL 与模型强绑定，且有效期为 48 小时 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
部分耗时较长的模型（如文生图、文生视频）采用异步机制，需先创建任务获取 `task_id`，再轮询或通过事件总线接收完成通知 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

> **注意**：文档中明确指出“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 同时又强调“调用调优模型**仅能由其所在业务空间的 API Key 调用**”。二者逻辑一致（权限隐含于空间归属），但表述侧重不同——前者强调授权豁免，后者强调空间隔离，无实质矛盾。

## 关键参数

- **临时 API Key 有效期**：默认 60 秒，可通过 `expire_in_seconds` 参数设置 TTL，范围为 `[1, 1800]` 秒，适用于浏览器或移动端等不可信环境 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **文件上传绑定参数**：上传时必须指定 `model_name`，且后续模型调用必须使用同一模型名称，否则请求失败。  
- **连接复用参数**（Java SDK）：`connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）等直接影响高并发性能，需根据实际 QPS 调整 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。  
- **异步任务查询参数**：`start_time`/`end_time` 格式为 `YYYYMMDDhhmmss`，时间跨度不得超过 24 小时；`status` 可过滤 `PENDING`、`RUNNING`、`SUCCEEDED` 等状态。

## 使用方式

### 模型调用
- **OpenAI 兼容方式**：适用于标准模型，需配置 `base_url`（北京地域为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡地域为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`），并使用对应子业务空间的 API Key。  
- **DashScope 原生方式**：支持所有模型，北京地域无需配置 `base_url`；新加坡地域需显式设置 `dashscope.base_http_api_url` 或 SDK 的 `base_url`。  

### 文件上传
- 通过 `/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证，再 POST 至 OSS Host 完成上传，返回 `oss://` URL。  
- **关键头信息**：调用模型时，HTTP 请求头必须包含 `X-DashScope-OssResourceResolve: enable`，否则解析失败 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  

### 异步任务通知
- 推荐使用 **事件总线（EventBridge）** 避免轮询限流（20 QPS）。可配置 HTTP 回调 URL 或 RocketMQ 作为事件目标，事件类型为 `dashscope:System:AsyncTaskFinish` [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。  
- 若必须轮询，使用 `GET /api/v1/tasks/{task_id}` 查询单任务，或 `GET /api/v1/tasks/` 批量查询，注意 `task_id`、`model_name`、`status` 等过滤参数。

## 限制和注意事项

- **临时文件存储**：非生产级方案。文件大小上限 1 GB，上传限流 100 QPS（按“主账号+模型”维度），且 48 小时后自动清理。生产环境务必使用 OSS [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **临时 API Key**：无法手动删除，到期自动失效；继承父 Key 的全部权限，包括模型访问控制，需谨慎发放。  
- **子业务空间模型调用**：调用调优模型时，**仅支持 DashScope 原生接口**，不支持 OpenAI 兼容方式 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  
- **异步任务取消**：仅支持取消 `PENDING` 状态的任务，`RUNNING` 或已完成状态无法取消，调用返回 `UnsupportedOperation` 错误码 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **连接复用**：Python SDK 中 `requests.Session` 或 `aiohttp.ClientSession` 需显式传入 `session` 参数至 `Generation.call()` 或 `AioGeneration.call()`，否则不生效 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)


