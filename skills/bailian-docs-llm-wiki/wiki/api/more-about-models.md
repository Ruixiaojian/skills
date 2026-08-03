# [more](more.md) about models

阿里云百炼平台提供多种模型调用机制与配套能力，涵盖同步/异步任务处理、多模态文件支持、子业务空间隔离、连接复用优化及安全凭证管理。本文面向开发者，系统梳理核心能力、关键参数、使用方式及约束条件，帮助构建稳定、高效、可扩展的模型服务集成方案。

## 支持的模型/功能

百炼支持两类主要模型调用路径：  
- **标准模型**（如 `qwen-plus`、`wanx2.1-t2i-turbo`）：需在对应业务空间显式授权调用权限，支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope 原生接口 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)；  
- **调优后私有模型**：仅限部署所在子业务空间的 API Key 调用，无需额外授权，但不支持 OpenAI 兼容方式 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  

异步能力适用于长耗时任务，包括图像生成、视频合成、语音识别等，需通过 `POST /api/v1/tasks` 创建任务并配合查询/取消接口使用 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
多模态模型（如 `qwen-vl-plus`）依赖外部文件输入，平台提供免费临时 OSS 存储，上传后返回 `oss://` 格式 URL，有效期 48 小时 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 4 中提及“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但文档 4 同时明确“调用标准模型前，需为该空间[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)”。二者逻辑一致，无矛盾；但需注意“标准模型”与“调优模型”的权限模型差异，不可混用。

## 关键参数

| 参数 | 作用 | 取值范围/说明 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID v4 格式字符串，由创建接口返回 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传绑定模型名 | 必须与后续模型调用的 `model` 字段完全一致，否则报错 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 启用 OSS 资源解析 | HTTP Header 必填项，否则 `oss://` URL 无法被服务端识别 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，高并发场景建议调至 256 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全凭证
- **生产环境**：优先使用永久 API Key 配置环境变量 `DASHSCOPE_API_KEY`；  
- **前端/移动端等不可信环境**：必须通过后端服务调用 `/api/v1/tokens` 接口生成临时 API Key，避免密钥泄露 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 2. 异步任务
- **轮询模式**：调用 `/api/v1/tasks/{task_id}` 查询状态（QPS 限流 20），适用于低频或调试场景；  
- **事件驱动模式**：配置 EventBridge 事件总线，监听 `dashscope:System:AsyncTaskFinish` 事件，通过 HTTP 回调或 RocketMQ 消费通知，规避轮询限流与资源浪费 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 3. 多模态文件
- 上传前确认目标模型支持该文件类型及大小（如 `qwen-vl-plus` 支持 ≤1GB 图片）；  
- 调用模型时，在请求体中传入 `oss://...` URL，并在 Header 中添加 `X-DashScope-OssResourceResolve: enable`；  
- **严禁用于生产环境**：临时 URL 48 小时过期且上传接口 QPS 限流 100，高并发场景请使用阿里云 OSS [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

### 4. 子业务空间
- 使用子空间专属 API Key，确保模型调用与费用归属隔离；  
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)需设置 `base_url`（北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`）；  
- DashScope 原生接口需显式配置 `base_http_api_url`（新加坡地域需替换 `{WorkspaceId}`） [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

### 5. 连接优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数，重点调整 `connectionPoolSize` 与 `maximumAsyncRequests`；  
- **Python SDK**：同步调用使用 `requests.Session()`，异步调用使用 `aiohttp.TCPConnector`，均需显式传入 `session` 参数 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 限制和注意事项

- **临时 API Key**：继承父 Key 全部权限，无法提前撤销，仅靠 TTL 自动失效 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)；  
- **异步任务保留期**：成功/失败任务默认保留 24 小时，超时后数据自动清理，需及时拉取结果 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)；  
- **文件上传绑定**：`model_name` 严格匹配调用模型，跨模型复用 URL 将导致 400 错误；同一主账号下不同子空间的文件不可共享 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)；  
- **地域隔离**：北京、新加坡、弗吉尼亚三地 API Key 与 Endpoint 独立，不可混用，尤其注意临时 Key 生成接口的地域 Endpoint [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)；  
- **限流策略**：文件上传（100 QPS）、异步任务查询（20 QPS）、临时 Key 生成（未明示但受底层配额约束）均为硬性限制，超限直接返回 `429` 或错误码，需实现退避重试 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)、[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


