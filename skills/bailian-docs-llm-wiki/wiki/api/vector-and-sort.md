# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/[多模态](../concepts/multi-modal.md)向量化（embedding）与文本排序（rerank）两大核心能力，分别用于将非结构化内容映射到语义向量空间、以及对召回结果进行精细化相关性重排序。二者常协同用于 RAG、搜索引擎、推荐系统等场景，支持同步、异步及 OpenAI 兼容调用方式。

## 支持的模型与功能

### 向量化模型（Embedding）

- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等版本，适用于纯文本语义表征 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **批处理文本向量**：`text-embedding-async-v2` / `text-embedding-async-v1`，专为超大批量（单次最多 100,000 行）文本设计，采用异步任务模式 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **[多模态](../concepts/multi-modal.md)向量**：`qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等，支持文本、图像、视频及其组合输入，并提供独立向量与融合向量两种生成模式 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  

### 排序模型（Rerank）

- **纯文本排序**：`qwen3-rerank`（推荐）、`gte-rerank-v2`（即将下线），支持 query-document 相关性打分与 top-k 截断。  
- **[多模态](../concepts/multi-modal.md)排序**：`qwen3-vl-rerank`，支持文本、图片、视频作为 query 或 document 的任意组合排序，适用于跨模态检索 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  
> **注意**：`gte-rerank` 系列模型将于 2026 年 05 月 30 日下线，新项目请优先选用 `qwen3-rerank` 或 `qwen3-vl-rerank`。

## 关键参数

| 参数名 | 类型 | 说明 | 适用模型 |
|--------|------|------|----------|
| `model` | string | 必填，指定模型名称（如 `"text-embedding-v4"`、`"qwen3-rerank"`） | 全部 |
| `input` / `documents` / `query` | string / array / object | 输入内容格式因模型而异：<br>- 文本向量：支持 string、string[]、file；<br>- Rerank：`qwen3-rerank` 要求 `query` 和 `documents` 平级；`qwen3-vl-rerank` 要求嵌套在 `input` 对象中 | 全部 |
| `dimensions` | integer | 指定向量维度（如 `1024`），仅部分模型支持（`text-embedding-v3/v4`、`qwen3-vl-embedding` 等） | 文本/多模态向量 |
| `enable_fusion` | boolean | 仅 `qwen3-vl-embedding` 支持，设为 `true` 时融合所有输入为单向量 | 多模态向量 |
| `top_n` | integer | 返回最相关的前 N 个结果，默认返回全部 | Rerank |
| `instruct` | string | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），影响排序策略，仅 `qwen3-rerank` / `qwen3-vl-rerank` 生效 | Rerank |
| `encoding_format` | string | 当前仅支持 `"float"` | 文本向量（同步） |

## 使用方式

### 同步调用（文本向量）
通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用，适合小批量（≤20 条）实时请求：
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
resp = client.embeddings.create(
    model="text-embedding-v4",
    input=["文本1", "文本2"],
    dimensions=1024
)
```

### 异步调用（批处理向量）
适用于海量文本（100,000 行以内），需先创建任务再轮询结果：
```python
from dashscope import BatchTextEmbedding
result = BatchTextEmbedding.call(
    model=BatchTextEmbedding.Models.text_embedding_async_v2,
    url="https://your-bucket/object.txt",
    text_type="document"
)
# 后续通过 task_id 查询结果
```

### Rerank 调用
区分模型选择不同 endpoint：
- `qwen3-rerank`：使用 `/compatible-api/v1/reranks`（OpenAI 兼容风格）  
- `qwen3-vl-rerank` / `gte-rerank-v2`：使用 `/api/v1/services/rerank/text-rerank/text-rerank`（DashScope 原生风格）  
示例（`qwen3-rerank`）：
```python
resp = dashscope.TextReRank.call(
    model="qwen3-rerank",
    query="用户问题",
    documents=["候选文档1", "候选文档2"],
    top_n=3
)
```

## 限制和注意事项

- **[Token](../concepts/token.md) 与行数限制**：  
  - `qwen3.7-text-embedding` 单条最长 128,000 [Token](../concepts/token.md)，批量最多 20 行；  
  - `text-embedding-v4` 单条最长 8,192 [Token](../concepts/token.md)，批量最多 10 行；  
  - `text-embedding-async-v2` 单次最多 100,000 行，单行 ≤2,048 Token；  
  - `qwen3-rerank` 单次请求总 Token 上限为 `Query Tokens × Document 数 + Document Tokens 总和 ≤ 120,000`。  

- **地域与 endpoint 差异**：  
  > **注意**：文档中 `text-embedding-batch-api.md` 明确要求 HTTP 调用必须携带 `X-DashScope-Async: enable` 请求头，否则报错“current user api does not support synchronous calls”；而 `text-embedding-synchronous-api.md` 的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)默认为同步，两者 endpoint 和鉴权方式不可混用 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  

- **免费额度与有效期**：  
  所有模型均提供开通后 90 天内的免费额度（如 `qwen3.7-text-embedding` 为 100 万 Token），详见各模型概览表格 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  

- **多模态输入规范**：  
  图片/视频 URL 必须公开可访问；Base64 图片需符合 `data:image/{format};base64,{data}` 格式；`qwen2.5-vl-embedding` 不支持 `multi_images`，且仅返回融合向量 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)


