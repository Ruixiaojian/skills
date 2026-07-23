# [more](more.md) about models

阿里云百炼平台支持多种模型调用模式，涵盖同步与异步任务、多模态文件处理、子业务空间隔离、连接复用优化及安全凭证管理等核心能力。本文面向开发者，系统梳理模型调用的关键机制、参数配置、使用约束及最佳实践，帮助构建高可用、高性能的 AI 应用。

## 支持的模型/功能

百炼平台支持两类主要调用路径：  
- **同步模型**（如 `qwen-plus`、`qwen-max`）：适用于文本生成类低延迟场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音识别 `paraformer-8k-v1`）：因处理耗时长，需通过任务 ID 轮询或事件通知获取结果。异步能力由统一的[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)提供支撑，覆盖任务创建、状态查询、批量检索与取消（仅限 `PENDING` 状态）。  

此外，平台支持多模态输入：调用图像/视频/音频模型前，需先上传本地文件获取临时 `oss://` URL（有效期 48 小时），且该 URL 必须与目标模型严格绑定，不可跨模型复用 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 3 中提到“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，无需模型调用授权”，但文档 3 同时强调“此类模型仅能由其所在业务空间的 API Key 调用”。这与文档 6 中“临时API Key 继承生成它的API Key 所拥有的全部权限”存在隐含冲突——若父 Key 无子空间模型权限，则生成的临时 Key 也无法调用。实际行为以权限继承逻辑为准，建议在子空间中显式授权。

## 关键参数

| 参数 | 说明 | 典型值 | 注意事项 |
|------|------|--------|----------|
| `task_id` | 异步任务唯一标识 | `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | 查询/取消操作必需，需妥善存储 |
| `model_name` | 模型名称（区分大小写） | `qwen-plus`, `wanx2.1-t2i-turbo` | 文件上传、模型调用、事件过滤均需一致；子空间调用必须匹配该空间已授权模型 |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | `enable` | 缺失将导致模型调用失败，见[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `expire_in_seconds` | 临时 API Key 有效期 | `1800`（30 分钟） | 范围 `[1, 1800]`，超时自动失效，不可手动删除 |
| 连接池参数（Java/Python SDK） | 控制 HTTP 连接复用行为 | `connectionPoolSize=256`, `limit=100` | 高并发场景下需调优，避免连接耗尽或服务端过载 |

## 使用方式

### 异步任务处理
- **轮询模式**：调用 `/api/v1/tasks/{task_id}` 查询单任务，或 `/api/v1/tasks/` 批量查询（支持按 `start_time`/`end_time`/`status`/`model_name` 过滤）。所有接口 QPS 限流为 **20**，需控制轮询频率。  
- **事件驱动模式**：通过[事件总线 EventBridge](../../raw/model-api-reference/more-about-models/async-task-api.md) 配置 HTTP 回调或 RocketMQ 目标，接收 `dashscope:System:AsyncTaskFinish` 事件，再发起一次结果查询。该方式规避轮询限流，适合高并发场景。

### 子业务空间调用
- 必须使用**子空间专属 API Key**，不可混用默认空间 Key；  
- OpenAI 兼容调用：`base_url` 设为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；  
- DashScope 原生调用：北京地域直接使用默认域名，新加坡地域需替换为 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；  
- 权限管控：标准模型需在子空间中[显式授权](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)，调优模型则自动继承空间归属权限。

### 连接复用配置
- **Java SDK**：通过 `Constants.connectionConfigurations` 设置连接池参数（如 `connectionPoolSize`、`maximumAsyncRequests`），默认启用；  
- **Python SDK**：同步调用传入 `requests.Session`，异步调用传入 `aiohttp.ClientSession`，推荐使用 `with` 语句管理生命周期。

### 安全凭证管理
- 在前端/移动端等不可信环境，应由后端服务调用 `/api/v1/tokens` 接口生成临时 API Key（TTL 可设），避免永久 Key 泄露；  
- 临时 Key 权限完全继承父 Key，包括模型访问范围与知识库限制。

## 限制和注意事项

- **文件上传**：单文件 ≤ 1 GB；QPS 限流 **100**（按主账号+模型维度）；临时 URL 仅 48 小时有效，**严禁用于生产环境**；生产环境请使用 OSS 自建存储 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **异步任务保留期**：任务完成后数据默认保留 **24 小时**，超时后无法查询，需及时获取结果。  
- **临时 API Key**：最大 TTL 为 1800 秒（30 分钟），到期自动失效，不支持提前撤销。  
- **地域与 Endpoint**：北京与新加坡地域的 API Key 不互通，Endpoint 域名结构不同（如新加坡需带 `WorkspaceId`），调用前务必确认地域配置。  
- **权限继承风险**：子空间模型调用权限与临时 API Key 的权限均严格继承自父 API Key。若父 Key 权限过大（如可调用所有模型），可能违反最小权限原则，建议为不同场景创建专用 Key 并精细授权。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)


