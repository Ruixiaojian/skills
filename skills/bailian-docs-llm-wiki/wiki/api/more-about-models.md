# [more](more.md) about models

百炼平台提供多种模型调用机制与配套能力，以支持不同场景下的开发需求。本文档面向开发者，系统梳理模型调用的核心能力：包括异步任务管理、子业务空间隔离、临时文件上传、连接复用优化，以及安全的临时 API Key 生成机制。所有能力均基于 DashScope 统一 API 层，需配合有效的 API Key 使用。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）：适用于文本生成、多模态理解等毫秒级响应场景，直接返回结果。
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音识别 `paraformer-16k-1`）：因处理耗时长，采用“提交任务 → 查询状态 → 获取结果”三步流程，详见[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

此外，平台提供以下关键辅助功能：
- **子业务空间模型调用**：通过独立 API Key 和权限管控，实现模型访问隔离与费用分账，适用于多租户或业务线分治场景 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。
- **本地文件上传获取临时 URL**：为多模态模型提供 `oss://` 格式临时存储地址（有效期 48 小时），上传时必须指定目标模型且与后续调用一致 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **HTTP 回调或 RocketMQ 接收异步通知**：替代轮询，通过事件总线主动推送任务完成事件（`dashscope:System:AsyncTaskFinish`），提升实时性并规避 20 QPS 限流 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

> **注意**：文档 4 中提到“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，无需模型调用授权”，但该描述与文档 2 中“异步任务仅支持当前 API Key 所属主账号下的任务”存在隐含冲突——调优模型实际仍受主账号及空间权限双重约束，开发者应以控制台实际配置的模型调用权限为准。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `task_id` | 异步任务唯一标识符，用于查询、取消任务 | `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `expire_in_seconds` | 临时 API Key 有效期（秒），范围 `[1, 1800]` | `1800`（30 分钟） | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `model_name` | 文件上传时必需指定的模型名，决定存储策略与后续调用兼容性 | `qwen-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 调用模型时**必须显式声明**的请求头 | — | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize`（Java） / `limit`（Python） | SDK 连接池核心参数，直接影响高并发吞吐能力 | Java 默认 `32`，推荐生产环境设为 `256`；Python `limit=100` | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 异步任务全流程（推荐结合事件通知）
```bash
# 步骤1：提交异步任务（如文生图）
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{"model": "wanx2.1-t2i-turbo", "input": {"prompt": "a cat"}}'

# 步骤2：配置事件总线监听 dashscope:System:AsyncTaskFinish 事件（避免轮询）
# 步骤3：收到通知后，用 task_id 查询结果
curl -X GET "https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 2. 子业务空间调用（OpenAI 兼容模式）
- 使用**该子空间专属 API Key**；
- 设置 `base_url` 为对应地域兼容地址（北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`）；
- 模型名（如 `qwen-plus`）与默认空间一致，但权限由子空间独立管控。

### 3. 临时文件上传与使用
- 调用 `GET /api/v1/uploads?action=getPolicy&model=qwen-vl-plus` 获取上传凭证；
- 用凭证直传 OSS，获得 `oss://...` URL；
- 在模型请求中传入该 URL，并**必须添加 Header**：`X-DashScope-OssResourceResolve: enable`。

### 4. SDK 连接复用（Java/Python）
- **Java**：通过 `Constants.connectionConfigurations` 全局配置连接池参数（如 `connectionPoolSize=256`）；
- **Python**：创建 `requests.Session()` 或 `aiohttp.ClientSession()` 并传入 `session=` 参数至 `Generation.call()` 或 `AioGeneration.call()`。

## 限制和注意事项

- **临时 API Key**：继承源 API Key 的全部权限（含模型/知识库访问限制），且**无法手动删除**，仅能等待 TTL 到期自动失效 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **临时文件**：  
  - 有效期严格为 **48 小时**，过期后 URL 失效；  
  - 上传限流为 **100 QPS（按主账号+模型维度）**，**禁止用于生产环境或压测**；  
  - 生产环境务必使用阿里云 OSS 等长期稳定存储。
- **异步任务生命周期**：任务完成后保留 **24 小时**，超时后数据被自动清理，不可恢复。
- **地域与 Endpoint 绑定**：北京、新加坡、弗吉尼亚等地域的 API Key **不通用**，且各 Endpoint（如 `dashscope.aliyuncs.com` vs `maas.aliyuncs.com`）不可混用，需严格匹配。
- **连接复用生效前提**：Python SDK 的 `session` 参数仅对 `Generation.call()` 和 `AioGeneration.call()` 生效；Java SDK 的全局配置需在首次调用前完成初始化。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


