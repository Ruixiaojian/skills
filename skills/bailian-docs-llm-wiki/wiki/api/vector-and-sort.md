# vector and sort

百炼平台的 vector and sort 功能涵盖文本/多模态向量化（embedding）与文本/多模态排序（rerank）两大能力，支撑语义搜索、RAG、跨模态检索等核心场景。向量化模型将原始内容映射到统一语义空间，排序模型则对召回结果进行精细化相关性重排。两类服务均提供同步、异步及 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，适配不同规模与延迟要求。

## 支持的模型/功能

- **文本向量化**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2` 等通用模型，以及 `text-embedding-async-v2`（批处理专用）[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态向量化**：支持 `qwen3-vl-embedding`（独立/融合）、`tongyi-embedding-vision-plus-2026-03-06`（独立/融合）、`qwen2.5-vl-embedding`（仅融合）等，覆盖文本、图像、视频及其组合输入 [原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **文本与多模态排序**：`qwen3-rerank`（纯文本，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)）、`qwen3-vl-rerank`（文本/图像/视频混合查询与文档）、`gte-rerank-v2`（已进入下线流程，2026年5月30日终止服务）[原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  

> **注意**：`gte-rerank-v2` 已明确标注将于 2026 年 5 月 30 日下线，新项目应使用 `qwen3-rerank` 或 `qwen3-vl-rerank` 替代；而 `text-embedding-v1` 在文档1中列出但未在文档2/3/4中被任何示例或参数说明引用，其功能与维护状态存疑，不建议新接入。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 指定向量维度（如 `1024`, `2048`），非所有模型均支持；`multimodal-embedding-v1`、`tongyi-embedding-vision-plus` 等固定维度模型不接受该参数。 |
| `enable_fusion` | `qwen3-vl-embedding` | `bool` 类型，设为 `true` 时将 `contents` 中所有模态输入融合为单个向量；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过同 content 对象内混写 `text`/`image`/`video` 实现融合，**不使用此参数**。 |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回排序后前 N 个结果；`qwen3-rerank` 的 `top_n` 位于请求体顶层，而 `qwen3-vl-rerank`/`gte-rerank-v2` 需置于 `parameters` 对象内。 |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 任务指令字符串（如 `"Given a web search query, retrieve relevant passages..."`），显著影响排序策略，**仅英文有效**；`gte-rerank-v2` 不支持。 |
| `text_type` | `text-embedding-async-v2`（批处理） | 区分 `query`（查询文本）与 `document`（底库文本），用于优化非对称检索效果；对聚类等对称任务可省略（默认 `document`）。 |

## 使用方式

- **同步调用（小批量、低延迟）**：适用于 ≤20 行文本（`qwen3.7-text-embedding`）或 ≤500 文档（`qwen3-rerank`）。使用 OpenAI 兼容 SDK 或 HTTP POST 到 `/compatible-mode/v1/embeddings` 或 `/compatible-api/v1/reranks`。示例见 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **异步批处理（超大批量）**：适用于 100,000 行文本（`text-embedding-async-v2`）或大文件（≤200MB）。需两步：1）调用 `/api/v1/services/embeddings/text-embedding/text-embedding` 创建任务；2）轮询 `/api/v1/tasks/{task_id}` 获取结果。详情参见 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态输入**：统一使用 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` 接口，`input.contents` 为模态对象数组（如 `{"text": "..."}`, `{"image": "url"}`），融合模式按模型规则配置（见上表）。  
- **排序多模态查询**：`qwen3-vl-rerank` 支持 `query` 为 `{"text": ...}` 或 `{"image": ...}`，`documents` 可混合 `text`/`image`/`video`；`qwen3-rerank` 仅支持纯文本 `query` 和 `documents` 字符串列表。

## 限制和注意事项

- **[Token](../concepts/token.md) 与尺寸限制**：  
  - `qwen3.7-text-embedding` 单行最大 128,000 [Token](../concepts/token.md)，`text-embedding-v4` 仅 8,192 [Token](../concepts/token.md)；  
  - `qwen3-vl-embedding` 图片单张 ≤10 MB，视频 ≤50 MB；`tongyi-embedding-vision-plus` 图片 ≤3 MB；  
  - `qwen3-rerank` 单次请求总 Token = `Query Tokens × Document 数量 + Document Tokens 总和`，上限 120,000；`qwen3-vl-rerank` 文本文档上限 100 条、图片 40 条、视频 4 条。  
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，新加坡地域同名模型无免费额度 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **[异步任务](../concepts/asynchronous-task.md)生命周期**：批处理任务 ID 查询有效期为 **24 小时**，结果 URL 也仅保留 24 小时，需及时下载。  
- **模型兼容性陷阱**：`qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-api/v1/reranks`），而 `qwen3-vl-rerank` 和 `gte-rerank-v2` 必须使用 `/api/v1/services/rerank/...` 接口，**混用会导致 404 或参数错误**。  
- **编码与格式**：图像/视频 URL 必须公开可访问；Base64 图像需符合 `data:image/{format};base64,{data}` 格式；多图 `multi_images` 仅 `tongyi-embedding-vision-plus` 系列支持。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


