# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/多模态向量化（embedding）与语义排序（rerank）两大核心能力，支撑[检索增强生成](../concepts/rag.md)（RAG）、跨模态搜索、推荐系统等场景。向量模型将原始内容映射到统一语义空间，排序模型则对召回结果进行精细化相关性重排。两类服务均提供同步、异步及多模态接口，支持灵活的参数控制与生产级部署。

## 支持的模型/功能

- **文本向量化**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等通用模型，适用于中英文及201种主流语种；[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 提供单次最多 20 行输入（北京地域），而 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md) 支持单任务最高 100,000 行文本，适合大规模底库预计算。
- **多模态向量化**：`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型支持文本、图像、视频及其组合输入，可生成**独立向量**（每模态各一）或**融合向量**（多模态统一表征），详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本/多模态排序**：`qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（跨模态）、`gte-rerank-v2`（兼容旧版）三类模型，其中 `qwen3-rerank` 已成为推荐主力，`gte-rerank` 将于 2026 年 5 月 30 日下线；[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 接口支持 `top_n` 截断、`instruct` 任务指令引导等关键能力。

> **注意**：文档 1 中 `text-embedding-v2` 的“最大行数”为 25，而文档 4 中同名模型未在批处理表格中列出，且文档 1 明确标注其单价为 0.0007 元（Batch 调用 0.00035 元），但文档 4 的批处理模型仅列 `text-embedding-async-v1/v2`，二者命名与能力边界未明确对齐，实际使用请以控制台最新模型列表为准。

## 关键参数

- **`dimensions`**：指定输出向量维度（如 `1024`, `2048`），仅 `qwen3.7-text-embedding`、`text-embedding-v3/v4` 及多模态模型（如 `qwen3-vl-embedding`）支持；`text-embedding-v1`、`multimodal-embedding-v1` 等固定维度模型不接受该参数。
- **`encoding_format`**：同步 API 中控制输出格式，`"float"`（默认）返回浮点数组，`"base64"` 返回 Base64 编码字符串，节省传输体积。
- **`enable_fusion`**：仅 `qwen3-vl-embedding` 支持，设为 `true` 时将 `contents` 中所有模态融合为单一向量；`tongyi-embedding-vision-plus-2026-03-06` 等新版模型改用“同 content 对象内多字段”方式实现融合，不再依赖此参数。
- **`instruct`**：排序模型专用参数（`qwen3-rerank`/`qwen3-vl-rerank`），用于指定任务类型（如 `"Given a web search query, retrieve relevant passages..."`），直接影响排序策略，建议使用英文。
- **`text_type`**：批处理 API 中区分 `query` 与 `document` 类型，对非对称检索任务（如 RAG）可提升精度，默认为 `document`。

## 使用方式

- **同步调用**：适用于低延迟、小批量场景（≤20 行文本或 ≤10 个多模态元素）。使用 OpenAI 兼容 SDK 或原生 HTTP 请求，Endpoint 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`（文本）或 `https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`（多模态）。
- **异步批处理**：适用于海量数据（如千万级文档向量化）。需先调用 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（带 `X-DashScope-Async: enable` 头），再轮询 `GET /api/v1/tasks/{task_id}` 获取结果 URL；SDK 封装了 `BatchTextEmbedding.async_call()` 和 `wait()` 等便捷方法。
- **排序调用**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks` 接口，`qwen3-vl-rerank`/`gte-rerank-v2` 使用 `/api/v1/services/rerank/text-rerank/text-rerank`，注意请求体结构差异——前者 `query`/`documents` 与 `model` 同级，后者需嵌套在 `input` 对象内。

## 限制和注意事项

- **Token 与尺寸限制**：`qwen3.7-text-embedding` 单行支持 128,000 Token（北京），而 `text-embedding-v4` 仅 8,192；多模态模型中，`qwen3-vl-embedding` 图片限 10 MB，视频限 50 MB；超出将被截断，影响结果准确性。
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，新加坡地域同名模型无免费额度；批处理模型 `text-embedding-async-v2` 免费额度为 2000 万 Token。
- **模型弃用风险**：`gte-rerank` 系列已进入下线倒计时，新项目应优先选用 `qwen3-rerank`；`qwen2.5-vl-embedding` 仅支持融合向量，不支持 `multi_images`，选型时需确认业务是否需要独立向量能力。
- **异步任务生命周期**：批处理任务 ID 有效期仅 24 小时，结果 URL 也仅保留 24 小时，务必及时下载；并发运行中任务上限为 3 个，排队中总数不超过 50 个。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)


