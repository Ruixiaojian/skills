# vector and sort

`vector and sort` 是百炼平台提供的核心向量化与排序能力集合，涵盖文本、多模态内容的向量生成（vector），以及对召回结果进行语义相关性重排序（sort/rerank）。该能力支撑[检索增强生成](../concepts/rag.md)（RAG）、跨模态搜索、内容聚类等关键AI应用，支持同步、异步及OpenAI兼容等多种调用方式。

## 支持的模型/功能

### 向量生成（Vector）
- **通用文本向量**：`qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`，适用于语义搜索、聚类、分类等场景。其中 `qwen3.7-text-embedding` 支持最长 128,000 [Token](../concepts/token.md) 的单条输入 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **多模态向量**：`qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06`、`tongyi-embedding-vision-flash-2026-03-06` 等，支持文本、图像、视频及其组合的统一语义空间编码，可用于跨模态检索与融合表征 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **批处理文本向量**：`text-embedding-async-v2`、`text-embedding-async-v1`，专为超大规模文本（单次最多 100,000 行）设计，采用异步任务模式 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 排序（Sort/Rerank）
- **纯文本排序**：`qwen3-rerank`，支持最多 500 个文档的高效重排序，兼容 OpenAI Rerank 接口，推荐替代已下线的 `gte-rerank` 模型 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **多模态排序**：`qwen3-vl-rerank`，支持文本、图像、视频混合查询与文档的跨模态相关性排序，适用于图像聚类、跨模态搜索等场景。
- **历史模型**：`gte-rerank-v2` 仍可使用，但官方已明确其将于 2026 年 05 月 30 日下线，迁移至 `qwen3-rerank` 或 `qwen3-vl-rerank` 为最佳实践。

> **注意**：文档中 `qwen3-vl-rerank` 的最大文档数描述存在不一致——一处写为“文本：100 / 图片：40 / 视频：4”，另一处表格中仅写“500”。根据 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 中“单次请求最大文档数”说明及实际参数约束，应以按模态类型分档的限制为准（即文本最多 100 条、图片最多 40 条、视频最多 4 条），而非统一 500 条。该差异已在模型能力对照表中体现，开发者需按实际模态组合计算上限。

## 关键参数

| 参数名 | 适用模型 | 类型 | 说明 |
|--------|----------|------|------|
| `model` | 全部 | string | 必选。模型名称，如 `"qwen3-rerank"`、`"tongyi-embedding-vision-plus-2026-03-06"`。 |
| `input` / `query` / `documents` | 全部 | object / array / string | 输入内容结构因模型而异：`qwen3-rerank` 使用扁平 `query` + `documents`；`qwen3-vl-rerank` 和多模态向量模型使用嵌套 `input.contents` 或 `input.query` + `input.documents`。 |
| `dimension` | `qwen3.7-text-embedding`, `text-embedding-v4`, `text-embedding-v3`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | integer | 可选。指定输出向量维度，不同模型支持值不同（如 `qwen3-vl-embedding` 支持 256–2560）。`text-embedding-v2/v1` 及 `tongyi-embedding-vision-plus/flash`（非快照版）不支持此参数。 |
| `enable_fusion` | `qwen3-vl-embedding` | boolean | 可选。设为 `true` 时将 `contents` 中所有模态融合为单个向量；默认 `false` 为独立向量。`tongyi-embedding-vision-plus-2026-03-06` 等快照版不使用此参数，改用同 content 对象内多模态字段实现融合。 |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | integer | 可选。返回排序后前 N 个结果，默认返回全部。 |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank`, `qwen3-vl-embedding` | string | 可选。任务指令，用于引导模型行为（如 `"Given a web search query..."`），建议英文。对 `qwen3-vl-embedding` 可提升效果约 1%–5%。 |
| `fps` | `qwen3-vl-rerank`, `qwen3-vl-embedding` | float | 可选。视频帧采样比例 `[0,1]`，默认 `1.0`。 |
| `res_level` | `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | integer | 可选。输入分辨率档位（0/1/2/3），影响单图 token 数。 |

## 使用方式

### 向量生成
- **同步调用（小批量）**：使用 `/compatible-mode/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`（原生）端点。支持字符串、字符串列表、文件输入。示例：
  ```bash
  curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{"model": "text-embedding-v4", "input": ["hello", "world"], "dimensions": 1024}'
  ```
- **异步批处理（超大批量）**：使用 `/api/v1/services/embeddings/text-embedding/text-embedding` 端点，需设置 `X-DashScope-Async: enable` 头，并传入 `input.url` 指向文本文件（每行一条）。结果通过 `GET /api/v1/tasks/{task_id}` 查询 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：`contents` 数组中可混合 `{"text":...}`, `{"image":...}`, `{"video":...}`, `{"multi_images":[...]}`。融合向量需按模型要求配置（`qwen3-vl-embedding` 用 `enable_fusion=true`；快照版将多模态字段置于同一对象内）。

### 排序
- **文本排序**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks`，参数扁平化；`qwen3-vl-rerank` 和 `gte-rerank-v2` 使用 `/api/v1/services/rerank/text-rerank/text-rerank`，参数嵌套在 `input` 下。
- **多模态排序**：`query` 和 `documents` 元素支持 `text`/`image`/`video` 字段，例如 `{"image": "url"}` 或 `{"text": "string"}`。

## 限制和注意事项

- **[Token](../concepts/token.md) 与尺寸限制**：各模型有严格输入限制。例如 `qwen3.7-text-embedding` 单条文本上限 128,000 [Token](../concepts/token.md)，而 `text-embedding-v4` 仅 8,192 Token；多模态模型对图片大小（如 `qwen3-vl-embedding` ≤10 MB）、视频格式（H.264/H.265）和数量（如 `qwen3-vl-rerank` 视频最多 4 条）均有明确要求。
- **免费额度与计费**：所有模型均提供开通后 90 天内的免费额度（如 `qwen3.7-text-embedding` 各 100 万 Token），但额度类型和有效期规则不同，详见各模型概览表 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **限流策略**：异步批处理有并发任务数限制（单用户最多 3 个运行中任务，排队中总数 ≤50）；同步接口有 RPS 限制，超出将触发限流 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)。
- **模型下线提醒**：`gte-rerank` 系列模型已进入下线倒计时，务必迁移到 `qwen3-rerank` 或 `qwen3-vl-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **SDK 封装差异**：DashScope SDK 对参数进行了扁平化封装（如 `top_n` 直接作为方法参数），而 HTTP 接口需遵循嵌套结构（如 `parameters.top_n`），调用时需注意区分。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)


