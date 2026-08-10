# vector and sort

`vector and sort` 是百炼平台提供的核心向量化与排序能力集合，涵盖文本、[多模态](../concepts/multi-modal.md)内容的向量生成（embedding）以及对召回结果的语义重排序（rerank）。该能力支撑[检索增强生成](../concepts/rag.md)（RAG）、跨模态搜索、内容聚类等典型AI应用，支持同步/异步调用模式，并提供OpenAI兼容接口以降低迁移成本。所有模型均需通过API Key认证，且部分功能受地域、额度和限流策略约束。

## 支持的模型/功能

### 向量生成（Embedding）
- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等模型，适用于语义搜索、聚类等场景。其中 `qwen3.7-text-embedding` 支持最长 128,000 [Token](../concepts/token.md) 的单条输入，而 `text-embedding-v4` 限制为 8,192 [Token](../concepts/token.md) [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **[多模态](../concepts/multi-modal.md)向量**：支持 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，可处理 text/image/video 及其组合，提供独立向量（各模态单独编码）与融合向量（跨模态联合编码）两种模式 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **批处理向量**：`text-embedding-async-v2` 支持单次最多 100,000 行文本的异步批量处理，适用于大规模底库向量化 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 排序（Rerank）
- **纯文本排序**：`qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，支持 `instruct` 指令定制排序策略（如问答检索或语义相似度），最大文档数为 500 条 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **[多模态](../concepts/multi-modal.md)排序**：`qwen3-vl-rerank` 支持 text/image/video 混合查询与文档，例如以图搜文、以文搜视频，但文档数限制依模态类型而异（文本 100 条、图片 40 条、视频 4 条）。
- **已下线模型注意**：`gte-rerank` 系列将于 2026 年 05 月 30 日下线，官方明确推荐迁移到 `qwen3-rerank` 或 `qwen3-vl-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档 1 中称 `tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` “仅支持独立向量”，但文档 1 后续表格又列出二者支持 `multi_images` 多图序列——该能力本质属于独立向量范畴（每张图生成一个向量），无矛盾；而文档 4 中 `qwen3-vl-rerank` 的“单条最大输入[Token](../concepts/token.md)”标注为 8,000，但其实际计算逻辑是 `Query Tokens × Document 数量 + Document Tokens 总和 ≤ 请求最大输入Token（120,000）`，此处“单条”易引发歧义，应以文档 4 的公式说明为准。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `dimension` | `qwen3.7-text-embedding`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度，不同模型支持范围不同。`text-embedding-v2` 等旧模型不支持此参数 | `1024`, `2560` |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | 控制是否将 `contents` 中所有模态融合为 1 个向量；`tongyi-embedding-vision-plus-2026-03-06` 等新版模型通过将 text/image/video 放在同一 content 对象中实现融合，**不使用此参数** | `true` |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回排序后前 N 个结果，默认返回全部 | `5` |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 自定义任务指令，影响排序逻辑（如 `"Given a web search query..."` 强化问答匹配） | `"Retrieve semantically similar text."` |
| `fps` | `qwen3-vl-rerank`, `multimodal-embedding` 视频输入 | 视频帧抽取比例，范围 `[0,1]`，默认 `1.0` | `0.5` |
| `text_type` | `text-embedding-async-v2` | 标注文本用途（`query` 或 `document`），影响向量表示，对非对称检索任务重要 | `"query"` |

## 使用方式

### 调用路径
- **同步向量**：HTTP POST 到 `/api/v1/services/embeddings/...`（多模态）或 OpenAI 兼容 `/compatible-mode/v1/embeddings`（文本）。
- **异步向量**：HTTP POST 到 `/api/v1/services/embeddings/text-embedding/text-embedding` 并设置 `X-DashScope-Async: enable`，再 GET `/api/v1/tasks/{task_id}` 查询结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **排序**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks`；其余 rerank 模型使用 `/api/v1/services/rerank/text-rerank/text-rerank`。

### 输入格式差异
- **文本向量**：`input` 可为字符串、字符串数组或文件对象（SDK 支持直接传 file handle）。
- **多模态向量**：`input.contents` 为对象数组，每个元素为 `{"text": "..."} / {"image": "..."} / {"multi_images": [...]}` 等形式。
- **排序**：`qwen3-rerank` 的 `query` 和 `documents` 与 `model` 同级；`qwen3-vl-rerank` 必须包裹在 `input` 对象内，且 `query` 和 `documents` 元素支持模态字典（如 `{"image": "url"}`）。

### SDK 便捷调用
- 文本向量：`dashscope.TextEmbedding.call(model=..., input="...")`
- 批处理向量：`dashscope.BatchTextEmbedding.call(model=..., url="...")`
- 排序：`dashscope.TextReRank.call(model=..., query="...", documents=[...])`

## 限制和注意事项

- **地域与模型可用性**：`tongyi-embedding-vision-plus` 在新加坡地域仅支持中英文，而北京地域支持超30种语言；`qwen3-vl-rerank` 的视频输入仅支持 MP4/AVI/MOV 格式且必须为公开 URL [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **额度与计费**：免费额度按 Token 计，有效期为开通后 90 天；`multimodal-embedding-v1` 的图片/视频单价为 0.0009 元/千 Token，显著高于新版 `tongyi-embedding-vision-plus-2026-03-06`（0.0005 元）[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **限流**：异步批处理任务并发上限为 3 个，排队中+运行中任务总数不超过 50 个；同步接口 RPS 限制需参考[限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)。
- **输入限制**：`text-embedding-v4` 单次请求最多 10 条文本，每条 ≤ 8,192 Token；`qwen3-vl-embedding` 单次 `contents` 总数 ≤ 20，图片 ≤ 10 张，视频 ≤ 1 条 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **响应解析**：`qwen3-rerank` 响应中 `results` 直接位于顶层，而 `qwen3-vl-rerank` 的 `results` 包裹在 `output` 内，SDK 封装后统一为 `resp.output.results`，但原始 HTTP 响应结构必须区分 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


