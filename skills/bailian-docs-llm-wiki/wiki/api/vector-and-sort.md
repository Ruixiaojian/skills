# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本向量化（embedding）、[多模态](../concepts/multi-modal.md)向量化、文本排序（rerank）三大能力，支撑语义搜索、RAG、跨模态检索等核心场景。所有服务均提供同步与异步两种调用模式，支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope 原生 SDK，并按 [Token](../concepts/token.md) 或任务计费。开发者可根据数据规模、延迟要求和模态类型选择合适模型与接口。

## 支持的模型/功能

### 文本向量模型（Embedding）
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等通用文本模型，适用于实时低延迟场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：支持 `text-embedding-async-v2` 和 `text-embedding-async-v1`，专为大规模文本（单次最多 100,000 行）设计，采用异步任务模式 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **[多模态](../concepts/multi-modal.md)向量模型**：支持 `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等，可生成独立向量（每模态一个向量）或融合向量（[多模态](../concepts/multi-modal.md)统一表征），覆盖文本、图像、视频输入 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 文本排序模型（Rerank）
- **qwen3-rerank**：纯文本排序，最高支持 500 个文档，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-api/v1/reranks`），参数扁平化（`query`、`documents` 与 `model` 同级）。
- **qwen3-vl-rerank**：多模态排序（文本/图像/视频混合），支持图文互搜、跨模态检索，需使用 `/api/v1/services/rerank/...` 接口。
- **gte-rerank-v2**：高并发文本排序模型，最大支持 30,000 文档，但已于 2026 年 05 月 30 日下线，官方明确推荐迁移至 `qwen3-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档 3 明确指出 `gte-rerank` 模型将于 2026 年 05 月 30 日下线，而文档 1 和文档 2 均未提及该下线计划，存在信息滞后。请以文档 3 的公告为准，新项目应避免选用 `gte-rerank-v2`。

## 关键参数

| 参数 | 适用模型/接口 | 说明 | 是否必选 |
|------|----------------|------|----------|
| `model` | 所有 | 模型名称，如 `"qwen3.7-text-embedding"`、`"qwen3-rerank"`、`"qwen3-vl-embedding"` | ✅ |
| `input` / `documents` / `query` | 因模型而异 | - 同步 embedding：`input` 支持 `string`、`array<string>` 或 `file`<br>- Rerank：`query` + `documents`（`qwen3-rerank`）或嵌套 `input.query` + `input.documents`（`qwen3-vl-rerank`） | ✅ |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3`, `text-embedding-v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 指定向量维度（如 `1024`），非所有模型均支持；`multimodal-embedding-v1` 等旧模型不支持该参数 | ❌（可选） |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时将 `contents` 中所有模态融合为 1 个向量；默认 `false`（独立向量） | ❌（仅 `qwen3-vl-embedding`） |
| `top_n` | Rerank 模型 | 返回排序后前 N 个结果，默认返回全部 | ❌（可选） |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Given a web search query..."`），显著影响排序策略 | ❌（可选） |
| `text_type` | 异步 embedding (`text-embedding-async-v2`) | 区分 `"document"`（底库）或 `"query"`（检索词），提升检索精度 | ❌（可选） |

## 使用方式

### 同步调用（Embedding & Rerank）
- **Embedding**：使用 OpenAI SDK 或 DashScope SDK，通过 `base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"` 调用 `/embeddings` 接口。支持单文本、文本列表、文件流输入。
- **Rerank（qwen3-rerank）**：使用 `/compatible-api/v1/reranks` 接口，参数扁平化（`model`, `query`, `documents`, `top_n` 同级），响应结构简洁（`results` 数组含 `index` 和 `relevance_score`）。
- **Rerank（qwen3-vl-rerank）**：使用 `/api/v1/services/rerank/...` 接口，`query` 和 `documents` 必须嵌套在 `input` 对象内，支持 `{"text": "..."}` 或 `{"image": "url"}` 格式。

### 异步调用（Batch Embedding）
- **HTTP 方式**：两步操作：① `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（需 `X-DashScope-Async: enable` 头），② `GET /api/v1/tasks/{task_id}` 查询结果。
- **SDK 方式**：使用 `BatchTextEmbedding.call()`（同步封装）或 `BatchTextEmbedding.async_call()`（原始异步），支持 `wait()`、`fetch()`、`cancel()` 等任务管理方法。

### 多模态向量
- **独立向量**：`contents` 数组中每个元素为独立模态（`{"text":...}`, `{"image":...}`），返回等长向量数组。
- **融合向量**：
  - `qwen3-vl-embedding`：设置 `"enable_fusion": true`；
  - `tongyi-embedding-vision-plus-2026-03-06`：将 `text`、`image`、`video` 放在同一 `content` 对象内（如 `{"text": "...", "image": "...", "video": "..."}`）。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：
  - 同步文本 embedding：`qwen3.7-text-embedding` 单行最高 128,000 [Token](../concepts/token.md)；`text-embedding-v4` 仅 8,192 Token。
  - Rerank：`qwen3-rerank` 单条 Query 最高 4,000 Token；`qwen3-vl-rerank` 请求总 Token 上限为 120,000（公式：`Query Tokens × Document 数 + Document Tokens 总和`）。
  - 多模态 embedding：`qwen3-vl-embedding` 文本上限 32,000 Token，图片单张 ≤10 MB，视频 ≤50 MB。

- **批量限制**：
  - 同步 embedding：`qwen3.7-text-embedding` 最多 20 行；`text-embedding-v4` 仅 10 行。
  - 异步 embedding：`text-embedding-async-v2` 单次请求最多 100,000 行，文件 ≤200 MB。
  - Rerank：`qwen3-rerank` 最多 500 文档；`qwen3-vl-rerank` 文本类最多 100 文档，图片类最多 40，视频类最多 4。

- **地域与定价差异**：
  - 同一模型（如 `qwen3.7-text-embedding`）在北京与新加坡地域单价不同（北京 0.0005 元/千 Token，新加坡 0.000525 元/千 Token），且免费额度政策不一致（如 `text-embedding-v4` 在新加坡无免费额度）。

- **兼容性与迁移**：
  - [OpenAI 兼容接口](../concepts/openai-compatible-api.md)仅支持部分模型（如 `qwen3.7-text-embedding`, `qwen3-rerank`），不支持 `qwen3-vl-rerank` 或多模态 embedding，后者必须使用 DashScope 原生 `/api/v1/services/...` 接口。
  - `gte-rerank-v2` 已标记为下线模型，新项目严禁使用；历史项目需按公告迁移至 `qwen3-rerank`。

- **其他**：
  - 异步 embedding 任务状态保留 24 小时，超时自动清除，请及时保存 `url` 结果。
  - `multimodal-embedding-v1` 不支持 `dimension` 参数，固定输出 1024 维向量。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)


