# [more](more.md) about models

本页面汇总了百炼平台在模型调用过程中涉及的进阶功能和配置，包括 API Key 管理、文件上传、异步任务管理、SDK 连接优化以及子业务空间调用等。这些内容适用于需要在生产环境中进行安全管控、性能优化或复杂任务编排的开发者。

---

## API Key 管理

### 临时 API Key

在浏览器、移动 App 等不可信环境中调用模型时，应避免直接暴露永久 API Key。百炼支持通过后端服务生成临时 API Key，有效期默认 60 秒，最长可设为 1800 秒。详见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

**请求方式：**

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**关键参数：**

| 参数 | 说明 |
|------|------|
| `expire_in_seconds` | 有效期（TTL），范围 [1, 1800] 秒，默认 60 秒 |

**返回值：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `token` | String | 生成的临时 API Key（`st-****` 格式） |
| `expires_at` | Number | 过期时间，UNIX 时间戳（秒） |

> **注意**：临时 API Key 继承生成它的永久 API Key 的全部权限。临时 API Key 到期后自动失效，不支持手动删除。

### 子业务空间调用

默认业务空间的 API Key 拥有所有模型的调用权限。如需限制特定用户可调用的模型范围，或对模型调用费用进行分账，可使用子业务空间。调用子业务空间中的模型时，**必须使用该子业务空间的 API Key**，其他调用方式与默认空间一致。详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

**使用前提：**

- 在子业务空间中创建 API Key 并配置到环境变量
- 调用标准模型（如 `qwen-plus`）前，需为该空间设置模型调用权限
- 调用在百炼调优并部署的模型无需额外授权，但仅能由其所在业务空间的 API Key 调用

**支持的调用方式：**

| 方式 | 标准模型 | 调优模型 |
|------|---------|---------|
| OpenAI 兼容 | ✅ | ❌ |
| DashScope SDK/HTTP | ✅ | ✅ |

---

## 文件上传与临时 URL

调用多模态、图像、视频或音频模型时，通常需要传入文件 URL。百炼提供免费临时存储空间，可将本地文件上传获取 `oss://` 前缀的临时 URL（有效期 48 小时）。详见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

**使用限制：**

| 限制项 | 说明 |
|--------|------|
| 文件与模型绑定 | 上传时指定模型名称，必须与后续调用的模型一致 |
| 文件与主账号绑定 | 上传与调用的 API Key 必须属于同一阿里云主账号 |
| 有效期 | 48 小时，过期自动清理 |
| 上传限流 | 按"主账号+模型"维度 100 QPS |
| 文件不可修改 | 上传后不可查询、修改或下载 |

**上传方式：**

1. **代码上传**（Python / Java）：调用 `https://dashscope.aliyuncs.com/api/v1/uploads` 获取上传凭证，再上传至 OSS
2. **命令行工具**：`dashscope oss.upload --model qwen-vl-plus --file cat.png`

> **注意**：使用 `oss://` 形式的临时 URL 调用模型时，**必须**在 HTTP 请求头中添加 `X-DashScope-OssResourceResolve: enable`。临时 URL 不建议用于生产环境，生产环境请使用阿里云 OSS 等稳定存储。

---

## 异步任务管理

图像生成、视频生成等处理时间较长的模型采用异步调用机制：先创建任务获取 `task_id`，再通过 ID 查询结果。

### 任务查询

| 接口 | 方法 | 说明 | 限流 |
|------|------|------|------|
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 根据 task_id 查询任务状态和结果 | 20 QPS |
| 批量查询任务 | `GET /api/v1/tasks/` | 支持按时间、模型、状态等条件筛选 | 20 QPS |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持取消 `PENDING` 状态的任务 | 20 QPS |

**任务状态值：**`PENDING`（排队中）、`RUNNING`（处理中）、`SUCCEEDED`（成功）、`FAILED`（失败）、`CANCELED`（已取消）、`UNKNOWN`（不存在或未知）

> **注意**：异步任务完成后通常保留 24 小时（具体以对应任务的 API 文档为准），超时后系统自动清理。查询接口支持查询当前 API Key 所属主账号下的所有任务，但无法跨主账号查询。

### 任务完成通知

频繁轮询任务结果接口会造成资源浪费并可能触发限流。百炼支持通过事件总线（EventBridge）主动推送任务完成通知，提供两种接收方式：

| 方案 | 适用场景 | 特点 |
|------|---------|------|
| HTTP 回调 URL | 通用场景 | 简单直接，需公网或 VPC 可达的 HTTP 接口 |
| RocketMQ | 对消息可靠性要求高的场景 | 支持消息无丢失和失败重试 |

事件源为 `acs.dashscope`，事件类型为 `dashscope:System:AsyncTaskFinish`。收到通知后只需一次查询即可获取任务结果。详细配置步骤请参考 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

---

## SDK 连接优化

高并发场景下，可通过连接复用优化网络连接的使用效率，减少请求超时和资源消耗。

### Java SDK

Java SDK 内置连接池机制，默认启用。核心配置参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `connectTimeout` | 120s | 建立连接的超时时间 |
| `readTimeout` | 300s | 读取数据的超时时间 |
| `writeTimeout` | 60s | 写入数据的超时时间 |
| `connectionIdleTimeout` | 300s | 空闲连接超时时间 |
| `connectionPoolSize` | 32 | 最大连接数 |
| `maximumAsyncRequests` | 32 | 最大并发请求数（需 ≤ 连接数） |
| `maximumAsyncRequestsPerHost` | 32 | 单主机最大并发请求数 |

### Python SDK

Python SDK 通过传入自定义 Session 实现连接复用：

- **异步场景**：使用 `aiohttp.ClientSession` + `aiohttp.TCPConnector`
- **同步场景**：使用 `requests.Session`

**最佳实践：**
- Java：根据并发量合理调整 `connectionPoolSize` 和 `maximumAsyncRequests`
- Python：推荐使用 `with` 语句管理 Session 生命周期
- 异步架构（asyncio、FastAPI 等）使用异步调用方式，传统架构使用同步方式

---

## 地域与 Endpoint

百炼支持多地域部署，不同地域的 API Key 和 Endpoint 不同：

| 地域 | DashScope Endpoint | OpenAI 兼容 Endpoint |
|------|--------------------|-----------------------|
| 北京 | `https://dashscope.aliyuncs.com/api/v1` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/api/v1` | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |

> **注意**：各地域的 API Key 不互通，请确保使用对应地域的 API Key 和 Endpoint。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)

