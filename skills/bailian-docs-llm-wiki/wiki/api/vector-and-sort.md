# vector and sort

`vector and sort` 是百炼平台提供的核心向量化与排序能力集合，涵盖文本、多模态内容的向量生成（embedding）以及基于语义相关性的精准重排序（rerank）。该能力支撑语义搜索、RAG、跨模态检索、聚类等关键AI应用，支持同步/异步调用模式，并提供OpenAI兼容接口与原生DashScope SDK两种集成方式。所有模型均需通过API Key认证，且部分功能受地域、Workspace ID及免费额度限制。

## 支持的模型与功能

### 文本向量模型（Embedding）
- **同步模型**：`qwen3.7-text-embedding`（最高128K token输入）、`text-embedding-v4`（默认1024维，支持`dimensions`参数）、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`  
- **异步批处理模型**：`text-embedding-async-v2`（单次最多100,000行，每行≤2,048 token）、`text-embedding-async-v1`  
- **多模态向量模型**：`qwen3-vl-embedding`（支持独立/融合向量）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06`（新版Qwen3底座）、`tongyi-embedding-vision-flash-2026-03-06`、`multimodal-embedding-v1`  
- **文本排序模型（Rerank）**：`qwen3-rerank`（推荐替代已下线的`gte-rerank`）、`qwen3-vl-rerank`（支持文本/图像/视频混合排序）、`gte-rerank-v2`（[将于2026年05月30日下线](https://www.aliyun.com/notice/118217)）

> **注意**：文档 4 明确指出 `gte-rerank` 模型即将下线，而文档 1 和文档 2 均未提及此生命周期状态，开发者应以 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 中的公告为准，避免长期依赖过时模型。

### 功能特性
- 向量维度可配置（如 `text-embedding-v4` 支持2048/1024/512等，`qwen3-vl-embedding` 支持2560/2048等）  
- 多模态融合向量（`qwen3-vl-embedding` 通过 `enable_fusion=true`；`tongyi-embedding-vision-plus-2026-03-06` 通过同 content 对象内混合 text/image/video 实现）  
- 排序任务指令（`instruct`）支持问答检索与语义相似度两类策略，详见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)  
- 异步批处理支持大文件（≤200MB）与超大批量（100,000行），适用于离线向量化场景  

## 关键参数

| 参数 | 类型 | 是否必选 | 说明 | 适用模型 |
|------|------|----------|------|----------|
| `model` | string | 必选 | 模型名称，如 `"text-embedding-v4"` 或 `"qwen3-rerank"` | 全部 |
| `input` / `query` / `documents` | string / array / object | 必选 | 输入内容格式依模型而异：<br>- 文本向量：支持 string、string[]、file<br>- 多模态向量：`{"contents": [{"text":"..."},{"image":"url"}]}`<br>- 排序：`query` + `documents` 数组 | 全部 |
| `dimensions` | integer | 可选 | 指定向量维度（如1024、2048），**仅 `text-embedding-v3/v4` 和多模态模型（除 `tongyi-embedding-vision-plus` 等固定维模型）支持** | [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)、[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) |
| `encoding_format` | string | 可选 | 返回向量格式，当前仅支持 `"float"` | [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) |
| `top_n` | integer | 可选 | 排序后返回前 N 个结果，默认返回全部 | [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) |
| `instruct` | string | 可选 | 排序任务指令（如 `"Given a web search query..."`），**仅 `qwen3-rerank` 和 `qwen3-vl-rerank` 支持** | [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) |
| `enable_fusion` | boolean | 可选 | 多模态融合开关，**仅 `qwen3-vl-embedding` 支持**；`tongyi-embedding-vision-plus-2026-03-06` 等新版模型通过结构化 input 实现融合，不使用此参数 | [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) |

## 使用方式

### 调用方式选择
- **小规模实时向量化**（≤20条文本或单图/单视频）：使用同步API（HTTP或OpenAI兼容SDK），响应快、调试便捷  
- **大规模批量向量化**（数万行文本或大文件）：必须使用异步批处理API（HTTP两步调用或DashScope SDK封装），避免超时  
- **多模态内容处理**（图文/视频混合）：统一调用 `/services/embeddings/multimodal-embedding/multimodal-embedding` 接口，按 `contents` 结构组织输入  
- **召回后精排**：根据模态选择模型——纯文本用 `qwen3-rerank`；图文/视频混合用 `qwen3-vl-rerank`  

### 接口地址与认证
- **同步/兼容接口**：`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/embeddings`（向量）或 `/compatible-api/v1/reranks`（排序）  
- **原生异步接口**：`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding`（批向量）或 `/api/v1/services/rerank/text-rerank/text-rerank`（排序）  
- **认证**：所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 头，且需提前配置环境变量或SDK密钥  

### 代码示例要点
- Python中调用OpenAI兼容接口时，`base_url` 需替换 `{WorkspaceId}` 并指定地域（如 `cn-beijing`）  
- Java SDK需注意 `EmbeddingCreateParams.builder()` 的链式调用顺序，`dimensions` 仅对 v3/v4 生效  
- 异步批处理需先 `create_task` 获取 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 查询结果  
- 多模态输入中，`multi_images` 仅 `tongyi-embedding-vision-plus` 系列支持；Base64图片需符合 `data:image/{format};base64,{data}` 格式  

## 限制和注意事项

- **[Token](../concepts/token.md)与尺寸限制**：  
  - `qwen3.7-text-embedding` 单文本最长128,000 token，但 `text-embedding-v4` 仅8,192 token —— 超长文本需分块处理  
  - 多模态模型中，`qwen3-vl-embedding` 图片限10MB、视频限50MB；`tongyi-embedding-vision-plus` 图片限3MB、视频限10MB  
  - `qwen3-vl-rerank` 单次最多处理100文本/40图片/4视频，且总输入[Token](../concepts/token.md) ≤120,000  

- **地域与模型可用性**：  
  - `text-embedding-async-v2` 仅北京地域可用；新加坡地域支持 `tongyi-embedding-vision-plus` 等模型，但参数细节可能不同  
  - `qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，而 `qwen3-vl-rerank` 使用原生接口，**二者请求体结构不兼容，不可混用**  

- **免费额度与计费**：  
  - 所有模型免费额度均自百炼开通起90天有效（如 `qwen3.7-text-embedding` 各100万[Token](../concepts/token.md)）  
  - 多模态模型按模态分别计费（文本0.0007元/千token，图片/视频0.0018元/千token）  

- **其他重要约束**：  
  - `text-embedding-v1/v2` 不支持 `dimensions` 参数，返回固定维度（1536/1536）  
  - `multimodal-embedding-v1` 固定1024维，不支持 `dimension` 参数  
  - 异步批处理任务结果URL有效期仅24小时，需及时下载保存  
  - `gte-rerank-v2` 已明确进入下线流程，新项目禁止接入，详见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 公告

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


