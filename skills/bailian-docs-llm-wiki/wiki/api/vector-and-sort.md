# vector and sort

`vector and sort` 是百炼平台提供的两类核心语义理解能力：向量化（vector）将文本、图像、视频等多模态内容映射为统一语义空间的数值向量，用于相似度计算与检索；排序（sort，即 rerank）则对召回结果进行二次精排，提升相关性排序质量。二者常组合使用——先通过向量检索快速召回候选集，再用排序模型重打分并排序，构成完整的语义搜索链路。

## 支持的模型/功能

### 向量模型
- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4` 等纯文本模型，适用于文本语义搜索、聚类、RAG 等场景。详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **多模态向量**：支持 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，可处理 text/image/video 及其组合，输出独立向量或融合向量，支撑跨模态检索。详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **批处理文本向量**：`text-embedding-async-v2` 等异步模型专为海量文本（单次最高 100,000 行）设计，适合离线批量向量化任务。详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 排序模型
- **纯文本排序**：`qwen3-rerank` 支持高并发、大文档数（最多 500 条）的文本重排，语种覆盖超 100 种，推荐作为 gte-rerank 的替代方案（后者将于 2026 年 5 月 30 日下线）。
- **多模态排序**：`qwen3-vl-rerank` 支持 text/image/video 混合输入，允许以任意模态（如图片）为 query 对多模态文档排序，适用于图像聚类、跨模态搜索等场景。详见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：`gte-rerank` 系列模型已进入下线倒计时，新项目应优先选用 `qwen3-rerank` 或 `qwen3-vl-rerank`。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `dimension` | `qwen3.7-text-embedding`, `text-embedding-v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度，不同模型支持范围不同，不支持该参数的模型（如 `text-embedding-v1`）返回固定维数 | `1024`, `2560` |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | 控制是否将 `contents` 中所有模态融合为单个向量；`tongyi-embedding-vision-plus-2026-03-06` 等新版模型**不使用此参数**，改用单 content 对象内嵌多模态字段实现融合 | `true` |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回排序后前 N 个结果，默认返回全部 | `10` |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），影响模型对 Query-Document 关系的理解方式 | `"Given a web search query, retrieve relevant passages that answer the query."` |
| `text_type` | `text-embedding-async-v2`（批处理） | 区分 `query` 与 `document` 类型，对非对称检索任务（如 RAG）可提升效果 | `"query"` |
| `res_level` | `tongyi-embedding-vision-plus-2026-03-06` 等 Qwen3 底座模型 | 图像分辨率档位（0–3），影响 token 消耗与精度平衡 | `1` |

> **注意**：`qwen2.5-vl-embedding` 仅支持融合向量且**不支持 `enable_fusion` 参数**（始终融合）；而 `tongyi-embedding-vision-plus-2026-03-06` 虽支持融合，但**必须通过将 text/image/video 放在同一 content 对象中触发**，而非设置 `enable_fusion=true` —— 这与 `qwen3-vl-embedding` 的设计逻辑不同，需严格区分。

## 使用方式

### 向量生成
- **同步调用（小规模）**：使用 `/compatible-mode/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/embeddings/...` 接口，直接传入 `input` 字符串或数组。适用于实时性要求高的场景。
- **异步批处理（大规模）**：使用 `/api/v1/services/embeddings/text-embedding/text-embedding` + `X-DashScope-Async: enable` 创建任务，再轮询 `GET /api/v1/tasks/{task_id}` 获取结果。适用于百万级文本离线向量化。
- **多模态输入**：`contents` 数组中每个元素为 `{ "text": "...", "image": "...", "video": "..." }` 或 `{"multi_images": [...]}`，具体格式见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序调用
- **文本排序**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks` 接口，`query` 和 `documents` 与 `model` 同级；`qwen3-vl-rerank` 使用 `/api/v1/services/rerank/text-rerank/text-rerank`，需包裹在 `input` 对象中。
- **多模态排序**：`qwen3-vl-rerank` 的 `query` 和 `documents` 均支持 `{"text":...}`, `{"image":...}`, `{"video":...}` 格式，允许混合模态输入。

## 限制和注意事项

- **输入长度与数量**：
  - 文本向量：`qwen3.7-text-embedding` 单条最长 128,000 [Token](../concepts/token.md)，批量最多 20 行；`text-embedding-v4` 单条限 8,192 [Token](../concepts/token.md)，批量最多 10 行。
  - 多模态向量：`qwen3-vl-embedding` 单次请求 contents 总数 ≤ 20，图片 ≤ 10 张，视频 ≤ 1 条；`tongyi-embedding-vision-plus-2026-03-06` 支持最多 64 张图片、8 条视频。
  - 排序模型：`qwen3-vl-rerank` 单次最多 100 文本/40 图片/4 视频；`qwen3-rerank` 最多 500 文本条目。

- **文件与 URL 限制**：
  - 图片/视频仅支持公开可访问 URL 或 Base64 Data URI（格式：`data:image/jpeg;base64,...`）；本地文件需先上传至 OSS 或其他公网可访问地址。
  - 批处理接口要求输入文件 URL 可被服务端直连，且单文件 ≤ 200MB。

- **地域与 endpoint 差异**：
  - 北京地域 endpoint 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`；新加坡地域需替换为 `ap-southeast-1`。
  - `qwen3-rerank` 使用 `/compatible-api/v1/reranks`，而 `qwen3-vl-rerank` 使用 `/api/v1/services/rerank/...`，**不可混用 endpoint**。

- **[Token](../concepts/token.md) 计费与限流**：
  - 向量模型按输入 Token 计费（文本、图片、视频分别计价）；排序模型按 `(Query Tokens × Document 数) + Σ(Document Tokens)` 总和计费。
  - 异步批处理有严格限流：单用户同时运行中任务 ≤ 3 个，排队中任务 ≤ 50 个（见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）。

- **语种与格式兼容性**：
  - 多模态模型普遍支持 30+ 语种，但 `tongyi-embedding-vision-plus` 旧版仅支持中英文；`qwen3-vl-embedding` 支持 33 种语言，覆盖更广。
  - 所有模型均要求 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头，且 `Content-Type: application/json` 为必需项。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)


