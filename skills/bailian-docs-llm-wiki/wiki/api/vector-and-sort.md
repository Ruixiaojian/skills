# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本向量化（embedding）、多模态向量化及文本排序（rerank）三大能力，用于构建语义搜索、RAG、推荐系统等AI应用的核心检索与排序链路。向量模型将输入内容映射到统一语义空间，支持余弦相似度计算；排序模型则对召回结果进行精细化重排序，提升相关性精度。所有服务均提供同步、异步及OpenAI兼容调用方式。

## 支持的模型/功能

### 文本向量化（Embedding）
- **通用文本模型**：`qwen3.7-text-embedding`（最大128K Token/行，20行/请求）、`text-embedding-v4`（8K Token/行，10行/请求）、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`  
- **批处理异步模型**：`text-embedding-async-v2`（100,000行/请求，2,048 Token/行）、`text-embedding-async-v1`  
- **OpenAI兼容接口**：支持通过 `/compatible-mode/v1/embeddings` 调用 `text-embedding-v4` 等模型，详见[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)

### 多模态向量化（Multimodal Embedding）
- **融合与独立向量**：`qwen3-vl-embedding`（支持 `enable_fusion=true` 生成融合向量）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06`（支持融合与独立，融合需将 text/image/video 放入同一 content 对象）  
- **输入类型**：支持 `text`、`image`（JPEG/PNG/WEBP等）、`video`（MP4/AVI/MOV等URL）、`multi_images`（最多64张）  
- **能力说明**：所有模态向量位于同一语义空间，可直接跨模态计算相似度，详见[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)

### 文本排序（Rerank）
- **主流模型**：`qwen3-rerank`（纯文本，500文档/请求）、`qwen3-vl-rerank`（多模态，文本/图片/视频混合排序）、`gte-rerank-v2`（已进入下线过渡期）  
- **关键提示**：`gte-rerank` 模型将于2026年05月30日下线，[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档明确建议迁移至 `qwen3-rerank`  
- **任务指令**：`qwen3-rerank` 和 `qwen3-vl-rerank` 支持 `instruct` 参数（如 `"Given a web search query, retrieve relevant passages..."`），用于引导排序策略

> **注意**：文档1中 `text-embedding-v2` 的单价标注为 `0.0007元`，而文档4中 `text-embedding-async-v2` 单价同为 `0.0007元`，但文档1未说明其是否支持异步；实际使用中，`text-embedding-async-*` 系列专为批量场景设计，不可与同步模型混用。

## 关键参数

| 参数 | 类型 | 说明 | 适用模型 |
|------|------|------|----------|
| `model` | string | 必选。模型名称，如 `"text-embedding-v4"`、`"qwen3-rerank"`、`"qwen3-vl-embedding"` | 全部 |
| `input` | string / array / object | 必选。文本字符串、字符串列表、文件或结构化多模态对象（含 `text`/`image`/`video` 字段） | 全部 |
| `dimensions` | integer | 可选。指定输出向量维度（如 `1024`, `2048`）。`qwen3.7-text-embedding` 支持 `2560`；`multimodal-embedding-v1` 不支持此参数 | `text-embedding-*`、`qwen3-vl-embedding`、`tongyi-*` 等 |
| `encoding_format` | string | 可选。仅支持 `"float"` | 同步文本向量模型 |
| `top_n` | integer | 可选。返回排序后前 N 个结果 | `qwen3-rerank`、`gte-rerank-v2`、`qwen3-vl-rerank` |
| `instruct` | string | 可选。英文任务指令，影响排序逻辑（如问答检索 vs 语义相似度） | `qwen3-rerank`、`qwen3-vl-rerank` |
| `enable_fusion` | boolean | 可选。仅 `qwen3-vl-embedding` 支持，设为 `true` 时融合所有输入为单向量 | `qwen3-vl-embedding` |
| `parameters` | object | 可选。HTTP调用中需嵌套，SDK中常扁平化。包含 `dimension`、`fps`、`res_level` 等 | 多模态与排序模型 |

## 使用方式

### 同步调用（文本向量）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
resp = client.embeddings.create(
    model="text-embedding-v4",
    input=["文本A", "文本B"],
    dimensions=1024
)
```
> 示例代码来自[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)，适用于中小规模实时向量化。

### 异步批处理（大规模文本）
```python
from dashscope import BatchTextEmbedding
result = BatchTextEmbedding.call(
    model=BatchTextEmbedding.Models.text_embedding_async_v2,
    url="https://your-bucket/file.txt",  # 每行一条文本，≤100,000行
    text_type="document"
)
```
> 批处理接口强制异步，需通过 `task_id` 查询结果，详见[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量（图文视频混合）
```python
import dashscope
resp = dashscope.MultimodalEmbedding.call(
    model="qwen3-vl-embedding",
    input={
        "contents": [
            {"text": "商品描述"},
            {"image": "https://example.com/1.jpg"},
            {"video": "https://example.com/vid.mp4"}
        ]
    },
    parameters={"enable_fusion": True}
)
```

### 文本排序（Rerank）
```python
# qwen3-rerank（纯文本）
resp = dashscope.TextReRank.call(
    model="qwen3-rerank",
    query="用户问题",
    documents=["候选1", "候选2"],
    top_n=3,
    instruct="Given a web search query..."
)

# qwen3-vl-rerank（多模态）
resp = dashscope.TextReRank.call(
    model="qwen3-vl-rerank",
    query={"image": "https://img.url"},
    documents=[{"text": "文本"}, {"image": "https://img2.url"}],
    top_n=2
)
```

## 限制和注意事项

- **Token限制**：`qwen3.7-text-embedding` 单行最长 128,000 Token；`text-embedding-v4` 为 8,192 Token；`qwen3-rerank` 单条 Query 或 Document 最长 4,000 Token；`qwen3-vl-embedding` 文本最长 32,000 Token  
- **数量限制**：`text-embedding-v4` 最多 10 行/请求；`qwen3-rerank` 最多 500 文档/请求；`qwen3-vl-rerank` 文本类最多 100 条，图片类最多 40 条  
- **免费额度**：各模型均有 90 天有效期的免费 Token 额度（如 `qwen3.7-text-embedding` 为 100 万 Token），具体以控制台为准  
- **地域与Endpoint**：北京地域使用 `cn-beijing.maas.aliyuncs.com`，新加坡地域需替换为 `ap-southeast-1.maas.aliyuncs.com`；多模态向量统一使用 `dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`  
- **限流策略**：异步批处理任务并发数上限为 3 个，排队中+运行中任务总数不超过 50 个；同步接口遵循通用[限流](https://help.aliyun.com/zh/model-studio/rate-limit)规则  
- **模型兼容性**：`tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` 不支持 `dimension` 参数，固定返回 1152 或 768 维；`multimodal-embedding-v1` 固定 1024 维  

> **注意**：文档3中 `tongyi-embedding-vision-plus` 在“模型概览”表格中标注图片大小限制为“单张大小不超过**3 MB**”，但在“输入格式与语种限制”表格中又写为“最多 **8 张**且单张大小不超过**3 MB**”，二者一致；而文档3另一处提到 `tongyi-embedding-vision-plus-2026-03-06` “建议单张大小不超过**5 MB**，最大**10 MB**”，该差异属版本演进，非矛盾。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)


