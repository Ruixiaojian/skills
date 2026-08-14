# vector and sort

`vector and sort` 是百炼平台提供的核心向量化与排序能力集合，涵盖文本、多模态内容的向量生成（embedding），以及对召回结果的精准重排序（rerank）。该能力支撑语义搜索、RAG、跨模态检索、聚类等关键AI应用，支持同步/异步调用、OpenAI兼容接口及专用SDK，适用于从单条文本到百万级批量处理的全场景需求。所有模型均按实际输入[Token](../concepts/token.md)计费，并提供地域化部署与免费额度。

## 支持的模型/功能

### 文本向量模型（Embedding）
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等通用文本模型，适用于实时低延迟场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：支持 `text-embedding-async-v2` 和 `text-embedding-async-v1`，专为超大批量（最高100,000行/请求）和长文件（≤200MB）设计，采用[异步任务](../concepts/async-task.md)模式 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量模型**：支持 `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等，可统一处理文本、图像、视频并生成独立向量或融合向量，实现跨模态语义对齐 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序模型（Rerank）
- **文本排序**：`qwen3-rerank`（推荐替代已下线的 `gte-rerank`），支持纯文本查询与文档排序，最大500文档/请求，语种覆盖100+主流语言。
- **多模态排序**：`qwen3-vl-rerank`，支持文本/图片/视频任意组合的查询与候选文档排序（如图搜文、文搜视频），按模态类型区分限制（文本100条、图片40张、视频4个）。
- **注意**：`gte-rerank` 系列模型（含 `gte-rerank-v2`）将于2026年05月30日下线，新项目请务必使用 `qwen3-rerank` 或 `qwen3-vl-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|------|----------|------|----------|
| `model` | 全部 | 模型名称，如 `"qwen3-rerank"`、`"qwen3-vl-embedding"` | 必选 |
| `input` / `query` / `documents` | 各模型不同 | 向量：支持 `string`、`array<string>`、`file` 或 `object`（含 `text`/`image`/`video` 字段）；排序：`query` 与 `documents` 结构依模型而异（`qwen3-rerank` 扁平，`qwen3-vl-rerank` 需嵌套 `input` 对象） | 必选 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `qwen2.5-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 指定向量维度，如 `1024`；`text-embedding-v2/v1`、`tongyi-embedding-vision-plus/flash`（非2026快照版）、`multimodal-embedding-v1` 不支持此参数 | 可选 |
| `encoding_format` | 同步文本向量 | 输出格式，`"float"`（默认）或 `"base64"` | 可选 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时将 `contents` 中所有模态融合为1个向量；`false`（默认）时各模态独立生成向量 | 可选（仅该模型） |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回排序后前 `n` 个结果；`qwen3-rerank` 位于顶层，其余需置于 `parameters` 内 | 可选 |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 任务指令字符串（如 `"Given a web search query..."`），影响排序策略；建议英文 | 可选 |

> **注意**：`qwen3-rerank` 的 `query` 和 `documents` 参数**不嵌套在 `input` 对象中**，而 `qwen3-vl-rerank` 和 `gte-rerank-v2` **必须**通过 `input.query` 和 `input.documents` 传递，否则报错。

## 使用方式

### 同步调用（文本向量 & 文本排序）
- **OpenAI兼容接口**：适用于熟悉OpenAI生态的用户，配置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（向量）或 `compatible-api/v1/reranks`（排序），直接使用 `openai` SDK。
- **DashScope SDK**：Python/Java SDK 提供 `dashscope.TextEmbedding`、`dashscope.TextReRank` 等封装，参数扁平化，无需手动构造 `input`/`parameters` 嵌套结构。

### 异步调用（批量向量 & 多模态向量）
- **HTTP批处理**：调用 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务，再用 `GET /api/v1/tasks/{task_id}` 轮询结果；需设置 `X-DashScope-Async: enable` 头。
- **多模态向量**：统一使用 `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 数组支持混合模态输入。
- **SDK批处理**：`dashscope.BatchTextEmbedding` 提供 `async_call()`、`fetch()`、`wait()` 等方法，自动处理轮询与状态管理。

### 输入格式示例
- **文本向量（单条）**：
  ```json
  { "model": "qwen3.7-text-embedding", "input": "hello world", "dimensions": 1024 }
  ```
- **多模态向量（融合）**：
  ```json
  {
    "model": "qwen3-vl-embedding",
    "input": { "contents": [{"text":"A cat","image":"https://..."}] },
    "parameters": { "enable_fusion": true }
  }
  ```
- **文本排序（qwen3-rerank）**：
  ```json
  {
    "model": "qwen3-rerank",
    "query": "What is vector search?",
    "documents": ["Vector search finds similar items...", "RAG uses retrieval..."],
    "top_n": 2
  }
  ```

## 限制和注意事项

- **[Token](../concepts/token.md)与尺寸限制**：
  - 同步文本向量：`qwen3.7-text-embedding` 单行最高128,000 [Token](../concepts/token.md)；`text-embedding-v4` 仅8,192 Token。
  - 批处理文本向量：`text-embedding-async-v2` 单行≤2,048 Token，单次最多100,000行，文件≤200MB。
  - 多模态向量：`qwen3-vl-embedding` 图片≤10 MB，视频≤50 MB；`tongyi-embedding-vision-plus-2026-03-06` 支持最多64张图片。
  - 排序：`qwen3-rerank` 单条Query≤4,000 Token；`qwen3-vl-rerank` 文本文档≤100条，图片≤40张，视频≤4个。

- **地域与限流**：
  - 北京/新加坡地域模型参数（如单价、免费额度）存在差异，详见各模型概览表 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
  - 批处理异步作业：单用户并发运行中任务≤3个，排队中+运行中总数≤50个 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

- **兼容性与弃用**：
  - `gte-rerank` 系列模型已标记为下线，新集成必须迁移至 `qwen3-rerank`。
  - `qwen2.5-vl-embedding` 仅支持融合向量，不支持 `enable_fusion=false` 或独立向量输出。
  - `tongyi-embedding-vision-plus/flash`（非2026快照版）不支持 `dimension` 参数，固定返回1152/768维向量。

- **错误处理**：
  - 同步调用失败时，响应含 `code`/`message`（如 `InvalidApiKey`）；[异步任务](../concepts/async-task.md)失败时，`task_status` 为 `FAILED` 并附带 `code`/`message`。
  - 所有成功响应中的 `relevance_score` 为本次请求内相对分数，**不可跨请求比较**。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


