# vector and sort

`vector and sort` 是百炼平台提供的核心语义处理能力集合，涵盖文本、多模态内容的向量化（embedding）以及检索结果的重排序（rerank）。向量模型将原始内容映射到统一语义空间，支撑跨模态检索、聚类与相似度计算；排序模型则对召回结果进行精细化打分与重排，显著提升RAG、搜索引擎等应用的相关性。两类能力均支持同步/异步调用、多语言及灵活参数配置。

## 支持的模型/功能

### 向量模型（Embedding）

- **通用文本向量**：提供同步与异步两种接口形态。
  - 同步模型（如 `qwen3.7-text-embedding`, `text-embedding-v4`, `text-embedding-v2`）适用于低延迟、小批量场景，单次最多支持 20–25 条文本，单条最长 128,000 [Token](../concepts/token.md)（[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)）。
  - 异步批处理模型（如 `text-embedding-async-v2`）适用于海量文本（单文件最多 100,000 行，200 MB），需通过任务 ID 查询结果（[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）。

- **多模态向量**：支持文本、图像、视频的联合或独立向量化。
  - `qwen3-vl-embedding` 和 `qwen2.5-vl-embedding` 均基于 Qwen 底座，前者支持独立/融合双模式，后者仅支持融合向量（[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)）。
  - `tongyi-embedding-vision-plus-2026-03-06` 等快照版本支持 `res_level` 和 `max_video_frames` 等高级参数，并兼容独立与融合向量生成。

### 排序模型（Rerank）

- **纯文本排序**：`qwen3-rerank` 是当前主力模型，支持 500 文档/请求、4,000 [Token](../concepts/token.md)/文档，采用兼容 OpenAI 的 `/compatible-api/v1/reranks` 接口。
- **多模态排序**：`qwen3-vl-rerank` 支持 text/image/video 混合查询与文档，最大文档数按模态类型动态限制（文本 100、图片 40、视频 4），使用 `/api/v1/services/rerank/text-rerank/text-rerank` 接口（[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)）。
- > **注意**：`gte-rerank` 系列模型已进入下线流程（2026年05月30日终止服务），新项目应优先选用 `qwen3-rerank` 或 `qwen3-vl-rerank`。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `dimension` / `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度，不同模型支持范围不同。注意：`text-embedding-v1/v2` 和 `tongyi-embedding-vision-plus` 不支持该参数（固定维度） | `1024`, `2560` |
| `enable_fusion` | `qwen3-vl-embedding` | 控制是否将 `contents` 中所有输入融合为单个向量（`true`）或各自生成独立向量（`false`，默认） | `true` |
| `top_n` | 所有 rerank 模型 | 返回排序后前 N 个结果，不指定则返回全部 | `10` |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Given a web search query..."`），影响相关性判断逻辑 | `"Retrieve semantically similar text."` |
| `fps` | `qwen3-vl-rerank`, 多模态 embedding 模型 | 视频帧抽取比例（0.0–1.0），用于控制视频处理开销 | `0.5` |
| `res_level` | `tongyi-embedding-vision-plus-2026-03-06` 等 | 输入分辨率档位（0–3），影响 token 消耗与精度平衡 | `1` |

> **注意**：`tongyi-embedding-vision-plus-2026-03-06` 和 `tongyi-embedding-vision-flash-2026-03-06` 的融合向量**不使用 `enable_fusion` 参数**，而是通过将 `text`/`image`/`video` 放在同一个 `content` 对象中实现（[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)）。

## 使用方式

### 向量生成（Embedding）

- **同步文本向量**（推荐小批量）：
  ```bash
  curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
        "model": "text-embedding-v4",
        "input": ["苹果", "香蕉", "橙子"],
        "dimensions": 1024
      }'
  ```

- **多模态独立向量**（`tongyi-embedding-vision-plus`）：
  ```bash
  curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
        "model": "tongyi-embedding-vision-plus",
        "input": {
          "contents": [
            {"text": "商品标题"},
            {"image": "https://example.com/1.jpg"}
          ]
        }
      }'
  ```

- **异步批处理**（大文件）：
  1. 创建任务：`POST /api/v1/services/embeddings/text-embedding/text-embedding` + `X-DashScope-Async: enable`
  2. 查询结果：`GET /api/v1/tasks/{task_id}`（[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）

### 排序（Rerank）

- **纯文本排序**（`qwen3-rerank`）：
  ```bash
  curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1/reranks' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
        "model": "qwen3-rerank",
        "query": "如何更换手机电池",
        "documents": ["步骤1：关机", "步骤2：拆后盖", "锂电池寿命约2年"],
        "top_n": 2
      }'
  ```

- **多模态排序**（`qwen3-vl-rerank`，图片查询）：
  ```bash
  curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
        "model": "qwen3-vl-rerank",
        "input": {
          "query": {"image": "https://example.com/photo.jpg"},
          "documents": [
            {"text": "手机维修指南"},
            {"image": "https://example.com/repair.jpg"}
          ]
        },
        "parameters": {"top_n": 1}
      }'
  ```

## 限制和注意事项

- **地域与 endpoint 差异**：北京地域使用 `cn-beijing.maas.aliyuncs.com`，新加坡地域需替换为 `ap-southeast-1.maas.aliyuncs.com`；多模态 embedding 统一使用 `dashscope.aliyuncs.com`（[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)）。
- **输入格式约束**：
  - 多模态 embedding 中，`video` 只支持 URL，不支持 Base64；`multi_images` 仅部分模型支持（如 `tongyi-embedding-vision-plus`）。
  - `qwen2.5-vl-embedding` **不支持多图输入**，且强制返回融合向量（[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)）。
- **[Token](../concepts/token.md) 计费与限流**：
  - 异步批处理有并发限制：单用户最多 3 个任务同时运行，排队中+运行中总数不超过 50（[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）。
  - `qwen3-vl-rerank` 的总输入 Token 计算公式为 `Query Tokens × Document 数量 + Document Tokens 总和`，不得超过 120,000（[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)）。
- **响应结构差异**：`qwen3-rerank` 响应无 `output` 包裹层，`results` 直接位于顶层；而 `qwen3-vl-rerank` 和 `gte-rerank-v2` 的 `results` 在 `output.results` 下（[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)）。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)


