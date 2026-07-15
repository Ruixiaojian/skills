# [more](more.md) about models

阿里云百炼平台提供多种模型调用机制与配套能力，涵盖同步/异步任务处理、多业务空间隔离、文件上传、连接优化等核心场景。本文面向开发者，系统梳理模型服务的关键能力、参数配置、使用方式及约束条件，帮助构建稳定、高效、安全的模型集成方案。

## 支持的模型/功能

百炼支持标准大语言模型（如 `qwen-plus`）、多模态模型（如 `qwen-vl-plus`）、图像生成（`wanx2.1-t2i-turbo`）、视频生成（`wanx2.1-kf2v-plus`）及语音识别（`paraformer-8k-v1`）等全类型模型。不同模型适用不同调用模式：

- **同步模型**（如文本生成）：直接调用 `/chat/completions` 或 `/generation` 接口，实时返回结果；
- **异步模型**（如文生图、文生视频）：需先创建任务获取 `task_id`，再通过[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 查询或取消，详见[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)；
- **多模态模型**：输入文件需先上传至临时存储并获取 `oss://` URL，且必须指定对应模型名称，详见[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)；
- **子业务空间模型**：调用非默认空间的模型（如千问-Plus）时，**必须使用该子空间专属 API Key**，且需提前配置模型调用权限，详见[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 4 中明确指出“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，无需模型调用授权”，但文档 3 的异步任务查询接口描述中称“支持查询当前 API Key 所属阿里云主账号下的所有任务（包括该主账号下通过任意 API Key 提交的任务）”。二者存在隐含冲突：若子空间调优模型仅允许本空间 API Key 调用，则其任务不应被主账号其他 API Key 查询到。实际行为以控制台权限配置为准，建议严格遵循子空间隔离原则，避免跨空间混用 API Key。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `task_id` | 异步任务唯一标识符 | UUID 格式字符串，如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 模型名称，用于文件上传绑定、权限校验及路由 | `qwen-plus`, `wanx2.1-t2i-turbo`, `paraformer-8k-v1` 等 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)、[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) |
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 固定字符串 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize`（Java） / `limit`（Python） | SDK 连接池大小 | Java 默认 32，可调至 256；Python `aiohttp.TCPConnector.limit` 默认 100 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 调用入口选择
- **[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**：适用于快速迁移或通用 SDK 集成，Base URL 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡）；
- **DashScope 原生接口**：适用于深度定制或需调用调优模型，Base URL 为 `https://dashscope.aliyuncs.com/api/v1`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`（新加坡）。

### 2. 文件上传与引用
调用多模态模型前，需先上传本地文件：
```bash
# 命令行工具（推荐）
dashscope oss.upload --model qwen-vl-plus --file cat.png
```
返回 `oss://dashscope-instant/xxx/cat.png` 后，在模型请求中作为 `url` 字段传入，并**必须添加请求头** `X-DashScope-OssResourceResolve: enable`。

### 3. 异步任务通知
避免轮询，推荐通过事件总线接收完成通知：
- 配置 HTTP 回调 URL 或 RocketMQ 作为事件目标；
- 订阅事件类型 `dashscope:System:AsyncTaskFinish`；
- 解析回调事件中的 `data.task_id` 和 `data.task_status`，再调用 `/api/v1/tasks/{task_id}` 获取结果。

### 4. 连接复用优化
高并发场景下务必启用连接复用：
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数；
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession()`。

## 限制和注意事项

- **临时文件存储**：`oss://` URL 有效期严格为 **48 小时**，超期自动清理；文件与模型强绑定，不可跨模型复用；上传限流为 **100 QPS（按主账号+模型维度）**，[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 明确警告“请勿用于生产环境、高并发及压测场景”，生产环境应使用 OSS 自建存储。
- **临时 API Key**：由永久 API Key 生成，继承其全部权限（含模型/知识库访问限制）；**无法手动删除**，仅能等待自动过期；各地域 Endpoint 不同，需按实际地域选用。
- **异步任务生命周期**：任务结果默认保留 **24 小时**（具体以对应模型文档为准），超时后无法查询；仅支持取消 `PENDING` 状态任务，`RUNNING` 或已完成任务不可取消。
- **子业务空间隔离**：子空间 API Key 仅能调用本空间授权模型；调优模型**不支持 OpenAI 兼容方式调用**，必须使用 DashScope 原生接口。
- **SDK 连接配置**：Java SDK 的 `maximumAsyncRequests` 必须 ≤ `connectionPoolSize`，否则可能阻塞；Python 异步调用中 `limit_per_host` 建议设为非零值（如 30），防止对单一域名发起过多连接。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


