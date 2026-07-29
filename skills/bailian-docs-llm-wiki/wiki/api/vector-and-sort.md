# vector and sort

百炼平台提供面向文本、多模态内容的向量化（vector）与排序（rerank）能力，覆盖从基础语义嵌入到跨模态精排的全链路需求。`vector` 类模型将输入（文本/图像/视频）映射为稠密向量，支持余弦相似度计算、聚类与检索；`sort`（即 rerank）模型则对召回结果进行细粒度相关性打分与重排序，显著提升 RAG、搜索等场景的准确率。两类能力均通过统一 API 接口提供，支持同步、异步及 OpenAI 兼容调用方式。

## 支持的模型/功能

- **文本向量模型**：支持 `qwen3.7-text-embedding`、`text-embedding-v4/v3/v2/v1` 等系列，适用于语义搜索、聚类、分类等任务；其中 `qwen3.7-text-embedding` 支持最长 128,000 [Token](../concepts/token.md) 单条输入，`text-embedding-v4` 支持动态 `dimensions` 参数 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  
- **多模态向量模型**：支持 `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等，可处理 text/image/video 及其组合，提供独立向量（每模态一个向量）与融合向量（多模态统一表征）两种模式 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **文本排序（Rerank）模型**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（跨模态）、`gte-rerank-v2`（已进入下线过渡期），用于对召回文档进行二次精准排序，支持 query-document 多模态混合输入 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  
- **批处理能力**：`text-embedding-async-v2` 等异步模型支持单次 100,000 行文本批量向量化，适用于大规模底库构建 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

> **注意**：`gte-rerank` 系列模型（含 `gte-rerank-v2`）将于 2026 年 05 月 30 日正式下线，新项目应优先选用 `qwen3-rerank` 或 `qwen3-vl-rerank`，详见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 中的官方公告。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `dimension` | `qwen3.7-text-embedding`, `text-embedding-v4/v3`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量输出维度；不同模型支持范围不同，不支持该参数的模型（如 `text-embedding-v2`、`tongyi-embedding-vision-plus`）返回固定维度 | `1024`, `2560` |
| `enable_fusion` | `qwen3-vl-embedding` | 控制是否启用融合向量模式（`true` 时将 `contents` 中所有模态融合为 1 个向量）；`tongyi-embedding-vision-plus-2026-03-06` 等新版模型改用同 content 对象内多模态字段实现融合，**不支持此参数** | `true` |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回排序结果中得分最高的前 N 项；默认返回全部 | `5` |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 自定义任务指令，影响排序策略（如 `"Given a web search query, retrieve relevant passages..."`），建议英文撰写 | `"Retrieve semantically similar text."` |
| `res_level` | `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 图像分辨率档位（0–3），影响 token 消耗与精度 | `1` |
| `fps` | `qwen3-vl-rerank`, `qwen3-vl-embedding` | 视频帧采样比例 `[0,1]`，降低帧数可减少计算开销 | `0.5` |

## 使用方式

- **同步调用（文本向量）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK，直接传入 `input`（字符串/列表/文件）和 `model`，支持 `dimensions` 和 `encoding_format="float"`。示例见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **异步批处理（文本向量）**：通过 `X-DashScope-Async: enable` 头触发异步任务，`input.url` 指向文本文件（每行一条），支持最大 100,000 行 × 2,048 [Token](../concepts/token.md)/行 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态向量**：HTTP 请求体中 `input.contents` 为数组，每个元素为 `{text: "..."} / {image: "..."} / {video: "..."} / {multi_images: [...]}`；融合向量需按模型要求设置 `enable_fusion=true`（`qwen3-vl-embedding`）或同对象内混写字段（`tongyi-embedding-vision-plus-2026-03-06`）[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **排序（Rerank）**：`qwen3-rerank` 使用 OpenAI 兼容 `/reranks` 接口，`query` 与 `documents` 同级；`qwen3-vl-rerank` 和 `gte-rerank-v2` 使用 `/text-rerank` 接口，需嵌套于 `input` 对象内，并支持 `text`/`image`/`video` 多模态文档 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 限制和注意事项

- **输入规模限制**：`text-embedding-v4` 单条文本上限 8,192 [Token](../concepts/token.md)，而 `qwen3.7-text-embedding` 支持 128,000 Token；`qwen3-vl-rerank` 单次请求最大文档数依模态类型而异（文本 100、图片 40、视频 4）；`qwen3-rerank` 支持最多 500 文档 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  
- **模态兼容性**：`qwen2.5-vl-embedding` 仅支持融合向量且不支持 `multi_images`；`tongyi-embedding-vision-plus`（非 2026 快照版）不支持 `dimension` 参数且仅支持独立向量 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **地域与 endpoint 差异**：北京地域 endpoint 为 `cn-beijing.maas.aliyuncs.com`，新加坡为 `ap-southeast-1.maas.aliyuncs.com`；多模态向量统一使用 `dashscope.aliyuncs.com` 域名，而文本向量与排序模型使用 `maas.aliyuncs.com` [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **免费额度与计费**：各模型免费额度独立（如 `qwen3.7-text-embedding` 100 万 Token/90 天），且按实际输入 Token 计费（含文本、图片、视频解析后 Token）；异步批处理任务状态仅保留 24 小时，需及时拉取结果 URL [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


