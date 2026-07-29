# [more](more.md) about models

百炼平台提供丰富的模型调用能力，涵盖同步/[异步任务](../concepts/asynchronous-task.md)处理、多模态文件支持、子空间隔离、连接优化及安全凭证管理。本文面向开发者，系统梳理核心能力、关键参数、使用方式及限制，帮助您高效、稳定地集成模型服务。

## 支持的模型/功能

百炼支持多种模型类型与调用模式：  
- **标准大模型**（如 `qwen-plus`、`qwen-vl-plus`）和**调优后专属模型**均可通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope 原生接口调用；  
- **长耗时模型**（如文生图、文生视频、语音识别等）统一采用**[异步任务](../concepts/asynchronous-task.md)机制**，需先创建任务再查询结果；  
- **多模态模型**（图像、音频、视频）依赖外部文件输入，平台提供免费临时存储并返回 `oss://` 格式 URL；  
- 所有模型均支持在**默认业务空间**或**子业务空间**中调用，子空间可实现权限隔离与费用分账 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)；  
- [异步任务](../concepts/asynchronous-task.md)完成通知支持**事件总线主动推送**（HTTP 回调或 RocketMQ），替代轮询，提升实时性并规避限流 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

> **注意**：文档 4 中明确指出“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但文档 3 的“前提条件”仅要求“获取API Key”，未提及子空间模型授权例外。实际开发中，若在子空间调用调优模型失败，请优先检查是否遗漏了该空间的模型调用权限配置——此为常见误配点。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `task_id` | 异步任务唯一标识符，用于查询或取消任务 | UUID 格式字符串，如 `a8532587-...-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒（默认 60 秒） | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `model_name` | 文件上传时必需指定的模型名，与后续调用模型严格一致 | 如 `qwen-vl-plus`, `wanx2.1-t2i-turbo` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时**必须**添加的请求头 | 字符串字面量 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` / `limit` | Java/Python SDK 连接池最大连接数 | Java 默认 32，Python `aiohttp.TCPConnector.limit` 默认 100 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 调用流程选择
- **短耗时模型**（文本生成等）：直接同步调用，推荐使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-mode/v1/chat/completions`）或 DashScope 原生接口（`/api/v1/services/aigc/text-generation/generation`）。  
- **长耗时模型**（图像/视频生成等）：必须走异步流程：  
  (1) 发起任务 → 获取 `task_id`；  
  (2) 通过 `GET /api/v1/tasks/{task_id}` 查询结果；  
  (3) 或配置事件总线接收 `dashscope:System:AsyncTaskFinish` 事件，避免轮询 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 2. 多模态文件处理
- 上传前：确认模型支持该文件类型，并确保 `model_name` 与调用时完全一致；  
- 上传后：获得 `oss://...` URL，**必须在模型调用请求头中添加 `X-DashScope-OssResourceResolve: enable`**；  
- 注意：文件有效期仅 48 小时，生产环境应使用 OSS 等长期存储方案。

### 3. 子业务空间调用
- 必须使用**该子空间生成的 API Key**；  
- 调用标准模型需提前在子空间内授权；调优模型则自动继承空间权限；  
- 地域差异：北京地域使用 `https://dashscope.aliyuncs.com/...`，新加坡地域需替换为 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。

### 4. 连接优化（高并发场景）
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize=256`）；  
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession(connector=...)`；  
- 所有配置均需在首次调用前完成初始化。

## 限制和注意事项

- **临时文件存储**：单文件 ≤ 1 GB；上传限流 100 QPS（按主账号+模型维度）；**严禁用于生产环境或压测** [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)；  
- **临时 API Key**：继承父 Key 全部权限，无法手动删除，到期自动失效；各地域 Endpoint 不互通；  
- **异步任务查询**：流量限制 20 QPS；任务数据保留约 24 小时（以具体模型文档为准）；仅支持取消 `PENDING` 状态任务；  
- **子空间模型调用**：API Key 与空间强绑定，跨空间调用将返回鉴权错误；  
- **连接复用**：Java SDK 默认启用连接池，Python SDK 需显式传入 Session 实例，否则每次调用新建连接；  
- **地域一致性**：API Key、Endpoint、事件总线地域（如 `cn-beijing`）三者必须匹配，否则请求失败。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


