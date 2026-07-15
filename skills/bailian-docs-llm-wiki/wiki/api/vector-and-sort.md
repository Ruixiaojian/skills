# vector and sort

百炼平台提供文本向量化（vector）、多模态向量化及文本排序（rerank）三大核心能力，覆盖语义搜索、RAG、跨模态检索等典型场景。所有服务均支持同步与异步调用模式，可通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope 原生 SDK 快速集成。开发者需根据数据规模、模态类型、延迟敏感度及精度要求选择合适模型与调用方式。

## 支持的模型/功能

- **通用文本向量模型**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`v3`、`v2`、`v1` 等版本，适用于纯文本语义表征；其中 `qwen3.7-text-embedding` 支持最高 128,000 [Token](../concepts/token.md) 单条输入与 2560 维向量输出 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **批处理异步向量模型**：`text-embedding-async-v2` 支持单次 100,000 行文本批量处理，适用于大规模离线向量化任务 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态向量模型**：`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等支持文本、图像、视频统一语义空间编码，提供独立向量与融合向量两种模式 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **文本排序（Rerank）模型**：`qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）、`gte-rerank-v2`（已进入下线过渡期）用于对召回结果进行精准重排序；注意 `gte-rerank` 模型将于 2026 年 05 月 30 日下线，应迁移至 `qwen3-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档 1 中 `text-embedding-v2` 的“单行最大 2,048 [Token](../concepts/token.md)”与文档 4 中 `qwen3-vl-rerank` 的“单条最大输入[Token](../concepts/token.md)：8,000（文本）”存在隐含矛盾——前者为向量模型输入限制，后者为排序模型输入限制，二者不可直接对比；但需注意 `qwen3-rerank` 的单条文档限制为 4,000 Token，而 `qwen3-vl-rerank` 文本类文档上限为 100 条 × 4,000 Token，实际使用中应以各模型自身文档为准。

## 关键参数

| 参数名 | 类型 | 说明 | 支持模型 |
|--------|------|------|----------|
| `model` | string | 必选，指定模型名称 | 全部 |
| `input` / `query` / `documents` | string / array / object | 必选，输入内容格式依模型而异：文本向量支持 `string`/`array<string>`/`file`；多模态向量使用 `contents: [{text:"..."}, {image:"..."}]`；排序模型中 `qwen3-rerank` 要求 `query` 和 `documents` 同级，`qwen3-vl-rerank` 则需嵌套在 `input` 对象内 | [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)、[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) |
| `dimensions` | integer | 可选，指定输出向量维度（如 1024、2048）；`text-embedding-v1/v2` 不支持该参数；`multimodal-embedding-v1` 固定 1024 维 | [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)、[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) |
| `encoding_format` | string | 可选，仅支持 `"float"` | [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) |
| `top_n` | integer | 可选，排序模型返回前 N 个结果 | [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) |
| `instruct` | string | 可选，排序任务指令（如 `"Retrieve semantically similar text."`），影响相关性判断逻辑 | [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) |
| `enable_fusion` | boolean | 可选，仅 `qwen3-vl-embedding` 支持，启用后将 `contents` 中所有模态融合为单一向量 | [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) |

## 使用方式

- **同步调用（低延迟、小批量）**：适用于实时搜索、RAG 在线推理。使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)时，`base_url` 需配置为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（文本向量）或 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1/reranks`（`qwen3-rerank`）；HTTP endpoint 为 `POST /embeddings` 或 `POST /reranks`。  
- **异步批处理（高吞吐、离线任务）**：适用于日志/商品库全量向量化。调用 `text-embedding-async-v2` 时需设置请求头 `X-DashScope-Async: enable`，并通过 `task_id` 轮询结果；文件需托管于公网可访问 URL（如 OSS），单文件 ≤ 200MB [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态联合处理**：使用 `qwen3-vl-embedding` 或 `tongyi-embedding-vision-plus-2026-03-06` 时，通过 `contents` 数组传入混合模态对象；融合向量需确保所有模态在同一 `content` 对象内（如 `{"text":"...", "image":"..."}`），而非分散在多个数组元素中 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **SDK 封装调用**：推荐使用 DashScope Python/Java SDK，自动处理认证、重试与响应解析。注意 SDK 参数扁平化（如 `top_n` 直接传参），而 HTTP 接口部分模型需嵌套在 `parameters` 或 `input` 内 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 限制和注意事项

- **Token 与行数限制严格区分**：`qwen3.7-text-embedding` 单条支持 128,000 Token 但最多 20 行；`text-embedding-v4` 单条仅 8,192 Token 且最多 10 行；`text-embedding-async-v2` 单次请求支持 100,000 行但每行限 2,048 Token —— 超限将被截断并导致语义失真。  
- **异步任务生命周期**：批处理任务 `task_id` 有效期为 24 小时，结果 URL 仅在此期间有效，需及时下载 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **模型兼容性风险**：`gte-rerank-v2` 已标记为下线模型，新项目禁止接入；`qwen2.5-vl-embedding` 仅支持融合向量且不支持 `multi_images`，与 `tongyi-embedding-vision-plus` 系列行为不一致，迁移时需重构输入结构。  
- **地域与 endpoint 绑定**：华北2（北京）地域的 `base_url` 与新加坡地域的 `base_url` 不同，且 `qwen3-rerank` 使用兼容模式 endpoint，而 `qwen3-vl-rerank` 使用原生 `/api/v1/services/...` endpoint，混用将导致 404 错误。  
- **免费额度时效性**：所有模型的免费额度（如 100 万 Token）均自百炼开通起 90 天内有效，过期未用完即作废。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


