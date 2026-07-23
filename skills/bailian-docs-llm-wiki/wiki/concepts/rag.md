# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其注入提示词（[prompt](../guides/prompt.md)），显著提升回答的事实准确性、领域专业性与时效性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是单一功能，而是贯穿多个模块的底层能力架构，具体体现为以下三类协同模式：

- **知识库驱动的端到端问答**：通过「知识问答」API（`/api/v2/apps/knowledge/chat`）或控制台知识问答应用，系统自动完成「问题理解 → 语义检索 → 答案生成」全流程。用户只需提供自然语言问题，无需关心中间步骤；支持极速单轮模式与 Agentic 多轮规划搜索（如自动拆解复杂问题、迭代检索）。

- **结构化数据源的动态增强**：借助「数据连接器」（Data Connection），RAG 可接入 MySQL、PostgreSQL、语雀、OSS 等实时/静态数据源。例如调用 `queryMySQL` 工具执行 SQL 获取最新业务数据，或 `searchYuqueDoc` 检索内部文档，结果直接作为上下文输入大模型，实现“数据库 + LLM”的混合推理。

- **框架级低代码集成**：开发者可通过 LlamaIndex（Python）或 Spring AI Alibaba（Java）等主流框架，以声明式方式构建 RAG 流程。例如使用 `DashScopeCloudIndex` 自动同步云端知识库，配合 `DashScopeRerank` 进行重排过滤，再交由 `qwen-plus` 生成答案——所有向量化、检索、重排、生成环节均由百炼托管，无需自建向量数据库或部署嵌入模型。

> ✅ 关键共识：百炼的 RAG 实现统一基于**预构建、已发布的知识库索引**，不支持运行时上传文档并即时索引；所有检索均依赖平台托管的向量/关键词混合召回 + 重排（Rerank）双阶段机制。

## 关键参数和配置

RAG 效果高度依赖以下可调参数，需根据场景权衡召回完整性与生成质量：

| 参数 | 作用 | 推荐值范围 | 生效位置 |
|------|------|------------|----------|
| `top_k` / `similarity_top_k` | 初步检索召回的切片数量（向量+关键词阶段） | 10–50（增大可提升召回率，但增加 Rerank 延迟） | 知识检索 API、LlamaIndex `as_retriever()`、Spring AI `DashScopeDocumentRetriever` |
| `max_retrieved` / `top_n` | 最终送入大模型的上下文切片数（经重排后截取） | 3–10（生产环境建议 ≤5，避免输入过长导致 token 超限或注意力稀释） | 知识问答 API 的隐式限制、LlamaIndex `SimilarityPostprocessor`、控制台知识库配置页 |
| `similarity_threshold` / `similarity_cutoff` | 重排后切片的最低相似度阈值（0.01–1.0） | 0.4–0.7（过高易漏召关键信息，过低引入噪声） | 控制台知识库设置、LlamaIndex `SimilarityPostprocessor`、Spring AI `DashScopeDocumentRetriever` |
| `metadata_filter` / `tags` | 基于元数据（如 `filename`, `date`）或标签（如 `bailian_mobile`）进行结构化过滤 | JSON 对象或字符串数组，支持 `AND/OR` 逻辑 | 知识检索 API `filter` 字段、LlamaIndex `MetadataFilters`、数据连接器查询参数 |

> ⚠️ 注意：`top_k` 在知识问答接口中实际生效上限为 10（后端策略强制截断），与文档标称的 50 不一致；务必以实际响应为准。

## 面向开发者，简洁实用

- **快速验证**：用 `curl` 直接调用知识检索 API，确认知识库是否返回预期切片；再切换为知识问答 API，观察生成答案是否引用了检索结果。
- **调试技巧**：启用 `stream=true` 并监听 `event: plan` 和 `event: tool_calls` 事件流，可清晰看到检索触发时机、召回文档 ID 及原始切片内容，便于定位召回失败或噪声干扰问题。
- **性能优化**：若延迟敏感，优先调小 `top_k` 和 `max_retrieved`；若准确率不足，先检查 `similarity_threshold` 是否过严，再考虑增加高质量文档或优化元数据标签。
- **安全边界**：所有 RAG 调用均受业务空间（workspaceId）隔离，知识库仅对绑定应用可见；敏感数据无需出域，全程在百炼华北2（北京）地域内处理。
- **避坑提醒**：  
  - 不要尝试在框架中覆盖默认切分/嵌入逻辑——百炼不支持自定义切分方式或嵌入模型；  
  - 文件上传请严格遵守 100 MB / 1000 页限制；  
  - 使用第三方模型（如 DeepSeek、Kimi）做 RAG 时，必须确保其所在地域与知识库一致（仅华北2 北京）。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)


