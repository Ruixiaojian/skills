# vector and sort

`vector and sort` 是百炼平台提供的两类核心向量计算能力：文本向量化（embedding）用于将文本映射为稠密向量，支撑语义搜索、聚类等任务；文本排序（rerank）则对召回的候选文档进行精细化相关性重排序，显著提升检索精度。二者常组合使用构建端到端的RAG或搜索系统，支持同步/异步调用模式及多语言、多模态输入。

## 支持的模型/功能

### 文本向量化（Embedding）

- **同步模型**：`qwen3.7-text-embedding`（最高128K [Token](../concepts/token.md)）、`text-embedding-v4`（默认1024维，支持64–2048维）、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`  
- **异步批处理模型**：`text-embedding-async-v2`（单次最多100,000行，每行≤2,048 [Token](../concepts/token.md)）、`text-embedding-async-v1`  
- **模型差异**：`qwen3.7-text-embedding` 支持超长文本（128K [Token](../concepts/token.md)），但批量上限仅20行；`text-embedding-v4` 与 `v3` 支持 `dimensions` 参数动态指定向量维度；`text-embedding-async-v2` 专为海量文本批量处理设计，单价更低（0.0007元/千Token）且免费额度达2000万Token [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 文本排序（Rerank）

- **主流模型**：`qwen3-rerank`（纯文本，最高500文档）、`qwen3-vl-rerank`（多模态，支持文本/图片/视频混合排序）、`gte-rerank-v2`（已进入下线过渡期）  
- **关键提示**：`gte-rerank` 模型将于2026年05月30日下线，官方明确推荐迁移至 `qwen3-rerank` 或 `qwen3-vl-rerank` [原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  
- **功能区分**：`qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-api/v1/reranks`），参数扁平化；其余模型使用 `/api/v1/services/rerank/...` 接口，需嵌套 `input` 和 `parameters` 结构 [原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档1中 `text-embedding-v2` 标注“各50万Token免费额度”，而文档2中 `text-embedding-async-v2` 标注“各2000万Token免费额度”。二者属不同服务类型（同步 vs 异步），额度独立计算，无矛盾；但开发者需注意免费额度不跨模型共享。

## 关键参数

| 参数名 | 类型 | 适用场景 | 说明 |
|--------|------|----------|------|
| `model` | string | 所有调用 | 必选。同步向量模型如 `"text-embedding-v4"`；排序模型如 `"qwen3-rerank"`；异步向量模型如 `"text-embedding-async-v2"`。 |
| `input` / `query` + `documents` | string/array/object | 向量/排序 | 向量：支持 string、string[]、file（同步）或 `{url: "..."}`（异步）。排序：`qwen3-rerank` 直接传 `query` 和 `documents`；`qwen3-vl-rerank` 需封装在 `input` 对象内，并支持 `{"text": "...", "image": "...", "video": "..."}` 多模态格式。 |
| `dimensions` | integer | 向量（v3/v4） | 可选。仅 `text-embedding-v3` 和 `text-embedding-v4` 支持，取值范围：64/128/256/512/768/1024/1536/2048（v4）或2560（qwen3.7）。默认1024。 |
| `top_n` | integer | 排序 | 可选。返回前N个结果。`qwen3-rerank` 与 `qwen3-vl-rerank` 均支持，但前者参数位于顶层，后者需置于 `parameters` 内。 |
| `instruct` | string | `qwen3-rerank` / `qwen3-vl-rerank` | 可选。控制排序策略，如 `"Given a web search query, retrieve relevant passages that answer the query."`（问答检索）或 `"Retrieve semantically similar text."`（语义相似度）。英文指令效果更佳。 |
| `text_type` | string | 异步向量（`text-embedding-async-*`） | 可选。`"document"`（默认，用于底库）或 `"query"`（用于查询），影响向量表示优化方向。 |

## 使用方式

### 同步向量化（推荐小批量、低延迟场景）
- **Endpoint**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`  
- **SDK示例（Python）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  resp = client.embeddings.create(
      model="text-embedding-v4",
      input=["hello", "world"],
      dimensions=768,
      encoding_format="float"
  )
  ```

### 异步向量化（推荐大批量、离线处理）
- **两步流程**：1) `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务 → 2) `GET /api/v1/tasks/{task_id}` 轮询结果  
- **文件要求**：输入文件需为HTTP可访问URL，每行一条文本，单行≤2,048 Token，总行数≤100,000，文件大小≤200MB [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 文本排序
- **纯文本排序（qwen3-rerank）**：使用兼容接口，参数扁平化：
  ```bash
  curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1/reranks \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d '{"model":"qwen3-rerank","query":"search query","documents":["doc1","doc2"],"top_n":3}'
  ```
- **多模态排序（qwen3-vl-rerank）**：使用专用接口，`input` 内嵌 `query` 和 `documents`，支持混合模态：
  ```json
  {
    "model": "qwen3-vl-rerank",
    "input": {
      "query": {"image": "https://..."},
      "documents": [
        {"text": "text doc"},
        {"image": "https://..."},
        {"video": "https://..."}
      ]
    },
    "parameters": {"top_n": 2}
  }
  ```

## 限制和注意事项

- **Token限制严格**：向量模型对输入长度敏感。`qwen3.7-text-embedding` 单条最长128K Token，但批量仅限20行；`text-embedding-v4` 单条限8,192 Token，批量限10行；`text-embedding-async-v2` 单行限2,048 Token，但支持100,000行 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。超长输入将被截断，导致向量失真。
- **异步任务生命周期**：异步任务ID有效期24小时，结果URL同样仅保留24小时，需及时下载 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **排序模型输入计算规则**：`qwen3-vl-rerank` 的 `request_max_input_tokens` 计算公式为 `Query Tokens × Document 数量 + Document Tokens 总和`，总和不可超过120,000。若超限，请求将失败。
- **地域与Endpoint绑定**：所有接口均需替换 `{WorkspaceId}` 为真实业务空间ID，并按地域选择base URL（如北京为 `cn-beijing.maas.aliyuncs.com`，新加坡为 `ap-southeast-1.maas.aliyuncs.com`），否则返回404或认证错误。
- **限流策略**：同步向量接口遵循通用[限流](https://help.aliyun.com/zh/model-studio/rate-limit)规则；异步向量额外限制：单用户并发运行中任务≤3个，排队+运行中总数≤50个 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


