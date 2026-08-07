# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/[多模态](../concepts/multi-modal.md)向量化（embedding）与文本/跨模态排序（rerank）两大核心能力，支撑语义搜索、RAG、聚类、跨模态检索等典型AI应用。向量模型将非结构化内容映射到统一语义空间，排序模型则对召回结果进行精细化相关性重排。两类服务均提供同步与异步调用方式，并支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。

## 支持的模型与功能

### 文本向量化（Embedding）

- **同步模型**：`qwen3.7-text-embedding`（最高128K [Token](../concepts/token.md)）、`text-embedding-v4`（支持多维度可选）、`text-embedding-v3/v2/v1`，适用于实时单条或小批量文本处理 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理模型**：`text-embedding-async-v2`（1536维，10万行/请求）、`text-embedding-async-v1`，专为大规模离线向量化设计，需通过任务ID轮询结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **[多模态](../concepts/multi-modal.md)向量化**：`qwen3-vl-embedding`（支持独立/融合向量）、`tongyi-embedding-vision-plus-2026-03-06`（Qwen3底座，支持多分辨率与融合）、`multimodal-embedding-v1` 等，统一处理文本、图像、视频输入 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）

- **纯文本排序**：`qwen3-rerank`（OpenAI兼容接口，500文档上限），推荐替代已下线的 `gte-rerank` 系列 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **[多模态](../concepts/multi-modal.md)排序**：`qwen3-vl-rerank`（支持 text/image/video 混合查询与文档），适用于跨模态检索场景，如以图搜文、视频片段排序。

> **注意**：文档 2 中 `qwen3.7-text-embedding` 的“最大行数”为20，而文档 4 中 `qwen3-vl-rerank` 的“最大文档数”为100（文本）/40（图片）/4（视频），二者属不同模型能力，无直接矛盾；但需注意 `qwen3-rerank` 与 `qwen3-vl-rerank` 的接口路径、参数结构及响应格式完全不同，不可混用。

## 关键参数

| 参数 | 适用模型 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必选，指定模型名称 | `"qwen3-rerank"`, `"qwen3-vl-embedding"` |
| `input` / `documents` / `query` | 按模型区分 | 向量模型用 `input`（支持 string/array/file/URL）；排序模型中 `qwen3-rerank` 直接传 `query` 和 `documents` 数组，`qwen3-vl-rerank` 则需嵌套在 `input` 对象内 | `{"text": "hello"}`, `["doc1", "doc2"]` |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding` 等 | 可选，指定输出向量维度 | `1024`, `2560` |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | 布尔值，启用后将 contents 中所有模态融合为单向量 | `true` |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回前 N 个最相关结果 | `5` |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 可选任务指令，影响排序策略（如问答检索 vs 语义相似度） | `"Given a web search query, retrieve relevant passages..."` |
| `fps` | `qwen3-vl-rerank`, `qwen3-vl-embedding` | 视频帧采样率（0–1） | `0.5` |

## 使用方式

### 调用路径与协议
- **同步文本向量**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md) `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`（文档 2）。
- **异步批处理**：专用 HTTP 接口 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding` + `X-DashScope-Async: enable`（文档 1）。
- **多模态向量**：统一接口 `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`（文档 3）。
- **文本排序**：`qwen3-rerank` 使用 OpenAI 兼容 `POST .../compatible-api/v1/reranks`；其余排序模型使用 `POST .../api/v1/services/rerank/text-rerank/text-rerank`（文档 4）。

### SDK 调用要点
- DashScope SDK 封装了底层差异：`BatchTextEmbedding.call()` 用于异步批处理（文档 1），`dashscope.TextReRank.call()` 用于排序（文档 4），`dashscope.MultimodalEmbedding.call()` 用于多模态向量（文档 3）。
- SDK 参数扁平化（如 `top_n`, `instruct` 直接传入），无需手动构造 `input` 或 `parameters` 嵌套对象，与 HTTP 接口结构不一致。

## 限制和注意事项

- **[Token](../concepts/token.md) 与尺寸限制**：
  - 同步文本向量：`qwen3.7-text-embedding` 单字符串最长 128K [Token](../concepts/token.md)；`text-embedding-v4` 单字符串限 8,192 Token，列表最多 10 条（文档 2）。
  - 异步批处理：单次请求最多 100,000 行，单行 ≤ 2,048 Token，文件 ≤ 200MB（文档 1）。
  - 多模态：`qwen3-vl-embedding` 图片 ≤ 10 MB，视频 ≤ 50 MB；`tongyi-embedding-vision-plus` 图片 ≤ 3 MB（文档 3）。
  - 排序：`qwen3-rerank` 单 Query ≤ 4,000 Token，总请求 Token ≤ 120,000（文档 4）。

- **并发与配额**：
  - 异步批处理：单用户并发运行中任务 ≤ 3 个，排队中+运行中总数 ≤ 50（文档 1）。
  - 免费额度：各模型独立计费，免费额度按 Token 计（如 `text-embedding-v4` 100万Token），有效期为开通后 90 天（文档 2、3、4）。

- **模型弃用**：
  > **注意**：`gte-rerank` 系列模型将于 2026-05-30 下线，必须迁移至 `qwen3-rerank` 或 `qwen3-vl-rerank`（文档 4）。

- **融合向量兼容性**：
  - `qwen3-vl-embedding` 使用 `enable_fusion=true` 参数开启融合；
  - `tongyi-embedding-vision-plus-2026-03-06` 等新模型通过将 `text`/`image`/`video` 放在同一 `content` 对象中实现融合，**不支持** `enable_fusion` 参数（文档 3）。

## 来源文档

- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


