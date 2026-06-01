# general text embedding

通用文本向量（General Text Embedding）模型可将文本数据转换为高维数值向量，适用于语义搜索、推荐、聚类、分类等下游任务。百炼平台提供同步调用和批处理两种接口模式，支持多语种文本向量化处理。

## 支持的模型

### 同步接口模型

| 模型名称 | 向量维度 | 最大行数 | 单行最大 Token 数 | 支持语种 |
|---------|---------|---------|-----------------|---------|
| text-embedding-v4 | 2048/1536/1024(默认)/768/512/256/128/64 | 10 | 8,192 | 100+ 主流语种及多种编程语言 |
| text-embedding-v3 | 1024(默认)/768/512/256/128/64 | 10 | 8,192 | 50+ 主流语种 |
| text-embedding-v2 | 1,536 | 25 | 2,048 | 中/英/西/法/葡/印尼/日/韩/德/俄 |
| text-embedding-v1 | 1,536 | 25 | 2,048 | 中/英/西/法/葡/印尼 |

text-embedding-v4 属于 Qwen3-Embedding 系列。详见 [同步接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-synchronous-api.md)。

### 批处理接口模型

| 模型名称 | 向量维度 | 单次最大行数 | 单行最大 Token |
|---------|---------|------------|--------------|
| text-embedding-async-v2 | 1,536 | 100,000 | 2,048 |
| text-embedding-async-v1 | 1,536 | 100,000 | 2,048 |

批处理模型支持的语种与同步模型 v2/v1 一致。详见 [批处理接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-batch-api.md)。

## 关键参数

### 同步接口（OpenAI 兼容）

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型名称，如 `text-embedding-v4` |
| `input` | string / array / file | 是 | 输入文本，支持字符串、字符串列表或文件 |
| `dimensions` | integer | 否 | 输出向量维度，仅 v3/v4 支持，默认 1024 |
| `encoding_format` | string | 否 | 返回格式，当前仅支持 `float` |

### 批处理接口（DashScope）

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型名称，如 `text-embedding-async-v2` |
| `input.url` | string | 是 | 待处理文本文件的 HTTP URL（一行一条） |
| `parameters.text_type` | string | 否 | `query`（查询文本）或 `document`（默认，底库文本） |

> **注意**：批处理接口的 `text_type` 参数在同步接口（OpenAI 兼容模式）中不可用。对于检索类非对称任务，建议使用 DashScope 原生接口或批处理接口以区分 query/document 类型。

## 使用方式

### 同步接口

同步接口兼容 OpenAI SDK，支持 Python、Java 和 curl 调用。

**Base URL：** `https://dashscope.aliyuncs.com/compatible-mode/v1`

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

completion = client.embeddings.create(
    model="text-embedding-v4",
    input='待向量化的文本',
    dimensions=1024,
    encoding_format="float"
)
print(completion.model_dump_json())
```

输入支持三种形式：单个字符串、字符串列表、文件对象。具体用法参见 [同步接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-synchronous-api.md)。

### 批处理接口

批处理接口采用异步模式，适合大规模文本向量化（单次最多 10 万行，文件不超过 200MB）。

HTTP 调用需两步完成：
1. 提交任务（需设置 `X-DashScope-Async: enable` 请求头），获取 `task_id`
2. 根据 `task_id` 轮询查询结果

DashScope SDK 封装了轮询逻辑，支持同步调用（自动等待完成）和异步调用（手动查询/等待/取消）。详见 [批处理接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-batch-api.md)。

```python
from dashscope import BatchTextEmbedding

result = BatchTextEmbedding.call(
    BatchTextEmbedding.Models.text_embedding_async_v2,
    url="https://your-file-url/texts.txt",
    text_type="document"
)
print(result)
```

## 限制和注意事项

- **Token 限制**：v3/v4 单行最大 8,192 Token，v1/v2 单行最大 2,048 Token。
- **批量限制**：同步接口 v3/v4 最多 10 行/次，v1/v2 最多 25 行/次；批处理接口最多 100,000 行/次。
- **维度选择**：`dimensions` 参数仅 text-embedding-v3 和 text-embedding-v4 支持，v1/v2 固定为 1536 维。其中 2048 维仅 v4 支持。
- **批处理并发**：单用户最多 50 个排队+运行中的异步作业，最多 3 个并发运行。
- **结果有效期**：批处理任务数据（状态、结果 URL）仅保留 24 小时，需及时下载。
- **免费额度**：同步模型 v3/v4 各 100 万 Token，v1/v2 各 50 万 Token；批处理模型各 2000 万 Token。有效期为百炼开通后 90 天。
- **前提条件**：需获取 API Key 并配置到环境变量，SDK 调用还需安装对应 SDK。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-batch-api.md)

