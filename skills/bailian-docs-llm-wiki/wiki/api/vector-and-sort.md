# vector and sort

`vector and sort` 是百炼平台提供的核心向量化与排序能力集合，涵盖文本、[多模态](../concepts/multimodal.md)内容的语义向量生成（embedding），以及对召回结果进行精细化相关性重排序（rerank）。该能力支撑语义搜索、RAG、跨模态检索、聚类等典型AI应用，支持同步/异步调用、OpenAI兼容接口及专用SDK，适用于从单条文本实时处理到百万级批量作业的全场景需求。所有模型均基于Qwen系列大模型底座优化，兼顾精度、速度与多语言支持。

## 支持的模型/功能

### 文本向量模型（Embedding）
- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等版本，覆盖 64–2560 维可选输出，最高单行 128,000 [Token](../concepts/token.md)（`qwen3.7-text-embedding`）[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理异步文本向量**：`text-embedding-async-v2`（最大 100,000 行/请求，单行 ≤2,048 [Token](../concepts/token.md)）和 `text-embedding-async-v1`，适用于大规模离线向量化任务 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **[多模态](../concepts/multimodal.md)向量**：支持文本、图像、视频统一语义空间表征，包括 `qwen3-vl-embedding`（支持独立/融合向量）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06`（新版Qwen3底座，支持多分辨率与融合）等 [原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序模型（Rerank）
- **纯文本排序**：`qwen3-rerank`（最大 500 文档/请求，单文档 ≤4,000 [Token](../concepts/token.md)），采用 [OpenAI 兼容接口](../concepts/openai-compatibility.md)，支持 `instruct` 任务指令微调排序策略 [原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **[多模态](../concepts/multimodal.md)排序**：`qwen3-vl-rerank`（支持 text/image/video 混合查询与文档，文本最多 100 条、图片最多 40 张、视频最多 4 条），适用于跨模态检索场景。
- **已弃用模型**：`gte-rerank` 系列将于 2026-05-30 下线，官方明确推荐迁移至 `qwen3-rerank` 或 `qwen3-vl-rerank`。

> **注意**：文档 1 中 `text-embedding-v2` 的“最大行数”为 25，而文档 2 中 `text-embedding-async-v2` 的“单次请求文本最大行数”为 100,000 —— 二者属不同接口（同步 vs 异步），参数不可直接对比；但需注意 `text-embedding-v2` 同步接口不支持批量输入超过 20 行（见文档 1 表格中“最大行数”列），实际批量应使用异步接口。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|------|----------|------|----------|
| `model` | 所有 | 模型名称，如 `"qwen3.7-text-embedding"`、`"qwen3-rerank"` | 必选 |
| `input` / `query` + `documents` | embedding / rerank | embedding：`string` / `array<string>` / `file` / `object`（多模态）；rerank：`query`（string or object） + `documents`（array） | 必选 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度，不同模型支持值不同（如 `qwen3-vl-embedding`: 2560/2048/...） | 可选（默认值见各模型概览） |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | `true` 时将 `contents` 中所有模态融合为 1 个向量；`false`（默认）则各模态独立生成向量 | 可选（仅多模态独立/融合场景） |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回排序后前 N 个结果 | 可选 |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 英文任务指令（如 `"Given a web search query..."`），影响排序逻辑 | 可选 |
| `text_type` | `text-embedding-async-v2`（batch） | `"document"`（默认）或 `"query"`，用于非对称检索场景优化 | 可选 |
| `url`（batch input） | `text-embedding-async-v2/v1` | 输入文件 HTTP URL，需公开可访问，文件 ≤200MB，单行 ≤2,048 Token | 必选（batch 场景） |

## 使用方式

### 同步调用（小规模、低延迟）
- **文本向量**：通过 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（`/compatible-mode/v1/embeddings`）或 DashScope SDK `client.embeddings.create()` 调用，支持字符串、字符串列表、文件流输入。示例：
  ```python
  client.embeddings.create(
      model="qwen3.7-text-embedding",
      input=["苹果", "香蕉"],
      dimensions=1024,
      encoding_format="float"
  )
  ```
- **文本排序**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks` 接口，参数扁平化（`query`, `documents`, `top_n` 同级）；`qwen3-vl-rerank` 使用 `/api/v1/services/rerank/...`，需嵌套 `input` 对象 [原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

### 异步调用（大规模、高吞吐）
- **文本批量向量**：调用 `/api/v1/services/embeddings/text-embedding/text-embedding`（HTTP）或 `BatchTextEmbedding.call()`（SDK），传入 `url` 指向含文本的文件（每行一条），返回 `task_id` 后轮询 `/api/v1/tasks/{task_id}` 获取结果 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：仅支持同步 HTTP 调用（`POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`），`input.contents` 为混合模态数组，支持 `text`/`image`/`video`/`multi_images` [原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 多模态输入格式
- **独立向量**：`contents: [{"text": "A"}, {"image": "url1"}, {"video": "url2"}]` → 返回 3 个向量。
- **融合向量**：
  - `qwen3-vl-embedding`：`{"enable_fusion": true}` + 多个 `{"text":...}`, `{"image":...}` 元素；
  - `tongyi-embedding-vision-plus-2026-03-06`：单个 `content` 对象内同时含 `text`/`image`/`video` 键 → 自动融合。

## 限制和注意事项

- **Token 与尺寸限制**：
  - `qwen3.7-text-embedding` 单行最高 128,000 Token，但 `text-embedding-v4` 仅 8,192 Token；务必按模型规格选择。
  - 多模态模型中，`qwen3-vl-embedding` 图片 ≤10 MB，视频 ≤50 MB；`tongyi-embedding-vision-plus` 图片 ≤3 MB，视频 ≤10 MB。
  - `qwen3-vl-rerank` 单次请求总 Token = `Query Tokens × Document 数量 + Document Tokens 总和`，上限 120,000。

- **地域与计费差异**：
  - 北京地域部分模型提供免费额度（如 `qwen3.7-text-embedding` 各 100 万 Token），新加坡地域无免费额度（见文档 1 表格）。
  - `text-embedding-async-v2` 在北京地域单价 0.0007 元/千 Token，且有 2000 万 Token 免费额度 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

- **限流与并发**：
  - 同步接口受 RPS 限制（具体值需查[限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)）；
  - 异步批处理严格限制：单用户同时运行中任务 ≤3 个，排队中+运行中任务总数 ≤50 个。

- **兼容性与迁移**：
  - `gte-rerank` 系列已标记为下线，必须迁移至 `qwen3-rerank` 或 `qwen3-vl-rerank`；
  - `qwen2.5-vl-embedding` 仅支持融合向量，不支持 `enable_fusion` 参数（因其恒为融合）；
  - `tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` 不支持 `dimension` 参数，向量维度固定。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


