# vector and sort

`vector and sort` 是百炼平台提供的核心向量化与排序能力集合，涵盖文本/多模态向量生成（embedding）、批量异步向量化、以及跨模态文本重排序（rerank）三大功能模块。该能力支撑语义搜索、RAG、推荐系统、聚类分析等典型AI应用，支持同步/异步调用、OpenAI兼容接口及专用SDK，并覆盖中文、英语等100+语种。所有模型均需通过API Key认证，且部分能力受地域和业务空间ID约束。

## 支持的模型/功能

- **文本向量模型（Embedding）**  
  - 同步模型：`qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`，详见[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
  - 批处理模型：`text-embedding-async-v2`、`text-embedding-async-v1`，支持单次10万行文本处理，适用于大规模离线向量化任务，详见[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  

- **多模态向量模型（Multimodal Embedding）**  
  支持文本、图像、视频统一语义空间编码，包括 `qwen3-vl-embedding`（支持独立/融合向量）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06` 等，详见[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  

- **文本排序模型（Rerank）**  
  提供 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）、`gte-rerank-v2`（已进入下线流程）三类模型，用于对召回结果进行精准二次排序，详见[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  
  > **注意**：`gte-rerank` 系列模型将于2026年05月30日下线，新项目应优先选用 `qwen3-rerank` 或 `qwen3-vl-rerank`，详见[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)中的公告说明。

## 关键参数

| 参数 | 类型 | 说明 | 支持模型 |
|------|------|------|----------|
| `model` | string | 必选。模型名称，如 `"text-embedding-v4"`、`"qwen3-vl-rerank"` | 全部 |
| `input` / `query` / `documents` | string / array / object | 必选。输入内容格式依模型而异：<br>• 文本向量：支持字符串、字符串数组、文件对象；<br>• 多模态向量：`contents` 数组，每个元素为 `{"text":...}`、`{"image":...}` 等；<br>• 排序模型：`query` + `documents` 数组，`qwen3-rerank` 不使用 `input` 对象层级 | 全部 |
| `dimensions` | integer | 可选。指定输出向量维度（如 `1024`, `2048`），非所有模型均支持。`text-embedding-v1/v2`、`tongyi-embedding-vision-plus` 等固定维度模型不支持此参数 | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 |
| `encoding_format` | string | 可选。仅支持 `"float"`（默认） | 同步文本向量模型 |
| `enable_fusion` | boolean | 可选。仅 `qwen3-vl-embedding` 支持，设为 `true` 时将 `contents` 中所有模态融合为单个向量 | `qwen3-vl-embedding` |
| `top_n` | integer | 可选。排序模型返回前 N 个结果 | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` |
| `instruct` | string | 可选。排序任务指令（如 `"Retrieve semantically similar text."`），影响排序策略，建议英文 | `qwen3-rerank`, `qwen3-vl-rerank` |

> **注意**：`qwen3-rerank` 的 `top_n` 和 `instruct` 参数位于请求体顶层，**不嵌套在 `parameters` 对象中**；而 `qwen3-vl-rerank` 和 `gte-rerank-v2` 的对应参数必须置于 `parameters` 对象内。此差异易导致调用失败，务必按[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)文档结构组织请求体。

## 使用方式

- **同步调用（文本向量）**  
  使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK，通过 `POST /compatible-mode/v1/embeddings` 发起请求。支持单文本、文本列表、文件流输入。示例（Python）：
  ```python
  from openai import OpenAI
  client = OpenAI(base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
  resp = client.embeddings.create(model="text-embedding-v4", input=["hello", "world"], dimensions=1024)
  ```

- **异步批处理（文本向量）**  
  通过 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务，再用 `GET /api/v1/tasks/{task_id}` 轮询结果。输入需为公开可访问的文本文件 URL，单文件最多 10 万行、200MB。详见[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

- **多模态向量**  
  使用专用 endpoint `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 中混合声明 `text`、`image`、`video` 等字段。融合向量需按模型要求设置 `enable_fusion=true` 或将多模态数据置于同一 `content` 对象内。

- **文本排序**  
  - `qwen3-rerank`：调用 `POST /compatible-api/v1/reranks`，参数扁平化（`query`, `documents`, `top_n` 同级）。  
  - `qwen3-vl-rerank` / `gte-rerank-v2`：调用 `POST /api/v1/services/rerank/text-rerank/text-rerank`，`query` 和 `documents` 封装在 `input` 对象内，`top_n` 等置于 `parameters`。  
  SDK 调用（如 `dashscope.TextReRank.call()`）自动适配不同模型的参数结构。

## 限制和注意事项

- **输入长度与批量限制**  
  - `qwen3.7-text-embedding`：单文本最长 128,000 [Token](../concepts/token.md)，批量最多 20 行；`text-embedding-v4`：单文本最长 8,192 [Token](../concepts/token.md)，批量最多 10 行；`text-embedding-v2`：单文本最长 2,048 [Token](../concepts/token.md)，批量最多 25 行。  
  - `text-embedding-async-v2`：单次请求最多 100,000 行，单行最长 2,048 Token，文件大小 ≤ 200MB。  
  - `qwen3-vl-rerank`：文本文档最多 100 条、图片最多 40 条、视频最多 4 条；总输入 Token 上限为 120,000（计算公式：`Query Tokens × Document 数量 + Document Tokens 总和`）。

- **地域与Endpoint差异**  
  同步/异步/多模态/排序接口的 base URL 不同，且北京、新加坡等地域的域名后缀（如 `cn-beijing.maas.aliyuncs.com` vs `ap-southeast-1.maas.aliyuncs.com`）必须严格匹配。错误的地域配置将导致 404 或认证失败。

- **免费额度与计费**  
  免费额度按模型独立发放（如 `text-embedding-v4` 各 100 万 Token），有效期为百炼开通后 90 天；`text-embedding-async-v2` 免费额度为各 2000 万 Token。超出后按实际消耗 Token 计费，单价见各模型概览表。

- **限流策略**  
  - 同步接口：受通用 [限流](https://help.aliyun.com/zh/model-studio/rate-limit) 约束；  
  - 异步批处理：单用户并发运行中任务数上限为 3 个，排队中+运行中任务总数上限为 50 个；  
  - 排序模型：无单独 RPS 说明，遵循平台级限流规则。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


