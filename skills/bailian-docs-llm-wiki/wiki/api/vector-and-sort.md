# vector and sort

`vector and sort` 是百炼平台提供的核心向量化与排序能力集合，涵盖文本、[多模态](../concepts/multi-modal.md)内容的向量生成（embedding）以及跨模态/纯文本的语义相关性重排序（rerank）。该能力支撑语义搜索、RAG、推荐系统、聚类等典型AI应用，支持同步、异步及OpenAI兼容调用方式，适用于从单条文本到百万级批量数据的不同场景。

## 支持的模型/功能

### 文本向量模型（Embedding）
- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等系列模型，提供 64–2560 维可选向量，覆盖 201 种语种 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理文本向量**：`text-embedding-async-v2`（最大 100,000 行/请求，单行 ≤2,048 [Token](../concepts/token.md)）和 `text-embedding-async-v1`，专为大规模离线向量化设计 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **[多模态](../concepts/multi-modal.md)向量**：支持文本、图像、视频统一语义空间编码，包括 `qwen3-vl-embedding`（支持独立/融合向量）、`tongyi-embedding-vision-plus-2026-03-06`（支持多分辨率 `res_level` 和视频帧数控制 `max_video_frames`）等 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序模型（Rerank）
- **纯文本排序**：`qwen3-rerank`（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，最大 500 文档/请求，单文档 ≤4,000 [Token](../concepts/token.md)），已替代即将下线的 `gte-rerank` 系列 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **[多模态](../concepts/multi-modal.md)排序**：`qwen3-vl-rerank` 支持文本、图片、视频混合查询与文档排序（如“以图搜文”、“以文搜视频”），最大支持 100 文本/40 图片/4 视频文档 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档 4 明确指出 `gte-rerank` 模型将于 2026 年 05 月 30 日下线，新项目应使用 `qwen3-rerank` 或 `qwen3-vl-rerank`，避免依赖已废弃模型。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|------|----------|------|----------|
| `model` | 所有 | 模型名称，如 `"text-embedding-v4"`、`"qwen3-rerank"` | 必选 |
| `input` / `query` + `documents` | 所有 | 向量：字符串、字符串列表或文件 URL；排序：`query`（字符串或模态对象）+ `documents`（字符串列表或模态对象数组） | 必选 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度，值域因模型而异（如 `text-embedding-v4`: 64–2048；`qwen3-vl-embedding`: 256–2560） | 可选（默认值见各模型概览） |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回前 N 个最相关结果 | 可选 |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | `true` 时将 `contents` 中所有模态融合为 1 个向量；`false`（默认）则各模态独立生成向量 | 可选（仅该模型） |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 任务指令（如 `"Retrieve semantically similar text."`），影响排序策略 | 可选 |
| `res_level` / `max_video_frames` | 仅 `tongyi-embedding-vision-plus-2026-03-06` / `tongyi-embedding-vision-flash-2026-03-06` | 分辨率档位（0–3）和视频最大采样帧数（≤64） | 可选 |

## 使用方式

### 同步调用（推荐小批量）
- **文本向量**：使用 OpenAI 兼容 SDK 或 HTTP POST 到 `/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`，支持 `input` 为字符串、列表或文件流 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **排序**：`qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) `/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1/reranks`；`qwen3-vl-rerank` 使用专用接口 `/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`。

### 异步调用（推荐大批量）
- **文本向量**：通过 `X-DashScope-Async: enable` 头发起批处理任务，上传含文本的 OSS URL，再轮询 `GET /api/v1/tasks/{task_id}` 获取结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量/排序**：暂不支持异步模式，需同步调用。

### SDK 封装
DashScope SDK 提供 `BatchTextEmbedding`（批向量）、`TextReRank`（排序）等高层封装，自动处理地域配置、认证与响应解析，降低集成复杂度。示例见各文档中 Python/Java SDK 调用片段。

## 限制和注意事项

- **[Token](../concepts/token.md) 与尺寸限制**：
  - `qwen3.7-text-embedding` 单文本最长 128,000 Token；`text-embedding-v4` 仅 8,192 Token；`qwen3-vl-embedding` 文本限 32,000 Token，图片 ≤10 MB，视频 ≤50 MB [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
  - `qwen3-rerank` 单次请求总 Token = `Query Tokens × Document 数量 + Document Tokens 总和`，上限 120,000；`qwen3-vl-rerank` 文本文档上限 100 条，图片上限 40 条 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **免费额度与计费**：各模型均有 90 天有效期的免费额度（如 `text-embedding-v4` 100 万 Token），超限后按实际消耗计费；注意 `text-embedding-async-v2` 单价为 0.0007 元/千 Token，而 `text-embedding-v4` Batch 调用为 0.00025 元/千 Token [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **地域与 endpoint 差异**：北京地域使用 `cn-beijing.maas.aliyuncs.com`，新加坡地域需替换为 `ap-southeast-1.maas.aliyuncs.com`；多模态向量统一使用 `dashscope.aliyuncs.com` 公共域名 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **模型能力差异**：`tongyi-embedding-vision-plus` 固定 1152 维，不支持 `dimension` 参数；`multimodal-embedding-v1` 不支持 `dimension` 且仅支持中英文；`qwen2.5-vl-embedding` 仅支持融合向量，不支持 `enable_fusion` 参数 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


