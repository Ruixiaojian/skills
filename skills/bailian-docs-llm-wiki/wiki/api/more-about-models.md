# [more](more.md) about models

阿里云百炼平台提供多种模型调用方式与配套能力，涵盖同步/异步任务处理、多业务空间隔离、文件临时托管、连接复用优化及事件驱动通知等核心场景。本文面向开发者，系统梳理关键能力、参数约束、使用路径及注意事项，帮助构建稳定、高效、可扩展的模型集成方案。

## 支持的模型/功能

百炼支持标准大语言模型（如 `qwen-plus`）、[多模态](../concepts/multi-modal.md)模型（如 `qwen-vl-plus`）、图像生成（如 `wanx2.1-t2i-turbo`）、视频生成（如 `wanx2.1-kf2v-plus`）及语音识别（如 `paraformer-16k-1`）等。不同模型适用不同调用模式：  
- **同步模型**（如文本生成）直接返回结果；  
- **异步模型**（如图像/视频生成）需通过 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 创建任务、轮询或订阅事件获取结果；  
- **子业务空间模型**（如非默认 Workspace 中部署的 `qwen-plus`）必须使用该空间专属 API Key，并显式配置对应地域的 `base_url`（北京为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`）[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  
> **注意**：文档 3 明确指出“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但文档 2 的异步任务接口描述中未区分标准模型与调优模型的权限逻辑，实际调用时请以控制台中该子空间的模型授权配置为准。

## 关键参数

| 参数 | 说明 | 约束 | 来源 |
|------|------|------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式，用于查询/取消任务 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时绑定的模型名 | 必须与后续模型调用的 `model` 参数一致，否则报错 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 缺失将导致模型调用失败 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器或 App 中调用模型前，后端应通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800` 生成临时 API Key，并将其透传给前端。该 Key 继承父 Key 全部权限，且**到期自动失效，不可手动删除** [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 2. [多模态](../concepts/multi-modal.md)[文件处理](../concepts/file-processing.md)
调用 `qwen-vl-plus` 等模型前，需先上传本地文件获取 `oss://` URL：  
- 调用 `GET https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model=qwen-vl-plus` 获取上传策略；  
- 按策略向 OSS 上传文件；  
- 得到 URL 后，在模型请求 Header 中**必须添加** `X-DashScope-OssResourceResolve: enable`。

### 3. 高并发连接优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池（如 `connectionPoolSize=256`, `readTimeout=300`）；  
- **Python SDK**：同步场景用 `requests.Session()`，异步场景用 `aiohttp.TCPConnector(limit=100)` 实现复用 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

### 4. 异步任务结果获取
- **轮询**：调用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`，QPS 限 20；  
- **事件驱动（推荐）**：在事件总线配置规则，监听 `dashscope:System:AsyncTaskFinish` 事件，目标设为 HTTP 回调或 RocketMQ，避免轮询限流与资源浪费 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

## 限制和注意事项

- **临时文件**：`oss://` URL 有效期严格为 **48 小时**，超时自动清理；文件与主账号、模型强绑定，不可跨账号/模型复用；上传限流 **100 QPS（按主账号+模型维度）**，**禁止用于生产环境或压测**，生产环境应使用 OSS [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **异步任务生命周期**：任务完成后保留 **24 小时**（具体以各模型文档为准），超时后无法查询；仅 `PENDING` 状态任务可取消 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **地域一致性**：API Key、Endpoint、Workspace ID 必须匹配同一地域（北京/新加坡/弗吉尼亚），混用将导致 `InvalidApiKey` 错误 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **子空间权限**：调用标准模型（如 `qwen-plus`）前，需在子业务空间中**显式授权**该模型；而调优部署的模型仅允许其所在空间的 API Key 调用，无需额外授权 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)




