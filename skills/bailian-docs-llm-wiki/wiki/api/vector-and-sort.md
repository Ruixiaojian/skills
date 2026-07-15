# vector and sort

`vector and sort` 是百炼平台提供的核心向量化与排序能力集合，涵盖文本、多模态内容的嵌入（Embedding）生成，以及基于语义相关性的精准重排序（Rerank）。该能力支撑[检索增强生成](../concepts/rag.md)（RAG）、跨模态搜索、聚类分析等关键AI应用，支持同步/异步调用、OpenAI兼容接口及多语言、多分辨率、多模态输入。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`（最高128K token）、`text-embedding-v4`（最高8K token）、`text-embedding-v3/v2/v1` 等系列，提供灵活维度选择（如256–2560维）和多语种支持（最多201种）[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理接口**：仅支持 `text-embedding-async-v1/v2`，适用于超大批量文本（单次最多100,000行），但不支持动态维度配置，固定输出1536维向量[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **OpenAI兼容模式**：通过 `compatible-mode/v1/embeddings` endpoint 调用 `text-embedding-v4` 等模型，支持 `dimensions` 和 `encoding_format` 参数，便于生态迁移[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

### 多模态向量模型
- 支持 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，统一文本/图像/视频向量空间，支持独立向量（各模态单独编码）与融合向量（跨模态联合编码）两种模式[原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- 关键参数如 `enable_fusion`（仅 `qwen3-vl-embedding`）、`res_level`（分辨率档位）、`max_video_frames`（视频帧采样上限）均需在 `parameters` 中显式指定。

### 排序（Rerank）模型
- `qwen3-rerank`：纯文本排序，OpenAI兼容接口，支持 `instruct` 任务提示词，最大文档数500条[原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- `qwen3-vl-rerank`：多模态排序，支持文本/图片/视频混合查询与文档，需使用 `input.query` 和 `input.documents` 结构化输入。
- `gte-rerank-v2`：已进入下线倒计时（2026年5月30日），建议迁移到 `qwen3-rerank` 或 `qwen3-vl-rerank`[原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档2中 `text-embedding-v4` 的“最大行数”为10，而文档1中 `text-embedding-async-v2` 的“单次请求文本最大行数”为100,000——二者属不同调用路径（同步 vs 异步），无矛盾；但文档2称 `qwen3.7-text-embedding` 支持“单行最长128,000 Token”，而文档1明确 `text-embedding-async-v2` 单行上限为2,048 Token，此为模型能力差异，非错误。

## 关键参数

| 参数名 | 适用场景 | 说明 | 必选/可选 |
|--------|----------|------|-----------|
| `model` | 所有接口 | 模型名称，如 `text-embedding-v4`、`qwen3-vl-rerank` | 必选 |
| `input` | 同步/多模态/Rerank | 字符串、字符串数组、文件对象或 `{"contents": [...]}` 结构体；异步批处理仅支持 `url` 字段 | 必选 |
| `dimensions` | 同步文本模型 | 指定向量维度（如1024），仅 `qwen3.7-text-embedding`、`text-embedding-v3/v4` 支持；`multimodal-embedding-v1` 等固定维度模型不支持 | 可选 |
| `text_type` | 异步批处理 | `"query"` 或 `"document"`，影响向量表征优化方向 | 可选（默认 `"document"`） |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时返回融合向量，`false`（默认）时返回独立向量 | 可选 |
| `top_n` | Rerank | 返回前N个最相关结果，`qwen3-rerank` 直接置于顶层，`qwen3-vl-rerank` 需置于 `parameters` 内 | 可选 |
| `instruct` | `qwen3-rerank` / `qwen3-vl-rerank` | 任务指令（如 `"Retrieve semantically similar text."`），显著影响排序策略 | 可选 |

## 使用方式

### 调用路径选择
- **小批量实时向量化**（≤25条文本）：优先使用同步接口 `POST /compatible-mode/v1/embeddings`，延迟低、响应快。
- **超大批量离线处理**（≥1000行）：必须使用异步批处理接口 `POST /api/v1/services/embeddings/text-embedding/text-embedding` + `GET /api/v1/tasks/{task_id}`，避免超时[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态内容处理**：统一使用 `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，按 `contents` 数组构造输入。
- **排序任务**：`qwen3-rerank` 用 OpenAI 兼容 `/compatible-api/v1/reranks`；其余 rerank 模型用 `/api/v1/services/rerank/text-rerank/text-rerank`。

### SDK 与 HTTP 差异
- DashScope SDK 对参数进行了扁平化封装（如 `BatchTextEmbedding.call(..., url=..., text_type=...)`），无需手动构造 `input` 和 `parameters` 嵌套结构；HTTP 则严格要求 JSON 层级[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- OpenAI SDK 调用需设置 `base_url` 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，并传入 `DASHSCOPE_API_KEY` 作为 `api_key`。

### 多模态输入示例
```json
{
  "model": "qwen3-vl-embedding",
  "input": {
    "contents": [
      {"text": "商品标题"},
      {"image": "https://example.com/1.jpg"},
      {"image": "https://example.com/2.jpg"},
      {"video": "https://example.com/demo.mp4"}
    ]
  },
  "parameters": {
    "enable_fusion": true,
    "dimension": 2048
  }
}
```

## 限制和注意事项

- **Token 与尺寸限制**：
  - 同步文本模型：`qwen3.7-text-embedding` 单行上限128,000 Token；`text-embedding-v4` 单行上限8,192 Token；异步批处理单行上限2,048 Token[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
  - 多模态模型：图片单张≤10 MB（`qwen3-vl-embedding`），视频≤50 MB；`tongyi-embedding-vision-plus` 图片≤3 MB[原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
  - Rerank：`qwen3-vl-rerank` 文本文档上限100条、图片上限40张、视频上限4个；总请求 Token 上限120,000[原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

- **并发与配额**：
  - 异步批处理：单用户并发运行中任务数上限3个，排队中+运行中总数上限50个[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
  - 免费额度：各模型独立计算，如 `text-embedding-v2` 享50万Token免费额度，`qwen3-vl-embedding` 享100万Token，均限百炼开通后90天内有效。

- **关键注意事项**：
  - HTTP 异步调用**必须**携带 `X-DashScope-Async: enable` 请求头，否则报错 `current user api does not support synchronous calls`。
  - `qwen2.5-vl-embedding` 仅支持融合向量，不支持 `enable_fusion` 参数（因其恒为 true）；`tongyi-embedding-vision-plus` 系列则不支持该参数，融合需将多模态字段置于同一 `content` 对象内。
  - `gte-rerank-v2` 已标记为下线模型，新项目请勿选用[原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 来源文档

- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


