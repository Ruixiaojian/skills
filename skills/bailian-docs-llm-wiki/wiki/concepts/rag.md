# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大语言模型生成能力深度融合的技术范式。它通过在模型推理前动态召回相关知识片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），显著提升模型回答的准确性、时效性与可溯源性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是抽象概念，而是已深度产品化的工程能力，贯穿于多个核心服务层：

- **知识库（Knowledge Base）**：是 RAG 的基础设施载体。支持文档、表格、音视频等[多模态](multi-modal.md)数据的自动解析、智能切片、向量化与语义检索；所有知识库均默认启用 RAG 流程——用户提问 → 平台执行混合检索（向量+关键词）→ Rerank 排序 → 注入 TopK 切片至 LLM 提示 → 生成带引用溯源的回答。

- **[knowledge](../api/knowledge.md) API**：提供面向业务集成的 RAG 端到端服务能力。`/knowledge/search` 实现纯检索（召回阶段），`/knowledge/qa` 实现流式 RAG 问答（含规划、工具调用、生成三阶段），开发者无需管理模型选型或 RAG 链路细节，仅需传入 `query` 和可选 `indices` 即可获得结构化结果。

- **智能体与工作流应用**：RAG 以“知识库节点”形式嵌入编排逻辑。可在智能体 Prompt 中声明知识依赖，或在工作流中拖拽知识库组件，配置 `retrieval_top_k`、`similarity_threshold` 等参数，实现条件触发式知识增强。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：提供标准化 SDK 接口，将百炼云端知识库封装为 `DashScopeCloudIndex` 或 `DashScopeDocumentRetriever`，使开发者能在熟悉框架内复用百炼的向量引擎与生成模型，快速构建 RAG 应用，无需自建 Embedding/Rerank/LLM 服务。

- **全渠道应用（网站/企微/钉钉/公众号）**：RAG 是开箱即用的增强能力。创建智能体应用时勾选知识库，即可在悬浮窗、群聊机器人等触点中自动启用知识增强问答，支持拒答控制、引用高亮与多轮上下文感知。

## 关键参数和配置

RAG 效果由检索与生成两个阶段的关键参数协同决定，百炼平台统一暴露以下核心可控项（均通过 API 或控制台配置）：

| 参数名 | 作用 | 典型取值 | 说明 |
|--------|------|----------|------|
| `top_k` / `similarity_top_k` / `retrieval_top_k` | 控制最终送入 LLM 的知识片段数量 | `3–5`（推荐） | 数值过大会增加 [Token](token.md) 消耗与噪声，过小易丢失关键信息；最大限制为 `20` |
| `similarity_threshold` / `similarity_cutoff` | 过滤低相关性召回片段的相似度下限 | `0.3–0.7`（依数据质量调整） | 设为 `0.0` 表示不过滤；设过高可能导致无召回（返回空） |
| `indices` / `cloud_index_name` / `INDEX_NAME` | 指定参与检索的知识库 ID 列表 | `["kb-xxx", "kb-yyy"]` | 多库联合检索最多支持 `15` 个知识库；未指定则使用默认库 |
| `stream` | 启用流式响应（仅知识问答接口） | `true`（默认） | 开启后通过 SSE 分块返回 `planning` → `tool_calling` → `generation` 阶段结果 |
| `temperature` / `max_tokens` | 影响生成阶段的确定性与长度 | `temperature=0.2`, `max_tokens=1024` | 属于 LLM 通用参数，与 RAG 检索正交，但共同决定最终输出质量 |

> ⚠️ 注意：百炼 **不开放** 自定义 embedding 模型、reranker 模型、文档切分策略或向量维度配置。所有向量化（如 `text-embedding-v4`）、重排序（如 `gte-rerank`）及切片逻辑均由平台统一托管，确保效果稳定与服务一致性。

## 面向开发者，简洁实用

- **快速上手**：只需 3 步完成 RAG 集成——① 在控制台创建并发布知识库；② 调用 `/knowledge/qa` API 或在智能体中绑定该库；③ 传入 `query`，其余由平台自动完成。
- **调试建议**：使用控制台「命中测试」验证召回质量；结合 SLS 日志查看 `response_body.data.nodes[]` 中的原始切片与分数，定位召回偏差。
- **成本优化**：`top_k` 直接影响 [Token](token.md) 消耗与 Rerank 费用，建议从 `3` 起调，配合 `similarity_threshold` 过滤低分噪声。
- **错误排查**：若无召回，请检查知识库状态是否为 `published`、地域是否为华北2（北京）、`indices` 是否拼写正确（字符串数组，非逗号分隔字符串）。
- **扩展性**：如需更细粒度控制（如元数据过滤、标签路由），请在知识库创建时配置 `Meta信息抽取` 与 `标签`，并在检索时通过 `filter` 参数（部分 API 支持）或工作流节点条件表达式使用。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [data connection overview](../guides/data-connection-overview.md)


