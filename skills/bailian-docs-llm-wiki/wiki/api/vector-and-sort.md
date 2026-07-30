# vector and sort

`vector and sort` 是百炼平台提供的核心语义理解能力套件，涵盖文本/[多模态](../concepts/multi-modal.md)向量化（embedding）与文本排序（rerank）两大功能模块。向量化模型将原始内容映射到统一语义空间，支撑检索、聚类等下游任务；排序模型则对召回结果进行精细化重排序，显著提升相关性精度。二者常协同用于 RAG、搜索引擎等生产级应用。

## 支持的模型与功能

### 文本向量化（Embedding）
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等通用文本模型，适用于低延迟、小批量场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：提供 `text-embedding-async-v2` 和 `text-embedding-async-v1` 异步模型，专为超大批量（单次最多 100,000 行）、长文本（单行最高 2,048 [Token](../concepts/token.md)）场景设计 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **[多模态](../concepts/multi-modal.md)向量化**：支持 `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，可处理 text/image/video 及其组合，支持独立向量与融合向量两种模式 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 文本排序（Rerank）
- **qwen3-rerank**：纯文本排序模型，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，支持 `instruct` 指令微调排序策略（如问答检索 vs 语义相似度），最大文档数 500 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **qwen3-vl-rerank**：[多模态](../concepts/multi-modal.md)排序模型，支持 text/image/video 混合查询与文档，适用于跨模态检索场景。
- **gte-rerank-v2**：高并发文本排序模型，最大文档数达 30,000，但已进入维护期；官方明确提示“gte-rerank 模型将于 2026 年 05 月 30 日下线，推荐使用 qwen3-rerank 替代” [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档 1 中 `text-embedding-v2` 的单价标注为 `0.0007元`，而文档 2 中 `text-embedding-async-v2` 的单价也为 `0.0007元`，但两者适用场景（同步 vs 异步）、输入限制（25 行 vs 100,000 行）和计费粒度（按 [Token](../concepts/token.md) 计费）存在本质差异，不可混用定价对比。

## 关键参数

| 参数名 | 类型 | 说明 | 适用模型 |
|--------|------|------|----------|
| `model` | string | 必选。模型名称，如 `"text-embedding-v4"`、`"qwen3-rerank"`、`"qwen3-vl-embedding"` | 全部 |
| `input` / `query` / `documents` | string/array/object | 输入内容。文本向量支持 string/array/file；排序模型中 `query` 和 `documents` 为必选字段，`qwen3-rerank` 要求扁平结构，其余模型需嵌套在 `input` 对象内 | 各模型按规范 |
| `dimensions` | integer | 可选。指定输出向量维度（如 `1024`, `2048`）。仅 `qwen3.7-text-embedding`、`text-embedding-v3/v4`、`qwen3-vl-embedding` 等部分模型支持 | [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) |
| `enable_fusion` | boolean | 可选。仅 `qwen3-vl-embedding` 支持，设为 `true` 时生成融合向量；`tongyi-embedding-vision-plus-2026-03-06` 等模型通过将 text/image/video 放入同一 content 对象实现融合，**不使用此参数** | [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) |
| `instruct` | string | 可选。仅 `qwen3-rerank` 和 `qwen3-vl-rerank` 支持，用于指定排序任务类型（如 `"Given a web search query..."`），影响相关性判断逻辑 | [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) |
| `top_n` | integer | 可选。返回排序后前 N 个结果，默认返回全部。`qwen3-rerank` 位于顶层，`gte-rerank-v2` 需置于 `parameters` 内 | [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) |

## 使用方式

### 接口调用方式
- **同步向量**：使用 OpenAI 兼容 SDK 或 HTTP POST 到 `/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`，支持 string/array/file 输入。
- **异步向量**：HTTP 调用需两步：1) POST 到 `/api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（带 `X-DashScope-Async: enable` 头）；2) GET `/api/v1/tasks/{task_id}` 查询结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **排序**：`qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) `POST /compatible-api/v1/reranks`；`qwen3-vl-rerank` 和 `gte-rerank-v2` 使用专用接口 `POST /api/v1/services/rerank/text-rerank/text-rerank`，请求体结构不同，务必区分 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **多模态向量**：统一使用 `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，通过 `contents` 数组传入混合模态数据。

### SDK 调用
- 向量：`dashscope.TextEmbedding`（同步）、`dashscope.BatchTextEmbedding`（异步）。
- 排序：`dashscope.TextReRank.call()`，参数扁平化（如 `query`, `documents`, `top_n` 直接传入），无需手动构造 `input`/`parameters` 嵌套对象。
- 多模态向量：`dashscope.MultimodalEmbedding.call()`，支持 `enable_fusion` 等参数直传。

## 限制和注意事项

- **输入长度与数量**：
  - `qwen3.7-text-embedding`：单字符串最长 128,000 [Token](../concepts/token.md)，批量最多 20 行。
  - `text-embedding-v4`：单字符串最长 8,192 Token，批量最多 10 行。
  - `text-embedding-async-v2`：单行最长 2,048 Token，单次最多 100,000 行。
  - `qwen3-rerank`：单 query/document 最长 4,000 Token，单次最多 500 文档。
  - `qwen3-vl-rerank`：文本同上，图片/视频有大小限制（如单图 ≤10 MB）[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

- **限流策略**：
  - 同步向量接口受全局 QPS 限制，具体阈值参考 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)。
  - 异步向量接口严格限制：单用户同时运行中任务 ≤3 个，排队+运行中总任务 ≤50 个 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

- **兼容性与弃用**：
  - `gte-rerank` 系列模型已标记为下线计划，新项目应优先选用 `qwen3-rerank`。
  - `multimodal-embedding-v1` 不支持 `dimension` 参数，固定 1024 维；`tongyi-embedding-vision-plus`/`flash` 亦不支持该参数 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

- **其他**：
  - 所有响应中的 `relevance_score` 为本次请求内的相对分数，**不可跨请求比较**。
  - 异步任务结果 URL 有效期仅 24 小时，需及时下载。
  - 多模态模型中 `qwen2.5-vl-embedding` 仅支持融合向量，不支持 `multi_images` 输入；`tongyi-embedding-vision-plus` 支持 `multi_images` 但不支持融合向量 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)


