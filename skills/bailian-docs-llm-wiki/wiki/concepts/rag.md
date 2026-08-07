# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大语言模型生成能力深度融合的技术范式。它通过在模型推理前动态召回相关知识片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），显著提升回答的准确性、专业性、可溯源性与事实一致性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是抽象概念，而是已工程化、开箱即用的核心能力，贯穿多个产品层级：

- **知识库（Knowledge Base）**：这是 RAG 的核心载体。开发者上传 PDF/DOCX/Excel/图片/音视频等私有数据，平台自动完成解析、切分、向量化与索引。调用时，系统按语义召回最相关的文本切片（chunk），并交由大模型生成最终回答。支持单库/多库联合检索、混合检索（向量+关键词）、Rerank 排序及元数据过滤。

- **知识检索与问答 API（`/search` 和 `/chat`）**：面向开发者提供标准化接口。`/search` 返回原始召回结果（用于自定义排序或预检），`/chat` 则端到端完成“检索→规划→工具调用→生成”全流程，支持流式响应（SSE），适用于构建智能客服、内部知识助手等生产应用。

- **数据连接（Data Connection）**：为 RAG 提供实时、动态的数据源支撑。文件、表格、OSS、语雀、钉钉等连接器均可构建向量索引；数据库类连接器（MySQL/PostgreSQL/PolarDB-X）还支持 SQL 查询执行，实现结构化数据与非结构化知识的协同增强。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：降低 RAG 工程门槛。LlamaIndex 提供 `DashScopeCloudIndex` 封装云端知识库，支持 `similarity_top_k`、`similarity_cutoff` 等参数控制；Spring AI Alibaba 通过 `DashScopeDocumentRetriever` 实现知识检索与 `ChatClient` 的无缝绑定，让 RAG 成为标准对话流程的一部分。

- **应用与渠道集成（Website / 企业微信 / 钉钉 / 微信公众号）**：RAG 能力被封装进低代码 AppFlow 模板。开发者只需关联已发布的知识库，配置相似度阈值与权重，即可在 10 分钟内上线具备专业问答能力的 AI 助手，无需编写胶水代码。

- **本地 RAG 变体（`local_rag.zip`）**：提供轻量级本地部署选项，适用于对数据主权或网络隔离有强要求的场景。支持自定义文档切分、本地嵌入模型（如 GTE-Chinese-Large）及完整参数调优链路。

## 关键参数和配置

RAG 效果高度依赖以下关键参数，需根据业务目标权衡精度、延迟与成本：

| 参数 | 作用域 | 典型取值 | 说明 |
|------|--------|----------|------|
| `top_k`（或 `retrieval_top_k`） | 检索层 | 3–5（默认 5，最大 20） | 控制初步召回切片数量。增大可提升召回完整性，但增加 Rerank [Token](token.md) 消耗与生成噪声风险。 |
| `similarity_threshold`（或 `similarity_cutoff`） | 检索层 | 0.2–0.6（0 表示不过滤） | 过滤 Rerank 后低于该分数的切片。值过高易漏召回，过低引入无关噪声，直接影响生成质量。 |
| `filter`（元数据过滤） | 检索层 | `{"source": "manual", "product": "A"}` | 在请求体中传入 JSON 对象，实现基于字段的精确匹配（如按来源、产品线、版本号过滤）。 |
| `temperature` / `top_p` | 生成层 | `temperature=0.1–0.3`, `top_p=0.9–1.0` | 控制生成确定性。RAG 场景建议低 temperature（≤0.3），确保答案忠实于检索内容。 |
| `stream` | 问答接口 | `true`（默认） | 启用 SSE 流式响应，适用于对话界面，降低用户等待感知。 |

> ⚠️ 注意：百炼平台**不支持指定底层 Embedding 或 LLM 模型 ID**。所有语义计算（向量化、Rerank、生成）均由平台托管模型自动调度，开发者仅需关注业务参数。

## 面向开发者，简洁实用

- **快速起步**：控制台 → [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) → 上传文件 → 发布 → 在智能体/工作流中添加“文档知识库”节点 → 设置 `similarity_threshold` → 发布应用。
- **API 直接调用**：使用 `curl` 或 SDK 调用 `/api/v1/indices/knowledge/search`（检索）或 `/api/v2/apps/knowledge/chat`（问答），务必携带 `Authorization: Bearer <API-Key>` 和正确的 `workspaceId` 域名。
- **调试技巧**：开启 `stream=false` 调试问答接口，查看完整三阶段响应（planning/tool calling/generation）；检查 `source_nodes` 字段验证检索结果是否相关。
- **性能优化**：高频查询启用显式缓存（`cache_control`）；多知识库场景优先启用路由（由 `qwen-plus` 自动分发），避免全库扫描；严格限制 `top_k` 与 `similarity_threshold`，平衡效果与成本。
- **避坑指南**：知识库必须为「已发布」且「状态 active」才生效；地域限定为华北2（北京）；OSS Bucket 需添加 `bailian-connector-access` 标签；环境变量名在不同框架中不一致（如 `DASHSCOPE_API_KEY` vs `AI_DASHSCOPE_API_KEY`），请严格按所选文档配置。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)


