# [more](more.md) about models

百炼平台提供多种模型调用机制与配套能力，涵盖同步/[异步任务](../concepts/asynchronous-task.md)处理、多[业务空间隔离](../concepts/workspace-isolation.md)、连接复用优化、文件临时托管及安全凭证管理。本文面向开发者，系统梳理核心能力、参数配置、使用方式及关键约束，帮助构建稳定、高效、可扩展的模型服务集成方案。

## 支持的模型与功能

百炼支持标准大语言模型（如 `qwen-plus`）、多模态模型（如 `qwen-vl-plus`）、图像生成（如 `wanx2.1-t2i-turbo`）、视频生成（如 `wanx2.1-kf2v-plus`）及语音识别（如 `paraformer-16k-1`）等。其中，**图像、视频、长音频等耗时型任务统一采用异步调用机制**，需先创建任务获取 `task_id`，再通过[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 查询结果或取消任务；而文本类模型（如千问系列）默认支持同步调用，亦可通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope 原生 SDK 调用。

> **注意**：文档 3 中提到“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，无需模型调用授权”，但该描述与权限管控逻辑存在潜在矛盾——实际中，子业务空间内调优模型仍需在该空间内完成模型授权绑定，否则调用将返回 `403 Forbidden`。请以控制台「模型调用权限」配置为准。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | [异步任务](../concepts/asynchronous-task.md)唯一标识符 | UUID 格式字符串，如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `connectionPoolSize`（Java） | 连接池最大连接数 | 默认 `32`，高并发建议设为 `256` | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `limit_per_host`（Python） | 单主机最大连接数 | 默认 `0`（无限制），生产环境建议设为 `30` | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `model_name`（文件上传） | 文件绑定的模型名称 | 必须与后续调用模型一致，如 `qwen-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |

## 使用方式

### 1. 多业务空间模型调用  
必须使用**目标子业务空间的 API Key**，并确保已为其授予对应模型调用权限（标准模型）或确认模型部署于该空间（调优模型）。OpenAI 兼容方式需设置 `base_url`：
- 北京地域：`https://dashscope.aliyuncs.com/compatible-mode/v1`  
- 新加坡地域：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`  
DashScope 原生方式需显式配置 `base_http_api_url` 或使用 Workspace ID 构造 endpoint。

### 2. [异步任务](../concepts/asynchronous-task.md)通知  
避免轮询导致限流（20 QPS），推荐通过[事件总线 EventBridge](../../raw/model-api-reference/more-about-models/async-task-api.md) 配置 HTTP 回调或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，解析 `data.task_id` 后单次查询结果。

### 3. 连接复用  
- **Java SDK**：通过 `Constants.connectionConfigurations` 设置连接池参数（如 `connectionPoolSize`, `readTimeout`）。  
- **Python SDK**：同步场景使用 `requests.Session()`，异步场景使用 `aiohttp.TCPConnector`，均需传入 `session` 参数至 `Generation.call()` 或 `AioGeneration.call()`。

### 4. 本地文件上传  
调用前需上传文件获取 `oss://` 开头的临时 URL（有效期 48 小时），并在模型请求 Header 中添加 `X-DashScope-OssResourceResolve: enable`。上传时必须指定 `model_name`，且该名称须与后续模型调用完全一致。

## 限制和注意事项

- **临时 API Key**：继承源 API Key 的全部权限（含知识库访问限制），不可手动删除，到期自动失效；各地域 API Key 不互通，调用时需匹配对应 endpoint [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **异步任务保留期**：成功/失败任务默认保留 24 小时，超时后数据被清理，无法查询。  
- **文件上传限制**：单文件 ≤ 1 GB；QPS 限流为 100（按主账号+模型维度）；**严禁用于生产环境或压测**，生产应使用 OSS 等长期存储 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **HTTP 回调安全性**：配置 HTTP 回调 URL 时，需确保服务端能校验 `source: acs.dashscope` 和 `type: dashscope:System:AsyncTaskFinish`，防止伪造事件。  
- **SDK 版本要求**：Java SDK 建议 ≥ 2.12.0，Python SDK 建议 ≥ 1.24.0，旧版本可能缺失连接复用或异步任务支持。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)


