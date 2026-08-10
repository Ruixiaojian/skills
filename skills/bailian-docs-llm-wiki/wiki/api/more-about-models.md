# [more](more.md) about models

百炼平台提供多种模型调用机制与配套能力，覆盖同步/[异步任务](../concepts/asynchronous-task.md)、[多模态](../concepts/multi-modal.md)文件处理、子空间隔离、连接优化等核心场景。本文档面向开发者，系统梳理模型服务的关键能力、参数配置、使用方式及约束条件，帮助构建稳定、高效、安全的模型集成方案。

## 支持的模型/功能

百炼支持两类主要模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）：适用于文本生成、[多模态](../concepts/multi-modal.md)理解等低延迟场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音识别 `paraformer-16k-1`）：适用于耗时较长的任务，需通过任务 ID 轮询或事件通知获取结果。  

[异步任务](../concepts/asynchronous-task.md)统一由 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 提供生命周期管理能力，包括查询单个/批量任务状态、取消 PENDING 状态任务等。  
对于高并发、大规模[异步任务](../concepts/asynchronous-task.md)，推荐采用 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)，避免轮询限流（20 QPS）并提升实时性。  

> **注意**：文档 3 中明确说明“任务完成后立即推送”，而文档 2 的轮询接口响应示例中 `end_time` 字段为字符串格式（如 `"2023-12-20 21:36:45.913"`），但文档 2 的批量查询接口出参描述中 `start_time`/`end_time` 字段类型标注为 `Long`（毫秒时间戳），二者存在格式矛盾。实际开发请以[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 响应体中的字段值为准，建议以字符串解析为主，并兼容毫秒级时间戳。

## 关键参数

| 参数 | 作用 | 取值范围/说明 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串，由创建任务接口返回 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传绑定模型名 | 必须与后续模型调用的 `model` 参数一致，如 `qwen-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 固定值，缺失将导致模型调用失败 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` / `limit` | 连接池最大连接数 | Java SDK 默认 32，Python `aiohttp.TCPConnector` 默认 100 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器、移动端等不可信环境调用模型时，**禁止硬编码永久 API Key**。应通过后端服务调用 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 接口，获取短期有效的 `st-***` [Token](../concepts/token.md)，并将其透传至前端用于模型请求。临时 Key 继承源 Key 的全部权限（含模型/知识库访问限制），且到期自动失效，无法手动删除。

### 2. [多模态](../concepts/multi-modal.md)文件输入
调用图像、视频、音频模型前，需先上传本地文件获取临时 URL：
- 调用 `GET https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证；
- 使用凭证将文件上传至 OSS，获得 `oss://...` 格式 URL；
- **必须在模型请求 Header 中添加 `X-DashScope-OssResourceResolve: enable`**，否则解析失败；
- 该 URL 有效期 48 小时，仅限同主账号、同模型使用，生产环境应迁移到 OSS 等长期存储。

### 3. 子业务空间调用
为实现模型权限隔离与费用分账，可创建子业务空间：
- 在子空间内创建专属 API Key；
- 对标准模型（如 `qwen-plus`）需单独授权调用权限；调优部署模型则无需额外授权，但仅限本空间 Key 调用；
- OpenAI 兼容方式需设置 `base_url`（北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`）；
- DashScope 原生方式需配置 `base_http_api_url`（北京：`https://dashscope.aliyuncs.com/api/v1`；新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`）。

### 4. 高性能连接管理
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize=256`），推荐版本 ≥ 2.12.0；
- **Python SDK**：同步调用使用 `requests.Session()`，异步调用使用 `aiohttp.ClientSession(connector=TCPConnector(...))`，显式传入 `session` 参数实现复用。

## 限制和注意事项

- **临时 Key 限制**：有效期最长 1800 秒（30 分钟），地域 Endpoint 需与生成 Key 的 API Key 所属地域一致（北京/新加坡/弗吉尼亚），跨地域调用失败。
- **异步任务保留期**：任务结果默认保留 24 小时（具体以各模型文档为准），超时后数据被自动清理，`GET /api/v1/tasks/{task_id}` 将返回 `UNKNOWN` 状态。
- **文件上传限制**：单文件 ≤ 1 GB；上传接口限流 100 QPS（按主账号+模型维度），**严禁用于生产环境压测**；`oss://` URL 不可下载/修改，仅作模型输入参数。
- **子空间模型权限**：调用标准模型必须显式授权，否则返回 `Forbidden` 错误；调优模型天然隔离，无需授权但不可跨空间调用。
- **连接复用风险**：Python 同步 `requests.Session` 若未正确关闭（如未用 `with` 或 `session.close()`），可能导致连接泄漏；Java 连接池 `connectionPoolSize` 设置过高可能压垮服务端，需结合 `maximumAsyncRequests` 协同调整。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


