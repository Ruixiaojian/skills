# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态召回相关知识片段，并将其作为上下文注入提示词，显著提升回答的事实准确性、领域专业性与时效性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是单一接口，而是贯穿多个能力层的横切架构，开发者可根据需求选择不同抽象层级的集成方式：

- **知识库（Knowledge Base）**：最核心的 RAG 落地载体。支持文档搜索、数据查询、多模态检索等类型；提供「单库检索」「多库联合检索（最多 15 个）」和「知识问答服务」三类能力。所有知识库均默认启用语义检索 + Rerank 排序，并支持 Query 改写、混合检索（向量+关键词）、标签/元数据过滤等精细化控制。

- **知识检索与问答（Knowledge API）**：面向开发者的标准化能力封装。  
  - `/search` 接口提供纯检索能力，返回按相关性排序的文本切片（chunk），适用于自定义 RAG 流程（如预处理、重排、提示工程）；  
  - `/chat` 接口为端到端 RAG 服务，自动完成「规划 → 工具调用（含知识检索）→ 生成」三阶段，支持流式响应（SSE）与拒答、溯源等生成控制。

- **智能体/工作流应用（LLM Application）**：将知识库作为可自主调用的工具之一。在 Agent 2.0 中，模型可基于用户问题动态决策是否检索、检索哪些知识库、如何融合结果，支持多轮上下文感知的改写与标签过滤，实现更灵活的 RAG 编排。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：面向代码优先的开发者。LlamaIndex 提供 `DashScopeCloudIndex` 封装云端知识库构建与查询；Spring AI Alibaba 提供 `DashScopeDocumentRetriever` 直接对接控制台知识库，支持自定义提示词与模型切换，快速嵌入现有 Java/Spring 生态。

- **应用评测（Application Evaluation）**：RAG 效果闭环的关键环节。自动评测任务会归因 BadCase 至具体环节（如“检索无效”“重排不佳”“切片不完整”），并给出针对性调优建议，帮助开发者持续优化 RAG 链路。

## 关键参数和配置

以下参数直接影响 RAG 效果，多数可在控制台「命中测试」或 API 请求体中调整：

| 参数 | 说明 | 推荐值 | 备注 |
|------|------|--------|------|
| `top_k`（召回片段数） | 最终送入大模型的检索结果数量 | `3–5`（通用问答）<br>`10–20`（复杂对比/列举） | 过高易引入噪声，且增加输入 token 消耗；需配合 `max_input_tokens` 控制总长度 |
| `similarity_threshold`（相似度阈值） | Rerank 后过滤切片的最低综合得分 | `0.3–0.5`（起步）<br>视评测集表现迭代调整 | 值 >0.6 可能导致空召回；低于 0.2 易引入低质内容 |
| `retrieval_mode` | 知识调用策略 | `must_use`（必定调用）<br>`on_demand`（按需） | 在智能体/工作流应用配置页设置，影响模型是否主动触发检索 |
| `initial_top_k`（初检 TopK） | 向量/关键词检索阶段返回的候选数 | `30–50`（默认 50） | 降低此值可节省 Rerank 费用，但可能牺牲召回广度 |
| `multi_round_rewrite`（多轮改写） | 是否启用历史会话辅助 Query 补全 | 开启（创建知识库时配置） | 对“手机X1参数？”→“阿里云百炼手机X1的参数信息？”类场景至关重要 |

> ⚠️ 注意：`/chat` 接口**不可显式指定 `model` 参数**——所用模型由业务空间内绑定的知识应用配置决定；知识库本身不计费，但其依赖的向量模型（`text-embedding-v4`）、重排模型（`qwen3-rerank`）及问答模型均按 token 单独计费。

## 面向开发者，简洁实用

- **快速验证**：在控制台「知识库」页点击「命中测试」，输入问题即可实时查看召回切片与最终回答，无需编码。
- **最小化集成**：调用 `/api/v2/apps/knowledge/chat`，只需 `Authorization` + `workspaceId` + 标准 `messages` 数组，5 分钟接入端到端 RAG。
- **效果调优三步法**：① 用自动评测定位瓶颈（如“检索无效”）→ ② 调整 `similarity_threshold` 或 `initial_top_k` → ③ 上传高质量文件并配置元数据抽取（如 `file_name` 作为来源标识）。
- **避坑提醒**：知识库仅在北京地域可用；所有知识库必须为「已发布」状态才参与检索；多文件同名时务必配置元数据，否则重排易混淆来源。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application evaluation](../guides/application-evaluation.md)
- [application use cases](../guides/application-use-cases.md)
- [llm application](../guides/llm-application.md)


