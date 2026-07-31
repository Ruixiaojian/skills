# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/[多模态](../concepts/multi-modal.md)向量化（embedding）与文本/[多模态](../concepts/multi-modal.md)排序（rerank）两大核心能力，用于构建语义搜索、RAG、跨模态检索等AI应用。向量模型将输入内容映射到统一语义空间，支持相似度计算与聚类；排序模型则对召回结果进行精细化重排，提升相关性精度。两类服务均提供同步、异步及OpenAI兼容接口，适配不同规模与延迟要求的场景。

## 支持的模型与功能

### 向量模型（Embedding）

- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4/v3/v2/v1` 等系列，适用于语义搜索、聚类、分类等任务。其中 `qwen3.7-text-embedding` 和 `text-embedding-v4/v3` 支持动态维度配置（如 `dimensions=1024`），而 `v1/v2` 固定维度（[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)）。
- **[多模态](../concepts/multi-modal.md)向量**：支持 `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，可处理 text/image/video 及其组合。`qwen3-vl-embedding` 通过 `enable_fusion=true` 开启融合向量；`tongyi-embedding-vision-plus-2026-03-06` 则需将多模态字段（如 `text`、`image`）置于同一 content 对象中实现融合（[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)）。
- **批处理向量**：`text-embedding-async-v2/v1` 专为海量文本设计，单次支持最多 100,000 行，文件大小上限 200MB（[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）。

### 排序模型（Rerank）

- **纯文本排序**：`qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-api/v1/reranks`），输入为扁平化 `query` + `documents` 数组，支持 `instruct` 任务提示；`gte-rerank-v2` 已进入下线过渡期（2026年05月30日终止），不建议新项目接入（[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)）。
- **多模态排序**：`qwen3-vl-rerank` 支持 text/image/video 混合查询与文档，需使用 `input.query` 和 `input.documents` 嵌套结构，且 `query` 可为文本或图片（如 `{"image": "url"}`）。

> **注意**：文档 4 中明确标注 `gte-rerank` 模型将于 2026 年 05 月 30 日下线，但文档 1 和文档 2 均未提及该生命周期信息，开发者应以 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 的官方公告为准，优先迁移至 `qwen3-rerank` 或 `qwen3-vl-rerank`。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `model` | 全部 | 必填，指定模型名称，如 `"qwen3-rerank"`、`"tongyi-embedding-vision-plus-2026-03-06"` | `"text-embedding-v4"` |
| `input` / `documents` | embedding: `input.contents`; rerank: `documents` 或 `input.documents` | embedding 输入为 `contents` 数组（含 `text`/`image`/`video` 字典）；rerank 输入为字符串数组（纯文本）或字典数组（多模态） | `[{"text":"hello"},{"image":"url"}]` |
| `query` | rerank | 必填，纯文本模型为字符串；`qwen3-vl-rerank` 支持 `{"text":"..."}` 或 `{"image":"url"}` | `"what is embedding?"` |
| `dimension` | 文本向量（`qwen3.7-text-embedding`, `text-embedding-v3/v4`）、多模态（`qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等） | 可选，指定输出向量维度，不同模型支持范围不同（如 `qwen3-vl-embedding`: 256–2560） | `1024` |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | 布尔值，启用后将 `contents` 中所有模态融合为单个向量；其他融合模型（如 `tongyi-embedding-vision-plus-2026-03-06`）不支持此参数 | `true` |
| `top_n` | rerank | 返回前 N 个最相关结果，默认返回全部 | `5` |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 可选任务指令，影响排序策略（如 `"Retrieve semantically similar text."`） | `"Given a web search query..."` |
| `fps` | `qwen3-vl-rerank`, 多模态向量模型 | 视频帧率控制（0.0–1.0），降低帧数可减少计算开销 | `0.5` |

## 使用方式

### 向量生成
- **同步调用（小批量）**：HTTP POST 到 `/api/v1/services/embeddings/...`（多模态）或 OpenAI 兼容 `/compatible-mode/v1/embeddings`（文本），直接返回向量数组。
- **异步批处理（超大批量）**：调用 `/api/v1/services/embeddings/text-embedding/text-embedding` 并设置 `X-DashScope-Async: enable`，先创建任务获取 `task_id`，再轮询 `/api/v1/tasks/{task_id}` 获取结果（[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）。
- **SDK 封装**：`dashscope.TextEmbedding.call()`（同步）、`dashscope.BatchTextEmbedding.call()`（异步）自动处理协议细节。

### 排序调用
- **纯文本排序**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md) `/compatible-api/v1/reranks`，参数扁平化（`model`, `query`, `documents`, `top_n` 同级）。
- **多模态排序**：使用专用接口 `/api/v1/services/rerank/text-rerank/text-rerank`，参数嵌套于 `input` 和 `parameters` 中。
- **SDK 调用**：`dashscope.TextReRank.call()` 统一入口，根据 `model` 自动路由至对应协议。

## 限制和注意事项

- **输入长度与数量**：
  - 文本向量：`qwen3.7-text-embedding` 单条最长 128,000 [Token](../concepts/token.md)，批量最多 20 条；`text-embedding-v4` 单条限 8,192 [Token](../concepts/token.md)，批量最多 10 条（[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)）。
  - 多模态向量：`qwen3-vl-embedding` 单次请求 `contents` 总数 ≤20，图片≤10张，视频≤1条；`tongyi-embedding-vision-plus-2026-03-06` 支持最多 64 张图片（[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)）。
  - 排序：`qwen3-rerank` 单次最多 500 文档；`qwen3-vl-rerank` 文本文档≤100、图片≤40、视频≤4（[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)）。

- **格式与编码**：
  - 图片/视频 URL 必须公开可访问；Base64 图片需符合 `data:image/{format};base64,{data}` 格式。
  - 视频仅支持 URL，且 `qwen3-vl-rerank` 仅支持 MP4/AVI/MOV，多模态向量模型支持更广格式（如 WEBM、MKV）。

- **计费与限流**：
  - 批处理接口 `text-embedding-async-v2` 有严格并发限制：单用户最多 3 个任务同时运行，排队中+运行中任务总数 ≤50（[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）。
  - 所有模型均受全局 API 限流约束，详见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit) 文档。

- **兼容性**：
  - `qwen3-rerank` 与 OpenAI `rerank` 接口完全兼容，但 `qwen3-vl-rerank` 和 `gte-rerank-v2` 使用百炼专属协议，不可混用参数结构。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


