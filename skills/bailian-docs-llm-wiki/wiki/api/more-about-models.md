# [more](more.md) about models

百炼平台提供多种模型调用机制与配套能力，覆盖同步/异步任务、多模态文件处理、子空间隔离、连接优化等核心场景。本文面向开发者，系统梳理关键能力、参数约束、使用方式及限制条件，帮助构建稳定、高效、安全的模型服务集成。

## 支持的模型/功能

百炼支持两类主要模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）：适用于文本生成、多模态理解等低延迟场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音识别 `paraformer-16k-1`）：因处理耗时长，需通过任务 ID 分步提交与查询，详见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  

此外，平台支持：
- **子业务空间模型调用**：通过独立 API Key 和专属 endpoint（如 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`）实现模型权限隔离与费用分账，适用于多租户或精细化管控场景；  
- **临时文件托管**：上传本地图片/音频/视频后获取 `oss://` 格式临时 URL（有效期 48 小时），用于多模态模型输入，但**必须与目标模型严格绑定**且调用时显式添加请求头 `X-DashScope-OssResourceResolve: enable`；  
- **事件驱动通知**：通过事件总线（EventBridge）配置 HTTP 回调或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，替代轮询，提升实时性并规避 20 QPS 限流，详见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

> **注意**：文档 4 中提到“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，无需模型调用授权”，但该描述与实际权限模型存在偏差——调优模型仍需在子空间中显式授权方可调用，否则返回 `Forbidden` 错误。请以控制台「模型调用权限」配置为准。

## 关键参数

| 参数 | 说明 | 约束 | 来源 |
|------|------|------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | 范围 `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串，由创建接口返回 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时指定的模型名 | 必须与后续模型调用的 `model` 字段完全一致，否则调用失败 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize`（Java） / `limit`（Python aiohttp） | 连接池最大连接数 | Java 默认 32，建议高并发场景调至 256；Python aiohttp 默认 100 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器或移动 App 中调用模型时，**禁止硬编码永久 API Key**。应通过可信后端调用 `/api/v1/tokens` 接口生成临时 Key，并设置合理 TTL（如 `expire_in_seconds=1800`），临时 Key 自动过期且不可手动删除。

### 2. 异步任务流程
- **提交任务**：调用对应模型的异步创建接口（如文生图），获取 `task_id`；  
- **查询结果**：轮询 `GET /api/v1/tasks/{task_id}`（≤20 QPS）或配置 EventBridge 事件通知；  
- **批量管理**：使用 `GET /api/v1/tasks/` 按 `start_time`/`end_time`/`status`/`model_name` 等条件筛选；  
- **取消任务**：仅支持取消 `PENDING` 状态任务，调用 `POST /api/v1/tasks/{task_id}/cancel`。

### 3. 子空间调用
- 使用子空间专属 API Key；  
- OpenAI 兼容模式：`base_url` 设为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡）；  
- DashScope 原生模式：北京地域无需 `base_url`，新加坡需设为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`。

### 4. 多模态文件处理
- 上传前确认模型支持该文件类型（如 `qwen-vl-plus` 支持图片）；  
- 调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；  
- 上传后获得 `oss://` URL，**必须在模型调用请求头中添加 `X-DashScope-OssResourceResolve: enable`**。

## 限制和注意事项

- **临时文件限制**：单文件 ≤ 1 GB；上传限流 100 QPS（按主账号+模型维度）；文件仅限同主账号下使用；**严禁用于生产环境**，生产推荐使用 OSS 长期存储；  
- **异步任务保留期**：任务完成后默认保留 24 小时（具体以各模型文档为准），超时后无法查询；  
- **临时 API Key 权限继承**：继承生成它的永久 Key 的全部权限（含模型/知识库访问限制），请勿授予过高权限；  
- **连接复用配置**：Java SDK 默认启用连接池，Python SDK 需显式传入 `session`；未配置时高并发易触发连接耗尽或超时；  
- **地域一致性**：API Key、Endpoint、临时 [Token](../concepts/token.md) 生成地址必须同地域（北京/新加坡/弗吉尼亚），跨地域调用将失败；  
- **错误码统一处理**：所有接口均遵循标准错误结构（`code`/`message`/`request_id`），请参考 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 进行重试或告警。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


