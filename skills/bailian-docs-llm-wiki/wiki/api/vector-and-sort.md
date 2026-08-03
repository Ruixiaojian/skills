# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/多模态向量化（embedding）与文本/跨模态排序（rerank）两大核心能力，支撑语义搜索、RAG、聚类、推荐等AI应用。向量模型将输入内容映射至统一语义空间，支持余弦相似度计算；排序模型则对召回结果进行精细化相关性重排序，提升最终结果准确率。所有服务均通过标准化 API 提供，支持同步、异步及 OpenAI 兼容调用方式。

## 支持的模型/功能

### 向量模型（Embedding）

- **通用文本向量**：`qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`，适用于纯文本语义表征 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **多模态向量**：`qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06`、`tongyi-embedding-vision-flash-2026-03-06`、`tongyi-embedding-vision-plus`、`tongyi-embedding-vision-flash`、`multimodal-embedding-v1`，支持 text/image/video 及其组合输入 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **批处理文本向量**：`text-embedding-async-v2`、`text-embedding-async-v1`，专为超大批量（最高 100,000 行）文本向量化设计，采用异步任务模式 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 排序模型（Rerank）

- **纯文本排序**：`qwen3-rerank`（推荐替代已下线的 `gte-rerank`），支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，适用于 RAG 和语义检索场景。  
- **多模态排序**：`qwen3-vl-rerank`，支持 text/image/video 混合查询与文档，适用于跨模态搜索、图像聚类等 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  
- **历史模型**：`gte-rerank-v2` 仍可用，但将于 2026 年 05 月 30 日下线，强烈建议迁移至 `qwen3-rerank`。

> **注意**：文档中 `qwen3-vl-rerank` 的最大文档数限制描述存在矛盾——表格中写“文本：100”，而后续说明称“单次请求最大文档数”因模态类型而异，且未明确给出混合模态下的具体数值。实际使用请以最新控制台或 SDK 返回的 `429` 错误提示为准。

## 关键参数

| 参数 | 适用模型 | 说明 | 示例值 |
|------|----------|------|--------|
| `dimension` | `qwen3.7-text-embedding`, `text-embedding-v4/v3`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 指定向量维度，不同模型支持范围不同；`text-embedding-v2/v1`、`tongyi-embedding-vision-plus/flash` 等旧版不支持 | `1024`, `2560` |
| `enable_fusion` | `qwen3-vl-embedding` | 控制是否融合多模态输入为单向量；`tongyi-embedding-vision-plus-2026-03-06` 等新版模型**不使用此参数**，改用同 content 对象内多模态字段实现融合 | `true` |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回排序后前 N 个结果；默认返回全部 | `5` |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 任务指令，影响排序策略（如问答检索 vs 语义相似度）；建议英文 | `"Given a web search query, retrieve relevant passages that answer the query."` |
| `fps` | `qwen3-vl-rerank`, `qwen3-vl-embedding` | 视频帧采样比例，范围 `[0,1]`，默认 `1.0` | `0.5` |
| `res_level` | `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 输入分辨率档位（0–3），影响 token 消耗与精度 | `1` |
| `text_type` | `text-embedding-async-v2/v1` | 区分 `query`（查询）与 `document`（底库），优化非对称检索效果 | `"query"` |

## 使用方式

### 向量生成
- **同步文本向量**：HTTP POST 到 `/compatible-mode/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/embeddings/text-embedding/text-embedding`（DashScope 原生），`input` 可为字符串、字符串数组或文件流。  
- **多模态向量**：HTTP POST 到 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`contents` 数组支持 `{"text":...}`, `{"image":...}`, `{"video":...}`, `{"multi_images":[...]}`；融合向量需按模型要求设置 `enable_fusion=true` 或将多模态字段置于同一对象内。  
- **批处理文本向量**：先调用 `/api/v1/services/embeddings/text-embedding/text-embedding`（带 `X-DashScope-Async: enable` 头）创建异步任务，再用 `GET /api/v1/tasks/{task_id}` 轮询结果；SDK 提供 `BatchTextEmbedding.call()` 封装。

### 排序调用
- **`qwen3-rerank`**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) `/compatible-api/v1/reranks`，`query` 和 `documents` 与 `model` 同级，无需嵌套 `input`。  
- **`qwen3-vl-rerank` / `gte-rerank-v2`**：使用原生接口 `/api/v1/services/rerank/text-rerank/text-rerank`，`query` 和 `documents` 必须包裹在 `input` 对象内；`qwen3-vl-rerank` 的 `query` 和 `documents` 元素支持 `{"text":...}`, `{"image":...}`, `{"video":...}` 结构。

## 限制和注意事项

- **输入长度与数量**：`qwen3.7-text-embedding` 单条文本最长 128,000 [Token](../concepts/token.md)，批量最多 20 条；`text-embedding-v4` 单条限 8,192 [Token](../concepts/token.md)，批量最多 10 条；`text-embedding-async-v2` 单次最多 100,000 行，单行限 2,048 [Token](../concepts/token.md)；`qwen3-vl-rerank` 文本文档上限 100 条，图片上限 40 张，视频上限 4 条。  
- **多模态兼容性**：`qwen2.5-vl-embedding` **仅支持融合向量**，不支持 `multi_images`；`tongyi-embedding-vision-plus/flash`（非 2026-03-06 版）**仅支持独立向量**，不支持 `enable_fusion`；`multimodal-embedding-v1` 不支持 `dimension` 参数，固定 1024 维。  
- **地域与 endpoint**：北京地域 base URL 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；务必替换 `{WorkspaceId}`。  
- **异步任务时效性**：批处理任务 ID 有效期为 24 小时，结果 URL 亦仅保留 24 小时，需及时下载。  
- **免费额度**：各模型均有独立免费额度（如 `qwen3.7-text-embedding` 100 万 Token），自开通百炼起 90 天有效，详见各模型概览表。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


