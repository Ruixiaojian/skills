# [more](more.md) about models

百炼平台提供多种模型调用机制与配套能力，涵盖同步/异步任务处理、多业务空间隔离、文件上传、连接优化等关键场景。本文面向开发者，系统梳理模型服务的核心能力、参数配置、使用方式及限制条件，帮助您高效、安全地集成模型能力。

## 支持的模型/功能

百炼支持两类主要模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen-max`）：适用于文本生成类请求，响应快、链路简单，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音识别 `paraformer-16k-1`）：因处理耗时长，需通过任务 ID 分两步完成（提交 → 查询），并支持批量状态查询与取消 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  

此外，部分[多模态](../concepts/multi-modal.md)模型（如 `qwen-vl-plus`）需传入文件 URL，平台提供免费临时 OSS 存储能力，上传后获得 `oss://` 格式 URL（有效期 48 小时）[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
> **注意**：文档 3 中提到“文生图、文生视频提供了 SDK，SDK 已实现轮询”，但文档 2 明确指出异步任务接口本身**不内置轮询逻辑**，SDK 实现属封装层行为；实际调用仍需按文档 2 的接口规范自行轮询或接入事件通知。

## 关键参数

| 参数 | 说明 | 典型值/范围 | 注意事项 |
|------|------|-------------|----------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒 | 默认 60 秒，超时自动失效，不可手动删除 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 字符串 | 必须用于查询或取消任务；任务完成后保留约 24 小时（具体以各模型文档为准） |
| `model_name` | 模型名称 | 如 `qwen-plus`, `wanx2.1-t2i-turbo` | 文件上传时必须指定且与后续调用模型一致；子业务空间调用需确保该空间已授权该模型 |
| `X-DashScope-OssResourceResolve` | 启用 OSS 资源解析 | `enable` | 使用 `oss://` URL 时**必须显式设置**此 Header，否则调用失败 |
| 连接池参数（Java/Python） | 控制 HTTP 连接复用 | 如 `connectionPoolSize=256`, `limit=100` | 高并发场景下需调优，避免阻塞或资源浪费 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 调用环境准备
- 所有调用均需有效 API Key，并推荐配置为环境变量 `DASHSCOPE_API_KEY`；  
- 子业务空间调用必须使用**该空间专属的 API Key**，且需提前在控制台为其授予对应模型权限 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)；  
- 临时 API Key 适用于前端/移动端等不可信环境，由后端安全生成并透传 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 2. 异步任务处理
- **轮询模式**：调用 `/api/v1/tasks/{task_id}` 查询状态（20 QPS 限流），支持 `PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED` 等状态判断；  
- **事件驱动模式**：通过事件总线（EventBridge）配置 HTTP 回调或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，避免轮询 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)；  
- **批量操作**：使用 `/api/v1/tasks/` 接口按时间、状态、模型名等条件批量查询任务；仅 `PENDING` 状态任务可取消。

### 3. [多模态](../concepts/multi-modal.md)文件处理
- 上传前调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取凭证；  
- 使用凭证直传 OSS，获得 `oss://` URL；  
- 在模型请求中传入该 URL，并在 Header 中添加 `X-DashScope-OssResourceResolve: enable`。

### 4. SDK 连接优化
- **Java**：通过 `Constants.connectionConfigurations` 全局配置连接池参数（如 `connectionPoolSize`, `readTimeout`）；  
- **Python**：同步调用传入 `requests.Session`，异步调用传入 `aiohttp.ClientSession`，复用底层 TCP 连接。

## 限制和注意事项

- **临时存储限制**：`oss://` URL 有效期严格为 **48 小时**，过期即失效；文件大小上限 **1GB**；上传接口限流 **100 QPS（主账号+模型维度）**，**严禁用于生产环境或压测**，生产环境应使用阿里云 OSS [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)；  
- **地域隔离**：API Key、Endpoint、临时 [Token](../concepts/token.md) 均按地域（北京/新加坡/弗吉尼亚）独立，跨地域调用将失败；  
- **权限继承**：临时 API Key 继承其生成者 API Key 的全部权限（含模型/知识库访问限制），无额外管控能力 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)；  
- **子空间约束**：在子业务空间调优部署的模型**仅能被该空间的 API Key 调用**，且不支持 OpenAI 兼容方式；标准模型调用则需显式授权；  
- **异步任务清理**：已完成任务数据约保留 24 小时，超时后无法查询，需及时获取结果。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


