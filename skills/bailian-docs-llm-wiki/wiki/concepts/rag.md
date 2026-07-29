# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是百炼平台的核心能力范式，指在大语言模型生成响应前，先从私有或领域知识源中语义检索相关上下文，并将检索结果与用户查询一并输入模型，从而提升回答的准确性、事实性、专业性与时效性。该机制天然融合了信息检索的精准性与大语言模型的生成能力，是构建可信AI应用的关键技术路径。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中不是单一接口，而是贯穿多个能力层的统一范式，具体体现为以下三种典型集成方式：

- **知识库问答（零代码/低代码）**：在控制台创建知识库后，直接绑定至智能体或工作流应用的「文档知识库」节点；系统自动完成查询理解、多库联合检索（支持向量+关键词混合检索）、Rerank 排序与上下文注入，开发者只需配置 `TopK`、相似度阈值、标签过滤等参数，无需编写检索逻辑。

- **API 直接调用（高可控性）**：通过 `/api/v2/apps/knowledge/chat`（端到端问答）或 `/api/v1/indices/knowledge/search`（纯检索）接口，以 RESTful 方式集成 RAG 能力。问答接口内部封装“查询规划 → 知识检索 → 答案生成”三阶段，支持 SSE [流式输出](streaming-output.md)（含 `planning`/`retrieving`/`generating` 事件），适用于需快速上线的业务系统。

- **框架集成（开发友好）**：借助 LlamaIndex 或 Spring AI Alibaba 等 SDK，在应用代码中声明式调用云端知识库。例如 LlamaIndex 中使用 `DashScopeCloudIndex.as_query_engine()`，可直接配置 `similarity_top_k`、`similarity_cutoff` 及 `DashScopeRerank`，复用百炼的向量化、切分与重排能力，避免本地维护向量基础设施。

此外，RAG 也深度融入数据连接与评测体系：平台托管型数据连接器（如 PDF/Excel）自动构建成知识库供 RAG 调用；应用评测则支持对 RAG 输出进行相关性、事实一致性等维度的自动化打分，形成“构建→部署→评估→优化”闭环。

## 关键参数和配置

RAG 行为主要由以下参数控制，按使用层级归类：

| 类别 | 参数名 | 作用 | 典型取值 | 说明 |
|------|--------|------|----------|------|
| **检索范围** | `knowledgeIds`（API）<br>`cloud_index_name`（框架） | 指定参与检索的知识库 | `["kb-xxx", "kb-yyy"]` | 未指定时默认使用应用绑定的所有已发布知识库；多库联合检索上限为 15 个。 |
| **召回控制** | `TopK` / `max_retrieve_count` | Rerank 后最终送入大模型的文本切片数 | `3–10` | 过大会增加 token 开销与幻觉风险；过小易丢失关键信息。工作流节点中即为此配置项。 |
| **精度调节** | `similarity_threshold`（控制台/SDK）<br>`similarity_cutoff`（LlamaIndex） | 过滤低于该分数的检索结果 | `0.3–0.7` | 值越高越严格（召回少但精准），值越低越宽松（召回多但噪声多）。 |
| **性能与成本** | `vector_top_k` / `keyword_top_k` | 初步向量/关键词检索返回的切片数 | `10–50` | 影响 Rerank 阶段费用（费用 = 总初步召回数 × 平均 token 数 × 单价），需权衡效果与成本。 |
| **生成控制** | `stream`（API）<br>`incremental_output`（SDK） | 控制响应输出模式 | `true`（推荐） | 启用流式可实现前端增量渲染；`incremental_output=True` 保证每次返回仅新增内容，非全量重传。 |

> ⚠️ 注意：所有 RAG 场景均**不支持自定义文档切分逻辑或嵌入模型**——向量构建、切分策略、Rerank 模型均由百炼后台统一调度，开发者仅可通过上述参数调控其行为。

## 面向开发者，简洁实用

- **快速起步**：优先使用 `/api/v2/apps/knowledge/chat` 接口，传入 `messages`（对话历史）和 `knowledgeIds`，即可获得流式问答响应；无需管理模型、提示词或检索链路。
- **调试技巧**：开启 SSE 流式响应后，监听 `retrieving` 事件中的 `chunks` 字段，可实时查看被召回的原始文本片段，快速验证知识库覆盖度与检索质量。
- **性能优化**：若发现响应慢或成本高，首先检查 `vector_top_k` 和 `keyword_top_k` 是否设置过大；其次调高 `similarity_threshold` 减少无效切片进入 Rerank 阶段。
- **错误排查**：确保知识库状态为 `已发布（Published）`；API Key 与 `workspaceId` 必须归属同一租户；文件上传后需等待解析完成（控制台显示“就绪”状态）方可参与检索。
- **扩展建议**：如需更细粒度控制（如自定义重排逻辑、混合外部 API 结果），应采用底层 OpenAPI（`CreateIndex`/`Retrieve`）+ 自定义 LLM 编排，而非使用封装好的知识问答接口。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application evaluation](../guides/application-evaluation.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application support](../guides/application-support.md)


