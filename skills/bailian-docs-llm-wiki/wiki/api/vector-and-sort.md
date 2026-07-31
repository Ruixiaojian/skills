# vector and sort

`vector and sort` 是百炼平台提供的核心向量化与排序能力集合，涵盖文本/多模态向量生成（embedding）和文本/多模态相关性重排序（rerank）两大功能模块。向量模型将原始内容映射到统一语义空间，支撑检索、聚类、分类等下游任务；排序模型则对召回结果进行精细化打分与重排，显著提升最终结果的相关性。所有能力均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope 原生 SDK 调用。

## 支持的模型与功能

### 文本向量模型（Embedding）
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等通用文本模型，适用于低延迟、小批量场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：支持 `text-embedding-async-v2` 和 `text-embedding-async-v1`，专为超大批量（最高 100,000 行）、长文件（≤200MB）设计，采用异步任务模式 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量模型**：支持 `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等，可处理 text/image/video 及其组合，提供独立向量与融合向量两种模式 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序模型（Rerank）
- **文本排序**：`qwen3-rerank`（推荐替代已下线的 `gte-rerank`），支持纯文本 query-document 排序，最大文档数 500，单条输入上限 4,000 [Token](../concepts/token.md)。
- **多模态排序**：`qwen3-vl-rerank`，支持跨模态 query（text/image）与混合文档（text/image/video）排序，按模态类型分别限制文档数（文本 100、图片 40、视频 4）。
- > **注意**：`gte-rerank` 系列模型（如 `gte-rerank-v2`）将于 2026 年 05 月 30 日下线，新项目请直接使用 `qwen3-rerank` 或 `qwen3-vl-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|------|----------|------|----------|
| `model` | 所有 | 模型名称，如 `"text-embedding-v4"`、`"qwen3-rerank"` | 必选 |
| `input` / `query` + `documents` | 所有 | 向量：字符串、字符串列表或文件 URL；排序：`query`（str/object）与 `documents`（str/array） | 必选 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 指定向量维度（如 `1024`, `2048`），部分模型（如 `multimodal-embedding-v1`）不支持 | 可选 |
| `encoding_format` | 同步文本向量 | 仅支持 `"float"` | 可选 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时返回融合向量（1 个），`false`（默认）返回独立向量（N 个） | 可选 |
| `top_n` | 所有排序模型 | 返回前 N 个最相关结果 | 可选 |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 任务指令（如 `"Retrieve semantically similar text."`），影响排序策略 | 可选 |
| `return_documents` | `gte-rerank-v2`, `qwen3-vl-rerank` | `true` 时在响应中返回原文 | 可选 |

> **注意**：`qwen3-rerank` 的 `top_n` 和 `instruct` 需与 `model` 同级传入，**不可**嵌套在 `parameters` 对象内；而 `qwen3-vl-rerank` 和 `gte-rerank-v2` 的 `top_n`、`return_documents` 等必须置于 `parameters` 对象中 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 使用方式

### 向量生成（Embedding）
- **同步调用（小批量）**：使用 OpenAI SDK 或 HTTP POST 到 `/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`，支持字符串、字符串列表、文件流输入。
- **批处理（大批量）**：通过 HTTP POST 到 `/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding` 创建异步任务，再轮询 `GET /api/v1/tasks/{task_id}` 获取结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态**：HTTP POST 到 `https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 中按 `{ "text": "...", "image": "...", "video": "..." }` 结构组织输入。

### 排序（Rerank）
- **文本排序**：`qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) `POST /{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1/reranks`；其余模型使用原生接口 `POST /{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`。
- **多模态排序**：`qwen3-vl-rerank` 的 `query` 和 `documents` 均支持对象格式（如 `{"text": "..."}` 或 `{"image": "..."}`），需严格匹配模态类型。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：不同模型差异显著。例如 `qwen3.7-text-embedding` 单行支持 128,000 [Token](../concepts/token.md)，而 `text-embedding-v4` 仅支持 8,192 Token；`qwen3-rerank` 单条输入上限为 4,000 Token，`qwen3-vl-rerank` 文本单条上限为 8,000 Token [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **并发与配额**：批处理接口 `text-embedding-async-v2` 限流为 1 RPS，且同时运行中任务数 ≤ 3 个；免费额度按模型单独计算（如 `text-embedding-v4` 各 100 万 Token）[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **[多模态输入](../concepts/multimodal-input.md)约束**：`qwen3-vl-embedding` 单次请求内容元素总数 ≤ 20（图片 ≤ 10，视频 ≤ 1）；`tongyi-embedding-vision-plus-2026-03-06` 图片总数 ≤ 64，视频 ≤ 8 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **地域与 endpoint**：北京地域使用 `cn-beijing.maas.aliyuncs.com`，新加坡地域需替换为 `ap-southeast-1.maas.aliyuncs.com`，且部分接口（如批处理查询）URL 路径不同 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **模型兼容性**：`tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` 不支持 `dimension` 参数，固定返回 1152/768 维；`multimodal-embedding-v1` 固定 1024 维 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


