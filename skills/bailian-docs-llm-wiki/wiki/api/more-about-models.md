# [more](more.md) about models

阿里云百炼平台提供多种模型调用机制与配套能力，涵盖同步/异步任务处理、多业务空间隔离、文件临时托管、连接复用优化等核心场景。本文面向开发者，系统梳理关键能力、参数约束、使用方式及注意事项，帮助构建稳定、高效、可扩展的模型集成方案。

## 支持的模型/功能

百炼支持标准大语言模型（如 `qwen-plus`）、多模态模型（如 `qwen-vl-plus`）、文生图（`wanx2.1-t2i-turbo`）、文生视频（`wanx2.1-kf2v-plus`）等全栈模型，并提供以下关键功能：

- **子业务空间隔离**：通过独立 Workspace 实现模型权限管控与费用分账，调用时必须使用对应空间的 API Key，且标准模型需[显式授权](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)；调优部署模型则仅限所在空间调用。
- **异步任务处理**：适用于图像生成、视频合成等长耗时任务，支持创建任务 → 查询结果 → 批量状态检查 → 取消排队中任务（仅 `PENDING` 状态）全流程管理。
- **事件驱动通知**：为避免轮询开销，推荐通过[事件总线 EventBridge](../../raw/model-api-reference/more-about-models/async-task-api.md)配置 HTTP 回调或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，实现任务完成后的实时响应。
- **临时文件托管**：上传本地图片/音视频至百炼临时 OSS 存储，获取 `oss://` 格式 URL（有效期 48 小时），调用时需在 Header 中显式添加 `X-DashScope-OssResourceResolve: enable`。

> **注意**：文档 3 中“DashScope 方式调用子业务空间模型”示例代码末尾被截断（Java SDK 示例未完整），实际使用请以 [最新版 DashScope Java SDK 文档](https://help.aliyun.com/zh/model-studio/install-sdk) 为准。

## 关键参数

| 参数 | 说明 | 约束/默认值 | 来源 |
|------|------|-------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | 范围 `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串，由创建接口返回 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时绑定的模型名 | 必须与后续模型调用一致，否则报错 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，建议高并发场景按需调至 256 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `limit_per_host` | Python `aiohttp` 每主机连接数限制 | 默认 0（无限制），建议设为 30 避免单点压测 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 调用子业务空间模型
- **OpenAI 兼容方式**：设置 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡），使用该空间的 API Key。
- **DashScope 原生方式**：北京地域无需额外配置 `base_url`；新加坡地域需设置 `dashscope.base_http_api_url = 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1'`。

### 2. 处理异步任务
- **轮询模式**：调用 `/api/v1/tasks/{task_id}`（20 QPS 限流），适用于低并发场景。
- **事件驱动模式**：在事件总线配置规则监听 `acs.dashscope` 源 + `dashscope:System:AsyncTaskFinish` 类型事件，目标设为 HTTP URL 或 RocketMQ，解析 `data.task_id` 后查询结果。

### 3. 上传并使用临时文件
- 调用 `GET https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略。
- 使用策略参数向 OSS Host 上传文件，获得 `oss://` URL。
- 在模型请求中传入该 URL，并**必须**添加 Header：`X-DashScope-OssResourceResolve: enable`。

### 4. 启用连接复用
- **Java SDK**：通过 `Constants.connectionConfigurations` 设置 `connectionPoolSize`、`maximumAsyncRequests` 等参数。
- **Python SDK**：
  - 同步：传入 `requests.Session()` 实例到 `Generation.call(session=...)`；
  - 异步：传入 `aiohttp.ClientSession(connector=...)` 到 `AioGeneration.call(session=...)`。

## 限制和注意事项

- **临时 API Key**：继承生成者 API Key 的全部权限（含模型/[知识库](../concepts/knowledge-base.md)访问限制），且无法手动删除，到期自动失效。
- **临时文件**：`oss://` URL 有效期严格为 48 小时；上传限流为 100 QPS（按主账号+模型维度），**不适用于生产环境或压测**，生产环境应使用阿里云 OSS。
- **异步任务查询**：任务数据保留期为 24 小时（部分任务可能更短），超时后无法查询；批量查询接口 `start_time` 与 `end_time` 时间跨度不得超过 24 小时。
- **子业务空间权限**：调用标准模型前，必须在控制台为该空间[设置模型调用权限](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)，否则返回 403 错误。
- **地域一致性**：API Key、Endpoint、事件总线地域必须匹配（如北京地域 Key 不能用于新加坡 Endpoint），各文档中明确标注了地域差异。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


