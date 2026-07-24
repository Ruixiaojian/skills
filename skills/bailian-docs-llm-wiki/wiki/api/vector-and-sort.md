# vector and sort

百炼平台提供面向文本、多模态内容的向量化（vector）与排序（rerank）能力，覆盖语义检索、RAG、跨模态搜索等核心场景。向量模型将原始内容映射到统一语义空间，支持余弦相似度计算；排序模型则对召回结果进行精细化重排，显著提升相关性精度。两类能力均通过标准化 API 提供，支持同步/异步调用、[OpenAI 兼容接口](../concepts/openai-compatible-api.md)及 SDK 封装。

## 支持的模型/功能

- **文本向量模型**：`qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`，适用于语义搜索、聚类、分类等任务；其中 `qwen3.7-text-embedding` 和 `text-embedding-v4/v3` 支持动态 `dimensions` 参数，其余为固定维度 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **多模态向量模型**：`qwen3-vl-embedding`（独立/融合双模式）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06` 与 `tongyi-embedding-vision-flash-2026-03-06`（独立/融合双模式，支持 `res_level` 和 `max_video_frames`），以及已下线的旧版 `tongyi-embedding-vision-plus` 等 [原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **文本排序模型**：`qwen3-rerank`（纯文本，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)）、`qwen3-vl-rerank`（跨模态，支持 text/image/video 混合查询与文档）、`gte-rerank-v2`（已进入下线过渡期，2026年05月30日终止服务）[原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  

> **注意**：`gte-rerank` 系列模型（含 `gte-rerank-v2`）已明确标注为“将于2026年05月30日下线”，文档 4 中强调“推荐使用 `qwen3-rerank` 模型替代”，开发者应避免新项目接入该系列。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `dimensions` / `dimension` | `qwen3.7-text-embedding`, `text-embedding-v4/v3`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 指定向量输出维度；不同模型支持范围不同，部分模型（如 `text-embedding-v2`）不支持该参数 | `1024`, `2560` |
| `enable_fusion` | `qwen3-vl-embedding` | 控制是否将 `contents` 中所有输入融合为单个向量；`qwen2.5-vl-embedding` 固定融合，`tongyi-2026-03-06` 系列改用同 content 对象方式实现融合 [原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) | `true` |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回排序后前 N 个结果；默认返回全部 | `5` |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank`, `qwen3-vl-embedding` | 自定义任务指令，影响排序或向量生成策略（如 `"Retrieve semantically similar text."`）；建议英文撰写 | `"Given a web search query, retrieve relevant passages that answer the query."` |
| `res_level`, `max_video_frames`, `fps` | `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06`, `qwen3-vl-rerank` | 分辨率档位（0–3）、视频最大帧数（≤64）、视频抽帧比例（0–1） | `res_level=2`, `max_video_frames=32`, `fps=0.5` |

## 使用方式

- **文本向量（同步）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-mode/v1/embeddings`）或 DashScope 原生 HTTP 接口（`/api/v1/services/embeddings/text-embedding/text-embedding`），支持 `input` 为字符串、字符串数组或文件流。SDK 调用时直接传入 `model`, `input`, `dimensions` 等扁平参数。  
- **文本向量（异步批处理）**：仅支持 `text-embedding-async-v1/v2`，需先 `POST` 创建任务（带 `X-DashScope-Async: enable` 头），再轮询 `GET /api/v1/tasks/{task_id}` 获取结果；输入必须为远程可访问的文本文件 URL，单文件 ≤200MB、≤100,000 行 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态向量**：统一调用 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`contents` 数组中按需组合 `text`/`image`/`video`/`multi_images` 字典；融合向量需根据模型选择 `enable_fusion=true`（`qwen3-vl-embedding`）或同 content 对象（`tongyi-2026-03-06` 系列）。  
- **文本排序**：`qwen3-rerank` 使用 OpenAI 兼容 `/compatible-api/v1/reranks` 接口，`query` 与 `documents` 平级；`qwen3-vl-rerank` 和 `gte-rerank-v2` 使用原生 `/api/v1/services/rerank/text-rerank/text-rerank` 接口，`query` 与 `documents` 必须嵌套在 `input` 对象内。SDK 调用统一使用 `dashscope.TextReRank.call()`，参数自动适配底层协议。

## 限制和注意事项

- **输入规模限制**：`qwen3.7-text-embedding` 单字符串最长 128,000 [Token](../concepts/token.md)，而 `text-embedding-v4` 仅支持 8,192 [Token](../concepts/token.md)；`qwen3-vl-rerank` 单次请求最大文档数依模态类型而异（文本 100、图片 40、视频 4）；`text-embedding-async-v2` 单文件最多 100,000 行且每行 ≤2,048 [Token](../concepts/token.md)。  
- **模态兼容性**：`qwen2.5-vl-embedding` 不支持 `multi_images` 输入，且仅接受单图+单文+单视频各一个；`tongyi-embedding-vision-plus`（非 2026 版本）仅支持独立向量，不支持融合；`multimodal-embedding-v1` 不支持 `dimension` 参数，固定 1024 维。  
- **地域与接口差异**：新加坡地域模型 endpoint 需替换 `cn-beijing` 为 `ap-southeast-1`；`qwen3-rerank` 的响应结构（顶层 `results`）与 `qwen3-vl-rerank`（嵌套于 `output.results`）不兼容，客户端需按模型分支解析。  
- **免费额度与限流**：所有模型均提供开通后 90 天内的免费额度（如 `qwen3.7-text-embedding` 各 100 万 Token），超出后按量计费；异步批处理有严格并发限制（单用户最多 3 个运行中任务，排队总数 ≤50）[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


