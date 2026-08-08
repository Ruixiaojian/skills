# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是百炼平台的核心架构范式，通过在大模型生成前动态检索相关知识片段并注入上下文，显著提升回答的准确性、事实性与领域专业性。它将“检索”与“生成”解耦为可配置、可观测、可优化的两个阶段，是构建可信企业级 AI 应用的技术基石。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中并非单一能力，而是贯穿多个层级的统一技术底座，具体体现为：

- **知识库服务层**：所有知识库（文档搜索、表格查询、图片问答、音视频搜索）均默认采用 RAG 架构。用户上传数据后，平台自动完成切分、向量化、索引构建；问答时，系统先执行语义检索（支持多知识库联合混排），再将 TopK 切片作为上下文输入大模型生成自然语言回答。

- **API 能力层**：`/api/v2/apps/knowledge/chat`（知识问答）和 `/api/v1/indices/knowledge/search`（知识检索）两个核心接口直接暴露 RAG 的两阶段能力——前者提供端到端流式响应（含 planning → tool calling → generation 三阶段 SSE 事件），后者返回原始检索结果，供开发者自定义后续处理逻辑。

- **应用编排层**：在智能体应用或工作流应用中，「知识库」节点即 RAG 的可视化封装。开发者可拖拽配置召回数量（TopK）、相似度阈值、知识库选择策略（固定/动态），并在提示词中通过 `{result}` 变量引用检索内容，实现灵活的上下文注入。

- **框架集成层**：LlamaIndex 和 Spring AI Alibaba 等主流框架通过 `DashScopeCloudIndex` 或 `DashScopeDocumentRetriever` 统一对接百炼云端 RAG 能力，屏蔽底层向量模型（如 `gte-rerank`）、索引服务与模型调度细节，让开发者聚焦业务逻辑。

- **低代码连接流层**：AppFlow 中的微信/企微/钉钉等预置模板，默认启用 RAG 增强。绑定知识库后，用户消息自动触发检索+生成闭环，支持“必定调用”或“按需调用”两种触发模式，兼顾响应速度与准确性。

> ⚠️ 注意：百炼 RAG 为**全托管方案**——不支持自定义嵌入模型、自定义文本切分策略或本地向量存储。所有向量化、检索、重排序均由平台统一完成，确保效果一致性与运维简化。

## 关键参数和配置

RAG 行为主要通过以下参数控制，按使用层级归类：

| 参数 | 所属层级 | 类型 | 说明 | 典型取值 |
|------|----------|------|------|-----------|
| `topK` | API / 应用节点 / 框架 | number | 检索阶段返回的最相关文本切片数 | `3`–`10`（默认 `5`，最大 `20`） |
| `similarity_threshold` | 知识库配置 / 应用节点 | float | 相似度过滤阈值（0.01–1.0），低于此值的切片被丢弃 | `0.35`（宽松）、`0.65`（严格） |
| `knowledgeIds` | API（检索） | string[] | 显式指定参与联合检索的知识库 ID 列表 | `["k-abc123", "k-def456"]` |
| `stream` | API（问答） | boolean | 是否启用 SSE 流式响应（默认 `true`） | `true`（推荐）、`false`（调试用） |
| `retrieval_mode`（应用节点） | 工作流/智能体配置页 | string | 控制知识库调用逻辑 | `"always"`（必定调用）、`"on_demand"`（按需调用） |

> ✅ 实用建议：  
> - 首次调优优先调整 `similarity_threshold` 和 `topK`，用典型 query 测试召回质量；  
> - 生产环境务必设置 `similarity_threshold ≥ 0.3`，避免低质噪声干扰生成；  
> - `topK` 过高（>10）可能增加 token 开销且边际收益递减，建议结合 `max_context_length` 综合评估。

## 面向开发者，简洁实用

- **不要重复造轮子**：百炼 RAG 已内置语义检索、多路混排（向量+关键词）、重排序（`gte-rerank`）、上下文截断与拼接逻辑。除非有特殊合规要求，否则无需自行实现检索链路。
- **流式是默认，也是最佳实践**：知识问答接口默认返回 SSE 流，前端应按 `event:` 字段解析 `planning`/`tool_calling`/`generation` 阶段，实现渐进式响应与实时反馈。
- **知识更新有延迟**：新文档完成向量化约需 1–3 分钟，请勿在上传后立即查询，可监听 `index_status == ACTIVE` 再启用服务。
- **错误诊断看 RequestId**：若 RAG 结果不准，复制响应头中的 `X-DashScope-Request-ID` 提交工单，并附上 query + 期望答案，便于平台侧定位检索或生成问题。
- **配额与地域强约束**：RAG 功能仅限华北2（北京）地域；标准版知识库 QPS 固定为 1，高并发场景请升级至旗舰版并配置足够 RCU。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [frameworks](../api/frameworks.md)
- [knowledge base](../guides/knowledge-base.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)


