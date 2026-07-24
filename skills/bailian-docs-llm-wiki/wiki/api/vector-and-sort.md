# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本向量化（embedding）、[多模态](../concepts/multi-modal.md)向量化、文本排序（rerank）三大能力，支撑语义搜索、RAG、跨模态检索等核心场景。所有接口均支持同步与异步调用，提供 OpenAI 兼容模式及原生 DashScope SDK 封装，开发者可根据数据规模、延迟要求和模态复杂度灵活选型。

## 支持的模型/功能

### 文本向量模型（Embedding）
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等通用文本模型，适用于实时低延迟场景。详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：支持 `text-embedding-async-v2` 和 `text-embedding-async-v1`，专为大规模离线批量处理设计，单次请求最多支持 100,000 行文本，适合构建知识库底库向量索引。
- **[多模态](../concepts/multi-modal.md)向量模型**：支持 `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等，可统一生成文本、图像、视频的语义向量，支持独立向量（每模态一向量）与融合向量（[多模态](../concepts/multi-modal.md)合一向量）两种模式，详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 文本排序模型（Rerank）
- **qwen3-rerank**：轻量高效，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)，适用于 RAG 场景的二次精排；支持 `instruct` 参数定制任务类型（如问答检索或语义相似度匹配）。
- **qwen3-vl-rerank**：多模态排序模型，支持文本/图片/视频混合查询与文档，适用于跨模态搜索。
- **gte-rerank-v2**：高并发排序模型，支持单次最多 30,000 文档排序，但已于 2026 年 5 月 30 日下线，官方明确推荐迁移至 `qwen3-rerank` —— 此信息在 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档中已标注为重要公告。

> **注意**：`gte-rerank` 系列模型（包括 `gte-rerank-v2`）已进入下线流程，新项目应避免使用；而 `qwen3-rerank` 是当前主力推荐模型，其接口路径（`/compatible-api/v1/reranks`）与 `qwen3-vl-rerank`（`/api/v1/services/rerank/...`）不同，不可混用。

## 关键参数

| 参数名 | 适用模型 | 说明 | 是否必选 |
|--------|----------|------|----------|
| `model` | 所有 | 模型名称，必须严格匹配文档中列出的合法值（如 `"text-embedding-v4"`、`"qwen3-rerank"`） | ✅ |
| `input` / `documents` / `query` | 因模型而异 | - 向量模型：接受 `string`、`string[]` 或 `file`<br>- rerank 模型：`qwen3-rerank` 要求 `query` 和 `documents` 同级；`qwen3-vl-rerank` 和 `gte-rerank-v2` 要求嵌套在 `input` 对象内 | ✅ |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-*` 等 | 指定向量维度，不同模型支持值不同（如 `text-embedding-v4` 支持 `2048/1536/1024/...`），不传则使用默认值 | ❌（可选） |
| `encoding_format` | 同步文本向量模型 | 当前仅支持 `"float"`，用于控制返回向量数值格式 | ❌（可选） |
| `top_n` | rerank 模型 | 返回排序后前 N 个结果，默认返回全部 | ❌（可选） |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 英文指令字符串，用于引导排序策略（如 `"Given a web search query..."`），影响相关性判断逻辑 | ❌（可选） |
| `enable_fusion` | `qwen3-vl-embedding` | `bool`，启用后将 `contents` 中所有模态融合为单一向量；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过将 `text`/`image`/`video` 放入同一 `content` 对象实现融合 | ❌（可选） |

## 使用方式

### 同步调用（低延迟、小批量）
- **文本向量**：使用 OpenAI SDK 或 DashScope SDK，base URL 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，Endpoint 为 `/embeddings`。
- **文本排序**：
  - `qwen3-rerank`：调用 `/compatible-api/v1/reranks`，`query` 和 `documents` 直接作为顶层字段；
  - `qwen3-vl-rerank`/`gte-rerank-v2`：调用 `/api/v1/services/rerank/text-rerank/text-rerank`，`query` 和 `documents` 必须包裹在 `input` 对象内。
- 示例（Python）：
  ```python
  # qwen3-rerank 同步调用
  from openai import OpenAI
  client = OpenAI(base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1", api_key=os.getenv("DASHSCOPE_API_KEY"))
  resp = client.rerank.create(model="qwen3-rerank", query="...", documents=[...], top_n=3)
  ```

### 异步调用（大批量、长耗时）
- **文本向量批处理**：调用 `/api/v1/services/embeddings/text-embedding/text-embedding`，需设置 `X-DashScope-Async: enable` 请求头，并传入 `input.url` 指向 OSS 或公网可访问的文本文件（每行一条）。
- **多模态向量**：仅支持 HTTP 同步调用（无原生异步接口），但因视频解析耗时较长，建议自行封装重试与轮询逻辑。
- **SDK 封装**：DashScope SDK 提供 `BatchTextEmbedding.async_call()` 和 `wait()` 方法简化异步任务管理，详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

## 限制和注意事项

- **[Token](../concepts/token.md) 与行数限制**：
  - `qwen3.7-text-embedding` 单文本最长 128,000 [Token](../concepts/token.md)，批量最多 20 行；
  - `text-embedding-v4` 单文本最长 8,192 [Token](../concepts/token.md)，批量最多 10 行；
  - `text-embedding-async-v2` 单文本最长 2,048 Token，批量最多 100,000 行；
  - `qwen3-rerank` 单次请求最大输入 Token 为 `Query Tokens × Document 数 + Document Tokens 总和`，上限 120,000；
  - 多模态模型中，`qwen3-vl-embedding` 文本长度上限为 32,000 Token，图片单张 ≤10 MB，视频 ≤50 MB。

- **地域与 WorkspaceId**：所有接口均需替换 `{WorkspaceId}` 为真实业务空间 ID，且 base URL 需匹配实际部署地域（如北京 `cn-beijing`、新加坡 `ap-southeast-1`）。

- **免费额度与计费**：各模型均有独立免费额度（如 `text-embedding-v4` 为 100 万 Token），有效期自百炼开通起 90 天；超出后按文档中标注单价计费（如文本输入 0.0005 元/千 Token）。

- **限流策略**：
  - 同步向量接口遵循全局 QPS 限流；
  - 异步批处理接口限制单用户并发运行中任务 ≤3 个，排队中任务 ≤50 个；
  - rerank 接口限流规则参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit) 文档。

- **响应兼容性**：`qwen3-rerank` 响应结构为扁平 `results` 数组；`qwen3-vl-rerank` 和 `gte-rerank-v2` 响应嵌套在 `output.results` 内，且仅当 `return_documents=true` 时返回原文。开发者需根据模型选择解析路径。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)


