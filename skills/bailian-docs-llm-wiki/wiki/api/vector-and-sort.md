# vector and sort

百炼平台提供文本向量化（vector）、多模态向量化（multimodal vector）和文本排序（rerank）三类核心能力，覆盖语义搜索、RAG、跨模态检索等典型场景。所有能力均通过标准化 API 提供，支持同步/异步调用、OpenAI 兼容模式及 DashScope SDK 封装，适用于从单条文本处理到百万级批量任务的全量需求。详细模型能力与参数约束请参考各接口文档。

## 支持的模型/功能

### 文本向量化
- **同步模型**：`qwen3.7-text-embedding`（最高 128K token 输入）、`text-embedding-v4`（默认 1024 维，支持 `dimensions` 参数）、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`  
- **异步批处理模型**：`text-embedding-async-v2`（单次最多 100,000 行）、`text-embedding-async-v1`  
- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：支持 `embeddings.create` 调用，需配置 `base_url` 为兼容模式地址（详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)）

### 多模态向量化
- **支持模态**：文本、图像（JPEG/PNG/WEBP 等）、视频（MP4/AVI/MOV 等 URL）及多图序列（`multi_images`）  
- **关键模型**：  
  - `qwen3-vl-embedding`：支持独立向量与融合向量（通过 `enable_fusion=true`），默认 2560 维  
  - `tongyi-embedding-vision-plus-2026-03-06`：支持融合向量（同 content 对象内[多模态输入](../concepts/multi-modal-input.md)）、`res_level` 和 `max_video_frames` 参数  
  - `qwen2.5-vl-embedding`：仅支持融合向量，不支持 `multi_images`  
- 详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)

### 文本排序（Rerank）
- **主流模型**：  
  - `qwen3-rerank`：纯文本排序，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-api/v1/reranks`），支持 `instruct` 任务指令  
  - `qwen3-vl-rerank`：跨模态排序（文本/图片/视频混合），支持图片/视频作为 query  
  - `gte-rerank-v2`（即将下线）：仅文本，最大支持 30,000 文档，[官方公告](https://www.aliyun.com/notice/118217) 明确推荐迁移至 `qwen3-rerank`  
- 接口路径与请求结构因模型而异，详见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)

> **注意**：`gte-rerank` 系列模型（含 `gte-rerank-v2`）将于 2026 年 05 月 30 日下线，新项目应直接使用 `qwen3-rerank` 或 `qwen3-vl-rerank`。

## 关键参数

| 参数 | 适用模型 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必选，指定模型名称 | `"text-embedding-v4"`, `"qwen3-vl-rerank"` |
| `input` / `query` / `documents` | 按模型区分 | 向量化：`input`（string/array/file）；排序：`query` + `documents`（array） | `"衣服的质量杠杠的..."`, `[{"text":"doc1"},{"image":"url"}]` |
| `dimensions` | `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 可选，指定输出向量维度；部分模型（如 `tongyi-embedding-vision-plus`）不支持 | `1024`, `2560` |
| `encoding_format` | 同步文本向量 | 仅支持 `"float"` | `"float"` |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | bool，启用融合向量生成 | `true` |
| `top_n` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 返回前 N 个结果 | `5` |
| `instruct` | `qwen3-rerank`, `qwen3-vl-rerank` | 任务指令，影响排序策略（如问答检索 vs 语义相似度） | `"Given a web search query, retrieve relevant passages..."` |
| `text_type` | 异步批处理（`text-embedding-async-*`） | 区分 `query`（检索查询）或 `document`（底库文本），影响向量表征 | `"query"` |

## 使用方式

### 同步调用（文本向量）
- **HTTP**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`  
- **SDK（OpenAI 兼容）**：使用 `openai` 客户端，设置 `base_url` 为兼容模式地址  
- **示例**（Python）：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  resp = client.embeddings.create(
      model="text-embedding-v4",
      input=["hello", "world"],
      dimensions=1024
  )
  ```

### 异步批处理（大文件）
- **HTTP**：两步调用 —— 先 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务，再 `GET /api/v1/tasks/{task_id}` 查询结果  
- **SDK**：`BatchTextEmbedding.call()`（同步封装）或 `BatchTextEmbedding.async_call()`（异步）  
- **注意**：输入必须为公开可访问的 URL 文件（如 OSS），单文件 ≤ 200MB，单行 ≤ 2048 token  

### 多模态向量
- **HTTP**：`POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`  
- **输入格式**：`input.contents` 为数组，每个元素为 `{"text": "..."}`, `{"image": "url"}`, `{"video": "url"}` 或 `{"multi_images": [...]}`  
- **融合向量**：`qwen3-vl-embedding` 需 `parameters.enable_fusion=true`；`tongyi-embedding-vision-plus-2026-03-06` 需将多模态字段置于同一对象内  

### 文本排序
- **纯文本**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks`，参数扁平化（`query`, `documents`, `top_n` 同级）  
- **跨模态**：`qwen3-vl-rerank` 使用 `/api/v1/services/rerank/text-rerank/text-rerank`，`query` 和 `documents` 均支持模态对象  
- **SDK**：统一使用 `dashscope.TextReRank.call()`，参数自动适配对应模型  

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：  
  - `qwen3.7-text-embedding` 单文本最长 128,000 token；`text-embedding-v4` 为 8,192；`qwen3-vl-embedding` 文本为 32,000；`qwen3-rerank` 单条文档为 4,000  
  - 总 [Token](../concepts/token.md) 计算规则：`qwen3-rerank` 为 `query_tokens + sum(doc_tokens)`；`qwen3-vl-rerank` 为 `query_tokens × doc_count + sum(doc_tokens)`，上限 120,000  

- **批量规模**：  
  - 同步向量：`qwen3.7-text-embedding` 最多 20 条；`text-embedding-v4` 最多 10 条  
  - 异步批处理：`text-embedding-async-v2` 单次最多 100,000 行  
  - 排序：`qwen3-rerank` 最多 500 文档；`qwen3-vl-rerank` 文本文档最多 100，图片最多 40，视频最多 4  

- **地域与 endpoint**：  
  - 同步/兼容接口：北京地域为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`  
  - 多模态/排序 HTTP 接口：公共 endpoint 为 `https://dashscope.aliyuncs.com/...`，新加坡地域需替换 host  
  - 异步批处理 SDK：需显式设置 `dashscope.base_http_api_url`  

- **免费额度与计费**：  
  - 所有模型均提供开通后 90 天内的免费额度（如 `text-embedding-v4` 为 100 万 token），具体额度见各模型概览表  
  - 多模态模型按模态分别计费（文本/图片/视频单价不同），详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)  

- **限流**：  
  - 同步接口受通用 [限流](https://help.aliyun.com/zh/model-studio/rate-limit) 约束  
  - 异步批处理：单用户并发运行中任务 ≤ 3 个，排队中 + 运行中任务 ≤ 50 个  
  - `qwen3-vl-rerank` 视频处理依赖 `fps` 参数控制帧数，避免超时  

> **注意**：`text-embedding-v1` 与 `text-embedding-v2` 的语种支持范围（50+/100+）在文档中存在表述差异，以 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 中表格为准；`multimodal-embedding-v1` 不支持 `dimension` 参数，固定 1024 维，与文档 3 中其他模型形成明确区分。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


