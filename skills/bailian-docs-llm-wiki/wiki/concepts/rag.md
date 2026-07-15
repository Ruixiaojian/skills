# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关文档片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），显著提升回答的事实准确性、领域专业性与可控性，避免幻觉，是百炼平台支撑私有知识问答、智能客服、企业知识助手等生产级应用的核心技术底座。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，“检索增强生成”并非单一接口，而是贯穿多个能力层级的横切架构模式，开发者可根据需求选择不同抽象层级的实现方式：

- **基础检索层（Knowledge API）**：直接调用 `/api/v1/indices/knowledge/search` 接口，执行跨知识库的语义检索，返回原始文本切片（chunk）。适用于需完全自控 RAG 流程（如自定义 Query 改写、混合检索、多路召回融合）的高级场景。
- **端到端问答层（Knowledge QA）**：调用 `/api/v2/apps/knowledge/chat` 接口，平台自动完成“检索 → 上下文组装 → 大模型生成 → 引用标注”全流程，支持流式 SSE 响应与三阶段（规划→工具调用→生成）输出，适合快速构建生产就绪的问答服务。
- **应用集成层（Application + Knowledge Base）**：在智能体或工作流应用中绑定已发布的知识库，并配置“必定调用”或“按需调用”策略；RAG 行为由 `application support` 统一调度，与[插件](plugin.md)、[流式输出](streaming-output.md)等能力无缝协同。
- **框架集成层（LlamaIndex / Spring AI Alibaba）**：通过 SDK 封装复用百炼云端知识库与模型能力。例如 LlamaIndex 使用 `DashScopeCloudIndex` 构建索引，Spring AI Alibaba 使用 `DashScopeDocumentRetriever` 直接检索，均无需管理向量存储与嵌入模型。
- **低代码渠道层（AppFlow）**：在网站、企业微信、钉钉等渠道嵌入 AI 助手时，后台自动启用 RAG 能力——只需上传文档、创建知识库并绑定至应用，即可零代码启用私有知识增强。

所有场景均依赖同一套知识库基础设施（切片、向量化、重排、元数据过滤），确保行为一致与效果可复现。

## 关键参数和配置

RAG 效果高度依赖以下关键参数，需根据业务目标权衡精度、延迟与成本：

| 参数 | 作用域 | 说明 | 推荐值 | 注意事项 |
|------|--------|------|--------|----------|
| `top_k` | 检索/API/框架 | 单次检索返回的最大文本切片数 | `3–10`（问答）、`5–20`（调试） | 知识 API 默认 `5`，最大 `20`；LlamaIndex 对应 `similarity_top_k`；Spring AI 对应 `topK` |
| `score_threshold` | 应用/API/框架 | 重排后相似度阈值（0.01–1.0），低于此值的切片被过滤 | `0.3–0.6` | 过高易漏召，过低引入噪声；需结合命中测试调优 |
| `enable_rerank` | 应用/API | 是否启用百炼内置重排模型（提升相关性排序质量） | `true`（默认） | 启用后增加少量延迟与 [Token](token.md) 消耗，但显著改善结果质量 |
| `tags` | 检索/API/控制台 | 按业务标签（如 `product_v2`, `faq_2024`）精准筛选知识库文件 | `["product_v2"]` | 最多支持 32 个标签，创建知识库时需预先配置 |
| `max_retrieve_count` | 知识库配置 | Rerank 阶段输入的最大候选切片数（影响 [Token](token.md) 消耗） | `20–100` | 初检 TopK 可设更高，但最终送入 Rerank 的数量受此限制 |

> ⚠️ 注意：`workspaceId` 是所有 RAG 请求的必需前置——必须用于构造专属 Base URL（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`），不可复用 DashScope 公共域名；且仅华北2（北京）地域可用。

## 面向开发者，简洁实用

- ✅ **快速上手**：控制台创建知识库 → 上传 PDF/DOCX → 发布 → 绑定至智能体应用 → 开启“必定调用”，5 分钟启用 RAG。
- ✅ **调试优先**：先用 `/api/v1/indices/knowledge/search` 查看原始检索结果，验证切片质量与 `score_threshold` 设置是否合理。
- ✅ **效果优化**：启用“智能切分”策略（优于固定长度）、配置 Meta 信息抽取（如 `file_name`）、添加业务标签，三者组合可大幅提升定向召回率。
- ✅ **成本控制**：`max_retrieve_count` 和 `top_k` 直接影响 [Token](token.md) 消耗；生产环境建议 `top_k=5` + `enable_rerank=true`，平衡效果与开销。
- ❌ **避坑提醒**：知识库未发布则不可检索；`workspaceId` 与 OpenAPI 的 `project_id` 无映射关系；SSE 流式响应需客户端正确解析 `text/event-stream`。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)


