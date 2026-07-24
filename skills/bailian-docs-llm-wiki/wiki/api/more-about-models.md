# [more](more.md) about models

百炼平台提供多种模型调用机制与配套能力，覆盖同步/[异步任务](../concepts/asynchronous-task.md)、多模态[文件处理](../concepts/file-processing.md)、子空间隔离、连接优化等关键场景。本文面向开发者梳理核心能力、参数配置、使用方式及限制，帮助构建稳定高效的模型服务集成。

## 支持的模型/功能

百炼支持两类主要调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）：适用于文本生成、多模态理解等低延迟场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音识别 `paraformer-16k-1`）：适用于耗时较长的任务，需通过任务 ID 轮询或事件通知获取结果。  

[异步任务](../concepts/asynchronous-task.md)统一由 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 提供生命周期管理（查询、批量查询、取消），并支持通过 [HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md) 避免轮询限流。  
> **注意**：文档 3 中提到“任务完成后立即推送”，但实际事件总线投递存在毫秒级延迟，不保证严格实时；生产环境应以查询接口返回的 `task_status` 为准，而非仅依赖事件时间戳。

多模态模型（如 VL、OCR、ASR）需传入文件 URL。百炼提供免费临时存储，上传后获得 `oss://` 前缀的临时 URL（有效期 48 小时），详见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

## 关键参数

| 参数 | 说明 | 典型值/范围 | 注意事项 |
|------|------|-------------|----------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒 | 默认 60 秒，不可超过 30 分钟 |
| `task_id` | [异步任务](../concepts/asynchronous-task.md)唯一标识 | UUID 格式字符串 | 必须在创建任务时保存，用于后续查询或取消 |
| `model_name` | 模型名称 | `qwen-plus`, `wanx2.1-t2i-turbo` 等 | 文件上传时必须指定，且与后续调用模型严格一致 |
| `X-DashScope-OssResourceResolve: enable` | 临时 OSS URL 解析头 | 固定字符串 | **必须显式添加**，否则模型调用将失败 |
| 连接池参数（Java） | `connectionPoolSize`, `maximumAsyncRequests` 等 | 默认 `32`，建议高并发下设为 `256` | 需确保 `maximumAsyncRequestsPerHost ≤ maximumAsyncRequests ≤ connectionPoolSize` |

## 使用方式

### 1. 调用子业务空间模型  
必须使用该子空间专属 API Key，并按地域选择正确 endpoint：  
- **北京地域**：OpenAI 兼容 `base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"`；DashScope 原生 `base_url = "https://dashscope.aliyuncs.com/api/v1"`  
- **新加坡地域**：需替换 `{WorkspaceId}`，如 `base_url = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"`  
> **注意**：调优部署的模型**仅支持 DashScope 原生协议**，不兼容 OpenAI 接口，详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

### 2. 上传文件并调用多模态模型  
```python
# 1. 获取临时 URL（需指定 model_name）
url = upload_file_and_get_url(api_key, "qwen-vl-plus", "/tmp/image.png")

# 2. 调用模型（必须带解析头）
headers = {
    "Authorization": f"Bearer {api_key}",
    "X-DashScope-OssResourceResolve": "enable"
}
data = {"input": {"image_url": url}, "model": "qwen-vl-plus"}
requests.post("https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation", 
              headers=headers, json=data)
```

### 3. 启用连接复用（高性能场景）  
- **Java SDK**：通过 `Constants.connectionConfigurations` 全局配置连接池；  
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession()`，详见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 限制和注意事项

- **临时 API Key**：继承源 Key 的全部权限（含模型/知识库访问限制），**无法提前撤销**，到期自动失效；各地域 API Key 不互通，调用前需确认 endpoint 匹配。  
- **临时文件 URL**：  
  - 有效期严格为 **48 小时**，过期后 URL 失效；  
  - 上传限流为 **100 QPS（按主账号+模型维度）**，不可扩容；  
  - **禁止用于生产环境**，生产推荐使用阿里云 OSS 并自行管理鉴权。  
- **异步任务**：  
  - 仅 `PENDING` 状态可取消，`RUNNING` 或已完成任务不可取消；  
  - 任务结果默认保留 **24 小时**（具体以对应模型文档为准），超时后数据自动清理；  
  - 查询接口限流 **20 QPS/账号**，高频轮询易触发限流。  
- **安全要求**：在浏览器/移动端等不可信环境调用模型时，**必须使用临时 API Key**，严禁暴露永久 Key，参见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


