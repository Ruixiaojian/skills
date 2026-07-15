# [more](more.md) about models

百炼平台提供多种模型调用机制与配套能力，涵盖同步/异步任务处理、多业务空间隔离、连接复用优化及安全凭证管理。本文面向开发者，系统梳理核心能力、关键参数、使用方式及限制条件，帮助构建稳定、高效、可扩展的模型服务集成方案。

## 支持的模型/功能

百炼支持两类主要模型调用路径：  
- **标准模型**（如 `qwen-plus`、`wanx2.1-t2i-turbo`）：需通过 API Key 显式授权调用权限，支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope 原生接口两种方式；  
- **调优后部署的模型**：仅限其所属子业务空间的 API Key 调用，无需额外模型授权，但不支持 OpenAI 兼容方式 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  

异步能力覆盖图像生成、视频合成、语音识别等长耗时任务，需通过 `POST /api/v1/tasks` 创建任务并配合轮询或事件通知获取结果。同步任务（如文本生成）则直接返回响应。  
> **注意**：文档 3 中称“调优后的模型仅支持通过 DashScope 调用”，但文档 4 的事件总线示例中明确包含 `paraformer-8k-v1`（ASR 模型），该模型属于调优类语音模型，且其 `user_api_unique_key` 格式与文档 3 描述一致。这表明调优模型实际也支持事件通知机制，文档 3 表述存在局限性。

## 关键参数

| 参数 | 说明 | 取值范围/默认值 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 `60` | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `connectionPoolSize` (Java) | HTTP 连接池最大连接数 | 默认 `32`，建议高并发场景设为 `256` | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `limit_per_host` (Python) | 单主机最大连接数 | 默认 `0`（无限制），建议设为 `30` | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全凭证管理
在不可信环境（如浏览器、App）中，**必须**使用后端服务生成临时 API Key，而非直接暴露永久 Key。调用 `/api/v1/tokens` 接口，传入 `expire_in_seconds` 控制 TTL，响应返回 `token` 和 `expires_at` 时间戳 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 2. 子业务空间调用
为实现模型权限隔离与费用分账，需在子业务空间创建专属 API Key，并按地域配置正确 endpoint：
- **北京地域**：OpenAI 兼容 `base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"`；DashScope 原生 `base_url = "https://dashscope.aliyuncs.com/api/v1"`；
- **新加坡地域**：需替换 `{WorkspaceId}`，如 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`。

### 3. 异步任务处理
- **轮询模式**：调用 `GET /api/v1/tasks/{task_id}` 查询状态（QPS 限流 20），支持 `PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED` 等状态判断；
- **事件驱动模式**：配置事件总线规则，监听 `dashscope:System:AsyncTaskFinish` 事件，通过 HTTP 回调或 RocketMQ 消费通知，避免轮询资源浪费 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 4. 连接复用优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize`, `readTimeout`）；
- **Python SDK**：同步调用传入 `requests.Session`，异步调用传入 `aiohttp.ClientSession` 并配置 `TCPConnector`。

## 限制和注意事项

- **临时 API Key**：无法手动删除，到期自动失效；继承父 Key 全部权限，包括模型/知识库访问限制 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)；  
- **异步任务生命周期**：成功/失败任务默认保留 24 小时，超时后数据被系统清理，查询将返回 `UNKNOWN` 状态；  
- **取消任务限制**：仅支持取消 `PENDING` 状态任务，`RUNNING` 或已完成任务不可取消，错误码 `UnsupportedOperation` 明确提示此约束 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)；  
- **地域隔离**：各 Region（北京/新加坡/弗吉尼亚）的 API Key 与 Endpoint 完全独立，混用将导致 `InvalidApiKey` 错误；  
- **SDK 版本要求**：Java SDK 建议 ≥ 2.12.0，Python SDK 需支持 `session` 参数传入，旧版本可能不兼容连接复用特性。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


