# vector and sort

`vector and sort` 是百炼平台提供的核心语义处理能力，涵盖文本/[多模态](../concepts/multi-modal.md)向量化（embedding）与检索后重排序（rerank）两大功能。向量化将原始内容映射到统一语义空间，支撑搜索、推荐、聚类等下游任务；排序模型则对召回结果进行精细化相关性打分与重排，显著提升最终结果准确率。两类能力均支持同步与异步调用模式，并覆盖中、英、日、韩等百余种语言及文本、图像、视频[多模态](../concepts/multi-modal.md)输入。

## 支持的模型/功能

- **文本向量模型**：包括 `qwen3.7-text-embedding`（支持256–2560维可选）、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2` 及异步批处理专用模型 `text-embedding-async-v2`。详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 和 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **文本排序模型**：`qwen3-rerank`（推荐替代已下线的 `gte-rerank`）、`gte-rerank-v2`（兼容旧版）及[多模态](../concepts/multi-modal.md)排序模型 `qwen3-vl-rerank`，支持文本、图像、视频混合查询与文档排序。
- **多模态向量模型**：`qwen3-vl-embedding`（支持独立/融合向量）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06` 等，实现跨模态统一表征。具体能力对比见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

> **注意**：文档 2 明确指出 `gte-rerank` 模型将于 2026 年 05 月 30 日下线，且文档 1 中 `text-embedding-v1` 的语种支持范围（仅 6 种）明显窄于后续版本（100+），应优先选用 `qwen3.7-text-embedding` 或 `text-embedding-v4`。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3`, `text-embedding-v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-03` 等 | 指定向量维度，不同模型支持值不同（如 `qwen3.7-text-embedding` 支持 256–2560）。`text-embedding-v2` 及 `multimodal-embedding-v1` 等不支持该参数。 |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | `true` 时将 `contents` 中所有模态融合为单个向量；默认 `false`（独立向量）。`tongyi-embedding-vision-plus-2026-03-06` 等新版模型通过将 text/image/video 放入同一 content 对象实现融合，**不使用此参数**。 |
| `top_n` | `qwen3-rerank`, `gte-rerank-v2`, `qwen3-vl-rerank` | 返回排序后前 N 个结果，默认返回全部。 |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Given a web search query, retrieve relevant passages..."`），影响相关性判断逻辑。建议英文书写。 |
| `text_type` | `text-embedding-async-v2` | 指定输入文本类型：`document`（默认，用于底库）或 `query`（用于检索查询），对非对称检索任务效果有提升。 |

## 使用方式

- **同步调用（小批量）**：适用于单次 ≤20 条文本（`qwen3.7-text-embedding`）或 ≤500 文档（`qwen3-rerank`）的实时场景。使用 OpenAI 兼容 SDK 或 HTTP POST 到 `/compatible-mode/v1/embeddings`（向量）或 `/compatible-api/v1/reranks`（排序）。示例见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理（大数据量）**：适用于百万级文本向量化。需先调用 `/api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（带 `X-DashScope-Async: enable` 头），再轮询 `/api/v1/tasks/{task_id}` 获取结果。文件需托管至公网可访问 URL，单文件 ≤200MB，单行 ≤2048 [Token](../concepts/token.md)。详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态输入**：使用 `multimodal-embedding` 接口，`contents` 数组支持混合 `text`、`image`、`video`、`multi_images`。融合向量需按模型要求设置 `enable_fusion=true`（`qwen3-vl-embedding`）或同 content 对象内并列多模态字段（`tongyi-embedding-vision-plus-2026-03-06`）。

## 限制和注意事项

- **[Token](../concepts/token.md) 与尺寸限制**：
  - `qwen3.7-text-embedding` 单行最高支持 128,000 [Token](../concepts/token.md)（北京地域），而 `text-embedding-v4` 仅 8,192 Token；多模态模型中 `qwen3-vl-embedding` 文本限 32,000 Token，图片限 10 MB。
  - `qwen3-vl-rerank` 单次请求最大文档数因模态类型而异（文本 100、图片 40、视频 4），且总 Token 计算公式为 `Query Tokens × Document 数量 + Document Tokens 总和`，不得超过 `请求最大输入Token`（120,000）。
- **地域与计费差异**：北京与新加坡地域的单价、免费额度不同（如 `qwen3.7-text-embedding` 北京有 100 万 Token 免费额度，新加坡无），调用前需确认业务空间所在地域及对应 endpoint。
- **模型兼容性**：`qwen3-rerank` 使用扁平化参数（`query`、`documents` 与 `model` 同级），而 `gte-rerank-v2` 和 `qwen3-vl-rerank` 要求嵌套在 `input` 对象中；SDK 封装后参数结构亦有差异，开发时需严格参照对应模型文档。
- **异步任务生命周期**：批处理任务 ID 有效期仅 24 小时，结果 URL 也仅保留 24 小时，务必及时下载。同时运行中任务数上限为 3 个，排队中任务上限为 50 个。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)


