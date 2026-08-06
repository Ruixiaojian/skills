# vector and sort

百炼平台提供文本向量（vector）、[多模态](../concepts/multimodal.md)向量（multimodal vector）和文本排序（sort / rerank）三类核心语义理解能力，分别用于语义表征、跨模态检索与相关性精排。所有能力均支持同步与异步调用模式，适配 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)及 DashScope 原生 SDK，适用于 RAG、搜索增强、聚类分析等生产场景。开发者可根据数据规模、模态类型、延迟敏感度和精度要求选择对应模型与接口。

## 支持的模型/功能

### 文本向量化
- **同步模型**：`qwen3.7-text-embedding`（最高 128K token 输入）、`text-embedding-v4`（推荐，支持 `dimensions` 动态指定）、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`  
- **异步批处理模型**：`text-embedding-async-v2`（单次最多 100,000 行）、`text-embedding-async-v1`  
- **OpenAI 兼容性**：所有同步文本向量模型均支持 OpenAI `/embeddings` 接口协议，详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)

### [多模态](../concepts/multimodal.md)向量化
- **支持模态**：文本、图片（JPEG/PNG/WEBP 等）、视频（MP4/AVI/MOV 等 URL）及多图序列（`multi_images`）  
- **核心模型**：`qwen3-vl-embedding`（支持独立/融合向量）、`tongyi-embedding-vision-plus-2026-03-06`（Qwen3 底座，支持 `res_level` 和 `max_video_frames`）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-flash-2026-03-06`（轻量级）  
- **关键能力**：所有模型输出向量位于统一语义空间，可直接计算跨模态余弦相似度，详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)

### 文本排序（Rerank）
- **主流模型**：`qwen3-rerank`（纯文本，最高 500 文档）、`qwen3-vl-rerank`（[多模态](../concepts/multimodal.md)，支持文/图/视频混合查询与文档）、`gte-rerank-v2`（已进入下线过渡期）  
- **重要提示**：`gte-rerank` 系列模型将于 2026 年 05 月 30 日正式下线，[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档明确建议迁移至 `qwen3-rerank` 或 `qwen3-vl-rerank`

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|------|----------|------|----------|
| `model` | 全部 | 模型名称，如 `"text-embedding-v4"`、`"qwen3-rerank"`、`"qwen3-vl-embedding"` | 必选 |
| `input` / `documents` / `query` | 按模型区分 | 同步向量：`input`（string/array/file）；排序：`query` + `documents`；多模态：`input.contents`（array of objects） | 必选 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-*2026-03-06` | 指定向量维度（如 `1024`, `2560`），不支持的模型将忽略该参数或报错 | 可选 |
| `encoding_format` | 同步文本向量 | 仅支持 `"float"` | 可选 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时融合所有 `contents` 为单向量；`false`（默认）时各模态独立生成向量 | 可选（仅该模型） |
| `top_n` | 所有排序模型 | 返回最相关的前 N 条结果，默认返回全部 | 可选 |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 任务指令（如 `"Retrieve semantically similar text."`），影响排序策略 | 可选 |
| `return_documents` | `gte-rerank-v2`, `qwen3-vl-rerank` | 是否在响应中返回原始文档内容（`true`/`false`） | 可选 |

> **注意**：`text-embedding-v1/v2` 不支持 `dimensions` 参数，但文档 1 中表格错误列出 `text-embedding-v2` 的向量维度为 `1536`（实际固定），而 `text-embedding-v3/v4` 明确支持该参数；请以 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 中“请求体”章节的参数说明为准。

## 使用方式

### 同步调用（低延迟、小批量）
- **文本向量**：使用 OpenAI SDK 或 DashScope SDK 调用 `/compatible-mode/v1/embeddings`  
  ```python
  client.embeddings.create(model="text-embedding-v4", input=["hello", "world"], dimensions=1024)
  ```
- **文本排序**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks`；其余排序模型使用 `/api/v1/services/rerank/...`  
- **多模态向量**：统一使用 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`

### 异步调用（大批量、长耗时）
- **文本批处理**：调用 `/api/v1/services/embeddings/text-embedding/text-embedding` 创建任务，再轮询 `/api/v1/tasks/{task_id}` 获取结果  
- **SDK 封装**：`BatchTextEmbedding.call()`（同步阻塞）或 `BatchTextEmbedding.async_call()`（返回 task 对象）  
- **文件要求**：输入文件需为 UTF-8 编码纯文本，每行一条待处理文本，单行 ≤ 2048 token，总行数 ≤ 100,000（`text-embedding-async-v2`）

### 多模态融合 vs 独立向量
- **独立向量**（默认）：`contents: [{"text":"A"}, {"image":"url1"}, {"video":"url2"}]` → 返回 3 个向量  
- **融合向量**：  
  - `qwen3-vl-embedding`：添加 `"parameters": {"enable_fusion": true}`  
  - `tongyi-*2026-03-06`：将多模态放入同一对象 `"contents": [{"text":"A","image":"url1"}]`  

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：  
  - `qwen3.7-text-embedding` 单文本最长 128,000 token；`text-embedding-v4` 为 8,192；`qwen3-rerank` query ≤ 4,000 token，总请求 token = `query_tokens × doc_count + sum(doc_tokens)` ≤ 120,000  
  - 多模态模型中，`qwen3-vl-embedding` 文本限 32,000 token，图片单张 ≤ 10 MB，视频 ≤ 50 MB  

- **并发与配额**：  
  - 异步批处理：单用户同时运行中任务 ≤ 3 个，排队中任务 ≤ 50 个（`text-embedding-async-v2`）  
  - 免费额度按模型独立计算（如 `text-embedding-v4` 100 万 token，`qwen3-rerank` 另计），有效期均为开通后 90 天  

- **模型兼容性与弃用**：  
  > **注意**：`gte-rerank` 系列模型已标记为下线，且文档 3 明确指出 `gte-rerank` 将于 2026 年 05 月 30 日终止服务；新项目应避免选用。  
  > **注意**：`multimodal-embedding-v1` 不支持 `dimension` 参数（固定 1024 维），但文档 4 表格中未标注此限制，实际调用会报错；请以 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) “模型能力对照”章节为准。  

- **地域与 endpoint**：  
  - 北京地域 base URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`  
  - 新加坡地域需替换为 `ap-southeast-1`，且部分模型（如 `tongyi-embedding-vision-plus`）仅在新加坡可用  

- **错误处理**：所有接口均返回标准 `request_id`，用于问题溯源；失败时响应含 `code` 和 `message` 字段，需参考 [错误码](https://help.aliyun.com/zh/model-studio/error-code) 解析。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)


