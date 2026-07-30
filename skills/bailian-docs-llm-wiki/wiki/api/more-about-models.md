# [more](more.md) about models

阿里云百炼平台提供多种模型调用机制与配套能力，涵盖同步/异步任务管理、[多模态](../concepts/multi-modal.md)文件处理、子业务空间隔离、连接优化及安全凭证管理。本文面向开发者，系统梳理核心能力、参数配置、使用方式及关键限制，帮助构建稳定、高效、可扩展的模型服务集成方案。

## 支持的模型/功能

百炼支持两类主要模型调用场景：  
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）：适用于文本生成、[多模态](../concepts/multi-modal.md)理解等低延迟场景，通过标准 HTTP 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)直接调用。  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音识别 `paraformer-16k-1`）：因处理耗时长，采用任务制流程，需先创建任务获取 `task_id`，再轮询或订阅事件获取结果。详细支持模型列表请参见 [模型文档](https://help.aliyun.com/zh/model-studio/getting-started/models)。  

此外，平台提供以下关键功能支撑模型使用：  
- 临时文件上传与 `oss://` URL 生成，用于[多模态](../concepts/multi-modal.md)输入；  
- 子业务空间（Workspace）隔离，实现模型权限管控与费用分账；  
- 临时 API Key 生成，适用于前端/移动端等不可信环境；  
- 异步任务状态管理（查询、批量查询、取消）及事件驱动通知（HTTP 回调 / RocketMQ）。  

> **注意**：文档 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 明确指出，调优后部署的私有模型**仅能通过 DashScope 原生接口调用**，不支持 OpenAI 兼容方式；而标准模型（如 `qwen-plus`）在子空间中调用时，需额外配置模型调用权限。该约束在其他文档中未被覆盖，属关键行为差异。

## 关键参数

| 参数 | 说明 | 取值范围 | 备注 |
|------|------|----------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒 | 默认 60 秒，详见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串 | 所有异步任务操作（查询、取消）均以此为路径参数 |
| `model_name` | 文件上传时必需指定的模型名 | 如 `qwen-vl-plus` | 决定文件存储策略与后续调用兼容性，[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 中强调“文件与模型绑定” |
| `connectionPoolSize`（Java） | HTTP 连接池最大连接数 | ≥1 | 默认 32，高并发场景建议调高，但需避免服务端过载，参见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `limit_per_host`（Python async） | 单主机最大连接数 | ≥0（0 表示无限制） | 推荐设为 30–50，平衡并发与服务端压力 |

## 使用方式

### 1. 调用模型
- **同步调用**：使用 `DASHSCOPE_API_KEY`，通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-mode/v1/chat/completions`）或 DashScope 原生接口（`/api/v1/services/aigc/text-generation/generation`）发起请求。子业务空间需使用其专属 API Key，并确保已授权对应模型。  
- **异步调用**：  
  - 先调用对应模型的创建接口（如文生图），获取 `task_id`；  
  - 再通过 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 查询结果（`GET /api/v1/tasks/{task_id}`）或批量状态（`GET /api/v1/tasks/`）；  
  - 或配置 [事件总线接收完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)，避免轮询限流（20 QPS）。  

### 2. 上传多模态文件
- 调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；  
- 使用策略参数向 OSS 直传文件，获得 `oss://...` URL；  
- **必须**在模型调用请求 Header 中添加 `X-DashScope-OssResourceResolve: enable`，否则解析失败；  
- 临时 URL 有效期 48 小时，生产环境应使用 OSS 等长期存储。  

### 3. 安全凭证管理
- 在不可信客户端（Web/APP）中，后端应调用 `/api/v1/tokens` 接口生成短期临时 Key，继承父 Key 权限但生命周期可控；  
- 临时 Key 不可手动删除，到期自动失效。  

### 4. 连接优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize`, `readTimeout`）；  
- **Python SDK**：同步场景用 `requests.Session()`，异步场景用 `aiohttp.TCPConnector`，显式传入 `session` 参数复用连接。  

## 限制和注意事项

- **临时文件限制**：单文件 ≤ 1 GB；上传限流 100 QPS（按主账号+模型维度）；文件仅限同主账号、同模型使用；**严禁用于生产环境或压测**，详见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **异步任务保留期**：任务完成后通常保留 24 小时，超时后数据自动清理，无法查询。  
- **地域隔离**：API Key、Endpoint、临时 [Token](../concepts/token.md) 均按地域（北京/新加坡/弗吉尼亚）独立，跨地域调用将失败。例如，新加坡地域的 Key 不能用于北京 Endpoint。  
- **子空间权限**：子业务空间调用标准模型前，必须在控制台为其[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)；调优模型则无需此步骤，但仅限本空间 Key 调用。  
- **临时 Key 继承性**：生成的临时 API Key 完全继承源 Key 的所有权限（含模型访问、知识库权限等），务必严格控制源 Key 权限粒度。  

> **注意**：[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 文档声明“已结束的任务在超时后将被系统自动清理”，而 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md) 未明确提及保留期。实际开发中应以前者为准，即任务完成 24 小时后事件总线推送的通知可能指向已不可查的任务，需在回调逻辑中做好容错（如静默忽略或记录告警）。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


