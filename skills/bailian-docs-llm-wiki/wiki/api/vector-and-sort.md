# vector and sort

百炼平台提供文本向量化（vector）、多模态向量化（multimodal vector）和文本排序（rerank）三大核心能力，覆盖语义搜索、RAG、跨模态检索、聚类等典型AI应用链路。所有能力均支持同步/异步调用、OpenAI兼容接口及原生DashScope SDK，并通过统一的API Key与业务空间ID进行身份与资源管理。开发者可根据数据规模、模态类型、延迟敏感度选择合适模型与接口模式。

## 支持的模型/功能

- **文本向量模型**：支持通用文本嵌入，包括 `qwen3.7-text-embedding`（最高128K Token）、`text-embedding-v4`（默认1024维，8K Token）、`text-embedding-v3`、`text-embedding-v2` 和 `text-embedding-v1`。详细参数见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理向量模型**：专为大规模文本设计，支持单次10万行输入，模型为 `text-embedding-async-v2`（1536维）和 `text-embedding-async-v1`，采用异步任务模式，适用于离线批量处理场景 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量模型**：支持文本、图像、视频统一语义空间表征，包括 `qwen3-vl-embedding`（支持独立/融合向量）、`tongyi-embedding-vision-plus-2026-03-06`（支持多分辨率与融合）、`qwen2.5-vl-embedding`（仅融合）等 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本排序（Rerank）模型**：对召回结果进行精准重排序，支持纯文本（`qwen3-rerank`）、多模态（`qwen3-vl-rerank`）及历史模型（`gte-rerank-v2`）。> **注意**：`gte-rerank` 系列模型将于2026年05月30日下线，[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档已明确标注迁移建议，新项目应优先选用 `qwen3-rerank` 或 `qwen3-vl-rerank`。

## 关键参数

| 参数名 | 适用模型 | 说明 | 是否必选 |
|--------|----------|------|----------|
| `model` | 全部 | 模型名称，如 `"text-embedding-v4"`、`"qwen3-vl-rerank"` | 必选 |
| `input` / `query` / `documents` | 因模型而异 | 向量：支持字符串、字符串数组或文件；排序：`query` + `documents` 数组；多模态：`input.contents` 数组，含 `text`/`image`/`video` 字典 | 必选 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-*` 等 | 指定向量维度，不同模型支持值不同（如 `text-embedding-v4`: 2048/1024/768…；`qwen3-vl-embedding`: 2560/1024…） | 可选（有默认值） |
| `encoding_format` | 同步文本向量 | 当前仅支持 `"float"` | 可选 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时将 `contents` 中所有模态融合为1个向量；`false`（默认）则各模态独立生成向量 | 可选（仅该模型） |
| `top_n` | 排序模型 | 返回排序后前 N 个结果 | 可选 |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 任务指令（如 `"Retrieve semantically similar text."`），影响排序策略 | 可选 |

> **注意**：`tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash`（非2026-03-06快照版）**不支持 `dimension` 参数**，向量维度固定为1152/768；而 `multimodal-embedding-v1` 同样不支持该参数，固定1024维 —— 此信息在 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 的“模型能力对照”表格中有明确说明，与部分旧文档描述存在不一致，以该文档为准。

## 使用方式

- **同步调用（小规模、低延迟）**：  
  使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-mode/v1/embeddings`）或 DashScope SDK 的 `TextEmbedding.call()`。支持单文本、文本列表、文件流输入。示例见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

- **异步批处理（大规模、容忍延迟）**：  
  通过 HTTP 创建任务（`/api/v1/services/embeddings/text-embedding/text-embedding`）或 SDK 的 `BatchTextEmbedding.call()` / `async_call()`。输入必须为公网可访问的文本文件 URL，单次最多10万行。任务状态需轮询查询。

- **多模态向量（跨模态场景）**：  
  使用 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` 接口，`input.contents` 传入混合模态对象数组。融合向量需按模型要求设置 `enable_fusion=true`（`qwen3-vl-embedding`）或同 content 对象内混写（`tongyi-embedding-vision-*2026-03-06`）。

- **文本排序（RAG精排）**：  
  `qwen3-rerank` 使用 OpenAI 兼容 `/compatible-api/v1/reranks` 接口（扁平参数结构）；`qwen3-vl-rerank` 和 `gte-rerank-v2` 使用 `/api/v1/services/rerank/text-rerank/text-rerank` 接口（嵌套 `input` 结构）。SDK 调用统一使用 `TextReRank.call()`，自动适配底层协议。

## 限制和注意事项

- **输入长度与数量限制**：  
  - `qwen3.7-text-embedding`：单文本最长128,000 Token，批量最多20行；  
  - `text-embedding-v4`：单文本最长8,192 Token，批量最多10行；  
  - `text-embedding-async-v2`：单次请求最多100,000行，单行最长2,048 Token；  
  - `qwen3-vl-rerank`：文本文档最多100条、图片最多40张、视频最多4个，且 `Query Tokens × Document数 + Document Tokens总和 ≤ 120,000`。

- **地域与Endpoint差异**：  
  所有接口均需替换 `{WorkspaceId}` 为真实业务空间ID，并根据地域选择 base URL（如北京：`cn-beijing.maas.aliyuncs.com`；新加坡：`ap-southeast-1.maas.aliyuncs.com`）。[OpenAI 兼容接口](../concepts/openai-compatible-api.md)与原生接口的 endpoint 路径和参数结构不同，不可混用。

- **免费额度与计费**：  
  各模型均有开通后90天内的免费额度（如 `text-embedding-v4` 为100万Token），超出后按实际消耗Token计费。多模态模型中，文本、图片、视频分项计费（如 `qwen3-vl-embedding`：文本0.0007元/千Token，图片/视频0.0018元/千Token）。

- **限流策略**：  
  同步接口受 RPS 与并发请求数限制；异步批处理接口限制单用户同时运行中任务≤3个、排队中+运行中任务总数≤50个。具体规则详见各文档中的“限流”章节。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


