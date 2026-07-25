# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本向量化（embedding）、多模态向量化（multimodal embedding）和文本排序（rerank）三大能力，支撑语义搜索、RAG、跨模态检索等核心场景。所有模型均提供同步/异步调用方式，支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope 原生 SDK，并严格区分输入类型（如 query/document）、模态组合（text/image/video）及向量生成模式（独立/融合），开发者需按任务需求选择对应模型与参数。

## 支持的模型/功能

### 文本向量化（Embedding）
- **同步模型**：`qwen3.7-text-embedding`（最高 128K [Token](../concepts/token.md) 输入）、`text-embedding-v4`（默认 1024 维，支持 `dimensions` 参数）、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`  
- **异步批处理模型**：`text-embedding-async-v2`（单次最多 100,000 行，每行 ≤2,048 [Token](../concepts/token.md)）、`text-embedding-async-v1`  
- **OpenAI 兼容性**：所有同步模型支持 `/compatible-mode/v1/embeddings` 接口，详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)

### 多模态向量化（Multimodal Embedding）
- **支持模型**：`qwen3-vl-embedding`（支持独立/融合向量，通过 `enable_fusion=true` 切换）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06` 与 `tongyi-embedding-vision-flash-2026-03-06`（通过同 content 对象内混合 text/image/video 实现融合）、`tongyi-embedding-vision-plus` / `flash`（仅独立，支持 `multi_images`）  
- **关键能力**：所有模态向量位于同一语义空间，可直接计算余弦相似度；支持跨模态检索（如以文搜图）、多图序列输入（最多 64 张）及视频帧采样（`fps` 参数）  
- 详细输入格式与模型能力对照见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)

### 文本排序（Rerank）
- **主流模型**：`qwen3-rerank`（纯文本，500 文档上限，推荐用于 RAG 场景）、`qwen3-vl-rerank`（多模态，支持 text/image/video 混合查询与文档）、`gte-rerank-v2`（已进入维护期，将于 2026 年 5 月 30 日下线）  
- **接口差异**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks`，其余模型使用 `/api/v1/services/rerank/text-rerank/text-rerank`；参数结构不同（如 `qwen3-rerank` 不嵌套 `input` 和 `parameters`）  
- > **注意**：文档 2 中明确指出 `gte-rerank` 模型即将下线，而文档 1 和文档 3 均未提及该信息，开发者应优先迁移至 `qwen3-rerank` 或 `qwen3-vl-rerank`，参考 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 的迁移指引

## 关键参数

| 参数名 | 类型 | 适用模型 | 说明 |
|--------|------|----------|------|
| `model` | string | 全部 | 必选，值需严格匹配模型概览表中的名称（如 `"text-embedding-v4"`、`"qwen3-rerank"`） |
| `input` / `documents` / `query` | string/array/object | 因模型而异 | 向量模型：支持 string、string[]、file；rerank 模型：`qwen3-rerank` 要求顶层 `query` + `documents`，`qwen3-vl-rerank` 要求 `input.query` + `input.documents`；多模态模型要求 `input.contents` 数组 |
| `dimensions` | integer | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 可选，指定输出向量维度；`text-embedding-v2/v1`、`tongyi-embedding-vision-plus/flash`（非快照版）、`multimodal-embedding-v1` 不支持此参数 |
| `encoding_format` | string | 同步文本向量模型 | 可选，当前仅支持 `"float"` |
| `enable_fusion` | boolean | 仅 `qwen3-vl-embedding` | 可选，设为 `true` 时将 `contents` 中所有模态融合为单个向量；其他融合模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过同 content 对象实现，不使用此参数 |
| `instruct` | string | `qwen3-rerank`, `qwen3-vl-rerank` | 可选，指导排序策略（如 `"Given a web search query, retrieve relevant passages..."`），影响相关性打分逻辑 |
| `top_n` | integer | rerank 模型 | 可选，返回前 N 个结果；`qwen3-rerank` 顶层传参，`gte-rerank-v2` / `qwen3-vl-rerank` 需置于 `parameters` 内 |

## 使用方式

### 同步调用（推荐小批量、低延迟场景）
- **文本向量**：使用 OpenAI SDK 或 DashScope SDK，base_url 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（同步）或 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`（DashScope 原生）  
- **排序模型**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks`；`qwen3-vl-rerank` / `gte-rerank-v2` 使用 `/api/v1/services/rerank/text-rerank/text-rerank`  
- **多模态向量**：统一使用 `https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`contents` 数组定义输入  

### 异步调用（推荐大批量、高吞吐场景）
- **文本批量向量**：调用 `/api/v1/services/embeddings/text-embedding/text-embedding`（带 `X-DashScope-Async: enable` 头），再轮询 `/api/v1/tasks/{task_id}` 获取结果；SDK 提供 `BatchTextEmbedding.async_call()` 封装  
- **注意事项**：异步任务 ID 有效期 24 小时；单用户并发运行中任务数上限为 3 个，排队中任务上限为 50 个（见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）

## 限制和注意事项

- **[Token](../concepts/token.md) 与尺寸限制**：  
  - `qwen3.7-text-embedding` 单文本最长 128,000 Token，但批量输入（array/file）最多 20 行；`text-embedding-v4` 单文本限 8,192 Token，批量最多 10 行  
  - `qwen3-vl-embedding` 图片单张 ≤10 MB，视频 ≤50 MB；`tongyi-embedding-vision-plus` 图片单张 ≤3 MB，视频 ≤10 MB  
  - `qwen3-rerank` 单次请求最多 500 文档，`qwen3-vl-rerank` 文本类文档上限 100，图片/视频类上限更低（见文档 2）  

- **语种与格式兼容性**：  
  - `qwen3.7-text-embedding` 支持 201 种语种，`text-embedding-v4` 支持 100+ 语种及编程语言，`text-embedding-v1` 仅支持 6 种；多模态模型语种支持差异显著（如 `qwen2.5-vl-embedding` 仅 11 种），选型时需核对 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)  

- **关键不兼容点**：  
  - `qwen3-rerank` 响应无 `output` 包裹层，`results` 直接在顶层；`qwen3-vl-rerank` / `gte-rerank-v2` 响应含 `output.results`  
  - `text-embedding-async-v2` 仅支持 HTTP 异步，若遗漏 `X-DashScope-Async: enable` 头将报错 `"current user api does not support synchronous calls"`  
  - `multimodal-embedding-v1` 不支持 `dimension` 参数，固定 1024 维；`tongyi-embedding-vision-plus/flash`（非快照版）同样不支持该参数  

- **计费与免费额度**：  
  - 同步模型按输入 Token 计费（如 `text-embedding-v4` 0.0005 元/千 Token），异步模型另有单价（如 `text-embedding-async-v2` 0.0007 元/千 Token）；免费额度按模型单独发放（如 `qwen3.7-text-embedding` 各 100 万 Token），有效期均为开通后 90 天

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)


