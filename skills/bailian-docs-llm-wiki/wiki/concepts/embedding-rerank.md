# 向量化与重排序

向量化（Embedding）是将文本、图像、视频等[多模态](multi-modal.md)内容映射为稠密数值向量的过程，用于表征语义；重排序（Rerank）是在初步检索结果基础上，基于查询与候选文档的细粒度语义匹配度进行二次精排，提升相关性排序质量。二者共同构成百炼平台语义检索能力的核心双阶段 pipeline：先通过向量相似度快速召回（retrieval），再通过重排序模型深度打分（ranking）。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识库（RAG）场景**：  
  知识库构建阶段调用向量化模型（如 `text-embedding-v4` 或 `qwen3-vl-embedding`）对切片（chunk）进行编码并存入向量索引；检索时，先以查询向量在索引中召回 TopK 初筛结果（默认 50 条），再交由重排序模型（如 `qwen3-rerank`）进行精细化打分与重排，最终返回最高相关性的前 N 条切片（如 `top_n=5`）。该两阶段设计兼顾效率与精度，是 RAG 效果的关键保障。

- **独立 API 调用场景**：  
  开发者可通过 `/api/v1/services/embeddings/...` 接口直接调用向量化服务（支持同步/异步批量），生成自定义数据的向量；也可通过 `/api/v1/services/rerank/...` 接口对任意文本或图文混合列表执行重排序，适用于非知识库类的定制化搜索、推荐、聚类等任务。

- **框架集成场景（LlamaIndex / Spring AI Alibaba）**：  
  框架封装了底层向量与重排序能力。例如 LlamaIndex 中配置 `DashScopeRerank` 后处理器，自动调用 `qwen3-rerank` 对检索节点重排；Spring AI Alibaba 的 `DashScopeDocumentRetriever` 默认启用平台托管的向量+重排序链路，开发者仅需指定 `INDEX_NAME` 和 `top_n` 即可获得端到端语义检索结果。

- **[多模态](multi-modal.md)应用场景**：  
  支持跨模态向量化（如 `qwen3-vl-embedding` 可融合 text+image 生成统一向量，或为各模态分别生成独立向量）和跨模态重排序（如 `qwen3-vl-rerank` 支持“以图搜文”“以文搜视频”），满足视觉理解、内容审核、跨模态推荐等需求。

- **知识增强型 API（`/api/v1/indices/knowledge/search`）**：  
  该高层接口内部已固化向量化与重排序流程，开发者无需显式调用底层模型——平台自动选用适配知识库类型的向量模型与 rerank 模型完成全流程处理，仅暴露 `query` 和 `top_k` 等业务参数。

## 关键参数和配置

| 参数名 | 适用场景 | 说明 | 推荐值/注意事项 |
|--------|----------|------|-----------------|
| `dimension` | 向量化（部分模型） | 指定向量维度，影响存储与计算开销。仅 `qwen3.7-text-embedding`、`qwen3-vl-embedding` 等新模型支持，旧模型（如 `text-embedding-v2`）不支持。 | `1024`（平衡精度与性能）、`2560`（高精度场景） |
| `enable_fusion` | [多模态](multi-modal.md)向量化（仅 `qwen3-vl-embedding`） | 控制是否将 `contents` 中所有模态融合为单个向量。新版模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过结构化输入实现融合，**不使用此参数**。 | `true`（需融合） / `false`（需独立向量） |
| `top_n` | 重排序（所有 rerank 模型） | 返回重排后最相关的前 N 条结果。直接影响费用（rerank 费用 = `top_n` × 文档数 × 单价）和下游 [Token](token.md) 消耗。 | `3–10`（RAG 场景常用）；注意 `qwen3-vl-rerank` 图片限制 40 条、视频限制 4 条 |
| `instruct` | 重排序（`qwen3-rerank` / `qwen3-vl-rerank`） | 自定义任务指令，引导模型关注特定匹配目标（如问答、相似度、摘要匹配）。强烈建议设置以提升领域适配性。 | `"Retrieve answers to factual questions."`、`"Rank by semantic similarity, not keyword overlap."` |
| `text_type` | 异步向量化（`text-embedding-async-v2`） | 标注文本用途（`query` 或 `document`），影响向量表示空间。对非对称检索（如问答场景）至关重要。 | 必须与实际用途一致，否则导致召回偏差 |
| `fps` | 多模态（视频输入） | 视频帧抽取比例（0–1），控制输入帧数与计算成本。 | `0.5`（平衡效果与性能）；默认 `1.0`（全帧） |

> ⚠️ 注意：  
> - 所有向量化与重排序模型均需通过 API Key 认证，且受地域（仅华北2北京）、额度与 QPS 限流约束；  
> - `gte-rerank` 系列将于 2026-05-30 下线，请尽快迁移到 `qwen3-rerank` 或 `qwen3-vl-rerank`；  
> - 知识库创建后，其向量模型与重排序策略**不可修改**，如需更换，需重建知识库。

## 面向开发者，简洁实用

- ✅ **优先选型**：文本场景用 `qwen3.7-text-embedding`（长文本支持） + `qwen3-rerank`；多模态场景用 `qwen3-vl-embedding` + `qwen3-vl-rerank`。  
- ✅ **调用技巧**：重排序前，初筛 `TopK` 不宜过大（建议 ≤100），避免冗余计算；`instruct` 是低成本提升效果的关键开关，务必设置。  
- ✅ **性能权衡**：异步向量化（`text-embedding-async-v2`）适合底库初始化；同步接口（OpenAI 兼容 `/v1/embeddings`）适合实时 query 向量化。  
- ✅ **调试建议**：使用控制台「命中测试」或 `Retrieve` API 直接观察原始分数与重排后顺序，验证 `similarity_cutoff` 和 `top_n` 配置合理性。  
- ❌ **避坑提示**：勿混用 `DASHSCOPE_API_KEY` 与 `AI_DASHSCOPE_API_KEY`；勿在知识库 API 中尝试传入自定义 embedding 模型——该能力当前未开放。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [knowledge](../api/knowledge.md)
- [application component api reference](../api/application-component-api-reference.md)


