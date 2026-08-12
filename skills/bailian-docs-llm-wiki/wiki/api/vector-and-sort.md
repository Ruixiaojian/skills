# vector and sort

`vector and sort` 是百炼平台提供的两类核心语义理解能力：**向量化（vector）** 将文本、图像、视频等多模态内容映射为稠密向量，支撑语义搜索、聚类与推荐；**排序（sort / rerank）** 对召回结果进行精细化相关性重排序，显著提升 RAG、搜索引擎等场景的最终准确率。二者常组合使用——先用向量模型召回候选集，再用排序模型精排。

## 支持的模型/功能

### 向量模型
- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2` 等，提供多种维度（如 256–2560）和语种支持（最多 201 种）[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **批处理文本向量**：`text-embedding-async-v2` 支持单次 10 万行、单行 2048 [Token](../concepts/token.md) 的大规模异步向量化 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态向量**：`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等支持文本/图像/视频统一语义空间编码，可生成独立向量或融合向量 [原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序模型
- **纯文本排序**：`qwen3-rerank`（推荐替代已下线的 `gte-rerank`）支持最高 500 文档/次、4000 [Token](../concepts/token.md)/query，兼容 OpenAI 风格接口 [原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  
- **多模态排序**：`qwen3-vl-rerank` 支持文本、图片、视频混合输入（如图文混合检索），最大文档数依模态类型动态调整（文本 100、图片 40、视频 4）[原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  
> **注意**：`gte-rerank` 系列模型将于 2026 年 5 月 30 日下线，文档中仍保留其调用示例，但生产环境应迁移至 `qwen3-rerank` 或 `qwen3-vl-rerank`。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度（如 `1024`）。不支持该参数的模型（如 `text-embedding-v2`, `multimodal-embedding-v1`）返回固定维度。 |
| `encoding_format` | 同步文本向量模型 | 取值 `"float"`（默认）或 `"base64"`，影响响应中向量的序列化格式。 |
| `top_n` | 所有排序模型 | 返回排序后前 N 个结果，默认返回全部。 |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 任务指令字符串（如 `"Given a web search query, retrieve relevant passages..."`），用于引导排序策略，仅英文有效。 |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | `true` 时将 `contents` 中所有模态融合为单个向量；`false`（默认）则各模态独立生成向量。`tongyi-embedding-vision-plus-2026-03-06` 等新版模型通过将 text/image/video 放入同一 content 对象实现融合，**不使用此参数**。 |
| `text_type` | 批处理文本向量模型 | `"query"` 或 `"document"`，用于非对称检索任务优化（如区分查询与底库文本）。 |

## 使用方式

### 向量调用
- **同步 API**：适用于小批量（≤20 行文本）实时场景，支持 `string`/`array<string>`/`file` 输入，使用 OpenAI 兼容 SDK 或 HTTP POST 到 `compatible-mode/v1/embeddings`。  
- **异步批处理**：适用于海量文本（≤10 万行），需先 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务，再 `GET /api/v1/tasks/{task_id}` 轮询结果 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态向量**：HTTP 请求体 `input.contents` 数组中按需混排 `{"text":"..."}`, `{"image":"..."}`, `{"video":"..."}`，通过 `parameters.enable_fusion` 或结构设计控制输出模式 [原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序调用
- **`qwen3-rerank`**：使用 `compatible-api/v1/reranks` 接口，`query` 和 `documents` 与 `model` 同级，无需嵌套 `input` 对象。  
- **`qwen3-vl-rerank` / `gte-rerank-v2`**：使用 `api/v1/services/rerank/text-rerank/text-rerank` 接口，`query` 和 `documents` 必须包裹在 `input` 对象内，且 `parameters` 为独立对象 [原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  
- **SDK 调用**：DashScope SDK（如 `dashscope.TextReRank.call`）将 HTTP 的嵌套结构扁平化，直接传参 `query`, `documents`, `top_n` 等，更简洁。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：  
  - 同步文本向量：`qwen3.7-text-embedding` 单行最高 128,000 Token，`text-embedding-v4` 仅 8,192 Token；超长文本将被截断，影响向量质量。  
  - 排序模型：`qwen3-rerank` 单 query 最高 4,000 Token；`qwen3-vl-rerank` 总请求 Token = `Query Tokens × Document 数 + Document Tokens 总和`，上限 120,000。  
- **并发与配额**：  
  - 异步批处理：单用户同时运行中任务 ≤3 个，排队中任务 ≤50 个 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
  - 免费额度：各模型免费额度独立（如 `qwen3.7-text-embedding` 100 万 Token），有效期为百炼开通后 90 天。  
- **地域差异**：北京与新加坡地域的模型单价、免费额度略有不同（如 `text-embedding-v4` 新加坡无免费额度），调用前需确认 workspace 所属地域。  
- **模型兼容性**：`qwen2.5-vl-embedding` 仅支持融合向量且不支持 `multi_images`；`tongyi-embedding-vision-plus` 固定 1152 维，不支持 `dimension` 参数。务必按 [原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 中的“模型能力对照”表选型。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)


