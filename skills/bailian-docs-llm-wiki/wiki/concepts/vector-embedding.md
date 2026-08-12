# 向量嵌入

向量嵌入（Vector Embedding）是将原始非结构化数据（如文本、图像、视频等）映射到高维稠密实数向量空间的数学表示过程，其核心目标是让语义相似的内容在向量空间中距离更近，从而支撑语义搜索、聚类、推荐与RAG等AI应用。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG知识库检索**：知识库构建时，文档被自动切片并经向量模型（如 `text-embedding-v4` 或 `qwen3-vl-embedding`）编码为向量，存入向量数据库；查询时，用户问题也被向量化，通过近似最近邻（ANN）检索召回语义最相关的文本片段。
- **多模态理解**：在图片问答、音视频搜索等场景中，`qwen3-vl-embedding` 等模型可对文本、图像、视频统一编码——支持独立向量输出（各模态分别生成向量）或融合向量输出（跨模态语义对齐后生成单一向量），用于跨模态检索与理解。
- **框架集成（LlamaIndex / Spring AI Alibaba）**：开发者无需自行部署嵌入模型，直接调用百炼托管的知识库或 `DashScopeCloudIndex`，底层自动使用平台预置向量模型完成嵌入；所有框架均不支持替换嵌入模型，确保服务一致性与性能优化。
- **向量+排序联合 pipeline**：典型流程为“向量召回 → 排序精排”：先用向量模型快速召回 TopK 候选（如 100 个切片），再交由 `qwen3-rerank` 或 `qwen3-vl-rerank` 进行细粒度相关性重排序，显著提升最终结果准确率。

## 关键参数和配置

| 参数 | 说明 | 典型值/约束 | 适用场景 |
|------|------|-------------|----------|
| `dimensions` | 指定向量维度（影响存储、计算开销与表达能力） | `256`, `1024`, `2560`；部分模型（如 `text-embedding-v2`）固定维度，不支持该参数 | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding` 等 |
| `encoding_format` | 控制响应中向量的序列化格式 | `"float"`（默认，返回浮点数组）、`"base64"`（压缩传输，需解码） | 同步文本向量 API |
| `enable_fusion` | 控制多模态输入是否融合为单一向量 | `true`（融合）、`false`（默认，各模态独立输出） | 仅 `qwen3-vl-embedding`；新版模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过请求结构隐式控制，**不使用此参数** |
| `text_type` | 区分查询文本与文档文本，优化非对称检索效果 | `"query"`（用于检索）、`"document"`（用于索引） | 批处理文本向量模型（`text-embedding-async-v2`） |
| `instruct` | 提供任务指令，引导排序模型行为（仅影响 rerank，但常与嵌入协同设计） | `"Retrieve passages relevant to a technical support query"`（英文） | `qwen3-rerank`, `qwen3-vl-rerank` |

> ⚠️ 注意：  
> - 向量模型本身**不接受 `instruct` 参数**；该参数属于排序模型，但在 RAG 流程中常与嵌入阶段语义对齐设计。  
> - 知识库创建后，所用嵌入模型及维度即固化，不可变更；如需更换，需重建知识库。  
> - 多模态嵌入中，`enable_fusion=true` 时，输入 `contents: [{"text":"A"}, {"image":"url"}]` 将输出 1 个融合向量；`false` 则输出 2 个独立向量。

## 面向开发者，简洁实用

- ✅ **选型建议**：  
  - 通用文本检索 → 优先用 `text-embedding-v4`（平衡精度与成本）；  
  - 高精度长文本 → `qwen3.7-text-embedding`（支持 2560 维）；  
  - 图文混合场景 → `qwen3-vl-embedding` + `enable_fusion=true`；  
  - 超大规模批处理（≤10 万行）→ 用 `text-embedding-async-v2`，注意设置 `text_type`。

- ✅ **调试技巧**：  
  - 向量相似度计算可用余弦相似度：`cosine_similarity(a, b) = dot(a,b) / (norm(a)*norm(b))`；百炼知识库默认阈值 `0.3` 可作为 baseline；  
  - 若召回结果语义偏差大，优先检查文本清洗质量（如特殊符号、乱码）和 `text_type` 是否误配（query/doc 混用会导致分布偏移）；  
  - 多模态嵌入失败常见原因为 `image`/`video` 字段 URL 无效或跨域未授权，请确保资源可公开访问或使用 base64 编码内联。

- ✅ **避坑提醒**：  
  - `gte-rerank` 系列将于 2026 年 5 月 30 日下线，新项目请直接使用 `qwen3-rerank`；  
  - LlamaIndex 和 Spring AI Alibaba 均**不支持自定义嵌入模型或切分逻辑**，所有向量化均由百炼云端完成；  
  - 异步批处理任务需轮询 `GET /api/v1/tasks/{task_id}` 获取结果，状态为 `SUCCEEDED` 后方可读取向量。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [frameworks](../api/frameworks.md)
- [knowledge base](../guides/knowledge-base.md)
- [application component api reference](../api/application-component-api-reference.md)


