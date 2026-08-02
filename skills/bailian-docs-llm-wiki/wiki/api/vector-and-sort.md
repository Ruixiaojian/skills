# vector and sort

百炼平台提供文本向量化（vector）、多模态向量化（multimodal vector）和文本排序（rerank）三大核心能力，覆盖语义搜索、RAG、跨模态检索、聚类等典型AI应用链路。所有能力均支持同步/异步调用，适配 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope 原生 SDK，并具备细粒度参数控制（如维度、融合模式、排序指令）和多地域部署支持。

## 支持的模型/功能

- **通用文本向量模型**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等版本，适用于单文本、批量文本及文件输入的语义表征 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **异步批处理向量模型**：专为超大规模文本（最高 100,000 行）设计，支持 `text-embedding-async-v2` 和 `text-embedding-async-v1`，需通过任务 ID 异步轮询结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态向量模型**：支持文本、图像、视频统一嵌入，包括 `qwen3-vl-embedding`（独立/融合双模式）、`tongyi-embedding-vision-plus-2026-03-06`（Qwen3 底座，支持多分辨率与融合）、`qwen2.5-vl-embedding`（仅融合）等 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **文本排序（Rerank）模型**：支持纯文本（`qwen3-rerank`）、多模态（`qwen3-vl-rerank`）及历史兼容（`gte-rerank-v2`）三类模型，用于对召回结果进行精准重排序。注意：`gte-rerank` 系列将于 2026 年 5 月 30 日下线，[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档已明确迁移建议。

> **注意**：文档 1 中 `text-embedding-v2` 的“单行最大 Token 数”标为 2,048，但文档 4 中 `qwen3-vl-rerank` 的“单条最大输入Token”为 8,000，而 `qwen3-rerank` 为 4,000；三者属不同模型栈，无直接矛盾。但需注意 `qwen3-rerank` 的 `query` 和 `documents` 输入限制（各 ≤4,000 Token）与 `qwen3-vl-rerank` 的混合模态总 Token 限制（≤120,000）存在显著差异，开发者应按模型选型严格遵循对应限制。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `qwen2.5-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 指定向量维度（如 1024、2048、2560），部分模型（如 `tongyi-embedding-vision-plus`）不支持该参数，固定返回指定维度。 |
| `encoding_format` | `text-embedding-*` 同步模型 | 仅支持 `"float"`，控制 Embedding 输出格式。 |
| `enable_fusion` | `qwen3-vl-embedding` | `bool` 类型，设为 `true` 时将 `contents` 中所有模态融合为单个向量；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过将 text/image/video 放在同一 content 对象实现融合，**不使用此参数**。 |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回排序后前 N 个结果，默认返回全部。注意 `qwen3-rerank` 的 `top_n` 与 `instruct` 同级，而 `qwen3-vl-rerank` 需置于 `parameters` 内。 |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 英文任务指令（如 `"Retrieve semantically similar text."`），影响排序策略，不指定则默认按问答检索任务处理。 |
| `text_type` | `text-embedding-async-v2` | 区分 `query`（查询文本）与 `document`（底库文本），提升检索效果；聚类等对称任务可省略（默认 `document`）。 |

## 使用方式

- **同步向量化（推荐小批量）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK，支持字符串、字符串列表、文件三种 `input` 格式。例如 Python 调用 `text-embedding-v4`：
  ```python
  client.embeddings.create(model="text-embedding-v4", input=["文本A", "文本B"], dimensions=1024)
  ```
- **异步批处理（推荐超大批量）**：必须通过 HTTP 创建任务（带 `X-DashScope-Async: enable` 头），再轮询 `GET /api/v1/tasks/{task_id}` 获取结果；SDK 封装了 `async_call`/`wait`/`fetch` 等便捷方法 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态向量化**：HTTP 请求体中 `input.contents` 为数组，每个元素为 `{"text": "..."}, {"image": "..."}, {"video": "..."}` 或 `{"multi_images": [...]}`；融合向量需按模型要求设置 `enable_fusion=true`（`qwen3-vl-embedding`）或同 content 对象内混写（`tongyi-embedding-vision-plus-2026-03-06`）。  
- **文本排序**：`qwen3-rerank` 使用 OpenAI 兼容 `/reranks` 接口，`query` 与 `documents` 平级；`qwen3-vl-rerank` 和 `gte-rerank-v2` 使用 `/text-rerank` 接口，`query` 与 `documents` 必须嵌套在 `input` 对象内。SDK 调用统一使用 `dashscope.TextReRank.call()`，参数扁平化（无需手动构造 `input`/`parameters` 嵌套）。

## 限制和注意事项

- **输入规模限制**：  
  - 同步文本向量：`qwen3.7-text-embedding` 单行最长 128,000 Token，最多 20 行；`text-embedding-v4` 单行最长 8,192 Token，最多 10 行；`text-embedding-v2` 单行最长 2,048 Token，最多 25 行。  
  - 异步批处理：`text-embedding-async-v2` 单次请求最多 100,000 行，单行最长 2,048 Token，文件大小 ≤200MB。  
  - 多模态向量：`qwen3-vl-embedding` 单次请求内容元素总数 ≤20（图片≤10，视频≤1）；`tongyi-embedding-vision-plus-2026-03-06` 图片≤64，视频≤8。  
  - 排序模型：`qwen3-rerank` 单次最多 500 个文档；`qwen3-vl-rerank` 文本文档≤100、图片≤40、视频≤4；总输入 Token ≤120,000（公式：`Query Tokens × Document 数 + Document Tokens 总和`）。  

- **地域与 endpoint 差异**：同步/兼容接口（如 `/compatible-mode/v1/embeddings`）和异步接口（如 `/api/v1/services/embeddings/...`）的 base URL 不同，且需替换 `{WorkspaceId}` 并匹配地域（如 `cn-beijing` 或 `ap-southeast-1`）。  

- **免费额度与限流**：各模型均有独立免费额度（如 `text-embedding-v4` 为 100 万 Token/90 天），超出后按量计费；异步批处理有并发任务数限制（如 `text-embedding-async-v2` 最多 3 个并发运行中任务）[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  

- **模型弃用提醒**：`gte-rerank` 系列模型将于 2026 年 5 月 30 日下线，新项目请优先选用 `qwen3-rerank` 或 `qwen3-vl-rerank`。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


