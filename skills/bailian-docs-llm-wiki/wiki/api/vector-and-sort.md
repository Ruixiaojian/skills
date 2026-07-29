# vector and sort

`vector and sort` 是百炼平台提供的核心向量化与排序能力集合，涵盖文本、多模态内容的嵌入（embedding）生成及跨模态/纯文本的精细化重排序（rerank）。该能力支撑语义搜索、RAG、推荐系统、聚类分析等典型AI应用，支持同步/异步调用、OpenAI兼容接口及SDK封装，适用于从单条短文本到百万级[Token](../concepts/token.md)批量处理的多样化场景。所有模型均基于阿里云自研大模型底座，提供多语言、多维度、多模态统一语义空间支持。

## 支持的模型与功能

### 文本向量模型（Embedding）
- **同步模型**：`qwen3.7-text-embedding`（最高128K [Token](../concepts/token.md)输入）、`text-embedding-v4`（支持动态`dimensions`参数，含2048/1536/1024等可选维度）、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`。详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理模型**：`text-embedding-async-v2`（1536维，单次最多10万行）、`text-embedding-async-v1`。适用于超大批量文件（≤200MB）的离线向量化任务，需通过任务ID轮询结果。详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量模型**：`qwen3-vl-embedding`（支持独立/融合向量）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06`（Qwen3底座，支持`res_level`和`max_video_frames`）、`multimodal-embedding-v1`等。支持文本、图像、视频任意组合输入，并在同一语义空间生成向量。详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序模型（Rerank）
- **纯文本排序**：`qwen3-rerank`（OpenAI兼容接口，最大500文档，单文档4K [Token](../concepts/token.md)），推荐替代已下线的`gte-rerank`系列。
- **多模态排序**：`qwen3-vl-rerank`（支持文本/图片/视频混合查询与文档，最大100文本/40图片/4视频），适用于跨模态检索场景。
- **历史模型**：`gte-rerank-v2`仍可用但不推荐新项目使用；其将于2026年5月30日下线，迁移指引见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档1中列出的`text-embedding-async-v1`在文档2的模型概览表中未体现语种支持完整性（仅列“中文、英语…”），而文档2明确说明`qwen3.7-text-embedding`支持201种语种，`text-embedding-v4`支持100+语种。实际开发应以文档2为准，`async-v1`为旧版模型，建议优先选用`async-v2`或同步模型。

## 关键参数

| 参数 | 适用模型 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必选，指定模型名称 | `"qwen3-rerank"`, `"qwen3-vl-embedding"` |
| `input` / `documents` / `query` | 按模型区分 | 同步embedding：`input`支持`string`/`array<string>`/`file`；rerank：`query`+`documents`分离；多模态：`input.contents`为对象数组 | `{"text": "hello"}`, `[{"image": "url"}, {"text": "desc"}]` |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`等 | 可选，指定输出向量维度（非所有模型都支持） | `1024`, `2048` |
| `enable_fusion` | 仅`qwen3-vl-embedding` | 布尔值，启用后将`contents`中所有模态融合为单个向量 | `true` |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 可选，返回前N个最相关结果 | `5` |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 可选，英文指令引导排序策略（如问答检索或语义相似度） | `"Given a web search query, retrieve relevant passages..."` |
| `fps` | `qwen3-vl-rerank`, `qwen3-vl-embedding` | 可选，视频帧采样率（0.0–1.0） | `0.5` |

## 使用方式

### 接口选择
- **小规模实时向量生成**（≤25条文本或单图/单视频）：使用同步API，HTTP endpoint为 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`（OpenAI兼容）或 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding`（DashScope原生）。
- **大规模离线批处理**（100行–10万行文本）：必须使用异步批处理API，先`POST`创建任务，再`GET /api/v1/tasks/{task_id}`轮询结果。详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量/排序**：统一使用 `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`（embedding）或 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`（rerank）。

### SDK调用要点
- DashScope SDK支持Python/Java，参数名与HTTP一致但结构扁平化（如`BatchTextEmbedding.call()`直接传`url`, `text_type`，无需嵌套`input`对象）。
- OpenAI SDK兼容模式需配置`base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"`，并使用`client.embeddings.create()`。
- 多模态排序SDK调用时，`query`和`documents`可直接传入字典（如`{"image": "url"}`），无需手动构造`input`对象。

## 限制和注意事项

- **Token与尺寸限制**：
  - `qwen3.7-text-embedding`单字符串最长128K Token；`text-embedding-v4`单字符串限8,192 Token；`text-embedding-async-v2`单行限2,048 Token且单次最多100,000行。
  - 多模态模型中，`qwen3-vl-embedding`图片≤10MB、视频≤50MB；`tongyi-embedding-vision-plus`图片≤3MB、视频≤10MB。
  - `qwen3-rerank`单次请求最大Token数为120,000（计算公式：`Query Tokens × Document 数量 + Document Tokens 总和`）。

- **地域与Endpoint差异**：
  - 北京地域使用`cn-beijing.maas.aliyuncs.com`；新加坡地域需替换为`ap-southeast-1.maas.aliyuncs.com`（见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）。
  - `qwen3-rerank`使用`/compatible-api/v1/reranks`，其余rerank模型使用`/api/v1/services/rerank/...`，不可混用。

- **[异步任务](../concepts/asynchronous-task.md)生命周期**：
  - [异步任务](../concepts/asynchronous-task.md)ID有效期24小时，结果URL仅保留24小时，需及时下载。
  - 单用户并发运行中异步作业上限为3个，排队中+运行中总数不超过50个（见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）。

- **模型弃用提醒**：
  > **注意**：`gte-rerank`系列模型（包括`gte-rerank-v2`）将于2026年5月30日下线，新项目请务必使用`qwen3-rerank`或`qwen3-vl-rerank`。迁移影响包括接口路径、参数结构（`qwen3-rerank`无`input`嵌套层）及计费单价变化。

## 来源文档

- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


