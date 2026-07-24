# [more](more.md) about models

阿里云百炼平台提供多种模型调用机制与配套能力，覆盖同步/异步任务、[多模态](../concepts/multi-modal.md)[文件处理](../concepts/file-processing.md)、子空间隔离、连接优化等核心场景。本文档面向开发者，系统梳理模型服务的关键能力、参数配置、使用方式及限制条件，帮助构建稳定、高效、安全的模型集成方案。

## 支持的模型/功能

百炼支持两类主要模型调用路径：  
- **标准模型**（如 `qwen-plus`、`wanx2.1-t2i-turbo`）：需在业务空间中显式授权后方可调用，支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope 原生接口两种方式；  
- **调优模型**（即用户在百炼平台训练并部署的私有模型）：仅限其所属业务空间的 API Key 调用，不支持 OpenAI 兼容方式，详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  

异步模型（如图像生成、视频合成、语音识别等）采用任务制流程，需先创建任务获取 `task_id`，再通过 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 查询或取消任务。部分异步任务还支持通过事件总线接收完成通知，避免轮询开销，具体参见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

> **注意**：文档 4 中提到“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但该描述与权限管控逻辑存在矛盾——实际生产环境中，调优模型虽不需额外授权，但仍严格绑定其所属子业务空间，且仅允许该空间的 API Key 调用。此为权限隔离机制，非“无需授权”。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识符 | UUID 格式字符串，如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` 临时 URL 时必需的请求头 | 固定字符串 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize`（Java） / `limit`（Python async） | 连接池最大连接数 | Java 默认 32，建议高并发场景设为 256；Python async 默认 100 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 调用子业务空间模型  
必须使用该子空间生成的 API Key，并按地域选择对应 endpoint：  
- 北京地域：`base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"`（OpenAI 兼容）或 `dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"`（DashScope 原生）；  
- 新加坡地域：`base_url = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"`（需替换 `{WorkspaceId}`）。  

### 2. 上传[多模态](../concepts/multi-modal.md)文件  
调用图像、视频、音频类模型前，需先上传本地文件获取 `oss://` 临时 URL（有效期 48 小时），并在模型请求中传入该 URL，同时**必须设置请求头 `X-DashScope-OssResourceResolve: enable`**。上传接口限流为 100 QPS（按主账号+模型维度），不可扩容。

### 3. 启用连接复用  
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize`、`readTimeout`）；  
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession(connector=...)`，避免每次请求重建 TCP 连接。

### 4. 获取临时 API Key  
适用于浏览器、移动端等不可信环境。后端服务调用 `POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800`，传入永久 API Key 的 `Authorization` 头，返回 `token` 和 `expires_at`。临时 Key 无法手动删除，到期自动失效。

## 限制和注意事项

- **临时文件存储**：`oss://` URL 有效期严格为 48 小时，过期后不可恢复；文件与模型强绑定（上传时指定 `model` 参数），且仅限同一主账号下使用；**禁止用于生产环境或压测场景**，生产环境应使用 OSS 等长期存储方案。  
- **异步任务生命周期**：任务结果默认保留 24 小时（以各模型文档为准），超时后自动清理；仅 `PENDING` 状态任务可取消，`RUNNING` 或已完成任务不可取消。  
- **API Key 隔离性**：子业务空间的 API Key 仅能调用该空间内已授权的模型；临时 API Key 继承父 Key 的全部权限（含模型/知识库访问限制），无额外作用域控制。  
- **限流策略**：  
  - 异步任务查询/取消接口：20 QPS（按主账号计）；  
  - 文件上传凭证接口：100 QPS（按主账号+模型计）；  
  - 临时 API Key 生成接口：未明确说明，但受底层鉴权服务通用限流约束。  
- **地域差异**：北京、新加坡、弗吉尼亚三地 API Key 不互通，Endpoint 地址不同，需按实际部署地域选用对应密钥与 URL。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


