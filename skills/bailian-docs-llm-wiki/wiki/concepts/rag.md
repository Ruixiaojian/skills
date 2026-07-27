# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。在百炼平台中，RAG 不是抽象概念，而是可配置、可编排、可监控的生产级能力——通过将私有知识库或结构化数据源动态注入模型推理上下文，显著提升回答的事实准确性、领域专业性与可控性。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中以多种形态落地，覆盖从低代码集成到深度开发的全栈路径：

- **开箱即用的知识问答服务**：调用 `/api/v1/indices/knowledge/qa` 接口，输入自然语言问题，平台自动完成语义检索 → 上下文注入 → 大模型生成 → 流式返回答案（含 `plan`/`tool_call`/`answer` 三阶段事件），无需开发者编写召回逻辑。
  
- **智能体（Agent）与工作流中的知识增强**：在智能体应用配置页绑定知识库，或在工作流中拖入“知识库”节点；模型在规划（Planning）阶段自动触发检索，结果以 `{result}` 形式注入下游 LLM 提示词，支持多知识库联合混排与权重调节。

- **框架级 RAG 构建**：
  - 使用 **LlamaIndex**：通过 `DashScopeCloudIndex` 创建云端索引，调用 `as_query_engine()` 并配置 `similarity_top_k` 和 `DashScopeRerank` 后处理器，实现端到端 RAG 查询；
  - 使用 **Spring AI Alibaba**：通过 `DashScopeDocumentRetriever` 将知识库检索结果自动注入 `ChatClient` 的上下文，与模型调用无缝衔接。

- **[数据连接](data-connection.md)驱动的动态 RAG**：对接 MySQL、PostgreSQL 等流处理类连接器时，`executeSQL` 工具可在运行时执行 SQL 查询，将实时结构化结果作为上下文喂给 LLM，实现“检索+生成”闭环，适用于报表解读、数据库问答等场景。

- **自定义 OpenAPI 组合方案**：调用底层 `Retrieve` 接口获取原始切片（chunk），再自行拼接 Prompt 并调用任意 LLM（如 `qwen3.7-plus`），完全掌控检索策略、上下文构造与模型选型——这是对 RAG 流程最细粒度的控制方式。

## 关键参数和配置

RAG 效果高度依赖以下核心参数，需根据业务场景调优：

| 参数类别 | 参数名 | 说明 | 典型值 | 生效层级 |
|----------|--------|------|--------|----------|
| **召回控制** | `top_k` | 最终返回给 LLM 的切片数量 | `3`–`10` | API 请求级（`knowledge/qa`）、工作流节点级、LlamaIndex `similarity_top_k` |
| | `similarity_threshold` | 过滤低相关性切片的相似度阈值 | `0.3`–`0.5` | 控制台知识库配置页、API `metadata_filter` 配合使用 |
| | `vector_top_k` / `keyword_top_k` | 向量/关键词初检召回数（影响 Rerank 输入规模） | `20`–`50` | 知识库高级设置页（仅旗舰版可见） |
| **上下文注入** | `metadata_filter` | 基于元数据（如 `file_name`, `cat_name`, 正则提取字段）精准过滤切片 | `{"file_name": "product_manual_v2.pdf"}` | `Retrieve` API 请求体、LlamaIndex `filters` |
| | `tags` | 按文件标签粗粒度筛选知识范围 | `["v2.0", "internal"]` | `knowledge/search` 或 `knowledge/qa` 请求参数 |
| **性能与规格** | RCU（Retrieval Compute Unit） | 计量知识库并发能力，1 RCU ≈ 50 QPS | 标准版：1 QPS；旗舰版：50–10,000 QPS | 业务空间资源包购买项，影响 `Retrieve` 和 `knowledge/*` 接口吞吐 |

> ⚠️ 注意：`knowledge/qa` 接口不支持指定 LLM 模型，其底层模型由业务空间默认配置决定；若需精确控制模型，请使用 `Retrieve` + 自定义 LLM 调用组合方案。

## 面向开发者，简洁实用

- **快速验证**：用 `curl` 直接调用知识检索接口，确认知识库已发布且 `top_k` 返回预期切片，是 RAG 调试的第一步。
- **避免硬编码**：模型名（如 `qwen3.5-plus`）、地域（`cn-beijing`）、WorkspaceId 均应从环境变量或配置中心读取，而非写死。
- **流式必开**：所有面向终端用户的 RAG 场景（网站助手、企微机器人），务必启用 `stream=true`，并正确处理 SSE 事件流，保障响应体验。
- **限流兜底**：客户端需实现指数退避重试（429 错误），并预设降级策略（如 fallback 到无知识库的纯 LLM 回答）。
- **效果调优优先级**：先检查知识库覆盖度（文档是否上传成功、状态为 `published`），再调相似度阈值，最后优化 Prompt 引导——90% 的 RAG 问题源于知识缺失或召回不准，而非模型本身。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [frameworks](../api/frameworks.md)
- [application component api reference](../api/application-component-api-reference.md)
- [data connection overview](../guides/data-connection-overview.md)
- [knowledge base](../guides/knowledge-base.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)


