# vector and sort

`vector and sort` 是百炼平台提供的核心向量化与排序能力集合，涵盖文本/[多模态](../concepts/multimodal.md)向量生成（embedding）和检索后精排（rerank）两大类服务。向量模型将原始内容映射到统一语义空间，支撑语义搜索、聚类、推荐等场景；排序模型则对召回结果进行相关性重排序，显著提升最终结果质量。两类能力均提供同步、异步及OpenAI兼容接口，支持灵活集成。

## 支持的模型与功能

### 文本向量模型（Embedding）
- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等多个版本，覆盖不同维度（64–2560）、语种（最多201种）与性能需求 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理异步向量**：`text-embedding-async-v2`（最大100,000行/请求）和 `text-embedding-async-v1`，适用于超大批量文本处理 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **[多模态](../concepts/multimodal.md)向量**：`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等支持文本、图像、视频输入，提供独立向量（各模态单独编码）与融合向量（跨模态联合编码）两种模式 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序模型（Rerank）
- **纯文本排序**：`qwen3-rerank`（OpenAI兼容接口，最大500文档/请求），推荐替代已下线的 `gte-rerank` 系列 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **[多模态](../concepts/multimodal.md)排序**：`qwen3-vl-rerank` 支持文本、图片、视频混合查询与文档排序，适用于跨模态检索场景。

> **注意**：文档 4 明确指出 `gte-rerank` 模型将于2026年05月30日下线，且其 `max_document_count`（30,000）与 `qwen3-rerank`（500）存在数量级差异，实际选型应以 `qwen3-rerank` 或 `qwen3-vl-rerank` 为准，避免依赖过时能力。

## 关键参数

| 参数 | 类型 | 说明 | 支持模型 |
|------|------|------|----------|
| `model` | string | 必选，指定模型名称 | 全部 |
| `input` / `query` / `documents` | string / array / object | 必选，输入内容格式依模型而异：<br>- 文本向量：支持 string、array<string>、file<br>- 多模态向量：`contents` 数组，含 `text`/`image`/`video`/`multi_images` 字段<br>- 排序：`query` + `documents` 数组，`qwen3-rerank` 不嵌套在 `input` 中 | 全部 |
| `dimensions` / `dimension` | integer | 可选，指定输出向量维度 | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等（详见各模型概览表） |
| `encoding_format` | string | 可选，仅支持 `"float"` | 文本向量同步接口 |
| `top_n` | integer | 可选，返回前 N 个排序结果 | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` |
| `instruct` | string | 可选，排序任务指令（如 `"Retrieve semantically similar text."`），影响相关性判断逻辑 | `qwen3-rerank`, `qwen3-vl-rerank` |
| `enable_fusion` | boolean | 可选，仅 `qwen3-vl-embedding` 支持，设为 `true` 启用多模态融合向量 | `qwen3-vl-embedding` |

## 使用方式

### 接口调用路径
- **同步文本向量**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`（OpenAI兼容）或 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding`（DashScope原生）。
- **异步批处理向量**：需两步调用——先 `POST .../api/v1/services/embeddings/text-embedding/text-embedding` 创建任务，再 `GET .../api/v1/tasks/{task_id}` 查询结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：`POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`。
- **排序**：`qwen3-rerank` 使用 `POST .../compatible-api/v1/reranks`；`qwen3-vl-rerank` 和 `gte-rerank-v2` 使用 `POST .../api/v1/services/rerank/text-rerank/text-rerank`。

### SDK 调用示例（Python）
```python
# 文本向量（同步）
from openai import OpenAI
client = OpenAI(base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
resp = client.embeddings.create(model="text-embedding-v4", input=["hello", "world"], dimensions=1024)

# 多模态向量
from dashscope import MultiModalEmbedding
resp = MultiModalEmbedding.call(
    model="qwen3-vl-embedding",
    input={"contents": [{"text": "cat"}, {"image": "https://..."}]},
    parameters={"enable_fusion": True}
)

# 文本排序
import dashscope
resp = dashscope.TextReRank.call(
    model="qwen3-rerank",
    query="what is embedding?",
    documents=["vector representation", "machine learning concept"],
    top_n=1
)
```

## 限制和注意事项

- **输入长度与批量限制**：
  - `qwen3.7-text-embedding`：单字符串最长 128,000 [Token](../concepts/token.md)，批量最多 20 行 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
  - `text-embedding-v4`：单字符串最长 8,192 [Token](../concepts/token.md)，批量最多 10 行。
  - `text-embedding-async-v2`：单次请求最多 100,000 行，单行最长 2,048 [Token](../concepts/token.md)，文件大小 ≤ 200MB [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
  - `qwen3-vl-rerank`：文本文档最多 100 条，图片最多 40 条，视频最多 4 条；总输入 Token ≤ 120,000 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

- **限流策略**：
  - 异步批处理任务：单用户并发运行中任务数上限为 3 个，排队中+运行中总数上限为 50 个 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
  - 所有模型均受全局[限流](https://help.aliyun.com/zh/model-studio/rate-limit)约束，超出将返回 `429` 错误。

- **其他重要事项**：
  - `multimodal-embedding-v1` 和 `tongyi-embedding-vision-plus` 等旧模型不支持 `dimension` 参数，向量维度固定。
  - `qwen2.5-vl-embedding` 仅支持融合向量，不支持独立向量；`tongyi-embedding-vision-plus` 仅支持独立向量 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
  - `qwen3-rerank` 的 `relevance_score` 为相对分数，仅用于本次请求内排序，不可跨请求比较。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


